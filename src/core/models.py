"""
设备信息数据模型定义
"""

from dataclasses import dataclass
from typing import Dict, Optional


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