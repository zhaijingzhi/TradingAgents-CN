"""
分析历史页面 - 查看和管理历史分析记录
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

def show_analysis_history():
    """显示分析历史页面"""
    st.title("📈 分析历史")
    
    # 检查是否要显示详情页面
    if 'selected_history_record' in st.session_state and st.session_state.selected_history_record:
        show_analysis_detail(st.session_state.selected_history_record)
    else:
        # 历史记录筛选器
        render_history_filters()
        
        # 历史记录列表
        render_history_list()
        
        # 历史统计
        render_history_statistics()

def render_history_filters():
    """渲染历史记录筛选器"""
    st.subheader("🔍 筛选条件")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        date_range = st.date_input(
            "日期范围",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            help="选择要查看的日期范围"
        )
    
    with col2:
        market_filter = st.selectbox(
            "市场类型",
            options=["全部", "美股", "A股", "港股"],
            help="筛选特定市场的分析记录"
        )
    
    with col3:
        status_filter = st.selectbox(
            "分析状态",
            options=["全部", "已完成", "失败", "进行中"],
            help="筛选特定状态的分析记录"
        )
    
    with col4:
        model_filter = st.selectbox(
            "使用模型",
            options=["全部", "阿里百炼", "DeepSeek V3", "Google AI"],
            help="筛选使用特定模型的分析记录"
        )
    
    # 应用筛选条件
    st.session_state.history_filters = {
        'date_range': date_range,
        'market': market_filter,
        'status': status_filter,
        'model': model_filter
    }

def render_history_list():
    """渲染历史记录列表"""
    st.subheader("📋 分析记录")
    
    # 获取筛选后的历史记录
    history_data = get_filtered_history()
    
    if not history_data:
        st.info("📭 没有找到符合条件的分析记录")
        return
    
    # 分页显示
    page_size = 10
    total_pages = (len(history_data) - 1) // page_size + 1
    
    if total_pages > 1:
        page = st.selectbox("页码", range(1, total_pages + 1), key="history_page")
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_data = history_data[start_idx:end_idx]
    else:
        page_data = history_data
    
    # 显示记录
    for idx, record in enumerate(page_data):
        render_history_record(record, idx)

def render_history_record(record, idx):
    """渲染单个历史记录"""
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
        
        with col1:
            # 状态图标和股票信息
            status_icons = {
                'completed': '✅',
                'failed': '❌',
                'running': '🔄'
            }
            icon = status_icons.get(record['status'], '❓')
            st.write(f"{icon} **{record['stock_symbol']}**")
            st.caption(f"{record['market_type']}")
        
        with col2:
            st.write(f"📅 {record['date']}")
            st.caption(f"⏱️ {record['duration']}")
        
        with col3:
            if record['status'] == 'completed':
                st.write(f"🎯 {record['recommendation']}")
                st.caption(f"置信度: {record['confidence']}")
            else:
                st.write("分析未完成")
                st.caption(record.get('error_msg', ''))
        
        with col4:
            st.write(f"🤖 {record['model']}")
            st.caption(f"分析师: {record['analysts_count']}个")
        
        with col5:
            if st.button("查看", key=f"view_history_{idx}", use_container_width=True):
                st.session_state.selected_history_record = record
                st.rerun()
        
        st.divider()

def show_analysis_detail(record):
    """显示分析详情"""
    # 添加返回按钮
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← 返回列表", use_container_width=True):
            st.session_state.selected_history_record = None
            st.rerun()
    
    st.subheader(f"📊 {record['stock_symbol']} 分析详情")
    
    # 基本信息
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("股票代码", record['stock_symbol'])
        st.metric("市场类型", record['market_type'])
    
    with col2:
        st.metric("分析日期", record['date'])
        st.metric("分析时长", record['duration'])
    
    with col3:
        st.metric("使用模型", record['model'])
        st.metric("分析师数量", f"{record['analysts_count']}个")
    
    # 分析结果
    if record['status'] == 'completed':
        st.subheader("📋 分析结果")
        
        # 投资建议
        recommendation_color = {
            'BUY': 'green',
            'SELL': 'red',
            'HOLD': 'orange'
        }.get(record['recommendation'], 'gray')
        
        st.markdown(f"""
        <div style="padding: 1rem; border-radius: 0.5rem; background-color: {recommendation_color}20; border-left: 4px solid {recommendation_color};">
            <h4 style="color: {recommendation_color}; margin: 0;">投资建议: {record['recommendation']}</h4>
            <p style="margin: 0.5rem 0 0 0;">置信度: {record['confidence']} | 风险评分: {record.get('risk_score', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 详细分析报告
        if record.get('detailed_analysis'):
            with st.expander("📄 详细分析报告", expanded=False):
                st.markdown(record['detailed_analysis'])
        
        # 导出选项
        st.subheader("📤 导出选项")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("导出为 Markdown", use_container_width=True):
                export_analysis_report(record, 'markdown')
        
        with col2:
            if st.button("导出为 Word", use_container_width=True):
                export_analysis_report(record, 'word')
        
        with col3:
            if st.button("导出为 PDF", use_container_width=True):
                export_analysis_report(record, 'pdf')
    
    else:
        st.error(f"分析状态: {record['status']}")
        if record.get('error_msg'):
            st.error(f"错误信息: {record['error_msg']}")

def render_history_statistics():
    """渲染历史统计"""
    st.subheader("📊 统计分析")
    
    # 获取统计数据
    stats_data = get_history_statistics()
    
    if not stats_data:
        st.info("暂无统计数据")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 分析次数趋势
        st.markdown("##### 📈 分析次数趋势")
        trend_data = stats_data.get('trend_data')
        if trend_data is not None and not trend_data.empty:
            fig = px.line(
                trend_data,
                x='date',
                y='count',
                title="每日分析次数",
                markers=True
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 投资建议分布
        st.markdown("##### 🎯 投资建议分布")
        recommendation_data = stats_data.get('recommendation_data')
        if recommendation_data is not None and not recommendation_data.empty:
            fig = px.pie(
                recommendation_data,
                values='count',
                names='recommendation',
                title="投资建议分布",
                color_discrete_map={
                    'BUY': 'green',
                    'SELL': 'red',
                    'HOLD': 'orange'
                }
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    # 成功率统计
    col3, col4 = st.columns(2)
    
    with col3:
        # 模型使用分布
        st.markdown("##### 🤖 模型使用分布")
        model_data = stats_data.get('model_data')
        if model_data is not None and not model_data.empty:
            fig = px.bar(
                model_data,
                x='model',
                y='count',
                title="模型使用次数"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        # 市场分布
        st.markdown("##### 🌍 市场分析分布")
        market_data = stats_data.get('market_data')
        if market_data is not None and not market_data.empty:
            fig = px.bar(
                market_data,
                x='market',
                y='count',
                title="市场分析次数"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

def get_filtered_history():
    """获取筛选后的历史记录"""
    filters = st.session_state.get('history_filters', {})
    
    try:
        # 尝试从Redis获取真实的分析历史数据
        from interfaces.streamlit.utils.async_progress_tracker import get_all_analysis_history
        real_history = get_all_analysis_history()
        
        if real_history:
            # 转换真实数据格式
            formatted_history = []
            for analysis_id, data in real_history.items():
                # 解析分析结果
                raw_results = data.get('raw_results', {})
                decision = raw_results.get('decision', {}) if raw_results else {}
                
                # 从多个位置获取股票代码
                stock_symbol = (
                    data.get('stock_symbol') or 
                    raw_results.get('stock_symbol') or 
                    'N/A'
                )
                
                # 从分析ID中提取时间戳
                import re
                timestamp_match = re.search(r'(\d{8}_\d{6})$', analysis_id)
                if timestamp_match:
                    timestamp_str = timestamp_match.group(1)
                    try:
                        from datetime import datetime
                        parsed_time = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                        formatted_date = parsed_time.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        formatted_date = timestamp_str
                else:
                    formatted_date = data.get('timestamp', '未知时间')
                
                # 确定市场类型
                market_type = data.get('market_type', '未知')
                if market_type == '未知' and stock_symbol != 'N/A':
                    # 根据股票代码推断市场类型
                    if stock_symbol.isdigit():
                        if len(stock_symbol) == 6:
                            if stock_symbol.startswith(('00', '30')):
                                market_type = 'A股'
                            elif stock_symbol.startswith('51'):
                                market_type = 'A股ETF'
                        elif len(stock_symbol) == 5:
                            market_type = '港股'
                    else:
                        market_type = '美股'
                
                # 格式化记录
                record = {
                    'id': analysis_id,
                    'stock_symbol': stock_symbol,
                    'market_type': market_type,
                    'date': formatted_date,
                    'duration': calculate_duration(data.get('start_time'), data.get('end_time')),
                    'status': data.get('status', 'unknown'),
                    'recommendation': decision.get('action', 'N/A'),
                    'confidence': f"{decision.get('confidence', 0)*100:.0f}%" if isinstance(decision.get('confidence'), (int, float)) else 'N/A',
                    'risk_score': decision.get('risk_score', 'N/A'),
                    'model': format_model_name(
                        data.get('llm_provider') or 
                        raw_results.get('llm_provider') or 
                        'unknown'
                    ),
                    'analysts_count': len(
                        data.get('analysts', []) or 
                        raw_results.get('analysts', [])
                    ),
                    'detailed_analysis': format_detailed_analysis(raw_results)
                }
                
                # 只添加有效的记录（至少有股票代码）
                if stock_symbol != 'N/A':
                    formatted_history.append(record)
            
            # 应用筛选条件
            filtered_history = apply_filters(formatted_history, filters)
            
            if filtered_history:
                return filtered_history
    
    except Exception as e:
        st.warning(f"获取历史数据时出错: {e}")
    
    # 如果没有真实数据或出错，返回模拟数据作为示例
    sample_data = [
        {
            'id': 'demo_analysis_001',
            'stock_symbol': 'AAPL',
            'market_type': '美股',
            'date': '2024-01-15 14:30:00',
            'duration': '5分32秒',
            'status': 'completed',
            'recommendation': 'BUY',
            'confidence': '85%',
            'risk_score': '中等',
            'model': '阿里百炼',
            'analysts_count': 4,
            'detailed_analysis': '# 苹果公司分析报告\n\n## 技术分析\n这是一个演示分析报告...'
        },
        {
            'id': 'demo_analysis_002',
            'stock_symbol': '000001',
            'market_type': 'A股',
            'date': '2024-01-14 10:15:00',
            'duration': '3分18秒',
            'status': 'completed',
            'recommendation': 'HOLD',
            'confidence': '72%',
            'risk_score': '低',
            'model': 'DeepSeek V3',
            'analysts_count': 3,
            'detailed_analysis': '# 平安银行分析报告\n\n## 基本面分析\n这是一个演示分析报告...'
        }
    ]
    
    return apply_filters(sample_data, filters)

def calculate_duration(start_time, end_time):
    """计算分析持续时间"""
    if not start_time or not end_time:
        return "未知"
    
    try:
        from datetime import datetime
        if isinstance(start_time, str):
            start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        else:
            start = start_time
            
        if isinstance(end_time, str):
            end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        else:
            end = end_time
            
        duration = end - start
        total_seconds = int(duration.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        
        return f"{minutes}分{seconds}秒"
    except:
        return "未知"

def format_model_name(llm_provider):
    """格式化模型名称"""
    model_names = {
        'dashscope': '阿里百炼',
        'deepseek': 'DeepSeek V3',
        'google': 'Google AI',
        'anthropic': 'Claude',
        'openai': 'OpenAI'
    }
    return model_names.get(llm_provider, llm_provider)

def format_detailed_analysis(raw_results):
    """格式化详细分析内容"""
    if not raw_results:
        return "# 分析报告\n\n暂无详细分析内容"
    
    # 尝试从结果中提取分析内容
    state = raw_results.get('state', {})
    if state:
        analysis_parts = []
        
        # 添加各个分析模块
        for key, content in state.items():
            if content and isinstance(content, str):
                analysis_parts.append(content)
        
        if analysis_parts:
            return "\n\n".join(analysis_parts)
    
    return "# 分析报告\n\n分析已完成，但详细内容格式化失败"

def apply_filters(data, filters):
    """应用筛选条件"""
    if not filters:
        return data
    
    filtered_data = data
    
    # 市场类型筛选
    market_filter = filters.get('market', '全部')
    if market_filter != '全部':
        filtered_data = [item for item in filtered_data if item['market_type'] == market_filter]
    
    # 状态筛选
    status_filter = filters.get('status', '全部')
    if status_filter != '全部':
        status_mapping = {
            '已完成': 'completed',
            '失败': 'failed',
            '进行中': 'running'
        }
        target_status = status_mapping.get(status_filter, status_filter)
        filtered_data = [item for item in filtered_data if item['status'] == target_status]
    
    # 模型筛选
    model_filter = filters.get('model', '全部')
    if model_filter != '全部':
        filtered_data = [item for item in filtered_data if item['model'] == model_filter]
    
    return filtered_data

def get_history_statistics():
    """获取历史统计数据"""
    # 模拟统计数据
    return {
        'trend_data': pd.DataFrame({
            'date': pd.date_range(end=datetime.now(), periods=7, freq='D'),
            'count': [2, 5, 3, 8, 6, 4, 7]
        }),
        'recommendation_data': pd.DataFrame({
            'recommendation': ['BUY', 'HOLD', 'SELL'],
            'count': [15, 8, 3]
        }),
        'model_data': pd.DataFrame({
            'model': ['阿里百炼', 'DeepSeek V3', 'Google AI'],
            'count': [12, 8, 6]
        }),
        'market_data': pd.DataFrame({
            'market': ['美股', 'A股', '港股'],
            'count': [15, 8, 3]
        })
    }

def export_analysis_report(record, format_type):
    """导出分析报告"""
    st.success(f"正在导出 {record['stock_symbol']} 的分析报告为 {format_type.upper()} 格式...")
    # 这里应该实现真实的导出功能