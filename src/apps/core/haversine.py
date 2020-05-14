from django.db.models import F, Func


class Sin(Func):
    function = 'SIN'


class Cos(Func):
    function = 'COS'


class Acos(Func):
    function = 'ACOS'


class Radians(Func):
    function = 'RADIANS'


def calculate_distance(target_field: tuple = ('latitude', 'longitude')):
    # radlat = Radians(lat)  # given latitude
    # radlong = Radians(lng)  # given longitude
    radlat = Radians(F('user_latitude'))
    radlong = Radians(F('user_longitude'))
    radflat = Radians(F(target_field[0]))
    radflong = Radians(F(target_field[1]))

    # 6371 for kilometers
    return 6371 * Acos(Cos(radlat) * Cos(radflat) *
                       Cos(radflong - radlong) +
                       Sin(radlat) * Sin(radflat))
