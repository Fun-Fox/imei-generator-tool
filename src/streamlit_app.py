"""Streamlit界面应用"""

import streamlit as st
import json
import pandas as pd
import random

from src.generator.device_info_generator import DeviceInfoGenerator
from src.executor.dg_command_generator import DGCommandGenerator
from src.config.device_models_config import display_device_models_config
from src.config.carrier_info_config import display_carrier_info_config
from src.config.device_models import get_models_by_brand, get_all_brands


def main():
    st.set_page_config(
        page_title="设备信息模拟与配置执行系统",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📱 设备信息模拟与配置执行系统")
    
    # 使用标签页组织功能
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 设备信息与DG命令", 
        "📘 DG命令详解", 
        "📱 设备型号配置", 
        "📡 运营商配置"
    ])
    
    # 初始化session state
    if "device_info_list" not in st.session_state:
        st.session_state.device_info_list = []
    
    if "commands_list" not in st.session_state:
        st.session_state.commands_list = []
    
    # 侧边栏配置
    st.sidebar.header("⚙️ 配置参数")
    
    # 设备数量
    count = st.sidebar.number_input("设备数量", min_value=1, max_value=100, value=5)
    
    # 设备品牌
    all_brands = get_all_brands()
    brand_options = ["随机"] + all_brands
    brand = st.sidebar.selectbox("设备品牌", options=brand_options)
    if brand == "随机":
        brand = None
    
    # 设备型号（基于品牌选择）
    model = None
    if brand:
        brand_models = get_models_by_brand(brand)
        model_names = list(brand_models.keys())
        model_options = ["随机"] + model_names
        selected_model_name = st.sidebar.selectbox("设备型号", options=model_options)
        if selected_model_name != "随机":
            model = f"{brand} {selected_model_name}"
    else:
        # 当没有选择特定品牌时，显示所有型号
        all_models = []
        for b in all_brands:
            brand_models = get_models_by_brand(b)
            for model_name in brand_models.keys():
                all_models.append(f"{b} {model_name}")
        model_options = ["随机"] + all_models
        model = st.sidebar.selectbox("设备型号", options=model_options)
        if model == "随机":
            model = None
    
    # 区域选择
    region_options = ["随机", "China", "Hong Kong", "Macao", "Taiwan", "USA"]
    region = st.sidebar.selectbox("区域", options=region_options)
    if region == "随机":
        region = None
    
    # 运营商选择
    if region and region != "随机":
        # 根据选择的区域动态显示运营商选项
        from src.config.carrier_info import get_carriers_by_region
        carriers = get_carriers_by_region(region)
        if carriers:
            carrier_options = ["随机"] + carriers
        else:
            carrier_options = ["随机"]
    else:
        carrier_options = ["随机", "China Mobile", "China Unicom", "China Telecom"]
    
    carrier = st.sidebar.selectbox("运营商", options=carrier_options)
    if carrier == "随机":
        carrier = None
    
    # 生成按钮
    generate_btn = st.sidebar.button("🚀 生成设备信息", type="primary")
    
    # 生成设备信息
    if generate_btn:
        with st.spinner("正在生成设备信息..."):
            generator = DeviceInfoGenerator()
            device_info_list = []
            
            for _ in range(count):
                device_info = generator.generate_device_info(model, region, carrier)
                device_info_list.append(device_info)
            
            st.session_state.device_info_list = device_info_list
            
            # 生成DG命令
            command_generator = DGCommandGenerator()
            commands_list = command_generator.generate_commands_batch(device_info_list)
            st.session_state.commands_list = commands_list
            
            st.sidebar.success(f"✅ 成功生成 {count} 条设备信息")
    
    # 设备信息与DG命令标签页
    with tab1:
        display_device_info_and_commands_tab()
    
    # DG命令详解标签页
    with tab2:
        display_dg_command_explanation()
    
    # 设备型号配置标签页
    with tab3:
        display_device_models_config()
    
    # 运营商配置标签页
    with tab4:
        display_carrier_info_config()


