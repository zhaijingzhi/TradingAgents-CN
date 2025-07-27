"""
投资组合管理页面 - 管理和跟踪投资组合
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_portfolio_management():
    """显示投资组合管理页面"""
    st.title("💼 投资组合管理")
    
    # 投资组合概览
    render_portfolio_overview()
    
    # 持仓管理
    render_holdings_management()
    
    # 组合分析
    render_portfolio_analysis()
    
    # 风险管理
    render_risk_management()

def render_portfolio_overview():
    """渲染投资组合概览"""
    st.subheader("📊 组合概览")
    
    # 获取组合数据
    portfolio_data = get_portfolio_data()
    
    if not portfolio_data:
        st.info("📭 您还没有创建投资组合，点击下方按钮开始创建")
        if st.button("➕ 创建新组合", type="primary"):
            show_create_portfolio_dialog()
        return
    
    # 组合选择器
    portfolio_names = list(portfolio_data.keys())
    selected_portfolio = st.selectbox(
        "选择投资组合",
        options=portfolio_names,
        help="选择要查看的投资组合"
    )
    
    current_portfolio = portfolio_data[selected_portfolio]
    
    # 组合指标
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="总市值",
            value=f"¥{current_portfolio['total_value']:,.2f}",
            delta=f"{current_portfolio['daily_change']:+.2f}%"
        )
    
    with col2:
        st.metric(
            label="总收益",
            value=f"¥{current_portfolio['total_profit']:,.2f}",
            delta=f"{current_portfolio['total_return']:+.2f}%"
        )
    
    with col3:
        st.metric(
            label="持仓数量",
            value=f"{current_portfolio['holdings_count']}只",
            delta=f"活跃: {current_portfolio['active_holdings']}"
        )
    
    with col4:
        st.metric(
            label="风险等级",
            value=current_portfolio['risk_level'],
            delta=current_portfolio['risk_score']
        )

def render_holdings_management():
    """渲染持仓管理"""
    st.subheader("📈 持仓管理")
    
    # 操作按钮
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ 添加持仓", use_container_width=True):
            show_add_holding_dialog()
    
    with col2:
        if st.button("📊 批量分析", use_container_width=True):
            show_batch_analysis_dialog()
    
    with col3:
        if st.button("📤 导出持仓", use_container_width=True):
            export_holdings()
    
    # 持仓列表
    holdings_data = get_holdings_data()
    
    if not holdings_data:
        st.info("当前组合没有持仓")
        return
    
    # 持仓表格
    df = pd.DataFrame(holdings_data)
    
    # 自定义列显示
    columns_config = {
        "stock_symbol": st.column_config.TextColumn("股票代码", width="small"),
        "stock_name": st.column_config.TextColumn("股票名称", width="medium"),
        "quantity": st.column_config.NumberColumn("持仓数量", format="%d"),
        "avg_cost": st.column_config.NumberColumn("平均成本", format="¥%.2f"),
        "current_price": st.column_config.NumberColumn("当前价格", format="¥%.2f"),
        "market_value": st.column_config.NumberColumn("市值", format="¥%.2f"),
        "profit_loss": st.column_config.NumberColumn("盈亏", format="¥%.2f"),
        "return_rate": st.column_config.NumberColumn("收益率", format="%.2f%%"),
        "weight": st.column_config.ProgressColumn("权重", min_value=0, max_value=100),
        "last_analysis": st.column_config.DateColumn("最后分析"),
        "recommendation": st.column_config.TextColumn("建议", width="small")
    }
    
    # 可编辑表格
    edited_df = st.data_editor(
        df,
        column_config=columns_config,
        use_container_width=True,
        num_rows="dynamic",
        key="holdings_editor"
    )
    
    # 保存更改
    if st.button("💾 保存更改"):
        save_holdings_changes(edited_df)
        st.success("持仓信息已更新")

def render_portfolio_analysis():
    """渲染组合分析"""
    st.subheader("📊 组合分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 资产配置饼图
        st.markdown("##### 🥧 资产配置")
        allocation_data = get_asset_allocation()
        if allocation_data is not None and not allocation_data.empty:
            fig = px.pie(
                allocation_data,
                values='weight',
                names='category',
                title="按行业分布",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 收益率分布
        st.markdown("##### 📈 收益率分布")
        return_data = get_return_distribution()
        if return_data is not None and not return_data.empty:
            fig = px.histogram(
                return_data,
                x='return_rate',
                nbins=20,
                title="持仓收益率分布",
                color_discrete_sequence=['#1f77b4']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # 组合表现趋势
    st.markdown("##### 📊 组合表现趋势")
    performance_data = get_portfolio_performance()
    if performance_data is not None and not performance_data.empty:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=performance_data['date'],
            y=performance_data['portfolio_value'],
            mode='lines',
            name='组合价值',
            line=dict(color='#1f77b4', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=performance_data['date'],
            y=performance_data['benchmark'],
            mode='lines',
            name='基准指数',
            line=dict(color='#ff7f0e', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="组合价值 vs 基准指数",
            xaxis_title="日期",
            yaxis_title="价值",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def render_risk_management():
    """渲染风险管理"""
    st.subheader("⚠️ 风险管理")
    
    # 风险指标
    risk_metrics = get_risk_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="波动率",
            value=f"{risk_metrics['volatility']:.2f}%",
            delta="年化" if risk_metrics['volatility'] < 20 else "偏高",
            delta_color="normal" if risk_metrics['volatility'] < 20 else "inverse"
        )
    
    with col2:
        st.metric(
            label="最大回撤",
            value=f"{risk_metrics['max_drawdown']:.2f}%",
            delta="可接受" if risk_metrics['max_drawdown'] > -10 else "需关注",
            delta_color="normal" if risk_metrics['max_drawdown'] > -10 else "inverse"
        )
    
    with col3:
        st.metric(
            label="夏普比率",
            value=f"{risk_metrics['sharpe_ratio']:.2f}",
            delta="优秀" if risk_metrics['sharpe_ratio'] > 1 else "一般",
            delta_color="normal" if risk_metrics['sharpe_ratio'] > 1 else "inverse"
        )
    
    with col4:
        st.metric(
            label="Beta系数",
            value=f"{risk_metrics['beta']:.2f}",
            delta="稳健" if abs(risk_metrics['beta'] - 1) < 0.2 else "波动",
            delta_color="normal" if abs(risk_metrics['beta'] - 1) < 0.2 else "inverse"
        )
    
    # 风险提示
    risk_alerts = get_risk_alerts()
    if risk_alerts:
        st.markdown("##### ⚠️ 风险提示")
        for alert in risk_alerts:
            if alert['level'] == 'high':
                st.error(f"🔴 {alert['message']}")
            elif alert['level'] == 'medium':
                st.warning(f"🟡 {alert['message']}")
            else:
                st.info(f"🔵 {alert['message']}")

def show_create_portfolio_dialog():
    """显示创建投资组合对话框"""
    with st.form("create_portfolio"):
        st.subheader("➕ 创建新投资组合")
        
        portfolio_name = st.text_input("组合名称", placeholder="例如：成长型组合")
        portfolio_desc = st.text_area("组合描述", placeholder="描述投资策略和目标")
        
        col1, col2 = st.columns(2)
        with col1:
            risk_tolerance = st.selectbox("风险承受能力", ["保守", "稳健", "积极", "激进"])
        with col2:
            investment_goal = st.selectbox("投资目标", ["保值", "稳定增长", "快速增长", "投机"])
        
        if st.form_submit_button("创建组合", type="primary"):
            create_portfolio(portfolio_name, portfolio_desc, risk_tolerance, investment_goal)
            st.success(f"投资组合 '{portfolio_name}' 创建成功！")
            st.rerun()

def show_add_holding_dialog():
    """显示添加持仓对话框"""
    with st.form("add_holding"):
        st.subheader("➕ 添加持仓")
        
        col1, col2 = st.columns(2)
        with col1:
            stock_symbol = st.text_input("股票代码", placeholder="例如：AAPL")
            quantity = st.number_input("持仓数量", min_value=1, value=100)
        
        with col2:
            avg_cost = st.number_input("平均成本", min_value=0.01, value=100.0, format="%.2f")
            purchase_date = st.date_input("购买日期", value=datetime.now())
        
        notes = st.text_area("备注", placeholder="购买理由或其他备注")
        
        if st.form_submit_button("添加持仓", type="primary"):
            add_holding(stock_symbol, quantity, avg_cost, purchase_date, notes)
            st.success(f"已添加 {stock_symbol} 到投资组合")
            st.rerun()

def show_batch_analysis_dialog():
    """显示批量分析对话框"""
    st.subheader("📊 批量分析持仓")
    
    holdings = get_holdings_data()
    if not holdings:
        st.warning("当前组合没有持仓")
        return
    
    # 选择要分析的股票
    selected_stocks = st.multiselect(
        "选择要分析的股票",
        options=[h['stock_symbol'] for h in holdings],
        default=[h['stock_symbol'] for h in holdings[:3]]  # 默认选择前3个
    )
    
    analysis_depth = st.select_slider(
        "分析深度",
        options=[1, 2, 3, 4, 5],
        value=3,
        format_func=lambda x: f"级别 {x}"
    )
    
    if st.button("🚀 开始批量分析", type="primary"):
        start_batch_analysis(selected_stocks, analysis_depth)

# 数据获取函数（模拟数据）
def get_portfolio_data():
    """获取投资组合数据"""
    return {
        "我的组合": {
            "total_value": 125000.00,
            "daily_change": 2.35,
            "total_profit": 25000.00,
            "total_return": 25.0,
            "holdings_count": 8,
            "active_holdings": 6,
            "risk_level": "稳健",
            "risk_score": "B+"
        }
    }

def get_holdings_data():
    """获取持仓数据"""
    return [
        {
            "stock_symbol": "AAPL",
            "stock_name": "苹果公司",
            "quantity": 100,
            "avg_cost": 150.00,
            "current_price": 175.50,
            "market_value": 17550.00,
            "profit_loss": 2550.00,
            "return_rate": 17.0,
            "weight": 25.5,
            "last_analysis": datetime.now() - timedelta(days=2),
            "recommendation": "HOLD"
        },
        {
            "stock_symbol": "TSLA",
            "stock_name": "特斯拉",
            "quantity": 50,
            "avg_cost": 200.00,
            "current_price": 180.00,
            "market_value": 9000.00,
            "profit_loss": -1000.00,
            "return_rate": -10.0,
            "weight": 13.1,
            "last_analysis": datetime.now() - timedelta(days=5),
            "recommendation": "SELL"
        }
    ]

def get_asset_allocation():
    """获取资产配置数据"""
    return pd.DataFrame({
        'category': ['科技', '金融', '消费', '医疗', '能源'],
        'weight': [40, 25, 15, 12, 8]
    })

def get_return_distribution():
    """获取收益率分布数据"""
    import numpy as np
    np.random.seed(42)
    return pd.DataFrame({
        'return_rate': np.random.normal(5, 15, 100)
    })

def get_portfolio_performance():
    """获取组合表现数据"""
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    np.random.seed(42)
    portfolio_values = 100000 + np.cumsum(np.random.normal(100, 500, 30))
    benchmark_values = 100000 + np.cumsum(np.random.normal(50, 300, 30))
    
    return pd.DataFrame({
        'date': dates,
        'portfolio_value': portfolio_values,
        'benchmark': benchmark_values
    })

def get_risk_metrics():
    """获取风险指标"""
    return {
        'volatility': 18.5,
        'max_drawdown': -8.2,
        'sharpe_ratio': 1.25,
        'beta': 1.15
    }

def get_risk_alerts():
    """获取风险提示"""
    return [
        {
            'level': 'medium',
            'message': 'TSLA持仓亏损超过10%，建议关注'
        },
        {
            'level': 'low',
            'message': '科技股权重较高，建议适当分散'
        }
    ]

# 操作函数
def create_portfolio(name, desc, risk_tolerance, investment_goal):
    """创建投资组合"""
    # 这里应该保存到数据库
    pass

def add_holding(symbol, quantity, cost, date, notes):
    """添加持仓"""
    # 这里应该保存到数据库
    pass

def save_holdings_changes(df):
    """保存持仓更改"""
    # 这里应该更新数据库
    pass

def start_batch_analysis(stocks, depth):
    """开始批量分析"""
    st.info(f"正在分析 {len(stocks)} 只股票，分析深度：{depth}级")
    # 这里应该启动批量分析任务

def export_holdings():
    """导出持仓"""
    st.success("持仓数据已导出到 portfolio_holdings.xlsx")