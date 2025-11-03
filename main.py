import requests
from datetime import date, datetime, timedelta
from jinja2 import Template
from weather_code_utils import weathercode_to_imgsrc
from date_time_utils import date_iso_zu_deutsch, from_iso_string, to_iso_string
from KalenderRenderHelper import KalenderRenderHelper
from dateutil.relativedelta import relativedelta
import json
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from enum import Enum

from WeatherData import WeatherData

#https://erikflowers.github.io/weather-icons/

class ColorOptions(Enum):
    sw = "sw"
    swr = "swr"
    rgb = "rgb"


def get_daily_index(data, target_date):
    try:
        return data['daily']['time'].index(target_date)
    except:
        return -1

def create_page(html_file_name, colorOption = ColorOptions.sw):
    # Aktuelles Datum und drei Tage in die Zukunft ermitteln
    today = datetime.now()
    iso_datum_heute = to_iso_string(today)
    iso_datum_plus_1 = to_iso_string((today + timedelta(days=1)))
    iso_datum_plus_2 = to_iso_string((today + timedelta(days=2)))
    iso_datum_plus_3 = to_iso_string((today + timedelta(days=3)))

    # Konfig laden
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Konfigurationsdatei nicht gefunden.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Fehler beim Parsen der JSON-Datei.")
        sys.exit(1)

    lat = config["latitude"]
    lon = config["longitude"]
    monatsNamen = config["monthNames"]
    tagesNamen = config["dayNames"]

    kalenderRenderHelper = KalenderRenderHelper(monatsNamen, tagesNamen)

    # Webrequest
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_sum,weather_code,temperature_2m_max,temperature_2m_min&hourly=temperature_2m,weather_code,precipitation&models=icon_seamless&current=temperature_2m,is_day,precipitation,weather_code,wind_speed_10m,wind_direction_10m&timezone=Europe%2FBerlin&forecast_days=5&wind_speed_unit=ms"
    response = requests.get(url)

    # Dateinamen
    file_name_template = "pageTemplate.html"
    match colorOption:
        case ColorOptions.sw:
            file_name_css = 'styleTemplateSW.css'
        case ColorOptions.swr:
            file_name_css = 'styleTemplateSWR.css'
        case ColorOptions.rgb:
            file_name_css = 'styleTemplateRGB.css'
        case _:
            file_name_css = 'styleTemplateSW.css'
        

    # Antwort des Webrrequest
    if response.status_code == 200:
        data = response.json()

        index_heute = get_daily_index(data, iso_datum_heute)
        index_plus_1 = get_daily_index(data, iso_datum_plus_1)
        index_plus_2 = get_daily_index(data, iso_datum_plus_2)
        index_plus_3 = get_daily_index(data, iso_datum_plus_3)

        tempUnit = data['current_units']['temperature_2m']
        precipitationUnit = data['current_units']['precipitation']
        windSpeedUnit = data['current_units']['wind_speed_10m']
        windDirectionUnit = data['current_units']['wind_direction_10m']

        # Wetterdaten heute
        currentDat = from_iso_string(data['current']['time'])
        currentWCd = data['current']['weather_code']
        currentMin = data['daily']['temperature_2m_min'][index_heute]
        currentMax = data['daily']['temperature_2m_max'][index_heute]
        weatherDataCurrent = WeatherData(currentDat, currentWCd, currentMin, currentMax, tempUnit)
        weatherDataCurrent.temp_current = data['current']['temperature_2m']
        weatherDataCurrent.precipitation = data['daily']['precipitation_sum'][index_heute]
        weatherDataCurrent.precipitation_unit = precipitationUnit
        weatherDataCurrent.wind = data['current']['wind_speed_10m']
        weatherDataCurrent.wind_unit = windSpeedUnit
        weatherDataCurrent.wind_direction = data['current']['wind_direction_10m']
        weatherDataCurrent.wind_direction_unit = windDirectionUnit

        # Wetterdaten morgen
        plus1Dat = from_iso_string(data['daily']['time'][index_plus_1])
        plus1WCd = data['daily']['weather_code'][index_plus_1]
        plus1Min = data['daily']['temperature_2m_min'][index_plus_1]
        plus1Max = data['daily']['temperature_2m_max'][index_plus_1]
        weatherDataPlus1 = WeatherData(plus1Dat, plus1WCd, plus1Min, plus1Max, tempUnit)

        # Wetterdaten übermorgen
        plus2Dat = from_iso_string(data['daily']['time'][index_plus_2])
        plus2WCd = data['daily']['weather_code'][index_plus_2]
        plus2Min = data['daily']['temperature_2m_min'][index_plus_2]
        plus2Max = data['daily']['temperature_2m_max'][index_plus_2]
        weatherDataPlus2 = WeatherData(plus2Dat, plus2WCd, plus2Min, plus2Max, tempUnit)

        # Wetterdaten überübermorgen
        plus3Dat = from_iso_string(data['daily']['time'][index_plus_3])
        plus3WCd = data['daily']['weather_code'][index_plus_3]
        plus3Min = data['daily']['temperature_2m_min'][index_plus_3]
        plus3Max = data['daily']['temperature_2m_max'][index_plus_3]
        weatherDataPlus3 = WeatherData(plus3Dat, plus3WCd, plus3Min, plus3Max, tempUnit)

        # HTML Template laden
        html_template = open(file_name_template).read()
        template = Template(html_template)

        # HTML rendern
        html_fertig = template.render(
            css = file_name_css,

            datum_heute = today.strftime("%d.%m.%Y"),
            temp_unit = weatherDataCurrent.temp_unit,
            
            weather_icon_current = weathercode_to_imgsrc(weatherDataCurrent.weathercode, True),
            weather_temp_current = weatherDataCurrent.temp_current,
            weather_temp_min_current = weatherDataCurrent.temp_min,
            weather_temp_max_current = weatherDataCurrent.temp_max,        
            weather_precipitation_current = weatherDataCurrent.precipitation,
            weather_wind_speed_current = weatherDataCurrent.wind,
            weather_wind_direction_current = weatherDataCurrent.wind_direction,
            
            datum_plus_1 = date_iso_zu_deutsch(iso_datum_plus_1),
            weather_icon_plus_1 = weathercode_to_imgsrc(weatherDataPlus1.weathercode, True),
            weather_temp_min_plus_1 = weatherDataPlus1.temp_min,
            weather_temp_max_plus_1 = weatherDataPlus1.temp_max,
            
            datum_plus_2 = date_iso_zu_deutsch(iso_datum_plus_2),
            weather_icon_plus_2 = weathercode_to_imgsrc(weatherDataPlus2.weathercode, True),
            weather_temp_min_plus_2 = weatherDataPlus2.temp_min,
            weather_temp_max_plus_2 = weatherDataPlus2.temp_max,
            
            datum_plus_3 = date_iso_zu_deutsch(iso_datum_plus_3),
            weather_icon_plus_3 = weathercode_to_imgsrc(weatherDataPlus3.weathercode, True),
            weather_temp_min_plus_3 = weatherDataPlus3.temp_min,
            weather_temp_max_plus_3 = weatherDataPlus3.temp_max,

            # Kalenderdaten
            kalender = kalenderRenderHelper.render(today),
            muellmorgen = kalenderRenderHelper.render_muell_morgen(today),
            kalender_plus_1 = kalenderRenderHelper.render(today + relativedelta(months=1)),
            kalender_plus_2 = kalenderRenderHelper.render(today + relativedelta(months=2))
        )

        # HTML speichern
        with open(html_file_name, "w", encoding="utf-8") as f:
            f.write(html_fertig)
    else:
        sys.exit(1)

