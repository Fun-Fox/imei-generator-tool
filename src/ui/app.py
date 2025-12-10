"""主应用程序界面"""

import streamlit as st

from src.ui.components import device_config_panel, location_config_panel, \
    carrier_config_panel, action_buttons, device_info_display
from src.generators.device_info_generator import DeviceInfoGenerator
from src.executors.dg_command_generator import DGCommandGenerator


def main():
    st.set_page_config(
        page_title="设备信息模拟器",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 页面标题和简介
    st.title("📱 设备信息模拟器")
    st.markdown("""
    #### 快速生成模拟设备信息和DG命令
    
    本工具可以帮助您快速生成各种移动设备的模拟信息，包括IMEI、IMSI、手机号码等，
    并自动生成相应的DG命令用于设备模拟。
    """)

    # 初始化session state
    if "device_info_list" not in st.session_state:
        st.session_state.device_info_list = []
    
    if "commands_list" not in st.session_state:
        st.session_state.commands_list = []
    
    # 侧边栏配置面板
    count, model = device_config_panel()
    region = location_config_panel()
    carrier = carrier_config_panel(region)
    generate_btn, reset_btn = action_buttons()
    
    # 重置功能
    if reset_btn:
        st.session_state.device_info_list = []
        st.session_state.commands_list = []
        st.sidebar.success("配置已重置")
    
    # 生成设备信息
    if generate_btn:
        with st.spinner("正在生成设备信息..."):
            generator = DeviceInfoGenerator()
            device_info_list = []
            
            # 处理参数
            final_model = model if model != "随机" else None
            final_region = region if region != "随机" else None
            final_carrier = carrier if carrier != "随机" else None
            
            for _ in range(count):
                device_info = generator.generate_device_info(final_model, final_region, final_carrier)
                device_info_list.append(device_info)
            
            st.session_state.device_info_list = device_info_list
            
            # 生成DG命令
            command_generator = DGCommandGenerator()
            commands_list = command_generator.generate_commands_batch(device_info_list)
            st.session_state.commands_list = commands_list
            
            st.sidebar.success(f"✅ 成功生成 {count} 条设备信息")
    
    # 主内容区域
    device_info_display(st.session_state.device_info_list, st.session_state.commands_list)
    
    # 使用说明
    with st.expander("📖 使用说明"):
        st.markdown("""
        #### 如何使用本工具：
        1. **配置参数**：在左侧边栏配置设备数量、品牌、型号、区域和运营商
        2. **生成信息**：点击"生成设备信息"按钮
        3. **查看结果**：在主界面查看生成的设备信息和DG命令
        4. **下载数据**：可以单独下载某个设备的DG命令，或批量下载所有命令
        
        #### 名词解释：
        - **IMEI**：国际移动设备识别码，用于唯一标识移动设备
        - **IMSI**：国际移动用户识别码，用于标识SIM卡用户
        - **DG命令**：用于在Android设备上模拟各种属性和状态的命令
        """)


if __name__ == "__main__":
    main()