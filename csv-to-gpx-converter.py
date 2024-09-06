import csv
from datetime import datetime
import xml.etree.ElementTree as ET

def csv_to_gpx(csv_file, gpx_file):
    # Create the root element
    gpx = ET.Element('gpx', version="1.1", creator="CSV to GPX Converter",
                     xmlns="http://www.topografix.com/GPX/1/1")

    # Create a track
    trk = ET.SubElement(gpx, 'trk')
    name = ET.SubElement(trk, 'name')
    name.text = "Converted from CSV"
    trkseg = ET.SubElement(trk, 'trkseg')

    # Read the CSV file
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create a trackpoint
            trkpt = ET.SubElement(trkseg, 'trkpt', lat=row['latitude'], lon=row['longitude'])
            
            # Add elevation
            ele = ET.SubElement(trkpt, 'ele')
            ele.text = row['altitude']
            
            # Add time
            time = ET.SubElement(trkpt, 'time')
            time.text = datetime.fromtimestamp(int(row['dataTime'])).isoformat() + "Z"

    # Create the tree and save to file
    tree = ET.ElementTree(gpx)
    tree.write(gpx_file, encoding='utf-8', xml_declaration=True)

# Usage
csv_to_gpx('backUpData.csv', 'output.gpx')

print("Conversion completed. GPX file has been created.")
