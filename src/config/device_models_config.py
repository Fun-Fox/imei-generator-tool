"""设备型号配置管理页面"""

import streamlit as st
from src.config.device_models import DEVICE_MODELS


def display_device_models_config():
    """显示和编辑设备型号配置"""
    st.header("📱 设备型号配置管理")
    
    # 说明
    st.markdown("""
    在这里可以管理设备品牌和对应的型号及TAC码。
    TAC (Type Allocation Code) 是IMEI号码的前8位，用于标识设备型号。
    """)
    
    # 显示当前配置
    st.subheader("当前设备型号配置")
    
    # 选择品牌
    brands = list(DEVICE_MODELS.keys())
    selected_brand = st.selectbox("选择品牌", options=["新增品牌"] + brands)
    
    if selected_brand == "新增品牌":
        # 添加新品牌
        new_brand = st.text_input("新品牌名称")
        
        if st.button("添加品牌"):
            if new_brand:
                if new_brand not in DEVICE_MODELS:
                    DEVICE_MODELS[new_brand] = {}
                    st.success(f"成功添加品牌 {new_brand}")
                    st.experimental_rerun()
                else:
                    st.error(f"品牌 {new_brand} 已存在")
            else:
                st.error("请填写品牌名称")
    else:
        # 编辑现有品牌
        st.subheader(f"编辑品牌: {selected_brand}")
        
        # 显示该品牌的所有型号
        models = DEVICE_MODELS.get(selected_brand, {})
        st.write(f"当前型号数量: {len(models)}")
        
        # 显示现有的型号列表
        if models:
            for model_name, tac in models.items():
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.text_input(f"型号名称", value=model_name, key=f"model_{selected_brand}_{tac}")
                with col2:
                    st.text_input(f"TAC码", value=tac, key=f"tac_{selected_brand}_{tac}")
                with col3:
                    if st.button("删除", key=f"del_{selected_brand}_{tac}"):
                        # 删除操作
                        del models[model_name]
                        DEVICE_MODELS[selected_brand] = models
                        st.success(f"已删除型号 {model_name} 及其TAC码")
                        st.experimental_rerun()
        else:
            st.info("该品牌暂无型号")
        
        # 添加新的型号
        st.subheader("添加新的型号")
        new_model_name = st.text_input("型号名称")
        new_tac = st.text_input("TAC码（8位数字）")
        if st.button("添加型号"):
            if new_model_name and new_tac:
                if len(new_tac) == 8 and new_tac.isdigit():
                    if new_model_name not in models:
                        models[new_model_name] = new_tac
                        DEVICE_MODELS[selected_brand] = models
                        st.success(f"成功添加型号 {new_model_name} 和TAC码 {new_tac}")
                        st.experimental_rerun()
                    else:
                        st.error(f"型号 {new_model_name} 已存在")
                else:
                    st.error("TAC码必须是8位数字")
            else:
                st.error("请输入型号名称和TAC码")


def main():
    """独立运行设备型号配置页面"""
    st.set_page_config(page_title="设备型号配置", layout="wide")
    display_device_models_config()


if __name__ == "__main__":
    main()