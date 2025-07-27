"""
系统设置页面 - 系统配置和管理
"""

import streamlit as st
import os
import json
from pathlib import Path

def show_system_settings():
    """显示系统设置页面"""
    st.title("⚙️ 系统设置")
    
    # 设置选项卡
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔑 API配置", 
        "🤖 模型设置", 
        "💾 数据管理", 
        "🔔 通知设置", 
        "🎨 界面设置"
    ])
    
    with tab1:
        render_api_settings()
    
    with tab2:
        render_model_settings()
    
    with tab3:
        render_data_settings()
    
    with tab4:
        render_notification_settings()
    
    with tab5:
        render_ui_settings()
    
    # 添加导航按钮
    add_navigation_buttons()

def render_api_settings():
    """渲染API配置设置"""
    st.subheader("🔑 API密钥配置")
    
    # API配置表单
    with st.form("api_config"):
        st.markdown("##### 🇨🇳 国产AI模型")
        
        col1, col2 = st.columns(2)
        
        with col1:
            dashscope_key = st.text_input(
                "阿里百炼 API Key",
                value=get_masked_env_var("DASHSCOPE_API_KEY"),
                type="password",
                help="从 https://dashscope.aliyun.com/ 获取"
            )
            
            deepseek_key = st.text_input(
                "DeepSeek API Key",
                value=get_masked_env_var("DEEPSEEK_API_KEY"),
                type="password",
                help="从 https://platform.deepseek.com/ 获取"
            )
        
        with col2:
            baidu_key = st.text_input(
                "百度千帆 API Key",
                value=get_masked_env_var("BAIDU_API_KEY"),
                type="password",
                help="从百度智能云获取"
            )
            
            zhipu_key = st.text_input(
                "智谱AI API Key",
                value=get_masked_env_var("ZHIPU_API_KEY"),
                type="password",
                help="从 https://open.bigmodel.cn/ 获取"
            )
        
        st.markdown("##### 🌍 国际AI模型")
        
        col3, col4 = st.columns(2)
        
        with col3:
            openai_key = st.text_input(
                "OpenAI API Key",
                value=get_masked_env_var("OPENAI_API_KEY"),
                type="password",
                help="从 https://platform.openai.com/ 获取"
            )
            
            google_key = st.text_input(
                "Google AI API Key",
                value=get_masked_env_var("GOOGLE_API_KEY"),
                type="password",
                help="从 Google AI Studio 获取"
            )
        
        with col4:
            anthropic_key = st.text_input(
                "Anthropic API Key",
                value=get_masked_env_var("ANTHROPIC_API_KEY"),
                type="password",
                help="从 https://console.anthropic.com/ 获取"
            )
        
        st.markdown("##### 📊 数据源API")
        
        col5, col6 = st.columns(2)
        
        with col5:
            finnhub_key = st.text_input(
                "FinnHub API Key",
                value=get_masked_env_var("FINNHUB_API_KEY"),
                type="password",
                help="从 https://finnhub.io/ 获取"
            )
            
            tushare_token = st.text_input(
                "Tushare Token",
                value=get_masked_env_var("TUSHARE_TOKEN"),
                type="password",
                help="从 https://tushare.pro/ 获取"
            )
        
        with col6:
            alpha_vantage_key = st.text_input(
                "Alpha Vantage API Key",
                value=get_masked_env_var("ALPHA_VANTAGE_API_KEY"),
                type="password",
                help="从 https://www.alphavantage.co/ 获取"
            )
        
        # 保存按钮
        if st.form_submit_button("💾 保存API配置", type="primary"):
            save_api_config({
                "DASHSCOPE_API_KEY": dashscope_key,
                "DEEPSEEK_API_KEY": deepseek_key,
                "BAIDU_API_KEY": baidu_key,
                "ZHIPU_API_KEY": zhipu_key,
                "OPENAI_API_KEY": openai_key,
                "GOOGLE_API_KEY": google_key,
                "ANTHROPIC_API_KEY": anthropic_key,
                "FINNHUB_API_KEY": finnhub_key,
                "TUSHARE_TOKEN": tushare_token,
                "ALPHA_VANTAGE_API_KEY": alpha_vantage_key
            })
            st.success("✅ API配置已保存")
            st.rerun()
    
    # API状态检查
    st.markdown("---")
    st.subheader("🔍 API状态检查")
    
    if st.button("🔄 检查所有API状态"):
        check_all_api_status()

