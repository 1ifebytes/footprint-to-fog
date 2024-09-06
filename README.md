# CSV(footprint) to GPX(fog) Converter

This project provides a simple Python script to convert CSV (Comma-Separated Values) files containing GPS data into GPX (GPS Exchange Format) files. GPX is a lightweight XML data format for the interchange of GPS data (waypoints, routes, and tracks) between applications and Web services on the Internet.

## Features

- Converts CSV files with GPS data to GPX format
- Handles latitude, longitude, altitude, and timestamp data
- Creates a single track with track points in the GPX file
- Easy to use and modify for different CSV formats

## Requirements

- Python 3.x
- No additional libraries required (uses only Python standard library)

## Installation

1. Clone this repository or download the `csv_to_gpx.py` file.
2. Ensure you have Python 3.x installed on your system.

## Usage

1. Place your CSV file in the same directory as the `csv_to_gpx.py` script.
2. Open a terminal or command prompt and navigate to the directory containing the script.
3. Run the script using Python:

```
python3 csv_to_gpx.py
```

4. The script will create an `output.gpx` file in the same directory.

## CSV File Format

The script expects the CSV file to have the following columns:

- `latitude`: The latitude of the GPS point
- `longitude`: The longitude of the GPS point
- `altitude`: The altitude of the GPS point
- `dataTime`: The timestamp of the GPS point (in Unix timestamp format)

Example CSV format:

```
dataTime,locType,longitude,latitude,heading,accuracy,speed,distance,isBackForeground,stepType,altitude
1724976209,1,121.533817,31.206857,0.000000,35.000000,-1.000000,81.926268,1,0,13.073089
1724976314,1,121.533620,31.207559,0.000000,10.000000,2.880889,80.096253,1,0,11.000000
...
```

## Customization

If your CSV file has different column names or additional data you want to include in the GPX file, you can modify the `csv_to_gpx` function in the script to accommodate your specific needs.

## Contributing

Contributions to improve the script or add new features are welcome. Please feel free to submit a pull request or open an issue to discuss potential changes/additions.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

If you have any questions or feedback, please open an issue on the GitHub repository.

---

Happy converting!
