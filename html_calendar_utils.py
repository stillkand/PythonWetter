import os
import calendar
from datetime import date, timedelta
from ics import Calendar

# Deutsche Monatsnamen und Wochentage
deutsche_monate = [
    "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"
]
deutsche_wochentage = [
    "Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"
]

def render_html_calender(today):
    # Aktuelles Datum
    jahr = today.year
    monat = today.month
    tag = today.day

    dateinameLeerungstermine = f"ical/Leerungstermine{jahr}.ics"
    if os.path.exists(dateinameLeerungstermine):
        with open(dateinameLeerungstermine, "r", encoding="utf-8") as f:
            leerungskalender = Calendar(f.read())

    feiertagEvents = set() 
    dateinameFeiertage = f"ical/Feiertage{jahr}.ics"
    if os.path.exists(dateinameFeiertage):
        with open(dateinameFeiertage, "r", encoding="utf-8") as f:
            feiertagekalender = Calendar(f.read())    
            feiertagEvents = {event.begin.date() for event in feiertagekalender.events}

    # Kalenderdaten generieren
    cal = calendar.Calendar(firstweekday=0)  # Montag = 0
    tage = cal.monthdayscalendar(jahr, monat)

    # HTML generieren
    html = f"""
        <table>
            <caption>{deutsche_monate[monat-1]} {jahr}</caption>
            <tr>{"".join(f"<th>{tag}</th>" for tag in deutsche_wochentage)}</tr>
    """
    for woche in tage:
        html += "<tr>"
        for i, tag in enumerate(woche):
            if tag == 0:
                html += "<td></td>"
            else:
                classes = []
                datum = date(jahr, monat, tag)
                if datum in feiertagEvents:
                    classes.append("feiertag")
                if i >= 5:  # Samstag oder Sonntag
                    classes.append("weekend")
                if datum == date.today():
                    classes.append("today")
                class_attr = f" class='{' '.join(classes)}'" if classes else ""
                html += f"<td{class_attr}>{tag}"
                html += check_muell_termin(leerungskalender, datum)
                html += "</div></td>"
        html += "</tr>"
    html += "</table>"
    return html

def check_muell_termin(kalender, suchdatum):
    returnvalue = "<span class=\"marker\"> "

    events = [e for e in kalender.events if e.begin.date() == suchdatum]
    if events:
        for e in events:
            eventname = e.name.lower()

            if "restmüll" in eventname:
                returnvalue += "R "
            if "bioabfall" in eventname:
                returnvalue += "B "
            if "papier" in eventname:
                returnvalue += "P "
            if "gelbe tonne" in eventname:
                returnvalue += "G "
            if "problemmüll" in eventname:
                returnvalue += "S "

    returnvalue += "</span>"

    return returnvalue

def check_muell_morgen(today):
    returnvalue = ""
    # Aktuelles Datum
    jahr = today.year

    dateinameLeerungstermine = f"ical/Leerungstermine{jahr}.ics"
    if os.path.exists(dateinameLeerungstermine):
        with open(dateinameLeerungstermine, "r", encoding="utf-8") as f:
            leerungskalender = Calendar(f.read())
    
    morgen = (today + timedelta(days=1))
    events = [e for e in leerungskalender.events if e.begin.date() == morgen]
    if events:
        returnvalue = "<p class=\"muellmorgen\">morgen "

        for e in events:
            eventname = e.name.lower()

            if "restmüll" in eventname:
                returnvalue += "Restmüll "
            if "bioabfall" in eventname:
                returnvalue += "Biomüll "
            if "papier" in eventname:
                returnvalue += "Papiermüll "
            if "gelbe tonne" in eventname:
                returnvalue += "Gelbe Tonne "
            if "problemmüll" in eventname:
                returnvalue += "Problemmüll "

        returnvalue += "!!!</p>"
    
    return returnvalue