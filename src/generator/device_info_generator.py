"""设备信息生成器"""

import random
import json
from faker import Faker
from typing import Dict, List, Optional
from src.config.device_models import DEVICE_MODELS, get_all_models, get_models_by_brand, get_tac_by_brand_and_model, get_tac_by_full_model
from src.config.carrier_info import CARRIER_INFO, get_mcc_by_region, get_mnc_by_carrier, get_carriers_by_region, get_phone_prefix_by_region
from src.core.models import DeviceInfo


# 已移除DeviceInfo类定义，使用core.models中的定义


class DeviceInfoGenerator:
    """设备信息生成器主类"""
    
    def __init__(self):
        self.fake = Faker()
        self.fake.random.seed(42)  # 固定种子以确保一定程度的可重现性
    
    def generate_device_info(
        self, 
        model: Optional[str] = None, 
        region: Optional[str] = None,
        carrier: Optional[str] = None
    ) -> DeviceInfo:
        """
        生成完整的设备信息
        
        Args:
            model: 指定设备型号，如果为None则随机选择
            region: 指定区域（国家/地区），如果为None则随机选择
            carrier: 指定运营商，如果为None则随机选择
            
        Returns:
            DeviceInfo: 完整的设备信息对象
        """
        device_info = DeviceInfo()
        
        # 生成设备型号
        device_info.model = self._generate_model(model)
        
        # 生成地理位置信息
        device_info.country, device_info.region = self._generate_location(region)
        
        # 生成运营商信息
        device_info.carrier = self._generate_carrier(device_info.country, carrier)
        
        # 生成手机号码
        device_info.phone_number = self._generate_phone_number(device_info.country, device_info.carrier)
        
        # 生成IMEI
        device_info.imei = self._generate_imei(device_info.model)
        
        # 生成IMSI
        device_info.imsi = self._generate_imsi(device_info.country, device_info.carrier)
        
        # 生成其他硬件标识
        device_info.mac_address = self._generate_mac_address()
        device_info.android_id = self._generate_android_id()
        
        # 生成应用和系统信息
        device_info.app_version = self._generate_app_version()
        device_info.system_version = self._generate_system_version()
        
        # 生成网络信息
        device_info.ssid = self._generate_ssid()
        device_info.ip_address = self._generate_ip_address()
        device_info.network_type = self._generate_network_type()
        
        # 生成传感器数据
        device_info.accelerometer_data = self._generate_accelerometer_data()
        device_info.gyroscope_data = self._generate_gyroscope_data()
        
        # 生成经纬度
        device_info.latitude, device_info.longitude = self._generate_coordinates()
        
        return device_info
    
    def _generate_model(self, model: Optional[str] = None) -> str:
        """生成设备型号"""
        if model:
            return model
        # 随机选择品牌和型号
        all_brands = list(DEVICE_MODELS.keys())
        brand = random.choice(all_brands)
        brand_models = DEVICE_MODELS[brand]
        model_name = random.choice(list(brand_models.keys()))
        return f"{brand} {model_name}"
    
    def _generate_location(self, region: Optional[str] = None) -> tuple:
        """生成地理位置信息"""
        if region and region in CARRIER_INFO:
            country = region
        else:
            # 随机选择一个国家/地区
            country = random.choice(list(CARRIER_INFO.keys()))
        
        return country, country
    
    def _generate_carrier(self, country: str, carrier: Optional[str] = None) -> str:
        """生成运营商信息"""
        if carrier and carrier in CARRIER_INFO.get(country, {}).get("MNC", {}):
            return carrier
        
        # 从指定国家的运营商中随机选择
        carriers = get_carriers_by_region(country)
        if carriers:
            return random.choice(carriers)
        
        return "Unknown"
    
    def _generate_phone_number(self, country: str, carrier: str) -> str:
        """生成手机号码"""
        prefixes = get_phone_prefix_by_region(country)
        if not prefixes:
            return self.fake.msisdn()
        
        prefix = random.choice(prefixes)
        
        if country == "China":
            # 中国手机号码为11位
            remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            return f"+86{prefix}{remaining_digits}"
        elif country in ["Hong Kong", "Macao"]:
            # 港澳地区手机号码
            remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(7)])
            return f"+852{prefix}{remaining_digits}"
        elif country == "Taiwan":
            # 台湾地区手机号码
            remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            return f"+886{prefix}{remaining_digits}"
        elif country == "USA":
            # 美国手机号码
            remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(7)])
            return f"+1{prefix}{remaining_digits}"
        else:
            # 其他地区使用Faker生成
            return self.fake.msisdn()
    
    def _generate_imei(self, model: str) -> str:
        """生成IMEI号码"""
        # 解析品牌和型号
        parts = model.split(" ", 1)
        if len(parts) == 2:
            brand, model_name = parts
        else:
            brand = model
            model_name = model
        
        # 查找匹配的TAC码
        tac = get_tac_by_brand_and_model(brand, model_name)
        
        # 如果找不到精确匹配，随机选择一个TAC
        if not tac:
            all_tacs = []
            for models in DEVICE_MODELS.values():
                all_tacs.extend(list(models.values()))
            tac = random.choice(all_tacs) if all_tacs else "12345678"
        
        # 生成SNR（接下来6位）
        snr = f"{random.randint(0, 999999):06d}"
        
        # 生成校验位
        imei_without_check_digit = tac + snr
        check_digit = self._calculate_luhn_check_digit(imei_without_check_digit)
        
        return imei_without_check_digit + check_digit
    
    def _calculate_luhn_check_digit(self, digits: str) -> str:
        """使用Luhn算法计算校验位"""
        total = 0
        for i, digit in enumerate(reversed(digits)):
            n = int(digit)
            if i % 2 == 0:  # 从右边数，偶数位（索引为0, 2, 4...）
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        return str((10 - total % 10) % 10)
    
    def _generate_imsi(self, country: str, carrier: str) -> str:
        """生成IMSI号码"""
        mcc = get_mcc_by_region(country)
        if not mcc:
            mcc = "000"
        
        mnc_list = get_mnc_by_carrier(country, carrier)
        if mnc_list:
            mnc = random.choice(mnc_list)
        else:
            # 默认生成一个2位或3位的MNC
            mnc = f"{random.randint(0, 999):03d}" if random.choice([True, False]) else f"{random.randint(0, 99):02d}"
        
        # 计算MSIN长度，IMSI总长度为15位
        msin_length = 15 - len(mcc) - len(mnc)
        msin = ''.join([str(random.randint(0, 9)) for _ in range(msin_length)])
        
        return mcc + mnc + msin
    
    def _generate_mac_address(self) -> str:
        """生成MAC地址"""
        mac = [random.randint(0x00, 0xff) for _ in range(6)]
        return ':'.join(map(lambda x: f"{x:02x}", mac))
    
    def _generate_android_id(self) -> str:
        """生成Android ID"""
        return ''.join(random.choices('0123456789abcdef', k=16))
    
    def _generate_app_version(self) -> str:
        """生成应用版本"""
        major = random.randint(1, 5)
        minor = random.randint(0, 20)
        patch = random.randint(0, 50)
        return f"{major}.{minor}.{patch}"
    
    def _generate_system_version(self) -> str:
        """生成系统版本"""
        versions = ["Android 10", "Android 11", "Android 12", "Android 13", "Android 14"]
        return random.choice(versions)
    
    def _generate_ssid(self) -> str:
        """生成WiFi SSID"""
        return f"WiFi_{random.randint(1000, 9999)}"
    
    def _generate_ip_address(self) -> str:
        """生成IP地址"""
        return self.fake.ipv4()
    
    def _generate_network_type(self) -> str:
        """生成网络类型"""
        types = ["2G", "3G", "4G", "5G", "WiFi"]
        return random.choice(types)
    
    def _generate_accelerometer_data(self) -> Dict[str, float]:
        """生成加速度传感器数据"""
        return {
            "x": round(random.uniform(-10.0, 10.0), 2),
            "y": round(random.uniform(-10.0, 10.0), 2),
            "z": round(random.uniform(-10.0, 10.0), 2)
        }
    
    def _generate_gyroscope_data(self) -> Dict[str, float]:
        """生成陀螺仪传感器数据"""
        return {
            "x": round(random.uniform(-500.0, 500.0), 2),
            "y": round(random.uniform(-500.0, 500.0), 2),
            "z": round(random.uniform(-500.0, 500.0), 2)
        }
    
    def _generate_coordinates(self) -> tuple:
        """生成经纬度坐标"""
        # 生成全球范围内的随机坐标
        latitude = round(random.uniform(-90.0, 90.0), 6)
        longitude = round(random.uniform(-180.0, 180.0), 6)
        return latitude, longitude