import astral


def get_sunrise_sunset(city, date=None):
    a = astral.Astral()
    city = a[city]
    sun = city.sun(local=True, date=date)
    return sun["sunrise"], sun["sunset"]
