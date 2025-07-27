"""
侧边栏组件
"""

import streamlit as st
import os
from interfaces.streamlit.utils.model_config_manager import model_config_manager

def render_sidebar():
    """渲染侧边栏配置"""

    with st.sidebar:
        # 添加侧边栏标题和状态指示
        st.markdown("# 🤖 TradingAgents-CN")
        
        # 添加当前页面指示
        current_page = st.session_state.get('page_selector', '📊 仪表板')
        st.markdown(f"**当前页面**: {current_page}")
        st.markdown("---")
        # 页面导航
        st.markdown("### 📋 功能导航")
        
        # 页面选项
        page_options = [
            "📊 仪表板", 
            "📈 股票分析", 
            "💼 投资组合", 
            "📋 分析历史", 
            "📊 市场监控",
            "🤖 模型配置", 
            "⚙️ 系统设置",
            "💾 缓存管理", 
            "💰 Token统计"
        ]
        
        # 页面映射
        page_mapping = {
            "stock_analysis": "📈 股票分析",
            "model_config": "🤖 模型配置", 
            "analysis_history": "📋 分析历史",
            "system_settings": "⚙️ 系统设置",
            "portfolio_management": "💼 投资组合",
            "market_monitor": "📊 市场监控",
            "cache_management": "💾 缓存管理",
            "token_statistics": "💰 Token统计"
        }
        
        # 检查是否有来自其他页面的跳转请求
        current_page_from_state = st.session_state.get('current_page')
        if current_page_from_state and current_page_from_state in page_mapping:
            target_page = page_mapping[current_page_from_state]
            # 设置选择器的值
            st.session_state.page_selector = target_page
            # 清除跳转状态，避免重复跳转
            st.session_state.current_page = None
        
        # 处理来自query params的target_page导航
        if 'target_page' in st.session_state:
            st.session_state.page_selector = st.session_state.target_page
            # 清除target_page避免重复触发
            del st.session_state.target_page
        
        # 获取当前选择的页面
        if 'page_selector' not in st.session_state:
            st.session_state.page_selector = "📊 仪表板"
        
        # 获取默认索引
        try:
            default_index = page_options.index(st.session_state.page_selector)
        except ValueError:
            default_index = 0
            st.session_state.page_selector = page_options[0]
        
        page = st.selectbox(
            "选择功能模块",
            page_options,
            index=default_index,
            help="选择要使用的功能模块",
            key="page_selector"
        )
        
        st.markdown("---")
        
        # 添加快速导航按钮（在所有页面都显示）
        st.markdown("### 🚀 快速操作")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📈 快速分析", use_container_width=True, help="快速开始股票分析"):
                st.session_state.page_selector = "📈 股票分析"
                st.rerun()
        
        with col2:
            if st.button("📋 查看历史", use_container_width=True, help="查看分析历史"):
                st.session_state.page_selector = "📋 分析历史"
                st.rerun()
        
        # 如果不是股票分析页面，显示简化的侧边栏并返回页面信息
        if page != "📈 股票分析":
            render_simplified_sidebar()
            return {"page": page}

        # 显示当前模型状态
        st.markdown("### 🤖 当前模型")
        current_model_name = model_config_manager.get_current_model()
        current_model = model_config_manager.get_model_config(current_model_name)
        
        if current_model and current_model.is_available:
            st.success(f"✅ {current_model.display_name}")
            # 获取分析配置
            model_analysis_config = model_config_manager.get_model_for_analysis(current_model_name)
            llm_provider = model_analysis_config.get("llm_provider", "anthropic")
            deep_think_llm = model_analysis_config.get("deep_think_llm", "claude-3-5-sonnet-20241022")
            quick_think_llm = model_analysis_config.get("quick_think_llm", "claude-3-5-haiku-20241022")
            backend_url = model_analysis_config.get("backend_url", "https://anyrouter.top")
            
            # 显示模型详情
            with st.expander("📋 模型详情", expanded=False):
                st.info(f"**深度思考**: `{deep_think_llm}`")
                st.info(f"**快速思考**: `{quick_think_llm}`")
                st.info(f"**API端点**: `{backend_url}`")
        else:
            st.error("❌ 当前模型不可用")
            st.warning("请在模型配置页面设置可用的模型")
        
        # 快速切换到模型配置
        if st.button("⚙️ 配置模型", help="切换到模型配置页面", use_container_width=True):
            return {"page": "🤖 模型配置"}

        # AI模型配置 (保持兼容性)
        st.markdown("### 🧠 AI模型配置")

        # LLM提供商选择 - 从session state获取当前配置
        current_config = st.session_state.get('sidebar_config', {})
        current_provider = current_config.get('llm_provider', 'dashscope')
        
        provider_options = ["dashscope", "deepseek", "google"]
        try:
            provider_index = provider_options.index(current_provider)
        except ValueError:
            provider_index = 0
        
        llm_provider = st.selectbox(
            "LLM提供商",
            options=provider_options,
            index=provider_index,
            format_func=lambda x: {
                "dashscope": "阿里百炼",
                "deepseek": "DeepSeek V3",
                "google": "Google AI"
            }[x],
            help="选择AI模型提供商",
            key="sidebar_llm_provider"
        )

        # 根据提供商显示不同的模型选项
        current_model = current_config.get('llm_model', '')
        
        if llm_provider == "dashscope":
            dashscope_options = ["qwen-turbo", "qwen-plus-latest", "qwen-max"]
            try:
                model_index = dashscope_options.index(current_model) if current_model in dashscope_options else 1
            except ValueError:
                model_index = 1
                
            llm_model = st.selectbox(
                "模型版本",
                options=dashscope_options,
                index=model_index,
                format_func=lambda x: {
                    "qwen-turbo": "Turbo - 快速",
                    "qwen-plus-latest": "Plus - 平衡",
                    "qwen-max": "Max - 最强"
                }[x],
                help="选择用于分析的阿里百炼模型",
                key="sidebar_dashscope_model"
            )
        elif llm_provider == "deepseek":
            deepseek_options = ["deepseek-chat"]
            try:
                model_index = deepseek_options.index(current_model) if current_model in deepseek_options else 0
            except ValueError:
                model_index = 0
                
            llm_model = st.selectbox(
                "选择DeepSeek模型",
                options=deepseek_options,
                index=model_index,
                format_func=lambda x: {
                    "deepseek-chat": "DeepSeek Chat - 通用对话模型，适合股票分析"
                }[x],
                help="选择用于分析的DeepSeek模型",
                key="sidebar_deepseek_model"
            )
        else:  # google
            google_options = ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"]
            try:
                model_index = google_options.index(current_model) if current_model in google_options else 0
            except ValueError:
                model_index = 0
                
            llm_model = st.selectbox(
                "选择Google模型",
                options=google_options,
                index=model_index,
                format_func=lambda x: {
                    "gemini-2.0-flash": "Gemini 2.0 Flash - 推荐使用",
                    "gemini-1.5-pro": "Gemini 1.5 Pro - 强大性能",
                    "gemini-1.5-flash": "Gemini 1.5 Flash - 快速响应"
                }[x],
                help="选择用于分析的Google Gemini模型",
                key="sidebar_google_model"
            )
        
        # 高级设置
        with st.expander("⚙️ 高级设置"):
            enable_memory = st.checkbox(
                "启用记忆功能",
                value=False,
                help="启用智能体记忆功能（可能影响性能）"
            )
            
            enable_debug = st.checkbox(
                "调试模式",
                value=False,
                help="启用详细的调试信息输出"
            )
            
            max_tokens = st.slider(
                "最大输出长度",
                min_value=1000,
                max_value=8000,
                value=4000,
                step=500,
                help="AI模型的最大输出token数量"
            )
        
        st.markdown("---")

        # 系统配置
        st.markdown("**🔧 系统配置**")

        # API密钥状态
        st.markdown("**🔑 API密钥状态**")

        def validate_api_key(key, expected_format):
            """验证API密钥格式"""
            if not key:
                return "未配置", "error"

            if expected_format == "dashscope" and key.startswith("sk-") and len(key) >= 32:
                return f"{key[:8]}...", "success"
            elif expected_format == "deepseek" and key.startswith("sk-") and len(key) >= 32:
                return f"{key[:8]}...", "success"
            elif expected_format == "finnhub" and len(key) >= 20:
                return f"{key[:8]}...", "success"
            elif expected_format == "tushare" and len(key) >= 32:
                return f"{key[:8]}...", "success"
            elif expected_format == "google" and key.startswith("AIza") and len(key) >= 32:
                return f"{key[:8]}...", "success"
            elif expected_format == "openai" and key.startswith("sk-") and len(key) >= 40:
                return f"{key[:8]}...", "success"
            elif expected_format == "anthropic" and key.startswith("sk-") and len(key) >= 40:
                return f"{key[:8]}...", "success"
            elif expected_format == "reddit" and len(key) >= 10:
                return f"{key[:8]}...", "success"
            else:
                return f"{key[:8]}... (格式异常)", "warning"

        # 必需的API密钥
        st.markdown("*必需配置:*")

        # 阿里百炼
        dashscope_key = os.getenv("DASHSCOPE_API_KEY")
        status, level = validate_api_key(dashscope_key, "dashscope")
        if level == "success":
            st.success(f"✅ 阿里百炼: {status}")
        elif level == "warning":
            st.warning(f"⚠️ 阿里百炼: {status}")
        else:
            st.error("❌ 阿里百炼: 未配置")

        # FinnHub
        finnhub_key = os.getenv("FINNHUB_API_KEY")
        status, level = validate_api_key(finnhub_key, "finnhub")
        if level == "success":
            st.success(f"✅ FinnHub: {status}")
        elif level == "warning":
            st.warning(f"⚠️ FinnHub: {status}")
        else:
            st.error("❌ FinnHub: 未配置")

        # 可选的API密钥
        st.markdown("*可选配置:*")

        # DeepSeek
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        status, level = validate_api_key(deepseek_key, "deepseek")
        if level == "success":
            st.success(f"✅ DeepSeek: {status}")
        elif level == "warning":
            st.warning(f"⚠️ DeepSeek: {status}")
        else:
            st.info("ℹ️ DeepSeek: 未配置")

        # Tushare
        tushare_key = os.getenv("TUSHARE_TOKEN")
        status, level = validate_api_key(tushare_key, "tushare")
        if level == "success":
            st.success(f"✅ Tushare: {status}")
        elif level == "warning":
            st.warning(f"⚠️ Tushare: {status}")
        else:
            st.info("ℹ️ Tushare: 未配置")

        # Google AI
        google_key = os.getenv("GOOGLE_API_KEY")
        status, level = validate_api_key(google_key, "google")
        if level == "success":
            st.success(f"✅ Google AI: {status}")
        elif level == "warning":
            st.warning(f"⚠️ Google AI: {status}")
        else:
            st.info("ℹ️ Google AI: 未配置")

        # OpenAI (如果配置了且不是默认值)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key != "your_openai_api_key_here":
            status, level = validate_api_key(openai_key, "openai")
            if level == "success":
                st.success(f"✅ OpenAI: {status}")
            elif level == "warning":
                st.warning(f"⚠️ OpenAI: {status}")

        # Anthropic (如果配置了且不是默认值)
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key and anthropic_key != "your_anthropic_api_key_here":
            status, level = validate_api_key(anthropic_key, "anthropic")
            if level == "success":
                st.success(f"✅ Anthropic: {status}")
            elif level == "warning":
                st.warning(f"⚠️ Anthropic: {status}")

        st.markdown("---")

        # 系统信息
        st.markdown("**ℹ️ 系统信息**")
        
        st.info(f"""
        **版本**: 1.0.0
        **框架**: Streamlit + LangGraph
        **AI模型**: {llm_provider.upper()} - {llm_model}
        **数据源**: Tushare + FinnHub API
        """)
        
        # 帮助链接
        st.markdown("**📚 帮助资源**")
        
        st.markdown("""
        - [📖 使用文档](https://github.com/TauricResearch/TradingAgents)
        - [🐛 问题反馈](https://github.com/TauricResearch/TradingAgents/issues)
        - [💬 讨论社区](https://github.com/TauricResearch/TradingAgents/discussions)
        - [🔧 API密钥配置](../docs/security/api_keys_security.md)
        """)
    
    return {
        'llm_provider': llm_provider,
        'llm_model': llm_model,
        'enable_memory': enable_memory,
        'enable_debug': enable_debug,
        'max_tokens': max_tokens
    }