def display_device_info_and_commands_tab():
    """显示设备信息与DG命令标签页"""
    if st.session_state.device_info_list and st.session_state.commands_list:
        st.subheader(f"📋 设备信息列表 (共 {len(st.session_state.device_info_list)} 条)")
        
        # 创建设备信息表格
        device_data = []
        for i, device_info in enumerate(st.session_state.device_info_list):
            device_data.append({
                "设备编号": i + 1,
                "型号": device_info.model,
                "IMEI": device_info.imei,
                "IMSI": device_info.imsi,
                "区域": device_info.region,
                "运营商": device_info.carrier,
                "手机号": device_info.phone_number,
                "网络类型": device_info.network_type,
                "IP地址": device_info.ip_address
            })
        
        df = pd.DataFrame(device_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # 提供JSON下载
        json_data = [device_info.to_dict() for device_info in st.session_state.device_info_list]
        json_str = json.dumps(json_data, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 下载JSON文件",
            data=json_str,
            file_name="device_info.json",
            mime="application/json"
        )
        
        # 显示详细信息与对应的DG命令
        st.subheader("🔍 DG命令详情")
        selected_device = st.selectbox(
            "选择设备查看DG命令",
            options=[f"设备 {i+1}" for i in range(len(st.session_state.device_info_list))],
            index=0
        )
        
        if selected_device:
            idx = int(selected_device.split()[1]) - 1
            device_info = st.session_state.device_info_list[idx]
            commands = st.session_state.commands_list[idx]
            
            # 显示对应的DG命令
            st.write("**💻 对应的DG命令及其生成规则:**")
            for i, command in enumerate(commands):
                # 为每条命令添加注释和生成规则
                comment, rule = get_command_comment_and_rule(command, device_info)
                if comment:
                    st.markdown(f"**{comment}**")
                if rule:
                    st.markdown(f"*生成规则: {rule}*")
                st.code(command, language="bash")
                st.markdown("---")  # 分隔线
                
            # 提供命令文件下载
            commands_text = "\n".join(commands)
            st.download_button(
                label="💾 下载DG命令文件",
                data=commands_text,
                file_name=f"dg_commands_device_{idx+1}.txt",
                mime="text/plain"
            )
    else:
        st.info("点击侧边栏的'生成设备信息'按钮开始生成设备信息和DG命令")


def get_command_comment_and_rule(command, device_info):
    """为DG命令添加注释和生成规则"""
    if "prop.ro.product.manufacturer" in command:
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
        return "设置设备制造商", f"根据设备型号 '{device_info.model}' 推断品牌为 '{brand}'"
        
    elif "prop.ro.product.model" in command or "prop.ro.product.device" in command:
        return "设置设备型号", f"直接使用生成的设备型号 '{device_info.model}'"
        
    elif "prop.ro.serialno" in command:
        # 从命令中提取序列号
        serial_no = command.split("=")[-1]
        return "设置设备序列号", f"生成16位随机十六进制字符串: {serial_no}"
        
    elif "sim.imei" in command:
        imei = device_info.imei
        tac = imei[:8]
        snr = imei[8:14]
        cd = imei[14]
        return f"设置IMEI（TAC: {tac}）", f"TAC({tac})根据设备型号确定，SNR({snr})随机生成6位数字，校验位({cd})通过Luhn算法计算得出"
        
    elif "sim.state=1" in command and "sim.numeric" in command:
        numeric = command.split("sim.numeric=")[1].split(" ")[0]
        mcc = numeric[:3]
        mnc = numeric[3:]
        imsi_part = command.split("sim.imsi=")[1].split(" ")[0][:len(numeric)]
        return "设置SIM卡状态和运营商信息", f"MCC({mcc})根据区域'{device_info.region}'确定，MNC({mnc})根据运营商'{device_info.carrier}'确定，SIM状态设置为1(就绪)"
        
    elif "sim.spn" in command:
        spn = command.split("sim.spn=")[1].split(" ")[0].strip('"')
        return "设置运营商名称", f"根据运营商'{device_info.carrier}'设置服务提供商名称为'{spn}'"
        
    elif "sim.iccid" in command:
        iccid = command.split("=")[-1]
        mcc = iccid[2:5]
        mnc = iccid[5:8] if iccid[5:8].isdigit() else iccid[5:7]
        return "设置ICCID", f"格式: 89(电信用途)+{mcc}(MCC)+{mnc}(MNC)+10位随机数字"
        
    elif "sim.msisdn" in command:
        msisdn = command.split("=")[-1]
        return "设置手机号码", f"根据区域'{device_info.region}'和运营商'{device_info.carrier}'生成手机号: {msisdn}"
        
    elif "sim.netType" in command:
        net_type = command.split("=")[-1]
        mapping = {"gsm": "2G", "cdma": "3G", "lte": "4G", "nr": "5G", "wifi": "WiFi"}
        network_desc = mapping.get(net_type, net_type)
        return "设置网络类型", f"根据生成的网络类型'{device_info.network_type}'映射为DG支持的格式'{net_type}'({network_desc})"
        
    elif "sim.country" in command:
        country = command.split("=")[-1]
        return "设置SIM卡国家代码", f"根据区域'{device_info.country}'映射为国家代码'{country}'"
        
    elif "net.if.mac" in command:
        mac = command.split("=")[-1]
        return "设置MAC地址", f"生成6组2位十六进制数，用冒号分隔: {mac}"
        
    elif "prop.android.id" in command:
        android_id = command.split("=")[-1]
        return "设置Android ID", f"生成16位十六进制字符串: {android_id}"
        
    elif "net.wifi.ssid" in command:
        ssid = command.split("=")[-1]
        return "设置WiFi名称", f"生成WiFi名称: {ssid}"
        
    elif "net.wifi.ipaddress" in command:
        ip = command.split("=")[-1]
        return "设置WiFi IP地址", f"生成随机IPv4地址: {ip}"
        
    elif command.startswith("dg geo fix"):
        parts = command.split(" ")
        lon, lat = parts[3], parts[4]
        return "设置地理位置", f"使用生成的经纬度坐标: 经度{lon}, 纬度{lat}"
        
    elif command.startswith("dg sensor set acceleration"):
        parts = command.split(" ")
        x, y, z = parts[4], parts[5], parts[6]
        return "设置加速度传感器数据", f"生成三轴加速度数据: X={x}, Y={y}, Z={z}"
        
    elif command.startswith("dg sensor set gyroscope"):
        parts = command.split(" ")
        x, y, z = parts[4], parts[5], parts[6]
        return "设置陀螺仪传感器数据", f"生成三轴陀螺仪数据: X={x}, Y={y}, Z={z}"
        
    elif "battery.batteryLevel" in command:
        level = command.split("=")[-1]
        return "设置电池电量", f"随机生成20-90之间的电量值: {level}%"
        
    elif "sensor.mock" in command:
        return "启用传感器模拟", "设置传感器模拟开关为true，并启用预设路径"
        
    return "", ""


def display_dg_command_explanation():
    """显示DG命令详解标签页"""
    st.header("📘 DG命令详解")
    
    st.markdown("""
    ## DG命令完整说明
    
    DG命令用于模拟Android设备的各种属性和状态。以下是所有支持的命令分类说明：
    
    ### 1. 基础配置命令
    
    #### 属性配置格式
    ```
    dg config [-a/--add MODULE.KEY=VALUE] [-r/--remove MODULE.KEY] [-c/--clear]
    ```
    
    ### 2. 系统属性配置 (prop模块)
    
    ```
    # 设置系统属性（可通过getprop访问）
    dg config -a prop.ro.product.manufacturer=vivo
    dg config -a prop.ro.product.model=V2025
    dg config -a prop.ro.serialno=R9JN601MMDE
    dg config -a prop.android.id=1234567890abcdef
    ```
    
    ### 3. SIM卡配置 (sim模块)
    
    #### 基础SIM卡命令
    ```
    # 开启SIM卡并设置IMEI
    dg config -a sim.state=1 -a sim.imei=8622660302123456
    
    # 配置完整的SIM信息（中国联通示例）
    dg config -a sim.state=1 \\
              -a sim.imei=867981023273033 \\
              -a sim.numeric=46001 \\
              -a sim.msisdn=18513335519 \\
              -a sim.gid1=ff \\
              -a sim.netType=lte \\
              -a sim.imsi=460013331515018 \\
              -a sim.iccid=89860118801046878907
    
    # 关闭SIM卡
    dg config -a sim.state=0
    ```
    
    #### 运营商信息配置
    ```
    # 设置运营商信息
    dg config -a sim.spn="China Mobile" \\
              -a sim.operatorLongName="China Mobile" \\
              -a sim.operatorShortName="CMCC"
    ```
    
    ### 4. 网络配置 (net模块)
    
    ```
    # 设置WiFi信息
    dg config -a net.wifi.ssid=Tenda_X8812
    dg config -a net.wifi.ipaddress=192.168.1.100
    dg config -a net.wifi.enabled=false  # 关闭WiFi
    
    # 设置MAC地址
    dg config -a net.if.mac=02:00:00:00:00:00
    ```
    
    ### 5. 电池配置 (battery模块)
    
    ```
    # 设置电池电量
    dg config -a battery.batteryLevel=20
    
    # 设置电池容量
    dg config -a battery.profileCapacity=9000
    ```
    
    ### 6. 定位配置 (location/sim/geolocation模块)
    
    ```
    # 设置GPS定位
    dg config -a location.mock=true -a location.lat=39.962128 -a location.lon=116.349792
    
    # 设置基站定位
    dg config -a sim.lac=4138 -a sim.cid=62793
    
    # 使用geo命令设置定位
    dg geo fix 116.349792 39.962128
    ```
    
    ### 7. 传感器配置 (sensor模块)
    
    ```
    # 启用传感器模拟并设置行走场景
    dg config -a sensor.mock=true -a sensor.path=walk
    
    # 设置具体传感器数据
    dg sensor set acceleration 0.0 0.0 9.8
    dg sensor set gyroscope 0.0 0.0 0.0
    ```
    
    ### 8. 应用管理配置 (am模块)
    
    ```
    # 设置应用进程保活
    dg config -a am.persistentPkgs=com.tencent.mm
    
    # 设置前台应用
    dg config -a am.fg.pkg=com.tencent.mm
    ```
    
    ### 9. 系统配置 (system模块)
    
    ```
    # 开启ROOT权限
    dg config -a system.su=true
    ```
    
    ### 10. 配置文件方式
    
    ```
    # 使用本地配置文件
    chmod 644 /data/local/test.prop
    dg config -a /data/local/test.prop
    
    # 使用远程配置文件
    dg config -a https://abc.com/test.prop
    ```
    
    ### 11. 查看配置信息
    
    ```
    # 查看所有配置
    dg config output
    dg dump
    
    # 查看特定模块信息
    dg dump prop sim battery proxy
    
    # 查看ROM版本信息
    dg dump base
    
    # 查看设备信息
    dg dump device
    ```
    
    ### 重要注意事项
    
    1. **IMSI一致性要求**：IMSI的前几位必须与sim.numeric保持一致
    2. **MCC/MNC格式**：MCC为3位数字，MNC通常为2-3位数字
    3. **配置生效时机**：大多数配置在设置后重启应用即生效
    4. **系统属性限制**：不要修改可能影响系统正常运行的系统属性
    5. **网络配置**：代理host不支持动态ip的域名，建议使用固定ip
    """)


if __name__ == "__main__":
    main()