import os
import sys
import click
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time
import re
from geopy import Point

namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

def convert(kml_file, gpx_file, interval=0, date=''):
    tree = ET.parse(kml_file)
    root = tree.getroot()
    
    gpx_header = '<?xml version="1.0" encoding="UTF-8"?>\n'
    gpx_header += '<gpx version="1.1" xmlns="http://www.topografix.com/GPX/1/1">\n'
    gpx_footer = '</gpx>'

    coordinates = []
    timestamps = []

    # Path getter
    for document in root.findall('.//kml:Document', namespace):
        for folder in document.findall('.//kml:Folder', namespace):
            for name in folder.findall('.//kml:name', namespace):
                if name.text == 'Route':
                    for placemark in folder.findall('.//kml:Placemark', namespace):
                        # Get timestamps
                        for timestamp in placemark.findall('.//kml:TimeStamp', namespace):
                            for time in timestamp.findall('.//kml:when', namespace):
                                timestamps.append(time.text)
                                
                        # Get coordinates
                        for point in placemark.findall('.//kml:Point', namespace):
                            for coord in point.findall('.//kml:coordinates', namespace):
                                coords = coord.text.split(',')  # 116.534554,39.497799,792.48
                                lon, lat, alt = coords
                                coordinates.append((lon, lat, alt))
                else:
                    continue
    
    print(f"Found {len(coordinates)} coordinates and {len(timestamps)} timestamps.")
    
    # Track point fixer
    fixed_coordinates = []
    fixed_timestamps = []
    if interval:
        std_interval = interval  # seconds
        for idx, (coord, time) in enumerate(zip(coordinates, timestamps)):
            fixed_coordinates.append(coord)
            fixed_timestamps.append(time)
            if idx == len(coordinates) - 1:
                break
            else:
                next_time = datetime.fromisoformat(timestamps[idx+1])
                current_time = datetime.fromisoformat(fixed_timestamps[-1])
                time_diff = (next_time - current_time).total_seconds()
                
                # Time Interval Solution
                needed_points = int(time_diff / std_interval)
                if needed_points > 1:
                    original_point = Point(coord[1], coord[0], coord[2])
                    destination = Point(coordinates[idx+1][1], coordinates[idx+1][0], coordinates[idx+1][2])
                    for i in range(1, needed_points):
                        fixed_timestamps.append((current_time + timedelta(seconds=std_interval * i)).isoformat())
                        fraction = i / needed_points
                        new_point = Point(original_point[0] + fraction * (destination[0] - original_point[0]), 
                                        original_point[1] + fraction * (destination[1] - original_point[1]), 
                                        original_point[2] + fraction * (destination[2] - original_point[2]))
                        fixed_coordinates.append((new_point[1], new_point[0], new_point[2]))
                          
        print(f"Fixed {len(fixed_coordinates)} coordinates and {len(fixed_timestamps)} timestamps.")
        
    else:
        fixed_coordinates = coordinates
        fixed_timestamps = timestamps
        
    # Date fixer
    if date:
        date_diff = (datetime.fromisoformat(fixed_timestamps[0]) + timedelta(hours=8)).date() - datetime.strptime(date, '%Y-%m-%d').date()  # UTC+8
        for idx, time in enumerate(fixed_timestamps):
            fixed_timestamps[idx] = (datetime.fromisoformat(time) - timedelta(days=date_diff.days)).isoformat()
    
    # GPX file writer       
    gpx_tracks = ''
    gpx_tracks += '<trk>\n'
    gpx_tracks += '<trkseg>\n'
    for coord, time in zip(fixed_coordinates, fixed_timestamps):
        gpx_tracks += f'<trkpt lat="{coord[1]}" lon="{coord[0]}">\n'
        gpx_tracks += f'<ele>{coord[2]}</ele>\n'
        gpx_tracks += f'<time>{datetime.fromisoformat(time).strftime("%Y-%m-%dT%H:%M:%S.000Z")}</time>\n'
        gpx_tracks += '</trkpt>\n'
    gpx_tracks += '</trkseg>\n'
    gpx_tracks += '</trk>\n'
    
    gpx_content = gpx_header + gpx_tracks + gpx_footer

    with open(gpx_file, 'w') as f:
        f.write(gpx_content)

    print(f"Conversion complete. Saved to {gpx_file}")
    
# CLI
@click.command()
def setup():
    kml_file = click.prompt("Please enter the KML file path")
    kml_file = re.sub(r"^.*?['\"](.*?)[\"'].*$", r"\1", kml_file)
    if not os.path.isfile(kml_file):
        click.echo(f"Error: {kml_file} does not exist.")
        time.sleep(3)
        sys.exit(1)
    gpx_file = click.prompt("Please type the desired name of the GPX file to be saved", 
                        default=os.path.splitext(kml_file)[0] + ".gpx")
    interval = click.prompt("Please type the desired interval between track points for solving discontinuous path, if there is no need, click the ENTER.", 
                        type=int, default=0)
    date = click.prompt("Please type the desired departure date of the flight in the format 'YYYY-MM-DD' (In CST), if there is no need, click the ENTER.", 
                        default='')
    convert(kml_file, gpx_file, interval, date)
    print("Conversion complete.")
    time.sleep(3)
    sys.exit(0)

if __name__ == "__main__":
    setup()