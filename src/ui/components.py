"""UI组件库"""

import streamlit as st
from src.config.device_models import get_all_brands, get_models_by_brand


def device_config_panel():
    """设备配置面板"""
    st.sidebar.header("📱 设备配置")
    
    # 设备数量
    count = st.sidebar.number_input("设备数量", min_value=1, max_value=100, value=5)
    
    # 设备品牌
    all_brands = get_all_brands()
    brand_options = ["随机"] + all_brands
    brand = st.sidebar.selectbox("设备品牌", options=brand_options)
    
    # 设备型号（基于品牌选择）
    model = None
    if brand and brand != "随机":
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
        selected_model = st.sidebar.selectbox("设备型号", options=model_options)
        if selected_model != "随机":
            model = selected_model
    
    return count, model


def location_config_panel():
    """位置配置面板"""
    st.sidebar.header("📍 位置配置")
    
    # 区域选择
    region_options = ["随机", "China", "Hong Kong", "Macao", "Taiwan", "USA"]
    region = st.sidebar.selectbox("区域", options=region_options)
    if region == "随机":
        region = None
    
    return region


def carrier_config_panel(region):
    """运营商配置面板"""
    st.sidebar.header("📡 运营商配置")
    
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
        carrier_options = ["随机", "China Mobile", "China Unicom", "China Telecom", "AT&T", "Verizon"]
    
    carrier = st.sidebar.selectbox("运营商", options=carrier_options)
    if carrier == "随机":
        carrier = None
    
    return carrier


def action_buttons():
    """操作按钮面板"""
    st.sidebar.header("⚡ 操作")
    
    # 生成按钮
    generate_btn = st.sidebar.button("🚀 生成设备信息", type="primary", use_container_width=True)
    
    # 重置按钮
    reset_btn = st.sidebar.button("🔄 重置配置", use_container_width=True)
    
    return generate_btn, reset_btn


def device_info_display(device_info_list, commands_list):
    """设备信息展示面板"""
    if device_info_list and commands_list:
        # 设备信息总览
        st.subheader(f"📋 设备信息总览 (共 {len(device_info_list)} 条)")
        
        # 创建设备信息表格
        import pandas as pd
        device_data = []
        for i, device_info in enumerate(device_info_list):
            device_data.append({
                "设备编号": i + 1,
                "型号": device_info.model,
                "IMEI": device_info.imei,
                "IMSI": device_info.imsi,
                "区域": device_info.region,
                "运营商": device_info.carrier,
                "手机号": device_info.phone_number
            })
        
        df = pd.DataFrame(device_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # 提供JSON下载
        import json
        json_data = [device_info.__dict__ for device_info in device_info_list]
        json_str = json.dumps(json_data, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 下载设备信息(JSON)",
            data=json_str,
            file_name="device_info.json",
            mime="application/json",
            use_container_width=True
        )
        
        # 显示详细信息与对应的DG命令
        st.divider()
        st.subheader("🔍 DG命令详情")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_device = st.selectbox(
                "选择设备查看DG命令",
                options=[f"设备 {i+1}" for i in range(len(device_info_list))],
                index=0
            )
            
            idx = int(selected_device.split()[1]) - 1
            device_info = device_info_list[idx]
            
            st.markdown("**设备详细信息:**")
            st.markdown(f"- **型号**: {device_info.model}")
            st.markdown(f"- **IMEI**: {device_info.imei}")
            st.markdown(f"- **IMSI**: {device_info.imsi}")
            st.markdown(f"- **区域**: {device_info.region}")
            st.markdown(f"- **运营商**: {device_info.carrier}")
            st.markdown(f"- **手机号**: {device_info.phone_number}")
            st.markdown(f"- **网络类型**: {device_info.network_type}")
            st.markdown(f"- **IP地址**: {device_info.ip_address}")
        
        with col2:
            commands = commands_list[idx]
            
            st.markdown("**💻 对应的DG命令:**")
            commands_text = "\n".join(commands)
            st.code(commands_text, language="bash")
            
            # 提供命令文件下载
            st.download_button(
                label="💾 下载DG命令文件",
                data=commands_text,
                file_name=f"dg_commands_device_{idx+1}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        # 批量下载所有命令
        st.divider()
        all_commands = "\n\n".join(["\n".join(cmd_list) for cmd_list in commands_list])
        st.download_button(
            label="📦 批量下载所有DG命令",
            data=all_commands,
            file_name="all_dg_commands.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.info("ℹ️ 请在左侧边栏配置参数并点击'生成设备信息'按钮开始使用")