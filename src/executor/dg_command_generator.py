"""DG命令生成器"""

from typing import List
from src.generator.device_info_generator import DeviceInfo


class DGCommandGenerator:
    """DG命令生成器主类"""
    
    def __init__(self):
        pass
    
    def generate_commands(self, device_info: DeviceInfo) -> List[str]:
        """
        基于设备信息生成DG命令列表
        
        Args:
            device_info: 设备信息对象
            
        Returns:
            List[str]: DG命令列表
        """
        commands = []
        
        # 添加设备制造商和品牌设置命令
        if device_info.model:
            # 根据设备型号推断品牌
            brand = "Unknown"
            if "Samsung" in device_info.model or "SM-" in device_info.model:
                brand = "samsung"
            elif "iPhone" in device_info.model:
                brand = "apple"
            elif "Huawei" in device_info.model or "ELE-" in device_info.model or "VOG-" in device_info.model:
                brand = "huawei"
            elif "Xiaomi" in device_info.model or "POCO" in device_info.model or "Redmi" in device_info.model:
                brand = "xiaomi"
            elif "OPPO" in device_info.model or "CPH" in device_info.model:
                brand = "oppo"
            elif "Vivo" in device_info.model or "V20" in device_info.model:
                brand = "vivo"
            
            commands.append(f"dg config -a prop.ro.product.manufacturer={brand}")
            commands.append(f"dg config -a prop.ro.product.brand={brand}")
        
        # 添加设备型号修改命令
        if device_info.model:
            commands.append(f"dg config -a prop.ro.product.model={device_info.model}")
            commands.append(f"dg config -a prop.ro.product.device={device_info.model}")
        
        # 添加序列号设置命令
        # 生成一个随机序列号（16位十六进制字符串）
        import random
        serial_no = ''.join(random.choices('0123456789ABCDEF', k=16))
        commands.append(f"dg config -a prop.ro.serialno={serial_no}")
        
        # 添加IMEI设置命令
        if device_info.imei:
            commands.append(f"dg config -a sim.imei={device_info.imei}")
        
        # 添加IMSI设置命令
        if device_info.imsi:
            commands.append(f"dg config -a sim.imsi={device_info.imsi}")
        
        # 添加SIM国家设置命令
        if device_info.country:
            country_code_map = {
                "China": "CN",
                "Hong Kong": "HK",
                "Macao": "MO",
                "Taiwan": "TW",
                "USA": "US",
                "Unknown": "US"  # 默认值
            }
            country_code = country_code_map.get(device_info.country, "US")
            commands.append(f"dg config -a sim.country={country_code}")
        
        # 添加手机号设置命令
        if device_info.phone_number:
            commands.append(f"dg config -a sim.msisdn={device_info.phone_number}")
        
        # 添加MAC地址设置命令
        if device_info.mac_address:
            commands.append(f"dg config -a net.if.mac={device_info.mac_address}")
        
        # 添加Android ID设置命令
        if device_info.android_id:
            commands.append(f"dg config -a prop.android.id={device_info.android_id}")
        
        # 添加网络类型设置命令
        if device_info.network_type:
            # 将网络类型转换为DG支持的格式
            net_type_map = {
                "2G": "gsm",
                "3G": "cdma", 
                "4G": "lte",
                "5G": "nr",
                "WiFi": "wifi"
            }
            net_type = net_type_map.get(device_info.network_type, "wifi")
            commands.append(f"dg config -a sim.netType={net_type}")
        
        # 添加SSID设置命令
        if device_info.ssid:
            commands.append(f"dg config -a net.wifi.ssid={device_info.ssid}")
        
        # 添加IP地址设置命令
        if device_info.ip_address:
            commands.append(f"dg config -a net.wifi.ipaddress={device_info.ip_address}")
        
        # 添加地理位置模拟命令
        commands.append(f"dg geo fix {device_info.longitude} {device_info.latitude}")
        
        # 添加传感器数据模拟命令
        if device_info.accelerometer_data:
            acc = device_info.accelerometer_data
            commands.append(f"dg sensor set acceleration {acc['x']} {acc['y']} {acc['z']}")
        
        if device_info.gyroscope_data:
            gyro = device_info.gyroscope_data
            commands.append(f"dg sensor set gyroscope {gyro['x']} {gyro['y']} {gyro['z']}")
        
        return commands
    
    def generate_commands_batch(self, device_info_list: List[DeviceInfo]) -> List[List[str]]:
        """
        批量生成DG命令列表
        
        Args:
            device_info_list: 设备信息对象列表
            
        Returns:
            List[List[str]]: DG命令列表的列表
        """
        return [self.generate_commands(device_info) for device_info in device_info_list]