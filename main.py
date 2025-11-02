import requests
from datetime import date, datetime, timedelta
from jinja2 import Template
from weather_code_utils import weathercode_to_imgsrc
from date_time_utils import dateTime_iso_zu_deutsch, date_iso_zu_deutsch
from html_calendar_utils import render_html_calender, check_muell_morgen
from dateutil.relativedelta import relativedelta

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time
import os

#https://erikflowers.github.io/weather-icons/

def get_daily_index(data, target_date):
    try:
        return data['daily']['time'].index(target_date)
    except:
        return -1

# Aktuelles Datum und drei Tage in die Zukunft ermitteln
today = datetime.now()
datum_heute = today.strftime("%Y-%m-%d")
datum_plus_1 = (today + timedelta(days=1)).strftime("%Y-%m-%d")
datum_plus_2 = (today + timedelta(days=2)).strftime("%Y-%m-%d")
datum_plus_3 = (today + timedelta(days=3)).strftime("%Y-%m-%d")

# Webrequest
url = "https://api.open-meteo.com/v1/forecast?latitude=49.5097&longitude=9.9708&daily=precipitation_sum,weather_code,temperature_2m_max,temperature_2m_min&hourly=temperature_2m,weather_code,precipitation&models=icon_seamless&current=temperature_2m,is_day,precipitation,weather_code,wind_speed_10m,wind_direction_10m&timezone=Europe%2FBerlin&forecast_days=5&wind_speed_unit=ms"
response = requests.get(url)

# Dateinamen
file_name_template = "pageTemplate.html"
file_name_composed = "page.html"

# Antwort des Webrrequest
if response.status_code == 200:
    data = response.json()

    index_heute = get_daily_index(data, datum_heute)
    index_plus_1 = get_daily_index(data, datum_plus_1)
    index_plus_2 = get_daily_index(data, datum_plus_2)
    index_plus_3 = get_daily_index(data, datum_plus_3)

    html_template = open(file_name_template).read()
    template = Template(html_template)

    html_fertig = template.render(
        datum_heute=dateTime_iso_zu_deutsch(data['current']['time']),
        
        weather_icon_current=weathercode_to_imgsrc(data['current']['weather_code'], True),
        weather_temp_current=data['current']['temperature_2m'],
        weather_temp_min_current=data['daily']['temperature_2m_min'][index_heute],
        weather_temp_max_current=data['daily']['temperature_2m_max'][index_heute],
        
        weather_precipitation_current=data['daily']['precipitation_sum'][index_heute],
        weather_wind_speed_current=data['current']['wind_speed_10m'],
        weather_wind_direction_current=data['current']['wind_direction_10m'],
        
        datum_plus_1=date_iso_zu_deutsch(datum_plus_1),
        weather_icon_plus_1=weathercode_to_imgsrc(data['daily']['weather_code'][index_plus_1], True),
        weather_temp_min_plus_1=data['daily']['temperature_2m_min'][index_plus_1],
        weather_temp_max_plus_1=data['daily']['temperature_2m_max'][index_plus_1],
        
        datum_plus_2=date_iso_zu_deutsch(datum_plus_2),
        weather_icon_plus_2=weathercode_to_imgsrc(data['daily']['weather_code'][index_plus_2], True),
        weather_temp_min_plus_2=data['daily']['temperature_2m_min'][index_plus_2],
        weather_temp_max_plus_2=data['daily']['temperature_2m_max'][index_plus_2],
        
        datum_plus_3=date_iso_zu_deutsch(datum_plus_3),
        weather_icon_plus_3=weathercode_to_imgsrc(data['daily']['weather_code'][index_plus_3], True),
        weather_temp_min_plus_3=data['daily']['temperature_2m_min'][index_plus_3],
        weather_temp_max_plus_3=data['daily']['temperature_2m_max'][index_plus_3],

        kalender=render_html_calender(today),
        muellmorgen=check_muell_morgen(today),
        kalender_plus_1=render_html_calender(today + relativedelta(months=1)),
        kalender_plus_2=render_html_calender(today + relativedelta(months=2))
    )

    with open(file_name_composed, "w", encoding="utf-8") as f:
        f.write(html_fertig)
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1600,1200")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    file_path = "file://" + os.path.abspath(file_name_composed)
    driver.get(file_path)
    time.sleep(1)
    driver.save_screenshot("test.png")
    driver.quit()
else:
    print("ERROR")