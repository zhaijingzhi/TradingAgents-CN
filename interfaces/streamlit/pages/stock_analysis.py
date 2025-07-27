"""
股票分析页面 - 专门的分析功能页面
"""

import streamlit as st
import datetime
import time
import uuid
from interfaces.streamlit.components.analysis_form import render_analysis_form
from interfaces.streamlit.components.async_progress_display import display_unified_progress
from interfaces.streamlit.components.results_display import render_results
from interfaces.streamlit.utils.analysis_runner import run_stock_analysis, validate_analysis_params, format_analysis_results
from interfaces.streamlit.utils.async_progress_tracker import AsyncProgressTracker
from interfaces.streamlit.utils.smart_session_manager import set_persistent_analysis_id

# 导入日志模块
from tradingagents.utils.logging_manager import get_logger
logger = get_logger('web')

def show_stock_analysis():
    """显示股票分析页面"""
    st.title("📈 股票分析")
    
    # 分析向导
    render_analysis_wizard()
    
    # 分析配置区域
    render_analysis_configuration()
    
    # 分析进度和结果
    render_analysis_progress_and_results()

def render_analysis_wizard():
    """渲染分析向导"""
    st.subheader("🧭 分析向导")
    
    with st.expander("📋 如何开始分析", expanded=False):
        st.markdown("""
        ### 🚀 快速开始指南
        
        1. **选择市场**: 选择要分析的股票市场（美股/A股/港股）
        2. **输入代码**: 输入股票代码（如 AAPL, 000001, 0700.HK）
        3. **选择分析师**: 选择参与分析的AI分析师类型
        4. **设置深度**: 选择分析的详细程度（1-5级）
        5. **开始分析**: 点击分析按钮，等待结果
        
        ### 💡 分析师说明
        - **📈 市场技术分析师**: 专注技术指标和图表分析
        - **💰 基本面分析师**: 分析财务数据和公司基本面
        - **📰 新闻分析师**: 评估新闻事件对股价的影响
        - **💭 社交媒体分析师**: 分析投资者情绪和讨论热度
        
        ### ⏱️ 预计时间
        - **1-2级**: 2-4分钟（快速分析）
        - **3级**: 4-8分钟（标准分析）
        - **4-5级**: 8-15分钟（深度分析）
        """)

def render_analysis_configuration():
    """渲染分析配置区域"""
    st.subheader("⚙️ 分析配置")
    
    # 检查是否有正在运行的分析
    if st.session_state.get('analysis_running', False):
        st.warning("⚠️ 当前有分析正在进行中，请等待完成后再开始新的分析")
        return
    
    # 渲染分析表单
    form_data = render_analysis_form()
    
    # 处理表单提交
    if form_data.get('submitted', False):
        handle_analysis_submission(form_data)

def handle_analysis_submission(form_data):
    """处理分析提交"""
    # 验证分析参数
    is_valid, validation_errors = validate_analysis_params(
        stock_symbol=form_data['stock_symbol'],
        analysis_date=form_data['analysis_date'],
        analysts=form_data['analysts'],
        research_depth=form_data['research_depth'],
        market_type=form_data.get('market_type', '美股')
    )
    
    if not is_valid:
        for error in validation_errors:
            st.error(error)
        return
    
    # 开始分析
    start_analysis(form_data)

