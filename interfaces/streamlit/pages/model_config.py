"""
模型配置页面
"""

import streamlit as st
import os
from interfaces.streamlit.utils.model_config_manager import model_config_manager

def show_model_config():
    """显示模型配置页面"""
    st.title("🤖 模型配置")
    
    # 获取所有模型
    models = model_config_manager.get_available_models()
    current_model_name = model_config_manager.get_current_model()
    
    # 显示当前模型
    current_model = model_config_manager.get_model_config(current_model_name)
    if current_model:
        if current_model.is_available:
            st.success(f"🎯 当前使用: **{current_model.display_name}**")
        else:
            st.error(f"❌ 当前模型不可用: **{current_model.display_name}**")
    
    st.markdown("---")
    
    # 模型选择
    st.subheader("🔄 切换模型")
    
    available_models = [m for m in models if m.is_available]
    
    if not available_models:
        st.warning("⚠️ 没有可用的模型，请先配置API密钥")
        st.markdown("### 📝 配置指南")
        st.markdown("""
        请在 `.env` 文件中配置以下API密钥之一：
        
        - **DEEPSEEK_API_KEY**: 自定义模型API密钥
        - **DASHSCOPE_API_KEY**: 阿里百炼API密钥  
        - **OPENAI_API_KEY**: OpenAI API密钥
        - **GOOGLE_API_KEY**: Google API密钥
        - **ANTHROPIC_API_KEY**: Anthropic API密钥
        """)
        return
    
    # 模型选择器
    model_options = {m.display_name: m.name for m in available_models}
    current_display_name = current_model.display_name if current_model else list(model_options.keys())[0]
    
    selected_display_name = st.selectbox(
        "选择要使用的模型",
        options=list(model_options.keys()),
        index=list(model_options.keys()).index(current_display_name) if current_display_name in model_options else 0,
        help="选择要切换到的模型"
    )
    
    selected_model_name = model_options[selected_display_name]
    selected_model = model_config_manager.get_model_config(selected_model_name)
    
    # 显示选中模型的详细信息
    if selected_model:
        st.markdown("### 📋 模型详情")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**提供商**: {selected_model.provider}")
            st.info(f"**深度思考模型**: `{selected_model.deep_think_model}`")
        
        with col2:
            st.info(f"**快速思考模型**: `{selected_model.quick_think_model}`")
            api_key = os.getenv(selected_model.api_key_env, "未配置")
            masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "未配置"
            st.info(f"**API密钥**: `{masked_key}`")
        
        st.write(f"**描述**: {selected_model.description}")
        
        # 切换按钮
        if selected_model_name != current_model_name:
            if st.button("🔄 切换到此模型", type="primary", use_container_width=True):
                if model_config_manager.update_env_file(selected_model_name):
                    st.success(f"✅ 已切换到 {selected_model.display_name}")
                    st.info("💡 请重启应用使配置生效")
                    st.rerun()
                else:
                    st.error("❌ 切换失败，请检查配置")
        else:
            st.success("✅ 当前已使用此模型")
    
    st.markdown("---")
    
    # 显示所有模型状态
    st.subheader("📊 所有模型状态")
    
    for model in models:
        with st.expander(f"{model.display_name} {'✅' if model.is_available else '❌'}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**名称**: {model.name}")
                st.write(f"**提供商**: {model.provider}")
                st.write(f"**状态**: {'可用' if model.is_available else '不可用'}")
            
            with col2:
                st.write(f"**API密钥环境变量**: `{model.api_key_env}`")
                if model.base_url_env:
                    st.write(f"**API端点环境变量**: `{model.base_url_env}`")
                if model.enabled_env:
                    st.write(f"**启用开关**: `{model.enabled_env}`")
            
            st.write(f"**描述**: {model.description}")
            st.write(f"**深度思考模型**: `{model.deep_think_model}`")
            st.write(f"**快速思考模型**: `{model.quick_think_model}`")
            
            if not model.is_available:
                st.warning(f"⚠️ 需要在 `.env` 文件中配置 `{model.api_key_env}`")
    
    st.markdown("---")
    
    # 配置指南
    st.subheader("📖 配置指南")
    
    with st.expander("🔧 如何配置API密钥", expanded=False):
        st.markdown("""
        ### 1. 编辑 .env 文件
        在项目根目录的 `.env` 文件中添加或修改以下配置：
        
        ```bash
        # 自定义模型 (推荐)
        DEEPSEEK_API_KEY=your_api_key_here
        DEEPSEEK_BASE_URL=https://anyrouter.top
        DEEPSEEK_ENABLED=true
        
        # 阿里百炼
        DASHSCOPE_API_KEY=your_dashscope_key_here
        
        # OpenAI
        OPENAI_API_KEY=your_openai_key_here
        
        # Google Gemini
        GOOGLE_API_KEY=your_google_key_here
        
        # Anthropic Claude
        ANTHROPIC_API_KEY=your_anthropic_key_here
        ```
        
        ### 2. 重启应用
        修改配置后需要重启应用使配置生效。
        
        ### 3. 验证配置
        在此页面查看模型状态，确保显示为"可用"。
        """)
    
    st.markdown("---")
    
    # 导航按钮 - 使用query params来避免session state冲突
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 返回主页", use_container_width=True, key="nav_home"):
            st.query_params.page = "dashboard"
            st.rerun()
    
    with col2:
        if st.button("📈 股票分析", use_container_width=True, key="nav_analysis"):
            st.query_params.page = "analysis"
            st.rerun()
    
    with col3:
        if st.button("⚙️ 系统设置", use_container_width=True, key="nav_settings"):
            st.query_params.page = "settings"
            st.rerun()