def render_model_settings():
    """渲染模型设置"""
    st.subheader("🤖 模型配置")
    
    # 默认模型设置
    with st.form("model_config"):
        st.markdown("##### 🎯 默认模型选择")
        
        col1, col2 = st.columns(2)
        
        with col1:
            default_provider = st.selectbox(
                "默认AI提供商",
                options=["dashscope", "deepseek", "openai", "google", "anthropic"],
                format_func=lambda x: {
                    "dashscope": "阿里百炼",
                    "deepseek": "DeepSeek",
                    "openai": "OpenAI",
                    "google": "Google AI",
                    "anthropic": "Anthropic"
                }[x],
                help="选择默认使用的AI提供商"
            )
        
        with col2:
            if default_provider == "dashscope":
                default_model = st.selectbox(
                    "默认模型",
                    options=["qwen-turbo", "qwen-plus", "qwen-max"],
                    help="选择默认使用的模型"
                )
            elif default_provider == "deepseek":
                default_model = st.selectbox(
                    "默认模型",
                    options=["deepseek-chat", "deepseek-coder"],
                    help="选择默认使用的模型"
                )
            else:
                default_model = st.text_input("模型名称", help="输入模型名称")
        
        st.markdown("##### ⚙️ 模型参数")
        
        col3, col4 = st.columns(2)
        
        with col3:
            temperature = st.slider(
                "Temperature (创造性)",
                min_value=0.0,
                max_value=2.0,
                value=0.7,
                step=0.1,
                help="控制输出的随机性，值越高越有创造性"
            )
            
            max_tokens = st.number_input(
                "最大Token数",
                min_value=100,
                max_value=8000,
                value=2000,
                help="控制输出的最大长度"
            )
        
        with col4:
            top_p = st.slider(
                "Top P (多样性)",
                min_value=0.0,
                max_value=1.0,
                value=0.9,
                step=0.1,
                help="控制输出的多样性"
            )
            
            frequency_penalty = st.slider(
                "频率惩罚",
                min_value=0.0,
                max_value=2.0,
                value=0.0,
                step=0.1,
                help="减少重复内容"
            )
        
        if st.form_submit_button("💾 保存模型配置", type="primary"):
            save_model_config({
                "default_provider": default_provider,
                "default_model": default_model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "frequency_penalty": frequency_penalty
            })
            st.success("✅ 模型配置已保存")

def render_data_settings():
    """渲染数据管理设置"""
    st.subheader("💾 数据管理")
    
    # 数据存储设置
    st.markdown("##### 📁 数据存储")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 数据目录设置
        current_data_dir = get_data_directory()
        st.text_input("数据目录", value=current_data_dir, disabled=True)
        
        if st.button("📂 更改数据目录"):
            show_change_data_directory_dialog()
    
    with col2:
        # 缓存设置
        cache_enabled = st.checkbox("启用数据缓存", value=True)
        cache_ttl = st.number_input("缓存过期时间(小时)", min_value=1, max_value=168, value=24)
    
    # 数据库设置
    st.markdown("##### 🗄️ 数据库配置")
    
    col3, col4 = st.columns(2)
    
    with col3:
        mongodb_enabled = st.checkbox("启用MongoDB", value=get_env_bool("MONGODB_ENABLED"))
        if mongodb_enabled:
            mongodb_host = st.text_input("MongoDB主机", value=os.getenv("MONGODB_HOST", "localhost"))
            mongodb_port = st.number_input("MongoDB端口", value=int(os.getenv("MONGODB_PORT", "27017")))
    
    with col4:
        redis_enabled = st.checkbox("启用Redis", value=get_env_bool("REDIS_ENABLED"))
        if redis_enabled:
            redis_host = st.text_input("Redis主机", value=os.getenv("REDIS_HOST", "localhost"))
            redis_port = st.number_input("Redis端口", value=int(os.getenv("REDIS_PORT", "6379")))
    
    # 数据清理
    st.markdown("##### 🧹 数据清理")
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        if st.button("🗑️ 清理缓存", use_container_width=True):
            clear_cache_data()
            st.success("缓存已清理")
    
    with col6:
        if st.button("📊 清理分析结果", use_container_width=True):
            clear_analysis_results()
            st.success("分析结果已清理")
    
    with col7:
        if st.button("📝 清理日志", use_container_width=True):
            clear_log_files()
            st.success("日志文件已清理")

