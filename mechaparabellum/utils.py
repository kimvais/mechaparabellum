from xml.etree import ElementTree as ET

from mechaparabellum.units import Unit


def modification_time(path):
    return path.lstat().st_mtime


def get_newest(log_files):
    newest = max(filter(lambda p: p.lstat().st_size > 100_000, log_files), key=modification_time)
    return newest


def to_str(elem):
    return ET.tostring(elem).decode('utf-8')


def get_unit(elem):
    return Unit(int(elem.find('UID').text))
