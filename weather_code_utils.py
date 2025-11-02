def weathercode_to_imgsrc(weathercode, isday):
    if isday:
        return weathercode_to_imgsrc_day(weathercode)
    else:
        return weathercode_to_imgsrc_night(weathercode)

def weathercode_to_imgsrc_day(weathercode):
    code_map = {
        0: "svg/wi-day-sunny.svg", # sunny
        1: "svg/wi-day-sunny.svg", # mainly sunny
        2: "svg/wi-day-cloudy.svg", # partly cloudy
        3: "svg/wi-cloudy.svg", # cloudy
        
        45: "svg/wi-day-fog.svg", # foggy
        48: "svg/wi-fog.svg", # rime fog
        
        51: "svg/wi-day-rain-mix.svg", # light drizzle
        53: "svg/wi-rain-mix.svg", # drizzle
        55: "svg/wi-rain-mix.svg", # heavy drizzle
        56: "svg/wi-day-rain-mix.svg", # light freezing drizzle
        57: "svg/wi-rain-mix.svg", # freezing  drizzle
        
        61: "svg/wi-day-rain.svg", # light rain
        63: "svg/wi-rain.svg", # rain
        65: "svg/wi-rain.svg", # heavy rain
        
        66: "svg/wi-day-sleet.svg", # light freezing  rain
        67: "svg/wi-sleet.svg", # freezing rain
        
        71: "svg/wi-day-snow.svg", # light snow
        73: "svg/wi-snow.svg", # snow
        75: "svg/wi-snow.svg", # heavy snow
        77: "svg/wi-snow.svg", # snow grains
        
        80: "svg/wi-day-showers.svg", # light showers
        81: "svg/wi-showers.svg", # showers
        82: "svg/wi-storm-showers.svg", # heavy showers
        85: "svg/wi-sleet", # light snow  showers
        86: "svg/wi-sleet", # snow showers
        
        95: "svg/wi-thunderstorm", # thunderstorm
        96: "svg/wi-hail.svg", # light thunderstorm with hail
        99: "svg/wi-hail.svg", # thunderstorm with hail
    }

    return code_map.get(weathercode, "svg/wi-na.svg")

def weathercode_to_imgsrc_night(weathercode):
    code_map = {
        0: "svg/wi-night-clear.svg", # clear
        1: "svg/wi-night-clearsvg", # mainly clear
        2: "svg/wi-night-alt-cloudy.svg", # partly cloudy
        3: "svg/wi-cloudy.svg", # cloudy
        
        45: "svg/wi-night-fog.svg", # foggy
        48: "svg/wi-fog.svg", # rime fog
        
        51: "svg/wi-night-rain-mix.svg", # light drizzle
        53: "svg/wi-rain-mix.svg", # drizzle
        55: "svg/wi-rain-mix.svg", # heavy drizzle
        56: "svg/wi-night-rain-mix.svg", # light freezing drizzle
        57: "svg/wi-rain-mix.svg", # freezing  drizzle
        
        61: "svg/wi-night-rain.svg", # light rain
        63: "svg/wi-rain.svg", # rain
        65: "svg/wi-rain.svg", # heavy rain
        
        66: "svg/wi-night-sleet.svg", # light freezing  rain
        67: "svg/wi-sleet.svg", # freezing rain
        
        71: "svg/wi-night-snow.svg", # light snow
        73: "svg/wi-snow.svg", # snow
        75: "svg/wi-snow.svg", # heavy snow
        77: "svg/wi-snow.svg", # snow grains
        
        80: "svg/wi-night-showers.svg", # light showers
        81: "svg/wi-showers.svg", # showers
        82: "svg/wi-storm-showers.svg", # heavy showers
        85: "svg/wi-sleet", # light snow  showers
        86: "svg/wi-sleet", # snow showers
        
        95: "svg/wi-thunderstorm", # thunderstorm
        96: "svg/wi-hail.svg", # light thunderstorm with hail
        99: "svg/wi-hail.svg", # thunderstorm with hail
    }

    return code_map.get(weathercode, "svg/wi-na.svg")