"""
主页面 - 功能导航
"""

import streamlit as st
from interfaces.streamlit.utils.model_config_manager import model_config_manager

def show_home():
    """显示主页面"""
    st.title("🏠 TradingAgents-CN 主页")
    
    # 显示当前模型状态
    current_model_name = model_config_manager.get_current_model()
    current_model = model_config_manager.get_model_config(current_model_name)
    
    if current_model and current_model.is_available:
        st.success(f"🎯 当前使用模型: **{current_model.display_name}**")
    else:
        st.warning("⚠️ 当前模型配置不可用，请检查API密钥配置")
    
    st.markdown("---")
    
    # 功能模块导航
    st.subheader("📋 功能模块")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🤖 模型配置", help="配置和切换AI模型", use_container_width=True):
            st.session_state.current_page = "model_config"
            st.rerun()
    
    with col2:
        if st.button("🧹 缓存管理", help="清理系统缓存", use_container_width=True):
            st.session_state.current_page = "cache_management"
            st.rerun()
    
    with col3:
        if st.button("📊 股票分析", help="进行股票分析", use_container_width=True):
            st.session_state.current_page = "stock_analysis"
            st.rerun()
    
    st.markdown("---")
    
    # 系统信息
    st.subheader("ℹ️ 系统信息")
    
    # 获取所有模型状态
    models = model_config_manager.get_available_models()
    available_models = [m for m in models if m.is_available]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("可用模型数量", len(available_models))
    
    with col2:
        st.metric("总模型数量", len(models))
    
    # 显示可用模型列表
    if available_models:
        st.subheader("✅ 可用模型")
        for model in available_models:
            with st.expander(f"{model.display_name}", expanded=False):
                st.write(f"**提供商**: {model.provider}")
                st.write(f"**描述**: {model.description}")
                st.write(f"**深度思考模型**: `{model.deep_think_model}`")
                st.write(f"**快速思考模型**: `{model.quick_think_model}`")
    
    # 显示不可用模型
    unavailable_models = [m for m in models if not m.is_available]
    if unavailable_models:
        st.subheader("❌ 不可用模型")
        for model in unavailable_models:
            with st.expander(f"{model.display_name} (需要配置)", expanded=False):
                st.write(f"**提供商**: {model.provider}")
                st.write(f"**描述**: {model.description}")
                st.warning(f"需要配置环境变量: `{model.api_key_env}`")