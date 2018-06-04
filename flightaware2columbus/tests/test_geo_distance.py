from flightaware2columbus.geo_distance import hav, get_distance_hav


def test_hav():
    assert hav(0) == 0
    assert round(hav(20), 5) == round((-0.5440211108893699) ** 2, 5)


def test_get_distance_hav():
    lon1, lat1 = (22.599578, 113.973129)  # 深圳野生动物园(起点）
    lon2, lat2 = (22.6986848, 114.3311032)  # 深圳坪山站 (百度地图测距：38.3km)
    d2 = get_distance_hav(lon1, lat1, lon2, lat2)
    known_distance = 38.3
    assert known_distance * 0.99 <= d2 <= known_distance * 1.01

    lon2, lat2 = (39.9087202, 116.3974799)  # 北京天安门(1938.4KM)
    d2 = get_distance_hav(lon1, lat1, lon2, lat2)
    known_distance = 1938.4
    assert known_distance * 0.99 <= d2 <= known_distance * 1.01

    lon2, lat2 = (34.0522342, -118.2436849)  # 洛杉矶(11625.7KM)
    d2 = get_distance_hav(lon1, lat1, lon2, lat2)
    known_distance = 11625.7
    assert known_distance * 0.99 <= d2 <= known_distance * 1.01

    lon11, lat11 = (22.599578, 114.973129)
    lon21, lat21 = (34.0522342, -117.2436849)
    assert get_distance_hav(lon1, lat1,
                            lon2, lat2) == get_distance_hav(lon11, lat11,
                                                            lon21, lat21)

    lon11, lat11 = (-22.599578, 114.973129)
    lon21, lat21 = (-34.0522342, -117.2436849)
    assert get_distance_hav(lon1, lat1,
                            lon2, lat2) == get_distance_hav(lon11, lat11,
                                                            lon21, lat21)
