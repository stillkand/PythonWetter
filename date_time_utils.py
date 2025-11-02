from datetime import datetime

def dateTime_iso_zu_deutsch(iso_string):
    try:
        zIso = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M")
        zDe = zIso.strftime("%d.%m.%Y")
        return zDe
    except:
        return "Ungültiges Format"
    
def time_iso_zu_deutsch(iso_string):
    try:
        zIso = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M")
        zDe = zIso.strftime("%H:%M")
        return zDe
    except:
        return "Ungültiges Format"

def date_iso_zu_deutsch(iso_string):
    try:
        zIso = datetime.strptime(iso_string, "%Y-%m-%d")
        zDe = zIso.strftime("%d.%m.%Y")
        return zDe
    except:
        return "Ungültiges Format"