def render_notification_settings():
    """渲染通知设置"""
    st.subheader("🔔 通知设置")
    
    # 通知方式
    st.markdown("##### 📢 通知方式")
    
    col1, col2 = st.columns(2)
    
    with col1:
        email_notifications = st.checkbox("邮件通知", value=False)
        if email_notifications:
            email_address = st.text_input("邮箱地址", placeholder="your@email.com")
            smtp_server = st.text_input("SMTP服务器", placeholder="smtp.gmail.com")
            smtp_port = st.number_input("SMTP端口", value=587)
    
    with col2:
        webhook_notifications = st.checkbox("Webhook通知", value=False)
        if webhook_notifications:
            webhook_url = st.text_input("Webhook URL", placeholder="https://your-webhook-url.com")
    
    # 通知事件
    st.markdown("##### 📋 通知事件")
    
    col3, col4 = st.columns(2)
    
    with col3:
        notify_analysis_complete = st.checkbox("分析完成", value=True)
        notify_analysis_failed = st.checkbox("分析失败", value=True)
        notify_high_risk = st.checkbox("高风险警告", value=True)
    
    with col4:
        notify_portfolio_change = st.checkbox("组合变动", value=False)
        notify_system_error = st.checkbox("系统错误", value=True)
        notify_api_limit = st.checkbox("API限制", value=True)
    
    if st.button("💾 保存通知设置", type="primary"):
        save_notification_settings({
            "email_notifications": email_notifications,
            "webhook_notifications": webhook_notifications,
            "notify_events": {
                "analysis_complete": notify_analysis_complete,
                "analysis_failed": notify_analysis_failed,
                "high_risk": notify_high_risk,
                "portfolio_change": notify_portfolio_change,
                "system_error": notify_system_error,
                "api_limit": notify_api_limit
            }
        })
        st.success("✅ 通知设置已保存")

def render_ui_settings():
    """渲染界面设置"""
    st.subheader("🎨 界面设置")
    
    # 主题设置
    st.markdown("##### 🎨 主题配置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.selectbox(
            "界面主题",
            options=["light", "dark", "auto"],
            format_func=lambda x: {"light": "浅色", "dark": "深色", "auto": "自动"}[x],
            help="选择界面主题"
        )
        
        primary_color = st.color_picker("主色调", value="#1f77b4")
    
    with col2:
        font_size = st.selectbox(
            "字体大小",
            options=["small", "medium", "large"],
            format_func=lambda x: {"small": "小", "medium": "中", "large": "大"}[x],
            index=1
        )
        
        sidebar_width = st.slider("侧边栏宽度", min_value=200, max_value=400, value=260)
    
    # 显示设置
    st.markdown("##### 📊 显示设置")
    
    col3, col4 = st.columns(2)
    
    with col3:
        show_debug_info = st.checkbox("显示调试信息", value=False)
        show_performance_metrics = st.checkbox("显示性能指标", value=False)
        auto_refresh_results = st.checkbox("自动刷新结果", value=True)
    
    with col4:
        default_chart_type = st.selectbox(
            "默认图表类型",
            options=["line", "bar", "candlestick"],
            format_func=lambda x: {"line": "线图", "bar": "柱图", "candlestick": "K线图"}[x]
        )
        
        results_per_page = st.number_input("每页结果数", min_value=5, max_value=50, value=10)
    
    # 语言设置
    st.markdown("##### 🌍 语言设置")
    
    language = st.selectbox(
        "界面语言",
        options=["zh-CN", "en-US"],
        format_func=lambda x: {"zh-CN": "简体中文", "en-US": "English"}[x],
        help="选择界面显示语言"
    )
    
    if st.button("💾 保存界面设置", type="primary"):
        save_ui_settings({
            "theme": theme,
            "primary_color": primary_color,
            "font_size": font_size,
            "sidebar_width": sidebar_width,
            "show_debug_info": show_debug_info,
            "show_performance_metrics": show_performance_metrics,
            "auto_refresh_results": auto_refresh_results,
            "default_chart_type": default_chart_type,
            "results_per_page": results_per_page,
            "language": language
        })
        st.success("✅ 界面设置已保存")
        st.info("部分设置需要刷新页面后生效")

