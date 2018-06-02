import xml.etree.ElementTree as ET


def xml_root():
    root = ET.Element('gpx')
    root.set('version', '1.1')
    root.set('creator', 'Ken Lai (ken.mercus.lai@gmail.com)')
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.set('xmlns', 'http://www.topografix.com/GPX/1/1')
    root.set('xsi:schemaLocation',
             'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd')
    return root


def xml_description(root, descriptions):
    trk = ET.SubElement(root, 'trk')
    name = ET.SubElement(trk, 'name')
    name.text = descriptions.get('filename', '')

    desc = ET.SubElement(trk, 'desc')
    desc.text = '\n'.join([i + ': ' + descriptions[i] for i in descriptions])
    return root


def xml_trackpoints(root, points):
    trkseg = ET.SubElement(root[0], 'trkseg')
    for lat, lon, ele, time in points:
        trkpt = ET.SubElement(trkseg, 'trkpt')
        trkpt.set('lat', lat)
        trkpt.set('lon', lon)
        tmp = ET.SubElement(trkpt, 'ele')
        tmp.text = ele
        tmp = ET.SubElement(trkpt, 'time')
        tmp.text = time
    return root


def write2xml(descriptions, points, filename='waypoints.gpx'):
    xml_data = xml_root()
    xml_data = xml_description(xml_data, descriptions)
    xml_data = xml_trackpoints(xml_data, points)

    with open(filename, 'wb') as f:
        f.write(ET.tostring(xml_data))
