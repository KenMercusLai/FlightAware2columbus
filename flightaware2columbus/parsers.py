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


def flatten_list(alist):
    ret = []
    for i in alist:
        if type(i) is list or type(i) is tuple:
            ret += list(i)
        else:
            ret.append(i)
    return ret


def slices_records(ret, distance_threshold=10):
    record_pairs = [i for i in zip(ret, ret[1:])]
    for i, v in enumerate(record_pairs):
        start_point, end_point = v
        distance = get_distance_hav(float(start_point[0]),
                                    float(start_point[1]),
                                    float(end_point[0]),
                                    float(end_point[1]))
        if distance > distance_threshold:
            n = int((distance / distance_threshold) + 1)
            record_pairs[i] = split_records(start_point, end_point, n)
    for i in flatten_list(record_pairs):
        print(i)
    print(len(flatten_list(record_pairs)))
    return flatten_list(record_pairs)


def split_records(start_point, end_point, n):
    def to_dt(dt_str):
        return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%SZ')

    def to_str(dt):
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    ret = []
    ret.append(start_point)

    latitude_step = (float(end_point[0]) - float(start_point[0])) / n
    longitude_step = (float(end_point[1]) - float(start_point[1])) / n
    height_step = (float(end_point[2]) - float(start_point[2])) / n
    date_time_step = (to_dt(end_point[3]) - to_dt(start_point[3])) / n

    for i in range(1, n + 1):
        ret.append((str(float(start_point[0]) + latitude_step * i),
                    str(float(start_point[1]) + longitude_step * i),
                    str(float(start_point[2]) + height_step * i),
                    to_str(to_dt(start_point[3]) + date_time_step * i)))
    return ret


def read_columbus(csv_file):
    ret = []
    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile)
        for (_, _, DATE, TIME, latitude,
             longitude, height, _, _, _) in list(reader)[1:]:
            if latitude[-1] == 'N':
                latitude = latitude[:-1].strip()
            else:
                latitude = '-' + latitude[:-1].strip()

            if longitude[-1] == 'E':
                longitude = longitude[:-1].strip()
            else:
                longitude = '-' + longitude[:-1].strip()

            date_time = convert_datetime(DATE, TIME)
            ret.append((latitude, longitude, height, date_time))
    return slices_records(ret, 1)


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
        ret['average_speed'] = str(round(ret['distance']
                                         / ret['time_recorded'].total_seconds()
                                         / 3600))
        ret['max_height'] = max([i[2] for i in records])
        ret['time_recorded'] = str(ret['time_recorded'])
        ret['distance'] = str(round(ret['distance']))
    return ret