# 辅助函数
def get_masked_env_var(var_name):
    """获取遮蔽的环境变量"""
    value = os.getenv(var_name, "")
    if value and len(value) > 8:
        return f"{value[:4]}{'*' * (len(value) - 8)}{value[-4:]}"
    return value

def get_env_bool(var_name, default=False):
    """获取布尔型环境变量"""
    value = os.getenv(var_name, "").lower()
    return value in ["true", "1", "yes", "on"] if value else default

def get_data_directory():
    """获取数据目录"""
    return os.getenv("TRADING_AGENTS_DATA_DIR", "./data")

def save_api_config(config):
    """保存API配置"""
    env_file = Path(".env")
    
    # 读取现有配置
    existing_config = {}
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    existing_config[key] = value
    
    # 更新配置
    for key, value in config.items():
        if value and not value.startswith('*'):  # 不保存遮蔽的值
            existing_config[key] = value
    
    # 写入配置
    with open(env_file, 'w', encoding='utf-8') as f:
        for key, value in existing_config.items():
            f.write(f"{key}={value}\n")

def save_model_config(config):
    """保存模型配置"""
    config_file = Path("config/model_config.json")
    config_file.parent.mkdir(exist_ok=True)
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def save_notification_settings(settings):
    """保存通知设置"""
    config_file = Path("config/notification_config.json")
    config_file.parent.mkdir(exist_ok=True)
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

def save_ui_settings(settings):
    """保存界面设置"""
    config_file = Path("config/ui_config.json")
    config_file.parent.mkdir(exist_ok=True)
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

def check_all_api_status():
    """检查所有API状态"""
    from interfaces.streamlit.utils.api_checker import check_api_keys
    
    with st.spinner("正在检查API状态..."):
        api_status = check_api_keys()
        
        st.subheader("📊 API状态报告")
        
        for api_name, status in api_status['details'].items():
            if status['configured']:
                st.success(f"✅ {api_name}: {status['display']}")
            else:
                st.error(f"❌ {api_name}: 未配置")

def show_change_data_directory_dialog():
    """显示更改数据目录对话框"""
    st.info("数据目录更改功能正在开发中...")

def clear_cache_data():
    """清理缓存数据"""
    import shutil
    cache_dir = Path("./cache")
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
        cache_dir.mkdir()

def clear_analysis_results():
    """清理分析结果"""
    import shutil
    results_dir = Path("./results")
    if results_dir.exists():
        shutil.rmtree(results_dir)
        results_dir.mkdir()

def clear_log_files():
    """清理日志文件"""
    import shutil
    logs_dir = Path("./logs")
    if logs_dir.exists():
        shutil.rmtree(logs_dir)
        logs_dir.mkdir()

def add_navigation_buttons():
    """添加导航按钮"""
    st.markdown("---")
    
    # 导航按钮 - 使用query params来避免session state冲突
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 返回主页", use_container_width=True, key="settings_nav_home"):
            st.query_params.page = "dashboard"
            st.rerun()
    
    with col2:
        if st.button("📈 股票分析", use_container_width=True, key="settings_nav_analysis"):
            st.query_params.page = "analysis"
            st.rerun()
    
    with col3:
        if st.button("🤖 模型配置", use_container_width=True, key="settings_nav_model"):
            st.query_params.page = "model_config"
            st.rerun()