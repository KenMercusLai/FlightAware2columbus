from datetime import datetime
from datetime import timedelta
from requests_html import HTMLSession


def find_log_url(flight_number: str, departure_date: str):
    session = HTMLSession()
    try:
        r = session.get(
            "https://flightaware.com/live/flight/" + flight_number).url
        r = session.get(r + '/history')
        log_url = [i for i in r.html.absolute_links
                   if departure_date in i][0] + '/tracklog'
        return log_url
    except NotImplemented:
        raise "flight doesn't exist"


def read_texts(html):
    if html.find('.show-for-medium-up'):
        return html.find('.show-for-medium-up')[0].text
    else:
        return html.text


def convert_latitude(lat):
    lat = float(lat)
    number = '{:.6f}'.format(abs(lat))
    if lat < 0:
        suffix = 'S'
    else:
        suffix = 'N'
    return number+suffix


def convert_longitude(lon):
    lon = float(lon)
    number = '{:.6f}'.format(abs(lon))
    if lon < 0:
        suffix = 'W'
    else:
        suffix = 'E'
    return number+suffix


def parse_tracking_log(flight_number: str, departure_date: str):
    session = HTMLSession()
    r = session.get(find_log_url(flight_number, departure_date))
    records = [('INDEX', 'TAG', 'DATE', 'TIME', 'LATITUDE N/S',
                'LONGITUDE E/W', 'HEIGHT', 'SPEED', 'HEADING', '123')]
    if r.ok:
        table_rows = r.html.find('tr.smallrow1, tr.smallrow2')
        for i in table_rows:
            cells = i.find('td')
            if len(cells) == 9:
                cell_content = list(map(read_texts, cells))
                record_time, latitude, longitude, _, _, _, _, _, _ = cell_content
                record_time = datetime.strptime(departure_date + ' ' + record_time,
                                                '%Y%m%d %a %H:%M:%S')
                if departure_date + record_time.strftime('%H%M%S') < records[-1][2]+records[-1][3]:
                    record_time += timedelta(days=1)
                latitude = convert_latitude(latitude)
                longitude = convert_longitude(longitude)
                records.append((len(records), 'T', record_time.strftime('%y%m%d'), record_time.strftime('%H%M%S'), latitude,
                                longitude, 0, 0, 0, 0))
    return records
