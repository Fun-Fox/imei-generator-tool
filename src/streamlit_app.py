"""Streamlit界面应用"""

import streamlit as st
import json
import pandas as pd
from typing import List

from src.generator.device_info_generator import DeviceInfoGenerator, DeviceInfo
from src.executor.dg_command_generator import DGCommandGenerator


def main():
    st.set_page_config(
        page_title="设备信息模拟与配置执行系统",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📱 设备信息模拟与配置执行系统")
    
    # 侧边栏配置
    st.sidebar.header("⚙️ 配置参数")
    
    # 设备数量
    count = st.sidebar.number_input("设备数量", min_value=1, max_value=100, value=5)
    
    # 设备型号
    model_options = ["随机", "Samsung", "Apple", "Huawei", "Xiaomi", "OPPO", "Vivo"]
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
    
    # 主界面
    tab1, tab2, tab3 = st.tabs(["📋 设备信息", "💻 DG命令", "📊 统计信息"])
    
    # 初始化session state
    if "device_info_list" not in st.session_state:
        st.session_state.device_info_list = []
    
    if "commands_list" not in st.session_state:
        st.session_state.commands_list = []
    
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
    
    # 设备信息标签页
    with tab1:
        if st.session_state.device_info_list:
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
            
            # 显示详细信息
            st.subheader("🔍 详细信息")
            selected_device = st.selectbox(
                "选择设备查看详细信息",
                options=[f"设备 {i+1}" for i in range(len(st.session_state.device_info_list))],
                index=0
            )
            
            if selected_device:
                idx = int(selected_device.split()[1]) - 1
                device_info = st.session_state.device_info_list[idx]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📱 基本信息**")
                    st.write(f"- 型号: {device_info.model}")
                    st.write(f"- IMEI: {device_info.imei}")
                    st.write(f"- IMSI: {device_info.imsi}")
                    st.write(f"- MAC地址: {device_info.mac_address}")
                    st.write(f"- Android ID: {device_info.android_id}")
                    
                    st.write("**🌐 网络信息**")
                    st.write(f"- 区域: {device_info.region}")
                    st.write(f"- 运营商: {device_info.carrier}")
                    st.write(f"- 手机号: {device_info.phone_number}")
                    st.write(f"- 网络类型: {device_info.network_type}")
                    st.write(f"- SSID: {device_info.ssid}")
                    st.write(f"- IP地址: {device_info.ip_address}")
                
                with col2:
                    st.write("**📍 位置信息**")
                    st.write(f"- 国家: {device_info.country}")
                    st.write(f"- 纬度: {device_info.latitude}")
                    st.write(f"- 经度: {device_info.longitude}")
                    
                    st.write("**📱 应用和系统信息**")
                    st.write(f"- 应用版本: {device_info.app_version}")
                    st.write(f"- 系统版本: {device_info.system_version}")
                    
                    st.write("**🎮 传感器数据**")
                    st.write(f"- 加速度计: X={device_info.accelerometer_data['x']}, "
                            f"Y={device_info.accelerometer_data['y']}, "
                            f"Z={device_info.accelerometer_data['z']}")
                    st.write(f"- 陀螺仪: X={device_info.gyroscope_data['x']}, "
                            f"Y={device_info.gyroscope_data['y']}, "
                            f"Z={device_info.gyroscope_data['z']}")
        else:
            st.info("点击侧边栏的'生成设备信息'按钮开始生成设备信息")
    
    # DG命令标签页
    with tab2:
        if st.session_state.commands_list:
            st.subheader("💻 DG命令列表")
            
            # 显示所有设备的DG命令
            for i, commands in enumerate(st.session_state.commands_list):
                with st.expander(f"📱 设备 {i+1} 的DG命令 ({len(commands)} 条)"):
                    for j, command in enumerate(commands):
                        st.code(command, language="bash")
            
            # 提供命令文件下载
            commands_text = ""
            for i, commands in enumerate(st.session_state.commands_list):
                commands_text += f"# 设备 {i+1} 的DG命令\n"
                for command in commands:
                    commands_text += f"{command}\n"
                commands_text += "\n"
            
            st.download_button(
                label="💾 下载DG命令文件",
                data=commands_text,
                file_name="dg_commands.txt",
                mime="text/plain"
            )
        else:
            st.info("需要先生成设备信息才能查看DG命令")
    
    # 统计信息标签页
    with tab3:
        if st.session_state.device_info_list:
            st.subheader("📊 统计信息")
            
            # 区域分布
            region_counts = {}
            carrier_counts = {}
            network_type_counts = {}
            
            for device_info in st.session_state.device_info_list:
                # 统计区域
                region = device_info.region
                region_counts[region] = region_counts.get(region, 0) + 1
                
                # 统计运营商
                carrier = device_info.carrier
                carrier_counts[carrier] = carrier_counts.get(carrier, 0) + 1
                
                # 统计网络类型
                network_type = device_info.network_type
                network_type_counts[network_type] = network_type_counts.get(network_type, 0) + 1
            
            # 显示统计图表
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**🌍 区域分布**")
                st.bar_chart(region_counts)
            
            with col2:
                st.write("**📡 运营商分布**")
                st.bar_chart(carrier_counts)
            
            with col3:
                st.write("**📶 网络类型分布**")
                st.bar_chart(network_type_counts)
            
            # 显示统计表格
            st.subheader("📋 详细统计")
            
            # 区域统计表格
            region_df = pd.DataFrame([
                {"区域": region, "数量": count, "占比": f"{count/len(st.session_state.device_info_list)*100:.1f}%"}
                for region, count in region_counts.items()
            ])
            st.write("**区域统计:**")
            st.dataframe(region_df, hide_index=True)
            
            # 运营商统计表格
            carrier_df = pd.DataFrame([
                {"运营商": carrier, "数量": count, "占比": f"{count/len(st.session_state.device_info_list)*100:.1f}%"}
                for carrier, count in carrier_counts.items()
            ])
            st.write("**运营商统计:**")
            st.dataframe(carrier_df, hide_index=True)
            
            # 网络类型统计表格
            network_df = pd.DataFrame([
                {"网络类型": network_type, "数量": count, "占比": f"{count/len(st.session_state.device_info_list)*100:.1f}%"}
                for network_type, count in network_type_counts.items()
            ])
            st.write("**网络类型统计:**")
            st.dataframe(network_df, hide_index=True)
        else:
            st.info("需要先生成设备信息才能查看统计信息")


if __name__ == "__main__":
    main()