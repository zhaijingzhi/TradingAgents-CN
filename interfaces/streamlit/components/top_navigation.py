"""
顶部导航栏组件
"""

import streamlit as st

def render_top_navigation():
    """渲染顶部导航栏"""
    
    # 自定义CSS样式
    st.markdown("""
    <style>
    .top-nav {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 0.5rem 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .nav-title {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0;
        text-align: center;
    }
    
    .nav-buttons {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        margin-top: 0.5rem;
        flex-wrap: wrap;
    }
    
    .nav-button {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 5px;
        text-decoration: none;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-button:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-1px);
    }
    
    .nav-button.active {
        background: rgba(255, 255, 255, 0.4);
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 页面配置
    pages = [
        {"key": "dashboard", "label": "📊 仪表板", "icon": "📊"},
        {"key": "stock_analysis", "label": "📈 股票分析", "icon": "📈"},
        {"key": "portfolio", "label": "💼 投资组合", "icon": "💼"},
        {"key": "history", "label": "📋 分析历史", "icon": "📋"},
        {"key": "market", "label": "📊 市场监控", "icon": "📊"},
        {"key": "model_config", "label": "🤖 模型配置", "icon": "🤖"},
        {"key": "settings", "label": "⚙️ 系统设置", "icon": "⚙️"},
        {"key": "cache", "label": "💾 缓存管理", "icon": "💾"},
        {"key": "tokens", "label": "💰 Token统计", "icon": "💰"}
    ]
    
    # 获取当前页面
    current_page = st.session_state.get('current_page', 'dashboard')
    
    # 渲染导航栏
    st.markdown("""
    <div class="top-nav">
        <h1 class="nav-title">🤖 TradingAgents-CN 股票分析平台</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # 渲染导航按钮
    cols = st.columns(len(pages))
    
    for i, page in enumerate(pages):
        with cols[i]:
            # 检查是否为当前页面
            is_active = current_page == page["key"]
            button_type = "primary" if is_active else "secondary"
            
            if st.button(
                page["label"], 
                key=f"nav_{page['key']}", 
                use_container_width=True,
                type=button_type,
                disabled=is_active
            ):
                st.session_state.current_page = page["key"]
                st.rerun()
    
    return current_page

def get_page_title(page_key):
    """获取页面标题"""
    titles = {
        "dashboard": "📊 仪表板",
        "stock_analysis": "📈 股票分析", 
        "portfolio": "💼 投资组合",
        "history": "📋 分析历史",
        "market": "📊 市场监控",
        "model_config": "🤖 模型配置",
        "settings": "⚙️ 系统设置",
        "cache": "💾 缓存管理",
        "tokens": "💰 Token统计"
    }
    return titles.get(page_key, "📊 仪表板")