from datetime import date

class WeatherData:
    def __init__(self, weatherdate,  weathercode, temp_min, temp_max, temp_unit):
        self.weatherdate = weatherdate
        self.weathercode = weathercode
        self.temp_min = temp_min
        self.temp_max = temp_max
        self._temp_unit = temp_unit
        self._temp_current = None
        self._precipitation = None
        self._precipitation_unit = None
        self._wind = None
        self._wind_unit = None
        self._wind_direction = None

    # region Properties
    # --- Datum ---
    @property
    def weatherdate(self):
        return self._weatherdate
    
    @weatherdate.setter
    def weatherdate(self, value):
        if not isinstance(value, date):
            raise TypeError("WeatherDate muss ein datetime.date Objekt sein.")
        self._weatherdate = value

    # --- Wettercode ---
    @property
    def weathercode(self):
        return self._weathercode
    
    @weathercode.setter
    def weathercode(self, value):
        if not isinstance(value, int):
            raise TypeError("WeatherCode muss eine ganze Zahl (int) sein.")
        self._weathercode = value
        
    # --- Mindesttemperatur ---
    @property
    def temp_min(self):
        return self._temp_min
    
    @temp_min.setter
    def temp_min(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("TempMin muss eine Zahl sein.")
        self._temp_min = value
        # Wenn bereits temp_max gesetzt ist, prüfen wir die Logik:
        if hasattr(self, "_temp_max") and self._temp_min > self._temp_max:
            raise ValueError("TempMin darf nicht größer sein als TempMax.")
    
    # --- Höchsttemperatur ---    
    @property
    def temp_max(self):
        return self._temp_max
    
    @temp_max.setter
    def temp_max(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("TempMax muss eine Zahl sein.")
        self._temp_max = value
        # Wenn bereits temp_min gesetzt ist, prüfen wir die Logik:
        if hasattr(self, "_temp_min") and self._temp_min > self._temp_max:
            raise ValueError("TempMin darf nicht größer sein als TempMax.")
    
    # --- Aktuelle Temperatur ---
    @property
    def temp_current(self):
        return self._temp_current
    
    @temp_current.setter
    def temp_current(self, value):
        self._temp_current = value
    
    # --- Einheit der Temperatur ---
    @property
    def temp_unit(self):
        return self._temp_unit
    
    # --- Niederschlag ---
    @property 
    def precipitation(self):
        return self._precipitation
    
    @precipitation.setter
    def precipitation(self, value):
        self._precipitation = value

    # --- Niederschlag Einheit ---
    @property 
    def precipitation_unit(self):
        return self._precipitation_unit
    
    @precipitation_unit.setter
    def precipitation_unit(self, value):
        self._precipitation_unit = value

    # --- Wind ---
    @property 
    def wind(self):
        return self._wind
    
    @wind.setter
    def wind(self, value):
        self._wind = value

    # --- Wind Einheit ---
    @property 
    def wind_unit(self):
        return self._wind_unit
    
    @wind_unit.setter
    def wind_unit(self, value):
        self._wind_unit = value

    # --- Wind Richtung ---
    @property 
    def wind_direction(self):
        return self._wind_direction
    
    @wind_direction.setter
    def wind_direction(self, value):
        self._wind_direction = value

    # --- Wind Richtung Einheit ---
    @property 
    def wind_direction_unit(self):
        return self._wind_direction_unit
    
    @wind_direction_unit.setter
    def wind_direction_unit(self, value):
        self._wind_direction_unit = value

    # endregion Properties

    # --- __repr__ für Entwickler/Debugging ---
    def __repr__(self):
        return (f"WeatherData(date={self.weatherdate}, weathercode={self.weathercode}, "
                f"temp_min={self.temp_min}{self.temp_unit}, "
                f"temp_max={self.temp_max}{self.temp_unit}, "
                f"temp_current={self.temp_current}{self.temp_unit}, "
                f"precipitation={self.precipitation}{self.precipitation_unit}, "
                f"wind={self.wind}{self.wind_unit}, "
                f"wind_direction={self.wind_direction}{self.wind_direction_unit})")

    # --- __str__ für Benutzer ---
    def __str__(self):
        parts = [
            f"Datum: {self.weatherdate}",
            f"Wettercode: {self.weathercode}",
            f"Temperatur: {self.temp_min}–{self.temp_max} {self.temp_unit}" + 
            (f", aktuell {self.temp_current}{self.temp_unit}" if self.temp_current is not None else ""),
            f"Niederschlag: {self.precipitation}{self.precipitation_unit}" if self.precipitation is not None else None,
            f"Wind: {self.wind}{self.wind_unit}" if self.wind is not None else None,
            f"Windrichtung: {self.wind_direction}{self.wind_direction_unit}" if self.wind_direction is not None else None
        ]
        # Filtere None-Werte weg
        return ", ".join(filter(None, parts))