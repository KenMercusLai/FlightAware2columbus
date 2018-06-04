import csv
import os
from datetime import datetime
from geo_distance import get_distance_hav


def convert_datetime(date_str, time_str, string=True):
    year, month, day = [int(date_str[i:i + 2])
                        for i in range(0, len(date_str), 2)]
    time_str = '{:0>6}'.format(time_str)
    hour, minute, second = [int(time_str[i:i + 2])
                            for i in range(0, len(time_str), 2)]
    dt = datetime(2000 + year, month, day, hour, minute, second)
    if string:
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    return dt


def split_records(start, end):
    pass


def read_columbus(csv_file):
    ret = []
    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile)
        for (_, _, DATE, TIME, latitude,
             longitude, height, _, _, _) in list(reader)[1:]:
            if latitude[-1] == 'N':
                latitude = latitude[:-1]
            else:
                latitude = '-' + latitude[:-1]

            if longitude[-1] == 'E':
                longitude = longitude[:-1]
            else:
                longitude = '-' + longitude[:-1]

            date_time = convert_datetime(DATE, TIME)
            ret.append((latitude, longitude, height, date_time))
    return ret


def desc_columbus(csv_file):
    ret = {}
    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile)
        ret['filename'] = os.path.basename(csv_file)
        records = []
        points = 0
        for (_, _, DATE, TIME, latitude,
             longitude, height, _, _, _) in list(reader)[1:]:
            points += 1
            if latitude[-1] == 'N':
                latitude = latitude[:-1]
            else:
                latitude = '-' + latitude[:-1]

            if longitude[-1] == 'E':
                longitude = longitude[:-1]
            else:
                longitude = '-' + longitude[:-1]

            date_time = convert_datetime(DATE, TIME, False)
            records.append((latitude, longitude, height, date_time))
        ret['points'] = str(points)
        ret['start_time'] = records[0][3].strftime('%Y-%m-%dT%H:%M:%SZ')
        ret['end_time'] = records[-1][3].strftime('%Y-%m-%dT%H:%M:%SZ')
        ret['time_recorded'] = records[-1][3] - records[0][3]
        ret['distance'] = get_distance_hav(float(records[-1][0]),
                                           float(records[-1][1]),
                                           float(records[0][0]),
                                           float(records[0][1]))
        ret['average_speed'] = str(round(ret['distance'] /
                                         ret['time_recorded'].total_seconds() /
                                         3600))
        ret['max_height'] = max([i[2] for i in records])
        ret['time_recorded'] = str(ret['time_recorded'])
        ret['distance'] = str(round(ret['distance']))
    return ret
