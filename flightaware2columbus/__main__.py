#!/usr/bin/env python
import click
import gpx_writer, parsers


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


# @click.command()
# @click.option('--flight', '-f', help='Flight number')
# @click.option('--output', '-o', default=None, help='GPX file to write to')
# def parse_flight_route(flight, output):
#     pass


main.add_command(columbus)
# main.add_command(parse_flight_route)

if __name__ == '__main__':
    main()
