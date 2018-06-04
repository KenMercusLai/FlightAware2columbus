# pylint: disable=no-self-use,missing-docstring

# import unittest
from unittest.mock import MagicMock

# import click
# from click.testing import CliRunner
from flightaware2columbus.__main__ import columbus
# from flightaware2columbus.parsers import read_columbus


def test_columnbus_echo():
    read_columbus = MagicMock()
    desc_columbus = MagicMock()
    xml_description = MagicMock()
    xml_trackpoints = MagicMock()
    write2xml = MagicMock()
    columbus('file.csv', None)
    assert read_columbus.assert_called_once()
    assert desc_columbus.assert_called_once()
    assert xml_description.assert_called_once()
    assert xml_trackpoints.assert_called_once()
    assert write2xml.assert_not_called()


def test_columnbus_to_gpx():
    read_columbus = MagicMock()
    desc_columbus = MagicMock()
    xml_description = MagicMock()
    xml_trackpoints = MagicMock()
    write2xml = MagicMock()
    columbus('file.csv', 'test.gpx')
    assert read_columbus.assert_called_once()
    assert desc_columbus.assert_called_once()
    assert xml_description.assert_called_once()
    assert xml_trackpoints.assert_called_once()
    assert write2xml.assert_called_once()
