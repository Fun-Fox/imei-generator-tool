"""设备型号配置文件"""

# 不同品牌和型号的设备列表
DEVICE_MODELS = {
    "Samsung": [
        "35050556",  # Galaxy S25
    ],
    "Apple": [
        "35281219",  # iPhone 16e
    ],
    "Huawei": [
        "86312106",   # P60 Art
    ],
    "Xiaomi": [
        "86749806",  # 14 Ultra
    ],
    "OPPO": [
        "86945807",   # Reno 12 Pro
    ],
    "Vivo": [
        "86004106",    # X90 Pro
    ]
}

# 根据品牌获取型号列表
def get_models_by_brand(brand):
    return DEVICE_MODELS.get(brand, [])

# 获取所有品牌
def get_all_brands():
    return list(DEVICE_MODELS.keys())

# 获取所有型号
def get_all_models():
    all_models = []
    for models in DEVICE_MODELS.values():
        all_models.extend(models)
    return all_models