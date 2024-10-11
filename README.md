# CSV to GPX Converter | CSV到GPX转换器

[English](#english) | [中文](#chinese)

<a name="english"></a>
## English

This project provides a simple Python script to convert CSV (Comma-Separated Values) files containing GPS data into GPX (GPS Exchange Format) files. GPX is a lightweight XML data format for the interchange of GPS data (waypoints, routes, and tracks) between applications and Web services on the Internet.

### Features

- Converts CSV files with GPS data to GPX format
- Handles latitude, longitude, altitude, and timestamp data
- Creates a single track with track points in the GPX file
- Easy to use and modify for different CSV formats

### Requirements

- Python 3.x
- No additional libraries required (uses only Python standard library)

### Installation

1. Clone this repository or download the `csv-to-gpx-converter.py` file.
2. Ensure you have Python 3.x installed on your system.

### Usage

1. Place your CSV file in the same directory as the `csv-to-gpx-converter.py` script.
2. Open a terminal or command prompt and navigate to the directory containing the script.
3. Run the script using Python:

```
python3 csv-to-gpx-converter.py
```

4. The script will create an `output.gpx` file in the same directory.

### CSV File Format

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

### Customization

If your CSV file has different column names or additional data you want to include in the GPX file, you can modify the `csv-to-gpx-converter` function in the script to accommodate your specific needs.

### Contributing

Contributions to improve the script or add new features are welcome. Please feel free to submit a pull request or open an issue to discuss potential changes/additions.

### License

This project is open source and available under the MIT License.

### Contact

If you have any questions or feedback, please open an issue on the GitHub repository.

Happy converting!

---

<a name="chinese"></a>
## 中文

这个项目提供了一个简单的Python脚本，用于将包含GPS数据的CSV（逗号分隔值）文件转换为GPX（GPS交换格式）文件。GPX是一种轻量级的XML数据格式，用于在互联网上的应用程序和Web服务之间交换GPS数据（航点、路线和轨迹）。

### 特性

- 将含有GPS数据的CSV文件转换为GPX格式
- 处理纬度、经度、海拔和时间戳数据
- 在GPX文件中创建带有轨迹点的单一轨迹
- 易于使用和修改，适用于不同的CSV格式

### 要求

- Python 3.x
- 不需要额外的库（仅使用Python标准库）

### 安装

1. 克隆此仓库或下载 `csv-to-gpx-converter.py` 文件。
2. 确保您的系统上安装了Python 3.x。

### 使用方法

1. 将您的CSV文件放在与 `csv-to-gpx-converter.py` 脚本相同的目录中。
2. 打开终端或命令提示符，并导航到包含脚本的目录。
3. 使用Python运行脚本：

```
python3 csv-to-gpx-converter.py
```

4. 脚本将在同一目录中创建一个 `output.gpx` 文件。

### CSV文件格式

脚本期望CSV文件具有以下列：

- `latitude`：GPS点的纬度
- `longitude`：GPS点的经度
- `altitude`：GPS点的海拔
- `dataTime`：GPS点的时间戳（Unix时间戳格式）

CSV格式示例：

```
dataTime,locType,longitude,latitude,heading,accuracy,speed,distance,isBackForeground,stepType,altitude
1724976209,1,121.533817,31.206857,0.000000,35.000000,-1.000000,81.926268,1,0,13.073089
1724976314,1,121.533620,31.207559,0.000000,10.000000,2.880889,80.096253,1,0,11.000000
...
```

### 自定义

如果您的CSV文件有不同的列名或您想在GPX文件中包含额外的数据，您可以修改脚本中的 `csv-to-gpx-converter` 函数以适应您的特定需求。

### 贡献

欢迎提供改进脚本或添加新功能的贡献。请随时提交拉取请求或打开问题来讨论潜在的更改/添加。

### 许可证

该项目是开源的，根据MIT许可证提供。

### 联系

如果您有任何问题或反馈，请在GitHub仓库上开一个问题。

祝您转换愉快！

