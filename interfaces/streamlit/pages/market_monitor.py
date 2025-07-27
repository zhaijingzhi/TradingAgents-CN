"""
市场监控页面 - 实时市场数据和热点监控
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

def show_market_monitor():
    """显示市场监控页面"""
    st.title("📊 市场监控")
    
    # 市场概览
    render_market_overview()
    
    # 热点板块
    render_hot_sectors()
    
    # 涨跌排行
    render_gainers_losers()
    
    # 市场情绪
    render_market_sentiment()

def render_market_overview():
    """渲染市场概览"""
    st.subheader("🌍 全球市场概览")
    
    # 主要指数
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="上证指数",
            value="3,245.67",
            delta="+1.23%",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="深证成指",
            value="12,456.89",
            delta="+0.87%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="纳斯达克",
            value="15,234.56",
            delta="-0.45%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="恒生指数",
            value="18,765.43",
            delta="+2.15%",
            delta_color="normal"
        )
    
    # 市场走势图
    st.markdown("##### 📈 今日走势")
    
    # 生成模拟数据
    times = pd.date_range(start='09:30', end='15:00', freq='5min')
    np.random.seed(42)
    
    fig = go.Figure()
    
    # 上证指数
    shanghai_data = 3200 + np.cumsum(np.random.normal(0, 5, len(times)))
    fig.add_trace(go.Scatter(
        x=times,
        y=shanghai_data,
        mode='lines',
        name='上证指数',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # 深证成指
    shenzhen_data = 12000 + np.cumsum(np.random.normal(0, 15, len(times)))
    fig.add_trace(go.Scatter(
        x=times,
        y=shenzhen_data,
        mode='lines',
        name='深证成指',
        line=dict(color='#ff7f0e', width=2),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="主要指数实时走势",
        xaxis_title="时间",
        yaxis=dict(title="上证指数", side="left"),
        yaxis2=dict(title="深证成指", side="right", overlaying="y"),
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_hot_sectors():
    """渲染热点板块"""
    st.subheader("🔥 热点板块")
    
    # 板块涨跌幅
    sector_data = pd.DataFrame({
        '板块': ['人工智能', '新能源汽车', '半导体', '生物医药', '军工', '消费电子', '房地产', '银行'],
        '涨跌幅': [8.5, 6.2, 4.8, 3.1, 2.7, 1.9, -1.2, -2.3],
        '成交额': [156.8, 234.5, 189.2, 98.7, 67.3, 145.6, 89.4, 234.1],
        '领涨股': ['科大讯飞', '比亚迪', '中芯国际', '恒瑞医药', '中航沈飞', '立讯精密', '万科A', '招商银行']
    })
    
    # 板块热力图
    fig = px.treemap(
        sector_data,
        path=['板块'],
        values='成交额',
        color='涨跌幅',
        color_continuous_scale='RdYlGn',
        title="板块成交额与涨跌幅热力图"
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # 板块详情表格
    st.markdown("##### 📋 板块详情")
    
    # 添加颜色格式化
    def color_negative_red(val):
        color = 'red' if val < 0 else 'green'
        return f'color: {color}'
    
    styled_df = sector_data.style.applymap(color_negative_red, subset=['涨跌幅'])
    st.dataframe(styled_df, use_container_width=True)

def render_gainers_losers():
    """渲染涨跌排行"""
    st.subheader("📊 涨跌排行")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🚀 涨幅榜")
        gainers_data = pd.DataFrame({
            '股票代码': ['300750', '002415', '000858', '600519', '000001'],
            '股票名称': ['宁德时代', '海康威视', '五粮液', '贵州茅台', '平安银行'],
            '现价': [245.67, 56.78, 189.34, 1678.90, 12.45],
            '涨跌幅': [10.01, 9.87, 8.56, 7.23, 6.78],
            '成交额': ['45.6亿', '23.4亿', '18.9亿', '67.8亿', '34.5亿']
        })
        
        st.dataframe(
            gainers_data,
            use_container_width=True,
            column_config={
                "涨跌幅": st.column_config.NumberColumn(
                    "涨跌幅(%)",
                    format="%.2f%%"
                ),
                "现价": st.column_config.NumberColumn(
                    "现价(¥)",
                    format="¥%.2f"
                )
            }
        )
    
    with col2:
        st.markdown("##### 📉 跌幅榜")
        losers_data = pd.DataFrame({
            '股票代码': ['002594', '300059', '000725', '600036', '002142'],
            '股票名称': ['比亚迪', '东方财富', '京东方A', '招商银行', '宁波银行'],
            '现价': [234.56, 23.45, 4.56, 45.67, 34.56],
            '涨跌幅': [-8.90, -7.65, -6.78, -5.43, -4.32],
            '成交额': ['78.9亿', '56.7亿', '23.4亿', '45.6亿', '12.3亿']
        })
        
        st.dataframe(
            losers_data,
            use_container_width=True,
            column_config={
                "涨跌幅": st.column_config.NumberColumn(
                    "涨跌幅(%)",
                    format="%.2f%%"
                ),
                "现价": st.column_config.NumberColumn(
                    "现价(¥)",
                    format="¥%.2f"
                )
            }
        )

def render_market_sentiment():
    """渲染市场情绪"""
    st.subheader("💭 市场情绪")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 情绪指标
        st.markdown("##### 📊 情绪指标")
        
        sentiment_metrics = {
            '恐慌贪婪指数': 65,
            'VIX恐慌指数': 18.5,
            '融资融券余额': 1.68,
            '北向资金净流入': 45.6
        }
        
        for metric, value in sentiment_metrics.items():
            if metric == '恐慌贪婪指数':
                if value > 75:
                    delta_color = "inverse"
                    delta = "极度贪婪"
                elif value > 55:
                    delta_color = "normal"
                    delta = "贪婪"
                elif value > 45:
                    delta_color = "off"
                    delta = "中性"
                else:
                    delta_color = "inverse"
                    delta = "恐慌"
                st.metric(metric, value, delta, delta_color=delta_color)
            elif metric == 'VIX恐慌指数':
                delta = "低波动" if value < 20 else "高波动"
                delta_color = "normal" if value < 20 else "inverse"
                st.metric(metric, value, delta, delta_color=delta_color)
            elif metric == '融资融券余额':
                st.metric(metric, f"{value}万亿", "历史高位")
            else:
                st.metric(metric, f"{value}亿", "净流入")
    
    with col2:
        # 资金流向
        st.markdown("##### 💰 资金流向")
        
        # 生成资金流向数据
        fund_flow_data = pd.DataFrame({
            '时间': pd.date_range(end=datetime.now(), periods=10, freq='D'),
            '主力净流入': np.random.normal(20, 30, 10),
            '散户净流入': np.random.normal(-15, 25, 10)
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=fund_flow_data['时间'],
            y=fund_flow_data['主力净流入'],
            name='主力资金',
            marker_color='red'
        ))
        
        fig.add_trace(go.Bar(
            x=fund_flow_data['时间'],
            y=fund_flow_data['散户净流入'],
            name='散户资金',
            marker_color='blue'
        ))
        
        fig.update_layout(
            title="近10日资金流向",
            xaxis_title="日期",
            yaxis_title="净流入(亿元)",
            barmode='group',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 新闻热点
    st.markdown("##### 📰 今日热点")
    
    news_data = [
        {
            'time': '14:30',
            'title': '央行宣布降准0.25个百分点，释放流动性约5000亿元',
            'impact': '利好',
            'sectors': ['银行', '地产', '基建']
        },
        {
            'time': '13:15',
            'title': '工信部发布新能源汽车产业发展规划，2030年销量占比达40%',
            'impact': '利好',
            'sectors': ['新能源汽车', '锂电池', '充电桩']
        },
        {
            'time': '11:45',
            'title': '美联储官员暗示可能暂停加息，美股期货大涨',
            'impact': '利好',
            'sectors': ['科技股', '成长股']
        },
        {
            'time': '10:20',
            'title': '某芯片公司因技术泄露被调查，半导体板块承压',
            'impact': '利空',
            'sectors': ['半导体', '芯片设计']
        }
    ]
    
    for news in news_data:
        with st.container():
            col_time, col_content, col_impact = st.columns([1, 6, 1])
            
            with col_time:
                st.write(f"**{news['time']}**")
            
            with col_content:
                st.write(news['title'])
                st.caption(f"相关板块: {', '.join(news['sectors'])}")
            
            with col_impact:
                if news['impact'] == '利好':
                    st.success(news['impact'])
                else:
                    st.error(news['impact'])
            
            st.divider()

def get_market_data():
    """获取市场数据"""
    # 这里应该从真实的数据源获取数据
    # 目前返回模拟数据
    pass

def get_sector_data():
    """获取板块数据"""
    # 这里应该从真实的数据源获取数据
    pass

def get_news_data():
    """获取新闻数据"""
    # 这里应该从新闻API获取数据
    pass