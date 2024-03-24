from geopy.distance import distance


def get_surrounding_square(lat: float, lng: float, radius_miles: int) -> dict:
    """
    Вычисляет координаты квадрата вокруг заданной точки.

    :param lat: Широта центральной точки в градусах.
    :param lng: Долгота центральной точки в градусах.
    :param radius_miles: Радиус вокруг центральной точки в милях.
    :return: Словарь с минимальной и максимальной широтой и минимальной
    и максимальной долготой (min_lng, max_lng) квадрата.
    """
    origin = (lat, lng)

    north = distance(miles=radius_miles).destination(origin, bearing=0)
    south = distance(miles=radius_miles).destination(origin, bearing=180)
    east = distance(miles=radius_miles).destination(origin, bearing=90)
    west = distance(miles=radius_miles).destination(origin, bearing=270)

    return {
        'min_lat': south[0],
        'max_lat': north[0],
        'min_lng': west[1],
        'max_lng': east[1]
    }
