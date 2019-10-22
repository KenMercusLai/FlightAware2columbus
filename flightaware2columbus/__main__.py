#!/usr/bin/env python
import os
import tempfile
import click
import gpx_writer
import parsers
import flight_parser


@click.group()
def main():
    pass


@click.command()
@click.option('--csv', '-c', type=click.STRING, help='Columbus csv file')
@click.option('--output', '-o', default=None, help='GPX file to write to')
def columbus(csv, output):
    track_points = parsers.read_columbus(csv)
    description = parsers.desc_columbus(csv)
    parsed_data = gpx_writer.xml_description(gpx_writer.xml_root(),
                                             description)
    parsed_data = gpx_writer.xml_trackpoints(parsed_data, track_points)
    if output:
        gpx_writer.write2xml(description,
                             track_points,
                             output)
    else:
        click.echo(parsed_data)


@click.command()
@click.option('--flight_no', '-f', type=click.STRING, help='Flight number')
@click.option('--departure_date', '-d', type=click.STRING, help='Departure date: YYYYMMDD')
@click.option('--output', '-o', default=None, help='GPX file to write to')
def flight(flight_no, departure_date, output):
    temp_csv = tempfile.mkstemp(text=True)[1]
    try:
        records = flight_parser.parse_tracking_log(flight_no, departure_date)
        with open(temp_csv, 'w') as f:
            for i in records:
                i = map(str, i)
                f.write(','.join(i) + '\r')
        track_points = parsers.read_columbus(temp_csv)
        description = parsers.desc_columbus(temp_csv)
        parsed_data = gpx_writer.xml_description(gpx_writer.xml_root(),
                                                 description)
        parsed_data = gpx_writer.xml_trackpoints(parsed_data, track_points)

        if output:
            gpx_writer.write2xml(description,
                                 track_points,
                                 output)
        else:
            click.echo(parsed_data)
    finally:
        os.remove(temp_csv)


main.add_command(columbus)
main.add_command(flight)

if __name__ == '__main__':
    main()
