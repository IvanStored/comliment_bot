from typing import Any


def dist_between_two_lat_lon(*args) -> float:
    from math import asin, cos, radians, sin, sqrt

    lat1, lat2, long1, long2 = map(radians, args)

    dist_lats = abs(lat2 - lat1)
    dist_longs = abs(long2 - long1)
    a = (
        sin(dist_lats / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dist_longs / 2) ** 2
    )
    c = asin(sqrt(a)) * 2
    radius_earth = 6378
    return c * radius_earth


def find_closest_lat_lon(data, v) -> Any:
    try:
        return min(
            data,
            key=lambda p: dist_between_two_lat_lon(
                v['lan'], p['lan'], v['lon'], p['lon']
            ),
        )
    except TypeError:
        print('Not a list or not a number.')
