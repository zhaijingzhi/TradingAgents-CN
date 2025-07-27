#!/usr/bin/env python3
"""
TradingAgents-CN Streamlit Web界面 - 顶部导航版本
"""

import streamlit as st
import os
import sys
from pathlib import Path
import datetime
import time
from dotenv import load_dotenv

# 导入日志模块
from tradingagents.utils.logging_manager import get_logger
logger = get_logger('web')

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 加载环境变量
load_dotenv(project_root / ".env", override=True)

# 导入自定义组件
from interfaces.streamlit.components.top_navigation import render_top_navigation, get_page_title
from interfaces.streamlit.utils.api_checker import check_api_keys

# 设置页面配置
st.set_page_config(
    page_title="TradingAgents-CN 股票分析平台",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",  # 折叠侧边栏，使用顶部导航
    menu_items=None
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 隐藏Streamlit默认元素 */
    .stAppToolbar, header[data-testid="stHeader"], .stDeployButton,
    [data-testid="stToolbar"], [data-testid="stDecoration"], 
    [data-testid="stStatusWidget"], #MainMenu, footer,
    .viewerBadge_container__1QSob {
        display: none !important;
    }
    
    /* 主容器样式 */
    .main .block-container {
        padding-top: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: none !important;
    }
    
    /* 页面内容样式 */
    .page-content {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* 成功/错误/警告框样式 */
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """初始化会话状态"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'analysis_running' not in st.session_state:
        st.session_state.analysis_running = False

def render_page_content(current_page):
    """根据当前页面渲染内容"""
    
    # 显示页面标题
    st.title(get_page_title(current_page))
    
    try:
        if current_page == "dashboard":
            from interfaces.streamlit.pages.dashboard import show_dashboard
            show_dashboard()
            
        elif current_page == "stock_analysis":
            from interfaces.streamlit.pages.stock_analysis import show_stock_analysis
            show_stock_analysis()
            
        elif current_page == "portfolio":
            from interfaces.streamlit.pages.portfolio_management import show_portfolio_management
            show_portfolio_management()
            
        elif current_page == "history":
            from interfaces.streamlit.pages.analysis_history import show_analysis_history
            show_analysis_history()
            
        elif current_page == "market":
            from interfaces.streamlit.pages.market_monitor import show_market_monitor
            show_market_monitor()
            
        elif current_page == "model_config":
            from interfaces.streamlit.pages.model_config import show_model_config
            show_model_config()
            
        elif current_page == "settings":
            from interfaces.streamlit.pages.system_settings import show_system_settings
            show_system_settings()
            
        elif current_page == "cache":
            from interfaces.streamlit.pages.cache_management import show_cache_management
            show_cache_management()
            
        elif current_page == "tokens":
            from interfaces.streamlit.modules.token_statistics import render_token_statistics
            render_token_statistics()
            
        else:
            st.error(f"未知页面: {current_page}")
            
    except ImportError as e:
        st.error(f"页面加载失败: {e}")
        st.info("请确保所有依赖模块已正确安装")
        
        # 提供返回仪表板的选项
        if st.button("🏠 返回仪表板"):
            st.session_state.current_page = "dashboard"
            st.rerun()

def main():
    """主应用程序"""
    
    # 初始化会话状态
    initialize_session_state()
    
    # 检查API密钥配置
    api_status = check_api_keys()
    
    # 渲染顶部导航栏
    current_page = render_top_navigation()
    
    # 如果API配置不完整，显示警告
    if not api_status['all_configured'] and current_page != 'settings':
        st.warning("⚠️ API密钥配置不完整，建议先进入系统设置配置API密钥")
        if st.button("🔧 前往系统设置"):
            st.session_state.current_page = "settings"
            st.rerun()
    
    # 渲染页面内容
    with st.container():
        render_page_content(current_page)
    
    # 页面底部信息
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.caption("🤖 TradingAgents-CN v0.1.10")
    
    with col2:
        st.caption("💡 基于多智能体的股票分析平台")
    
    with col3:
        if st.session_state.get('last_analysis_time'):
            st.caption(f"🕒 上次分析: {st.session_state.last_analysis_time.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()