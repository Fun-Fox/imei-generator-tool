"""
设备信息数据模型定义
"""

from dataclasses import dataclass
from typing import Dict, Optional
import json


@dataclass
class DeviceInfo:
    """设备信息数据结构"""
    model: str = ""
    imei: str = ""
    imsi: str = ""
    mac_address: str = ""
    android_id: str = ""
    app_version: str = ""
    system_version: str = ""
    ssid: str = ""
    ip_address: str = ""
    network_type: str = ""
    accelerometer_data: Optional[Dict[str, float]] = None
    gyroscope_data: Optional[Dict[str, float]] = None
    latitude: float = 0.0
    longitude: float = 0.0
    country: str = ""
    region: str = ""
    carrier: str = ""
    phone_number: str = ""
    
    def to_dict(self):
        """将设备信息转换为字典"""
        return {
            "model": self.model,
            "imei": self.imei,
            "imsi": self.imsi,
            "mac_address": self.mac_address,
            "android_id": self.android_id,
            "app_version": self.app_version,
            "system_version": self.system_version,
            "ssid": self.ssid,
            "ip_address": self.ip_address,
            "network_type": self.network_type,
            "accelerometer_data": self.accelerometer_data,
            "gyroscope_data": self.gyroscope_data,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "country": self.country,
            "region": self.region,
            "carrier": self.carrier,
            "phone_number": self.phone_number
        }
    
    def to_json(self):
        """将设备信息转换为JSON字符串"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)