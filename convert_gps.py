import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from geopy.distance import geodesic
import math
from datetime import datetime, timedelta
import argparse
import os
import pytz

def convert_utc_to_local(utc_timestamp):
    """将UTC时间戳转换为东八区时间戳"""
    utc_time = datetime.fromtimestamp(utc_timestamp, pytz.UTC)
    local_tz = pytz.timezone('Asia/Shanghai')  # 东八区
    local_time = utc_time.astimezone(local_tz)
    return int(local_time.timestamp())

def calculate_distance(lat1, lon1, lat2, lon2):
    """计算两点间的距离（米）"""
    return geodesic((lat1, lon1), (lat2, lon2)).meters

def calculate_bearing(lat1, lon1, lat2, lon2):
    """计算方位角"""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    d_lon = lon2 - lon1
    y = math.sin(d_lon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
    bearing = math.degrees(math.atan2(y, x))
    return float((bearing + 360) % 360)

def interpolate_points(start_point, end_point, num_points):
    """在两点之间进行线性插值"""
    times = np.linspace(start_point['dataTime'], end_point['dataTime'], num_points)
    lats = np.linspace(start_point['latitude'], end_point['latitude'], num_points)
    lons = np.linspace(start_point['longitude'], end_point['longitude'], num_points)
    speeds = np.linspace(start_point['speed'], end_point['speed'], num_points)
    alts = np.linspace(start_point['altitude'], end_point['altitude'], num_points)
    
    points = []
    for i in range(num_points):
        points.append({
            'dataTime': int(times[i]),
            'latitude': float(lats[i]),
            'longitude': float(lons[i]),
            'speed': float(speeds[i]),
            'altitude': float(alts[i])
        })
    return points

def process_trajectory(df, target_points=1812):
    """处理轨迹数据，包括插值和距离计算"""
    # 按时间排序
    df = df.sort_values('dataTime').reset_index(drop=True)
    
    # 计算需要的插值点数
    total_time = df['dataTime'].max() - df['dataTime'].min()
    avg_interval = total_time / (target_points - 1)
    
    # 存储处理后的点
    processed_points = []
    total_distance = 0.0
    
    for i in range(len(df) - 1):
        start_point = df.iloc[i].to_dict()
        end_point = df.iloc[i + 1].to_dict()
        
        time_diff = end_point['dataTime'] - start_point['dataTime']
        num_points = max(2, int(time_diff / avg_interval))
        
        # 生成插值点
        interpolated = interpolate_points(start_point, end_point, num_points)
        
        for j, point in enumerate(interpolated):
            if j > 0 or i == 0:
                if len(processed_points) > 0:
                    # 计算与前一点的距离
                    prev_point = processed_points[-1]
                    segment_distance = calculate_distance(
                        prev_point['latitude'], prev_point['longitude'],
                        point['latitude'], point['longitude']
                    )
                    total_distance += segment_distance
                    
                    # 计算方位角
                    heading = calculate_bearing(
                        prev_point['latitude'], prev_point['longitude'],
                        point['latitude'], point['longitude']
                    )
                else:
                    heading = 0.0
                
                point_data = {
                    'dataTime': point['dataTime'],
                    'locType': 1,
                    'longitude': point['longitude'],
                    'latitude': point['latitude'],
                    'heading': heading,
                    'accuracy': 10.0,
                    'speed': point['speed'],
                    'distance': float(total_distance),
                    'isBackForeground': 1,
                    'stepType': 1,
                    'altitude': point['altitude']
                }
                processed_points.append(point_data)
    
    # 转换为DataFrame
    result_df = pd.DataFrame(processed_points)
    
    # 确保所有数值列都是浮点型
    float_columns = ['longitude', 'latitude', 'heading', 'accuracy', 'speed', 'distance', 'altitude']
    for col in float_columns:
        result_df[col] = result_df[col].astype(float)
    
    return result_df

def convert_gps_data(input_file, output_dir=None):
    """主转换函数"""
    try:
        # 读取源CSV文件
        df = pd.read_csv(input_file)
        
        # 将UTC时间戳转换为本地时间戳（东八区）
        if 'UTC' in df.columns:
            # 如果有UTC列，使用它来转换时间
            df['dataTime'] = pd.to_datetime(df['UTC']).apply(lambda x: int(x.timestamp()))
        else:
            # 否则假设Timestamp已经是UTC时间戳
            df['dataTime'] = df['Timestamp']
        
        # 转换为本地时间
        df['dataTime'] = df['dataTime'].apply(convert_utc_to_local)
        
        # 分割Position列为经纬度
        df[['latitude', 'longitude']] = df['Position'].str.split(',', expand=True).astype(float)
        
        # 创建初始数据框
        initial_df = pd.DataFrame({
            'dataTime': df['dataTime'],
            'locType': 1,
            'longitude': df['longitude'],
            'latitude': df['latitude'],
            'heading': df['Direction'].astype(float),
            'accuracy': 10.0,
            'speed': (df['Speed'] * 0.51444444).astype(float),  # 转换为米/秒
            'distance': 0.0,
            'isBackForeground': 1,
            'stepType': 1,
            'altitude': df['Altitude'].astype(float)
        })
        
        # 处理轨迹
        processed_df = process_trajectory(initial_df)
        
        # 生成基于本地时间的输出文件名
        start_time = datetime.fromtimestamp(processed_df['dataTime'].min(), 
                                          pytz.timezone('Asia/Shanghai'))
        output_filename = start_time.strftime('%Y%m%d%H%M') + ' 0000.csv'
        
        # 如果指定了输出目录，确保目录存在
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, output_filename)
        else:
            output_path = output_filename
        
        # 保存为新的CSV文件
        processed_df.to_csv(output_path, index=False, float_format='%.6f')
        
        return processed_df, output_path
    
    except Exception as e:
        print(f"处理过程中出现错误：{str(e)}")
        raise

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='GPS轨迹数据转换工具')
    parser.add_argument('input_file', help='输入CSV文件路径')
    parser.add_argument('-o', '--output_dir', help='输出目录路径（可选）', default=None)
    parser.add_argument('-q', '--quiet', help='静默模式，不输出详细信息', action='store_true')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    try:
        # 执行转换
        df, output_path = convert_gps_data(args.input_file, args.output_dir)
        
        if not args.quiet:
            print(f"转换成功！")
            print(f"输出文件：{output_path}")
            print(f"\n处理后数据点数: {len(df)}")
            
            # 输出统计信息
            local_tz = pytz.timezone('Asia/Shanghai')
            start_time = datetime.fromtimestamp(df['dataTime'].min(), local_tz)
            end_time = datetime.fromtimestamp(df['dataTime'].max(), local_tz)
            
            print("\n轨迹统计信息：")
            print(f"时间范围: {start_time} 到 {end_time} (东八区)")
            print(f"总距离: {df['distance'].max():.2f} 米")
            print(f"平均速度: {df['speed'].mean():.2f} 米/秒")
            print(f"最大速度: {df['speed'].max():.2f} 米/秒")
            print(f"最大高度: {df['altitude'].max():.2f} 米")
            print(f"最小高度: {df['altitude'].min():.2f} 米")
        else:
            print(f"已生成：{output_path}")
            
    except Exception as e:
        print(f"错误：{str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
