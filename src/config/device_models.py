"""设备型号配置文件"""

# 不同品牌和型号的设备列表
# 格式: 品牌: {型号名称: TAC码}
DEVICE_MODELS = {
    "Samsung": {
        "Galaxy S25": "35050556",
    },
    "Apple": {
        "iPhone 16e": "35281219",
    },
    "Huawei": {
        "P60 Art": "86312106",
    },
    "Xiaomi": {
        "14 Ultra": "86749806",
    },
    "OPPO": {
        "Reno 12 Pro": "86945807",
    },
    "Vivo": {
        "X90 Pro": "86004106",
    }
}

# 根据品牌获取型号列表
def get_models_by_brand(brand):
    return DEVICE_MODELS.get(brand, {})

# 获取所有品牌
def get_all_brands():
    return list(DEVICE_MODELS.keys())

# 根据品牌和型号获取TAC码
def get_tac_by_brand_and_model(brand, model):
    brand_models = DEVICE_MODELS.get(brand, {})
    return brand_models.get(model, None)

# 获取所有型号
def get_all_models():
    all_models = []
    for brand, models in DEVICE_MODELS.items():
        for model in models:
            all_models.append(f"{brand} {model}")
    return all_models

# 根据完整型号名称获取TAC码
def get_tac_by_full_model(full_model):
    if not full_model:
        return None
    parts = full_model.split(" ", 1)
    if len(parts) != 2:
        return None
    brand, model = parts
    return get_tac_by_brand_and_model(brand, model)

# 获取所有TAC码
def get_all_tacs():
    all_tacs = []
    for models in DEVICE_MODELS.values():
        all_tacs.extend(list(models.values()))
    return all_tacs