def create_image(html_file_name, image_file_name, xRes, yRes, colorOption = ColorOptions.sw):
    create_page(html_file_name, colorOption)
    # PNG aus HTML erzeugen und speichern
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--force-device-scale-factor=1") 
    options.add_argument(f"--window-size={xRes},{yRes}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    file_path = "file://" + os.path.abspath(html_file_name)
    driver.get(file_path)

    # Viewport Berechnugnen, damit das Bild genau die gewünschte Größe hat
    set_viewport_size(driver,xRes,yRes)

    time.sleep(1)
    driver.save_screenshot(image_file_name)
    driver.quit()

def set_viewport_size(driver, width, height):
    """Set viewport size genau auf gewünschte Pixel."""
    # Aktuelle Fenstergröße lesen
    window_size = driver.get_window_size()
    # Viewportgröße auslesen
    inner_width = driver.execute_script("return window.innerWidth")
    inner_height = driver.execute_script("return window.innerHeight")
    # Differenz berechnen (Fensterrahmen, Scrollleisten, etc.)
    delta_width = window_size['width'] - inner_width
    delta_height = window_size['height'] - inner_height
    # Fenstergröße so anpassen, dass Viewport exakt passt
    driver.set_window_size(width + delta_width, height + delta_height)

htmlFileName = 'page.html'
imageFileName = 'page.png'

create_page(htmlFileName, ColorOptions.swr)
#create_image(htmlFileName, imageFileName, 1600,1200)