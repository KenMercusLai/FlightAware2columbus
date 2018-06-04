import unittest
from datetime import datetime
from tempfile import NamedTemporaryFile

from flightaware2columbus.parsers import (convert_datetime, desc_columbus,
                                          read_columbus)


class TestParsers(unittest.TestCase):
    def setUp(self):
        header = ('INDEX,TAG,DATE,TIME,LATITUDE N/S,'
                  'LONGITUDE E/W,HEIGHT,SPEED,HEADING,VOX\n')
        csv = header + """1,T,180522,072752,22.567899N,114.057558E,129,0,0,
        2,T,180522,072755,22.567909N,114.057575E,131,0,0,
        3,T,180522,072756,22.567909N,114.057571E,131,0,0,
        4,T,180522,072757,22.567909N,114.057570E,131,0,0,
        5,T,180522,072800,22.567903N,114.057561E,131,0,0,
        6,T,180522,072801,22.567896N,114.057543E,130,0,0,
        7,T,180522,072802,22.567888N,114.057521E,128,0,0,
        8,T,180522,072803,22.567881N,114.057503E,127,0,0,
        9,T,180522,072804,22.567878N,114.057493E,126,0,0,
        10,T,180522,072805,22.567874N,114.057483E,125,0,0,"""
        tmp_file = NamedTemporaryFile(mode='w', delete=False)
        tmp_file.write(csv)
        tmp_file.close()
        self.csv_file = tmp_file.name

    def test_read_columbus(self):
        ret = read_columbus(self.csv_file)
        assert ret[0] == ('22.567899', '114.057558',
                          '129', '2018-05-22T07:27:52Z')
        assert ret[3] == ('22.567909', '114.057570',
                          '131', '2018-05-22T07:27:57Z')
        assert ret[6] == ('22.567888', '114.057521',
                          '128', '2018-05-22T07:28:02Z')
        assert ret[9] == ('22.567874', '114.057483',
                          '125', '2018-05-22T07:28:05Z')

    def test_desc_columbus(self):
        ret = desc_columbus(self.csv_file)
        assert ret['points'] == '10'
        assert ret['start_time'] == '2018-05-22T07:27:52Z'
        assert ret['end_time'] == '2018-05-22T07:28:05Z'
        assert ret['time_recorded'] == '0:00:13'
        assert ret['distance'] == '0'
        assert ret['average_speed'] == '0'
        assert ret['max_height'] == '131'


def test_convert_datetime():
    assert convert_datetime('180522', '072752') == '2018-05-22T07:27:52Z'
    assert convert_datetime('180522', '072752', False) == datetime(
        2018, 5, 22, 7, 27, 52)
    assert convert_datetime('180522', '072802') == '2018-05-22T07:28:02Z'
    assert convert_datetime('180522', '072802', False) == datetime(
        2018, 5, 22, 7, 28, 2)
    assert convert_datetime('180522', '01') == '2018-05-22T00:00:01Z'
