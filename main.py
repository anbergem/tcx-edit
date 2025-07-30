import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone


def from_iso_format(string: str):
    return datetime.fromisoformat(string.replace("Z", "+00:00"))


def to_iso_format(value: datetime):
    return value.isoformat().replace("+00:00", "Z")


def replace(element, offset):
    original = from_iso_format(element.text)
    adjusted = original + offset
    element.text = to_iso_format(adjusted)


def main(input_file, start_time, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Register the namespace to avoid ns0 prefix on output
    ns = {
        'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
    }
    ET.register_namespace('', ns["tcx"])

    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone(timedelta()))
    original_time = None

    # Replace <Id>
    id_elem = root.find('.//tcx:Id', ns)
    if id_elem is not None:
        original_time = from_iso_format(id_elem.text)
        id_elem.text = to_iso_format(start_time)

    if original_time is None:
        raise ValueError("Could not find original time")

    offset = start_time - original_time

    # Replace Lap StartTime attribute
    lap_elem = root.find('.//tcx:Lap', ns)
    if lap_elem is not None:
        lap_elem.set('StartTime', to_iso_format(start_time))

    # Replace all times
    for time_elem in root.findall(".//tcx:Time", ns):
        replace(time_elem, offset)

    tree.write(output_file, encoding="utf-8", xml_declaration=True)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input tcx file")
    parser.add_argument(
        "new_start_time", type=datetime.fromisoformat, help="The output start time")
    parser.add_argument("-o", "--output-file",
                        default="output.tcx", help="Output tcx file")
    args = parser.parse_args()

    main(args.input_file, args.new_start_time, args.output_file)
