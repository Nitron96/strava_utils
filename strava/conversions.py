import math

METER_TO_MILE = 1609.34
METER_TO_KM = 1000

METER_TO_FEET = 3.28084


def round_down(value, decimals):
    return math.floor(value * 10**decimals)/10**decimals


def convert_distance(meters):
    return round_down(meters/METER_TO_MILE, 2)


def convert_elevation(meters):
    return round(meters*METER_TO_FEET)


# Take meters/second and returns seconds per mile (use timedelta to determine minutes/mile)
def convert_speed(speed):
    return round(1/speed * METER_TO_MILE)