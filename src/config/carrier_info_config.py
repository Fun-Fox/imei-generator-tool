"""运营商信息配置管理页面"""

import streamlit as st
from src.config.carrier_info import CARRIER_INFO


def display_carrier_info_config():
    """显示和编辑运营商信息配置"""
    st.header("📡 运营商信息配置管理")
    
    # 说明
    st.markdown("""
    在这里可以管理不同国家/地区的运营商信息，包括：
    - MCC (Mobile Country Code)：移动国家码
    - MNC (Mobile Network Code)：移动网络码
    - PhonePrefix：手机号前缀
    """)
    
    # 显示当前配置
    st.subheader("当前运营商配置")
    
    # 选择国家/地区
    regions = list(CARRIER_INFO.keys())
    selected_region = st.selectbox("选择国家/地区", options=["新增国家/地区"] + regions)
    
    if selected_region == "新增国家/地区":
        # 添加新国家/地区
        new_region = st.text_input("新国家/地区名称")
        new_mcc = st.text_input("MCC码（3位数字）")
        
        if st.button("添加国家/地区"):
            if new_region and new_mcc:
                if len(new_mcc) == 3 and new_mcc.isdigit():
                    # 初始化新的国家/地区配置
                    CARRIER_INFO[new_region] = {
                        "MCC": new_mcc,
                        "MNC": {},
                        "PhonePrefix": []
                    }
                    st.success(f"成功添加国家/地区 {new_region}，MCC: {new_mcc}")
                    st.experimental_rerun()
                else:
                    st.error("MCC码必须是3位数字")
            else:
                st.error("请填写国家/地区名称和MCC码")
    else:
        # 编辑现有国家/地区
        st.subheader(f"编辑国家/地区: {selected_region}")
        
        # 显示基本信息
        mcc = CARRIER_INFO[selected_region]["MCC"]
        new_mcc = st.text_input("MCC码", value=mcc)
        if new_mcc != mcc:
            if len(new_mcc) == 3 and new_mcc.isdigit():
                CARRIER_INFO[selected_region]["MCC"] = new_mcc
                st.success(f"MCC码已更新为 {new_mcc}")
            else:
                st.error("MCC码必须是3位数字")
        
        # 管理运营商
        st.subheader("运营商管理")
        carriers = list(CARRIER_INFO[selected_region]["MNC"].keys())
        selected_carrier = st.selectbox("选择运营商", options=["新增运营商"] + carriers)
        
        if selected_carrier == "新增运营商":
            # 添加新运营商
            new_carrier = st.text_input("新运营商名称")
            new_mncs = st.text_input("MNC码（多个用逗号分隔）")
            
            if st.button("添加运营商"):
                if new_carrier and new_mncs:
                    # 解析MNC码
                    mnc_list = [mnc.strip() for mnc in new_mncs.split(",") if mnc.strip()]
                    valid_mncs = []
                    for mnc in mnc_list:
                        if (len(mnc) in [2, 3]) and mnc.isdigit():
                            valid_mncs.append(mnc)
                    
                    if len(valid_mncs) == len(mnc_list):
                        CARRIER_INFO[selected_region]["MNC"][new_carrier] = valid_mncs
                        st.success(f"成功添加运营商 {new_carrier} 和MNC码 {valid_mncs}")
                        st.experimental_rerun()
                    else:
                        st.error("MNC码必须是2位或3位数字，多个用逗号分隔")
                else:
                    st.error("请填写运营商名称和至少一个MNC码")
        else:
            # 编辑现有运营商
            st.subheader(f"编辑运营商: {selected_carrier}")
            
            mncs = CARRIER_INFO[selected_region]["MNC"][selected_carrier]
            mnc_str = ", ".join(mncs)
            new_mncs = st.text_input("MNC码（多个用逗号分隔）", value=mnc_str)
            
            if st.button("更新MNC码"):
                if new_mncs:
                    # 解析MNC码
                    mnc_list = [mnc.strip() for mnc in new_mncs.split(",") if mnc.strip()]
                    valid_mncs = []
                    for mnc in mnc_list:
                        if (len(mnc) in [2, 3]) and mnc.isdigit():
                            valid_mncs.append(mnc)
                    
                    if len(valid_mncs) == len(mnc_list):
                        CARRIER_INFO[selected_region]["MNC"][selected_carrier] = valid_mncs
                        st.success(f"MNC码已更新为 {valid_mncs}")
                        st.experimental_rerun()
                    else:
                        st.error("MNC码必须是2位或3位数字，多个用逗号分隔")
                else:
                    st.error("请填写至少一个MNC码")
            
            if st.button("删除运营商"):
                del CARRIER_INFO[selected_region]["MNC"][selected_carrier]
                st.success(f"已删除运营商 {selected_carrier}")
                st.experimental_rerun()
        
        # 管理手机号前缀
        st.subheader("手机号前缀管理")
        prefixes = CARRIER_INFO[selected_region]["PhonePrefix"]
        prefix_str = ", ".join(prefixes)
        new_prefixes = st.text_area("手机号前缀（多个用逗号分隔）", value=prefix_str, height=100)
        
        if st.button("更新手机号前缀"):
            if new_prefixes:
                # 解析前缀
                prefix_list = [prefix.strip() for prefix in new_prefixes.split(",") if prefix.strip()]
                CARRIER_INFO[selected_region]["PhonePrefix"] = prefix_list
                st.success(f"手机号前缀已更新为 {prefix_list}")
                st.experimental_rerun()
            else:
                CARRIER_INFO[selected_region]["PhonePrefix"] = []
                st.success("手机号前缀已清空")


def main():
    """独立运行运营商信息配置页面"""
    st.set_page_config(page_title="运营商信息配置", layout="wide")
    display_carrier_info_config()


if __name__ == "__main__":
    main()