def start_analysis(form_data):
    """启动分析"""
    # 设置分析状态
    st.session_state.analysis_running = True
    st.session_state.analysis_results = None
    
    # 生成分析ID
    analysis_id = f"analysis_{uuid.uuid4().hex[:8]}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # 从session state获取侧边栏配置，避免重复调用render_sidebar
    config = st.session_state.get('sidebar_config', {
        'llm_provider': 'dashscope',
        'llm_model': 'qwen-plus-latest',
        'enable_memory': False,
        'enable_debug': False,
        'max_tokens': 4000
    })
    
    # 保存分析ID和配置
    form_config = st.session_state.get('form_config', {})
    set_persistent_analysis_id(
        analysis_id=analysis_id,
        status="running",
        stock_symbol=form_data['stock_symbol'],
        market_type=form_data.get('market_type', '美股'),
        form_config=form_config
    )
    
    # 创建异步进度跟踪器
    async_tracker = AsyncProgressTracker(
        analysis_id=analysis_id,
        analysts=form_data['analysts'],
        research_depth=form_data['research_depth'],
        llm_provider=config['llm_provider']
    )
    
    # 创建进度回调函数
    def progress_callback(message: str, step: int = None, total_steps: int = None):
        async_tracker.update_progress(message, step)
    
    # 显示启动信息
    st.success(f"🚀 分析已启动！分析ID: {analysis_id}")
    st.info(f"📊 正在分析: {form_data.get('market_type', '美股')} {form_data['stock_symbol']}")
    
    # 设置session state
    st.session_state.analysis_running = True
    st.session_state.current_analysis_id = analysis_id
    st.session_state.last_stock_symbol = form_data['stock_symbol']
    st.session_state.last_market_type = form_data.get('market_type', '美股')
    
    # 启动后台分析
    import threading
    
    def run_analysis_in_background():
        try:
            results = run_stock_analysis(
                stock_symbol=form_data['stock_symbol'],
                analysis_date=form_data['analysis_date'],
                analysts=form_data['analysts'],
                research_depth=form_data['research_depth'],
                llm_provider=config['llm_provider'],
                market_type=form_data.get('market_type', '美股'),
                llm_model=config['llm_model'],
                progress_callback=progress_callback
            )
            
            if results and results.get('success', False):
                async_tracker.mark_completed("✅ 分析成功完成！", results=results)
            else:
                error_msg = results.get('error', '未知错误') if results else '分析返回空结果'
                async_tracker.mark_failed(error_msg)
                
        except Exception as e:
            async_tracker.mark_failed(str(e))
            logger.error(f"❌ [分析失败] {analysis_id}: {e}")
        
        finally:
            from interfaces.streamlit.utils.thread_tracker import unregister_analysis_thread
            unregister_analysis_thread(analysis_id)
    
    # 启动分析线程
    analysis_thread = threading.Thread(target=run_analysis_in_background)
    analysis_thread.daemon = True
    analysis_thread.start()
    
    # 注册线程
    from interfaces.streamlit.utils.thread_tracker import register_analysis_thread
    register_analysis_thread(analysis_id, analysis_thread)
    
    logger.info(f"🧵 [后台分析] 分析线程已启动: {analysis_id}")
    
    # 刷新页面显示进度
    time.sleep(2)
    st.rerun()

def render_analysis_progress_and_results():
    """渲染分析进度和结果"""
    current_analysis_id = st.session_state.get('current_analysis_id')
    
    if not current_analysis_id:
        st.info("👆 请在上方配置分析参数并开始分析")
        return
    
    st.markdown("---")
    st.subheader("📊 分析进度")
    
    # 检查分析状态
    from interfaces.streamlit.utils.thread_tracker import check_analysis_status
    actual_status = check_analysis_status(current_analysis_id)
    is_running = (actual_status == 'running')
    
    # 同步状态
    if st.session_state.get('analysis_running', False) != is_running:
        st.session_state.analysis_running = is_running
    
    # 显示分析信息
    if is_running:
        st.info(f"🔄 正在分析: {current_analysis_id}")
    else:
        if actual_status == 'completed':
            st.success(f"✅ 分析完成: {current_analysis_id}")
        elif actual_status == 'failed':
            st.error(f"❌ 分析失败: {current_analysis_id}")
        else:
            st.warning(f"⚠️ 分析状态未知: {current_analysis_id}")
    
    # 显示进度
    is_completed = display_unified_progress(current_analysis_id, show_refresh_controls=is_running)
    
    # 显示结果
    if is_completed and st.session_state.get('analysis_results'):
        st.markdown("---")
        st.subheader("📋 分析结果")
        render_results(st.session_state.analysis_results)
    elif is_completed:
        # 尝试恢复结果
        try:
            from interfaces.streamlit.utils.async_progress_tracker import get_progress_by_id
            progress_data = get_progress_by_id(current_analysis_id)
            if progress_data and 'raw_results' in progress_data:
                raw_results = progress_data['raw_results']
                formatted_results = format_analysis_results(raw_results)
                if formatted_results:
                    st.session_state.analysis_results = formatted_results
                    st.rerun()
        except Exception as e:
            logger.error(f"结果恢复失败: {e}")
            st.error("分析已完成，但结果恢复失败。请重新开始分析。")

def render_analysis_templates():
    """渲染分析模板"""
    st.subheader("📋 分析模板")
    
    templates = {
        "快速分析": {
            "description": "适合日常监控，2-4分钟完成",
            "analysts": ["market", "technical"],
            "research_depth": 1
        },
        "标准分析": {
            "description": "平衡速度和深度，4-8分钟完成",
            "analysts": ["market", "technical", "fundamentals"],
            "research_depth": 3
        },
        "全面分析": {
            "description": "最详细的分析，8-15分钟完成",
            "analysts": ["market", "technical", "fundamentals", "sentiment"],
            "research_depth": 5
        }
    }
    
    col1, col2, col3 = st.columns(3)
    
    for idx, (name, template) in enumerate(templates.items()):
        col = [col1, col2, col3][idx]
        with col:
            with st.container():
                st.markdown(f"**{name}**")
                st.caption(template["description"])
                if st.button(f"使用 {name}", key=f"template_{idx}", use_container_width=True):
                    # 应用模板配置
                    st.session_state.template_analysts = template["analysts"]
                    st.session_state.template_depth = template["research_depth"]
                    st.success(f"已应用 {name} 模板")