def render_simplified_sidebar():
    """渲染简化的侧边栏（用于非股票分析页面）"""
    
    # 显示当前模型状态
    st.markdown("### 🤖 当前模型")
    current_model_name = model_config_manager.get_current_model()
    current_model = model_config_manager.get_model_config(current_model_name)
    
    if current_model and current_model.is_available:
        st.success(f"✅ {current_model.display_name}")
        
        # 显示简化的模型信息
        with st.expander("📋 模型信息", expanded=False):
            model_analysis_config = model_config_manager.get_model_for_analysis(current_model_name)
            llm_provider = model_analysis_config.get("llm_provider", "anthropic")
            deep_think_llm = model_analysis_config.get("deep_think_llm", "claude-3-5-sonnet-20241022")
            st.info(f"**提供商**: {llm_provider}")
            st.info(f"**模型**: {deep_think_llm}")
    else:
        st.error("❌ 当前模型不可用")
        st.warning("请在模型配置页面设置可用的模型")
    
    # 快速切换到模型配置
    if st.button("⚙️ 配置模型", help="切换到模型配置页面", use_container_width=True, key="simplified_config_model"):
        st.session_state.page_selector = "🤖 模型配置"
        st.rerun()
    
    st.markdown("---")
    
    # 显示简化的API状态
    st.markdown("### 🔑 API状态")
    
    # 检查关键API密钥
    api_keys = {
        "阿里百炼": os.getenv("DASHSCOPE_API_KEY"),
        "DeepSeek": os.getenv("DEEPSEEK_API_KEY"),
        "Tushare": os.getenv("TUSHARE_TOKEN"),
        "FinnHub": os.getenv("FINNHUB_API_KEY")
    }
    
    configured_count = 0
    for name, key in api_keys.items():
        if key and key not in ["your_finnhub_api_key_here", "your_deepseek_api_key_here"]:
            configured_count += 1
    
    if configured_count >= 2:  # 至少配置了2个API密钥
        st.success(f"✅ {configured_count}/{len(api_keys)} 个API已配置")
    elif configured_count >= 1:
        st.warning(f"⚠️ {configured_count}/{len(api_keys)} 个API已配置")
    else:
        st.error(f"❌ {configured_count}/{len(api_keys)} 个API已配置")
    
    # 快速跳转到系统设置
    if st.button("⚙️ 系统设置", help="查看详细API状态和系统配置", use_container_width=True, key="simplified_system_settings"):
        st.session_state.page_selector = "⚙️ 系统设置"
        st.rerun()
    
    st.markdown("---")
    
    # 显示系统信息
    st.markdown("### ℹ️ 系统信息")
    
    # 获取当前配置
    current_config = st.session_state.get('sidebar_config', {})
    llm_provider = current_config.get('llm_provider', 'dashscope')
    llm_model = current_config.get('llm_model', 'qwen-plus-latest')
    
    st.info(f"""
    **版本**: cn-0.1.10
    **当前模型**: {llm_provider.upper()}
    **框架**: Streamlit + LangGraph
    """)
    
    # 帮助链接
    st.markdown("### 📚 快速链接")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 使用文档", use_container_width=True, key="simplified_docs"):
            st.markdown("[📖 查看文档](https://github.com/hsliuping/TradingAgents-CN)")
    
    with col2:
        if st.button("🐛 问题反馈", use_container_width=True, key="simplified_issues"):
            st.markdown("[🐛 提交问题](https://github.com/hsliuping/TradingAgents-CN/issues)")
