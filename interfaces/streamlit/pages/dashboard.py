"""
仪表板页面 - 系统概览和快速操作
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import os

def show_dashboard():
    """显示仪表板页面"""
    st.title("📊 TradingAgents-CN 仪表板")
    
    # 系统状态概览
    render_system_overview()
    
    # 快速操作区域
    render_quick_actions()
    
    # 最近分析历史
    render_recent_analysis()
    
    # 系统统计
    render_system_statistics()

def render_system_overview():
    """渲染系统状态概览"""
    st.subheader("🔍 系统状态概览")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # API状态检查
        from interfaces.streamlit.utils.api_checker import check_api_keys
        api_status = check_api_keys()
        configured_apis = sum(1 for status in api_status['details'].values() if status['configured'])
        total_apis = len(api_status['details'])
        
        st.metric(
            label="API配置状态",
            value=f"{configured_apis}/{total_apis}",
            delta="已配置" if api_status['all_configured'] else "需配置"
        )
    
    with col2:
        # 模型状态
        try:
            from interfaces.streamlit.utils.model_config_manager import model_config_manager
            current_model = model_config_manager.get_current_model()
            model_config = model_config_manager.get_model_config(current_model)
            model_status = "可用" if model_config and model_config.is_available else "不可用"
            st.metric(
                label="当前模型",
                value=model_config.display_name if model_config else "未配置",
                delta=model_status
            )
        except:
            st.metric(label="当前模型", value="未知", delta="检查失败")
    
    with col3:
        # 缓存状态
        cache_size = get_cache_size()
        st.metric(
            label="缓存大小",
            value=format_size(cache_size),
            delta="正常" if cache_size < 1024*1024*100 else "需清理"  # 100MB阈值
        )
    
    with col4:
        # 今日分析次数
        today_count = get_today_analysis_count()
        st.metric(
            label="今日分析",
            value=f"{today_count}次",
            delta="活跃" if today_count > 0 else "待使用"
        )

def render_quick_actions():
    """渲染快速操作区域"""
    st.subheader("⚡ 快速操作")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🚀 开始新分析", use_container_width=True, type="primary"):
            st.session_state.current_page = "stock_analysis"
            st.rerun()
    
    with col2:
        if st.button("🤖 配置模型", use_container_width=True):
            st.session_state.current_page = "model_config"
            st.rerun()
    
    with col3:
        if st.button("📈 查看历史", use_container_width=True):
            st.session_state.current_page = "analysis_history"
            st.rerun()
    
    with col4:
        if st.button("⚙️ 系统设置", use_container_width=True):
            st.session_state.current_page = "system_settings"
            st.rerun()

def render_recent_analysis():
    """渲染最近分析历史"""
    st.subheader("📋 最近分析")
    
    # 获取最近的分析记录
    recent_analyses = get_recent_analyses(limit=5)
    
    if not recent_analyses:
        st.info("暂无分析记录，点击上方\"开始新分析\"开始您的第一次分析")
        return
    
    # 创建表格显示
    df = pd.DataFrame(recent_analyses)
    
    # 格式化显示
    for idx, analysis in enumerate(recent_analyses):
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            
            with col1:
                status_icon = "✅" if analysis['status'] == 'completed' else "❌" if analysis['status'] == 'failed' else "🔄"
                st.write(f"{status_icon} **{analysis['stock_symbol']}** ({analysis['market_type']})")
            
            with col2:
                st.write(f"📅 {analysis['date']}")
            
            with col3:
                st.write(f"🎯 {analysis['recommendation']}" if analysis.get('recommendation') else "分析中...")
            
            with col4:
                if st.button("查看", key=f"view_{idx}", use_container_width=True):
                    st.session_state.selected_analysis_id = analysis['id']
                    st.session_state.current_page = "analysis_detail"
                    st.rerun()

def render_system_statistics():
    """渲染系统统计图表"""
    st.subheader("📊 使用统计")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 分析次数趋势图
        st.markdown("##### 📈 分析次数趋势")
        trend_data = get_analysis_trend_data()
        if trend_data is not None and not trend_data.empty:
            fig = px.line(
                trend_data, 
                x='date', 
                y='count',
                title="最近7天分析次数",
                markers=True
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("暂无足够数据显示趋势")
    
    with col2:
        # 模型使用分布
        st.markdown("##### 🤖 模型使用分布")
        model_data = get_model_usage_data()
        if model_data is not None and not model_data.empty:
            fig = px.pie(
                model_data,
                values='count',
                names='model',
                title="模型使用分布"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("暂无模型使用数据")

# 辅助函数
def get_cache_size():
    """获取缓存大小"""
    cache_dirs = ["./cache", "./data", "./logs", "./results"]
    total_size = 0
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            for dirpath, dirnames, filenames in os.walk(cache_dir):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except:
                        pass
    return total_size

def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def get_today_analysis_count():
    """获取今日分析次数"""
    # 这里应该从数据库或日志中获取，暂时返回模拟数据
    return 0

def get_recent_analyses(limit=5):
    """获取最近的分析记录"""
    # 这里应该从数据库中获取，暂时返回模拟数据
    return []

def get_analysis_trend_data():
    """获取分析趋势数据"""
    # 模拟数据，实际应从数据库获取
    dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
    return pd.DataFrame({
        'date': dates,
        'count': [2, 5, 3, 8, 6, 4, 7]
    })

def get_model_usage_data():
    """获取模型使用数据"""
    # 模拟数据，实际应从数据库获取
    return pd.DataFrame({
        'model': ['阿里百炼', 'DeepSeek V3', 'Google AI'],
        'count': [15, 8, 5]
    })