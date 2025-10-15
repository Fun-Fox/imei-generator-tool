"""运营商信息配置文件"""

# 不同国家/地区的运营商信息
CARRIER_INFO = {
    "China": {
        "MCC": "460",
        "MNC": {
            "China Mobile": ["00", "02", "07"],      # 中国移动
            "China Unicom": ["01", "06", "09"],      # 中国联通
            "China Telecom": ["03", "05", "11"],     # 中国电信
        },
        "PhonePrefix": ["139", "138", "137", "136", "135", "134", "159", "158", "157", "152", "151", "150", 
                       "188", "187", "184", "183", "182", "178", "172", "170", "165", "157", "147", "144"]
    },
    "Hong Kong": {
        "MCC": "454",
        "MNC": {
            "CSL": ["00", "02", "10", "16", "18", "19"],
            "HKT": ["03", "04", "12", "13", "29"],
            "3": ["05", "06"],
            "China Mobile HK": ["12", "13"],
            "Smartone": ["07", "15"],
        },
        "PhonePrefix": ["5", "6", "9"]
    },
    "Macao": {
        "MCC": "455",
        "MNC": {
            "CTM": ["01", "04"],
            "China Telecom": ["02", "07"],
            "3": ["03", "05"],
        },
        "PhonePrefix": ["6"]
    },
    "Taiwan": {
        "MCC": "466",
        "MNC": {
            "Far EasTone": ["01", "02"],
            "Chunghwa Telecom": ["05", "06", "11", "16", "26", "88", "89"],
            "TWN Mobile": ["89", "92", "97"],
            "Asia Pacific": ["05", "06", "10", "88", "89"],
        },
        "PhonePrefix": ["09"]
    },
    "USA": {
        "MCC": "310",
        "MNC": {
            "Verizon": ["004", "010", "012", "013"],
            "AT&T": ["030", "070", "150", "170", "280", "380", "410", "560", "680"],
            "T-Mobile": ["260", "310", "660", "800"],
            "Sprint": ["012", "120", "260", "490", "800"],
        },
        "PhonePrefix": ["201", "202", "203", "205", "206", "207", "208", "209", "210", "212", "213", "214", 
                       "215", "216", "217", "218", "219", "224", "225", "228", "229", "231", "234", "239", 
                       "248", "251", "252", "253", "254", "256", "260", "262", "267", "269", "270", "272", 
                       "276", "281", "283", "301", "302", "303", "304", "305", "307", "308", "309", "310"]
    }
}

# 获取指定国家/地区的运营商列表
def get_carriers_by_region(region):
    if region in CARRIER_INFO:
        return list(CARRIER_INFO[region]["MNC"].keys())
    return []

# 获取指定国家/地区的MCC
def get_mcc_by_region(region):
    if region in CARRIER_INFO:
        return CARRIER_INFO[region]["MCC"]
    return None

# 获取指定运营商的MNC列表
def get_mnc_by_carrier(region, carrier):
    if region in CARRIER_INFO and carrier in CARRIER_INFO[region]["MNC"]:
        return CARRIER_INFO[region]["MNC"][carrier]
    return []

# 获取指定国家/地区的手机号前缀
def get_phone_prefix_by_region(region):
    if region in CARRIER_INFO:
        return CARRIER_INFO[region]["PhonePrefix"]
    return []