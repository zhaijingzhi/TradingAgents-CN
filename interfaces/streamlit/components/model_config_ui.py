"""
模型配置UI组件
提供可视化的模型选择和配置界面
"""

import streamlit as st
import os
from typing import Optional
from interfaces.streamlit.utils.model_config_manager import model_config_manager, ModelConfig

def render_model_config_page():
    """渲染模型配置页面"""
    st.title("🤖 模型配置管理")
    st.markdown("---")
    
    # 获取可用模型
    available_models = model_config_manager.get_available_models()
    current_model = model_config_manager.get_current_model()
    
    # 显示当前使用的模型
    current_model_config = model_config_manager.get_model_config(current_model)
    if current_model_config:
        st.success(f"🎯 **当前使用模型**: {current_model_config.display_name}")
        st.info(f"📝 **模型描述**: {current_model_config.description}")
    
    st.markdown("---")
    
    # 模型选择区域
    st.subheader("🔧 选择模型")
    
    # 创建两列布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 显示所有可用模型
        for model in available_models:
            with st.container():
                # 创建模型卡片
                is_current = model.name == current_model
                is_available = model.is_available
                
                # 状态图标
                if is_current:
                    status_icon = "🎯"
                    status_text = "当前使用"
                elif is_available:
                    status_icon = "✅"
                    status_text = "可用"
                else:
                    status_icon = "❌"
                    status_text = "未配置"
                
                # 模型卡片
                card_color = "success" if is_current else ("normal" if is_available else "error")
                
                with st.expander(f"{status_icon} {model.display_name} ({status_text})", expanded=is_current):
                    st.markdown(f"**提供商**: {model.provider}")
                    st.markdown(f"**描述**: {model.description}")
                    st.markdown(f"**深度思考模型**: `{model.deep_think_model}`")
                    st.markdown(f"**快速思考模型**: `{model.quick_think_model}`")
                    
                    # API密钥状态
                    api_key = os.getenv(model.api_key_env, "")
                    if api_key and api_key not in ["your_api_key_here", "xxx"]:
                        st.success(f"✅ API密钥已配置: `{model.api_key_env}`")
                        
                        # 如果有base_url配置，也显示
                        if model.base_url_env:
                            base_url = os.getenv(model.base_url_env, "")
                            if base_url:
                                st.info(f"🔗 API端点: `{base_url}`")
                        
                        # 切换按钮
                        if not is_current and is_available:
                            if st.button(f"🔄 切换到 {model.display_name}", key=f"switch_{model.name}"):
                                if switch_model(model.name):
                                    st.success(f"✅ 已切换到 {model.display_name}")
                                    st.rerun()
                                else:
                                    st.error("❌ 切换失败，请检查配置")
                    else:
                        st.error(f"❌ API密钥未配置: `{model.api_key_env}`")
                        st.markdown("请在 `.env` 文件中配置相应的API密钥")
    
    with col2:
        # 配置指南
        st.subheader("📋 配置指南")
        
        with st.expander("🔧 如何配置API密钥", expanded=True):
            st.markdown("""
            **步骤1**: 编辑 `.env` 文件
            
            **步骤2**: 添加或修改以下配置:
            
            ```bash
            # 自定义模型 (推荐)
            DEEPSEEK_API_KEY=your_api_key
            DEEPSEEK_BASE_URL=https://your-endpoint.com
            DEEPSEEK_ENABLED=true
            
            # 阿里百炼
            DASHSCOPE_API_KEY=your_dashscope_key
            
            # OpenAI
            OPENAI_API_KEY=your_openai_key
            
            # Google Gemini
            GOOGLE_API_KEY=your_google_key
            
            # Anthropic Claude
            ANTHROPIC_API_KEY=your_anthropic_key
            ```
            
            **步骤3**: 重启应用使配置生效
            """)
        
        with st.expander("💡 模型选择建议"):
            st.markdown("""
            **🎯 自定义模型**: 
            - 兼容Anthropic API
            - 支持自定义端点
            - 推荐用于生产环境
            
            **🇨🇳 阿里百炼**: 
            - 中文优化
            - 国内访问稳定
            - 成本相对较低
            
            **🌍 OpenAI GPT**: 
            - 功能强大
            - 生态完善
            - 需要国外网络
            
            **🔍 Google Gemini**: 
            - 免费额度大
            - 多模态支持
            - 推理能力强
            """)

def switch_model(model_name: str) -> bool:
    """切换模型"""
    try:
        # 更新环境文件
        success = model_config_manager.update_env_file(model_name)
        
        if success:
            # 更新session state中的配置
            model_config = model_config_manager.get_model_for_analysis(model_name)
            if 'analysis_config' not in st.session_state:
                st.session_state.analysis_config = {}
            
            st.session_state.analysis_config.update(model_config)
            
            # 记录切换日志
            model = model_config_manager.get_model_config(model_name)
            if model:
                st.session_state.current_model = model_name
                st.session_state.current_model_display = model.display_name
        
        return success
    except Exception as e:
        st.error(f"切换模型失败: {e}")
        return False

def get_current_model_info() -> Optional[ModelConfig]:
    """获取当前模型信息"""
    current_model = model_config_manager.get_current_model()
    return model_config_manager.get_model_config(current_model)

def render_model_selector_sidebar():
    """在侧边栏渲染简化的模型选择器"""
    with st.sidebar:
        st.markdown("### 🤖 当前模型")
        
        current_model_info = get_current_model_info()
        if current_model_info:
            st.success(f"✅ {current_model_info.display_name}")
            
            # 快速切换按钮
            available_models = [m for m in model_config_manager.get_available_models() if m.is_available]
            if len(available_models) > 1:
                model_names = [m.display_name for m in available_models]
                current_index = next((i for i, m in enumerate(available_models) if m.name == current_model_info.name), 0)
                
                selected_display = st.selectbox(
                    "快速切换模型",
                    model_names,
                    index=current_index,
                    key="sidebar_model_selector"
                )
                
                # 找到选中的模型
                selected_model = next((m for m in available_models if m.display_name == selected_display), None)
                if selected_model and selected_model.name != current_model_info.name:
                    if st.button("🔄 切换", key="sidebar_switch"):
                        if switch_model(selected_model.name):
                            st.success("✅ 切换成功")
                            st.rerun()
        else:
            st.error("❌ 无可用模型")
        
        if st.button("⚙️ 模型配置", key="sidebar_config"):
            st.session_state.show_model_config = True
            st.rerun()