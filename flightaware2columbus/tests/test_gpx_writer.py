import os
import unittest
import xml.etree.ElementTree as ET

from flightaware2columbus.gpx_writer import (write2xml, xml_description,
                                             xml_root, xml_trackpoints)


class TestGPX_Writer(unittest.TestCase):
    def setUp(self):
        self.test_filename = 'test.gpx'
        self.desc = {'filename': 'test.csv',
                     'points': '1234',
                     'start_time': '1234-01-01T11:22:33Z',
                     'end_time': '2345-12-12T11:22:33Z',
                     'time_recorded': '123 years 4 days 5 minutes 6 seconds',
                     'distance': '100 km',
                     'average_speed': '222km/h',
                     'max_speed': '333km/h',
                     'max_height': '100m'}
        self.points = [('22.567899', '114.057558', '129', '2018-05-22T15:27:52Z'),
                       ('22.567909', '114.057575', '131', '2018-05-22T15:27:55Z'),
                       ('22.567909', '114.057571', '131', '2018-05-22T15:27:56Z'),
                       ('22.567909', '114.057570', '131', '2018-05-22T15:27:57Z'),
                       ('22.567903', '114.057561', '131', '2018-05-22T15:28:00Z'),
                       ('22.567896', '114.057543', '130', '2018-05-22T15:28:01Z'),
                       ('22.567888', '114.057521', '128', '2018-05-22T15:28:02Z'),
                       ('22.567881', '114.057503', '127', '2018-05-22T15:28:03Z')]

    def test_xml_root(self):
        ret = xml_root()
        assert ret.attrib['version'] == '1.1'
        assert ret.attrib['creator'] == 'Ken Lai (ken.mercus.lai@gmail.com)'
        assert ret.attrib['xmlns:xsi'] == 'http://www.w3.org/2001/XMLSchema-instance'
        assert ret.attrib['xmlns'] == 'http://www.topografix.com/GPX/1/1'
        assert ret.attrib['xsi:schemaLocation'] == 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd'

    def test_xml_description(self):
        ret = xml_description(xml_root(), self.desc)
        assert ret[0][0].text == self.desc['filename']

        desc = ret[0][1].text
        assert all([all([i in desc, self.desc[i] in desc]) for i in self.desc])

        del self.desc['filename']
        ret = xml_description(xml_root(), self.desc)
        assert ret[0][0].text == ''

        desc = ret[0][1].text
        assert all([all([i in desc, self.desc[i] in desc]) for i in self.desc])

    def test_xml_trackpoints(self):
        ret = xml_description(xml_root(), self.desc)
        ret = xml_trackpoints(ret, self.points)
        assert ret[0][2][0].attrib['lat'] == '22.567899'
        assert ret[0][2][0].attrib['lon'] == '114.057558'
        assert ret[0][2][0][0].text == '129'
        assert ret[0][2][0][1].text == '2018-05-22T15:27:52Z'

        assert ret[0][2][3].attrib['lat'] == '22.567909'
        assert ret[0][2][3].attrib['lon'] == '114.057570'
        assert ret[0][2][3][0].text == '131'
        assert ret[0][2][3][1].text == '2018-05-22T15:27:57Z'

        assert ret[0][2][7].attrib['lat'] == '22.567881'
        assert ret[0][2][7].attrib['lon'] == '114.057503'
        assert ret[0][2][7][0].text == '127'
        assert ret[0][2][7][1].text == '2018-05-22T15:28:03Z'

    def test_write2xml(self):
        write2xml(self.desc, self.points, self.test_filename)
        root = ET.parse(self.test_filename).getroot()
        assert root[0][2][0].attrib['lat'] == '22.567899'
        assert root[0][2][0].attrib['lon'] == '114.057558'
        assert root[0][2][0][0].text == '129'
        assert root[0][2][0][1].text == '2018-05-22T15:27:52Z'
        os.remove(self.test_filename)
