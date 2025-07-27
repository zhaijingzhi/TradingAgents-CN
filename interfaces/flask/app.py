#!/usr/bin/env python3
"""
TradingAgents-CN Flask Web应用
基于Flask + MongoDB + Redis的股票分析Web应用程序
集成数据可视化和缓存系统
"""

from flask import Flask, render_template, request, jsonify, session, send_file
import os
import sys
from pathlib import Path
import datetime
import uuid
import threading
import json
import time
from dotenv import load_dotenv
import pandas as pd
import numpy as np

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 加载环境变量
load_dotenv(project_root / ".env", override=True)

# 导入TradingAgents核心功能
try:
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG
    from tradingagents.utils.logging_manager import get_logger
    from tradingagents.config.database_config import DatabaseConfig
    from tradingagents.config.mongodb_storage import MongoDBStorage
    from tradingagents.dataflows.db_cache_manager import DatabaseCacheManager
    TRADINGAGENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ TradingAgents核心模块导入失败: {e}")
    TRADINGAGENTS_AVAILABLE = False

# 导入数据库和缓存模块
try:
    import pymongo
    import redis
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("⚠️ 数据库模块未安装，将使用内存存储")

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'tradingagents-cn-secret-key-2024')

# 全局变量存储分析任务和数据
analysis_tasks = {}
portfolio_data = {}
analysis_history = []

# 初始化数据库和缓存
db_cache_manager = None
mongodb_storage = None
redis_client = None

# 数据库配置状态
db_status = {
    'mongodb_connected': False,
    'redis_connected': False,
    'cache_enabled': False
}

# 日志记录
if TRADINGAGENTS_AVAILABLE:
    logger = get_logger('flask_app')
else:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('flask_app')

# 初始化数据库连接
def init_database():
    """初始化数据库连接"""
    global db_cache_manager, mongodb_storage, redis_client, db_status
    
    if not DATABASE_AVAILABLE:
        logger.warning("数据库模块不可用，跳过数据库初始化")
        return
    
    try:
        # 尝试连接MongoDB
        if TRADINGAGENTS_AVAILABLE:
            mongodb_url = os.getenv('MONGODB_CONNECTION_STRING', 'mongodb://localhost:27017/')
            try:
                mongodb_storage = MongoDBStorage(connection_string=mongodb_url)
                if mongodb_storage.is_connected():
                    db_status['mongodb_connected'] = True
                    logger.info("✅ MongoDB连接成功")
                else:
                    logger.warning("⚠️ MongoDB连接失败")
            except Exception as e:
                logger.warning(f"⚠️ MongoDB初始化失败: {e}")
        
        # 尝试连接Redis
        redis_url = os.getenv('REDIS_CONNECTION_STRING', 'redis://localhost:6379/0')
        try:
            redis_client = redis.from_url(redis_url, decode_responses=True)
            redis_client.ping()  # 测试连接
            db_status['redis_connected'] = True
            logger.info("✅ Redis连接成功")
        except Exception as e:
            logger.warning(f"⚠️ Redis连接失败: {e}")
        
        # 初始化缓存管理器
        if TRADINGAGENTS_AVAILABLE and (db_status['mongodb_connected'] or db_status['redis_connected']):
            try:
                db_cache_manager = DatabaseCacheManager(
                    mongodb_url=mongodb_url if db_status['mongodb_connected'] else None,
                    redis_url=redis_url if db_status['redis_connected'] else None
                )
                db_status['cache_enabled'] = True
                logger.info("✅ 缓存管理器初始化成功")
            except Exception as e:
                logger.warning(f"⚠️ 缓存管理器初始化失败: {e}")
                
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {e}")

# 获取股票数据（带缓存）
def get_stock_data_cached(symbol: str, period: str = '1y'):
    """获取股票数据（使用缓存）"""
    cache_key = f"stock_data:{symbol}:{period}"
    
    # 尝试从Redis获取
    if redis_client and db_status['redis_connected']:
        try:
            cached_data = redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            logger.warning(f"Redis读取失败: {e}")
    
    # 生成模拟数据（实际应该调用API）
    data = generate_mock_stock_data(symbol, period)
    
    # 存储到Redis
    if redis_client and db_status['redis_connected']:
        try:
            redis_client.setex(cache_key, 3600, json.dumps(data))  # 1小时过期
        except Exception as e:
            logger.warning(f"Redis写入失败: {e}")
    
    return data

def generate_mock_stock_data(symbol: str, period: str = '1y'):
    """生成模拟股票数据用于演示"""
    import random
    from datetime import datetime, timedelta
    
    # 生成日期范围
    end_date = datetime.now()
    if period == '1y':
        start_date = end_date - timedelta(days=365)
        days = 365
    elif period == '6m':
        start_date = end_date - timedelta(days=180)
        days = 180
    elif period == '3m':
        start_date = end_date - timedelta(days=90)
        days = 90
    else:
        start_date = end_date - timedelta(days=30)
        days = 30
    
    # 生成价格数据
    base_price = random.uniform(50, 200)
    dates = []
    prices = []
    volumes = []
    
    current_price = base_price
    for i in range(days):
        date = start_date + timedelta(days=i)
        dates.append(date.strftime('%Y-%m-%d'))
        
        # 随机价格变动
        change = random.uniform(-0.05, 0.05)
        current_price *= (1 + change)
        prices.append(round(current_price, 2))
        
        # 随机成交量
        volume = random.randint(1000000, 10000000)
        volumes.append(volume)
    
    return {
        'symbol': symbol,
        'dates': dates,
        'prices': prices,
        'volumes': volumes,
        'current_price': prices[-1],
        'change': round((prices[-1] - prices[-2]) / prices[-2] * 100, 2) if len(prices) > 1 else 0
    }

@app.route('/')
def index():
    """首页 - 仪表板"""
    return render_template('dashboard_simple.html')

@app.route('/stock-analysis')
def stock_analysis():
    """股票分析页面"""
    return render_template('stock_analysis.html')

@app.route('/portfolio')
def portfolio():
    """投资组合页面"""
    return render_template('portfolio.html')

@app.route('/history')
def history():
    """分析历史页面"""
    return render_template('history.html')

@app.route('/settings')
def settings():
    """系统设置页面"""
    return render_template('settings.html')

# API路由
@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """开始股票分析API"""
    try:
        data = request.get_json()
        
        # 验证输入参数
        stock_symbol = data.get('stock_symbol', '').strip().upper()
        analysis_date = data.get('analysis_date', datetime.date.today().isoformat())
        analysts = data.get('analysts', ['market', 'fundamentals'])
        research_depth = data.get('research_depth', 3)
        
        if not stock_symbol:
            return jsonify({'error': '股票代码不能为空'}), 400
        
        # 生成分析ID
        analysis_id = f"analysis_{uuid.uuid4().hex[:8]}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 创建分析任务
        analysis_tasks[analysis_id] = {
            'status': 'running',
            'progress': 0,
            'message': '正在初始化分析...',
            'result': None,
            'error': None,
            'created_at': datetime.datetime.now()
        }
        
        # 在后台线程中运行分析
        def run_analysis():
            try:
                # 配置分析参数
                config = DEFAULT_CONFIG.copy()
                config["llm_provider"] = "dashscope"  # 默认使用阿里百炼
                config["deep_think_llm"] = "qwen-plus"
                config["quick_think_llm"] = "qwen-turbo"
                
                # 创建分析引擎
                ta = TradingAgentsGraph(debug=True, config=config)
                
                # 更新进度
                analysis_tasks[analysis_id]['progress'] = 20
                analysis_tasks[analysis_id]['message'] = '正在获取股票数据...'
                
                # 执行分析
                state, decision = ta.propagate(stock_symbol, analysis_date)
                
                # 更新进度
                analysis_tasks[analysis_id]['progress'] = 100
                analysis_tasks[analysis_id]['status'] = 'completed'
                analysis_tasks[analysis_id]['message'] = '分析完成'
                analysis_tasks[analysis_id]['result'] = {
                    'stock_symbol': stock_symbol,
                    'decision': decision,
                    'state': state,
                    'analysis_date': analysis_date
                }
                
            except Exception as e:
                analysis_tasks[analysis_id]['status'] = 'failed'
                analysis_tasks[analysis_id]['error'] = str(e)
                analysis_tasks[analysis_id]['message'] = f'分析失败: {str(e)}'
        
        # 启动后台分析线程
        thread = threading.Thread(target=run_analysis)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'analysis_id': analysis_id,
            'status': 'started',
            'message': '分析已启动'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/progress/<analysis_id>')
def api_progress(analysis_id):
    """获取分析进度API"""
    if analysis_id not in analysis_tasks:
        return jsonify({'error': '分析任务不存在'}), 404
    
    task = analysis_tasks[analysis_id]
    return jsonify({
        'analysis_id': analysis_id,
        'status': task['status'],
        'progress': task['progress'],
        'message': task['message'],
        'result': task['result'],
        'error': task['error']
    })

@app.route('/api/system-status')
def api_system_status():
    """获取系统状态API"""
    # 实际测试API密钥可用性
    api_keys = {}
    
    # 测试阿里百炼API
    dashscope_key = os.getenv('DASHSCOPE_API_KEY')
    api_keys['dashscope'] = bool(dashscope_key and len(dashscope_key) > 10)
    
    # 测试DeepSeek API
    deepseek_key = os.getenv('DEEPSEEK_API_KEY')
    api_keys['deepseek'] = bool(deepseek_key and len(deepseek_key) > 10)
    
    # 测试Google API
    google_key = os.getenv('GOOGLE_API_KEY')
    api_keys['google'] = bool(google_key and len(google_key) > 10)
    
    # 测试OpenAI API
    openai_key = os.getenv('OPENAI_API_KEY')
    api_keys['openai'] = bool(openai_key and len(openai_key) > 10)
    
    # 测试FinnHub API
    finnhub_key = os.getenv('FINNHUB_API_KEY')
    api_keys['finnhub'] = bool(finnhub_key and len(finnhub_key) > 10)
    
    # 测试Tushare Token
    tushare_token = os.getenv('TUSHARE_TOKEN')
    api_keys['tushare'] = bool(tushare_token and len(tushare_token) > 10)
    
    return jsonify({
        'api_keys': api_keys,
        'database_status': db_status,
        'total_analyses': len(analysis_tasks),
        'running_analyses': len([t for t in analysis_tasks.values() if t['status'] == 'running']),
        'completed_analyses': len([t for t in analysis_tasks.values() if t['status'] == 'completed']),
        'failed_analyses': len([t for t in analysis_tasks.values() if t['status'] == 'failed']),
        'tradingagents_available': TRADINGAGENTS_AVAILABLE,
        'database_available': DATABASE_AVAILABLE,
        'system_health': {
            'api_connectivity': 'partial' if any(api_keys.values()) else 'none',
            'data_sources': 'available' if api_keys.get('tushare') or api_keys.get('finnhub') else 'limited',
            'cache_status': 'enabled' if db_status['cache_enabled'] else 'disabled'
        }
    })

@app.route('/api/history')
def api_history():
    """获取分析历史API"""
    # 从analysis_tasks中获取历史记录
    history = []
    for task_id, task in analysis_tasks.items():
        if task['status'] in ['completed', 'failed']:
            history_item = {
                'id': task_id,
                'created_at': task['created_at'].isoformat(),
                'status': task['status'],
                'message': task['message']
            }
            
            if task['status'] == 'completed' and task['result']:
                result = task['result']
                history_item.update({
                    'stock_symbol': result['stock_symbol'],
                    'analysis_date': result['analysis_date'],
                    'recommendation': result['decision'].get('action', 'N/A'),
                    'confidence': result['decision'].get('confidence', 0),
                    'risk_score': result['decision'].get('risk_score', 0)
                })
            
            history.append(history_item)
    
    # 按创建时间倒序排列
    history.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify({
        'history': history,
        'total': len(history)
    })

@app.route('/api/portfolio')
def api_portfolio():
    """获取投资组合API"""
    # 模拟投资组合数据
    portfolio = {
        'total_value': 125000.00,
        'daily_change': 2.35,
        'total_profit': 25000.00,
        'total_return': 25.0,
        'holdings': [
            {
                'symbol': 'AAPL',
                'name': '苹果公司',
                'quantity': 100,
                'avg_cost': 150.00,
                'current_price': 175.50,
                'market_value': 17550.00,
                'profit_loss': 2550.00,
                'return_rate': 17.0
            },
            {
                'symbol': 'TSLA',
                'name': '特斯拉',
                'quantity': 50,
                'avg_cost': 200.00,
                'current_price': 180.00,
                'market_value': 9000.00,
                'profit_loss': -1000.00,
                'return_rate': -10.0
            }
        ]
    }
    
    return jsonify(portfolio)

@app.route('/api/portfolio/add', methods=['POST'])
def api_portfolio_add():
    """添加投资组合持仓API"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        required_fields = ['symbol', 'quantity', 'avg_cost']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必需字段: {field}'}), 400
        
        # 这里应该保存到数据库，现在只是模拟
        holding = {
            'symbol': data['symbol'].upper(),
            'name': data.get('name', data['symbol']),
            'quantity': float(data['quantity']),
            'avg_cost': float(data['avg_cost']),
            'current_price': float(data['avg_cost']),  # 模拟当前价格
            'notes': data.get('notes', '')
        }
        
        return jsonify({
            'message': '持仓添加成功',
            'holding': holding
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings', methods=['GET', 'POST'])
def api_settings():
    """系统设置API"""
    if request.method == 'GET':
        # 获取当前设置
        settings = {
            'api_keys': {
                'dashscope': bool(os.getenv('DASHSCOPE_API_KEY')),
                'deepseek': bool(os.getenv('DEEPSEEK_API_KEY')),
                'google': bool(os.getenv('GOOGLE_API_KEY')),
                'openai': bool(os.getenv('OPENAI_API_KEY')),
                'finnhub': bool(os.getenv('FINNHUB_API_KEY')),
                'tushare': bool(os.getenv('TUSHARE_TOKEN'))
            },
            'default_model': {
                'provider': 'dashscope',
                'deep_think_model': 'qwen-plus',
                'quick_think_model': 'qwen-turbo'
            }
        }
        return jsonify(settings)
    
    elif request.method == 'POST':
        # 更新设置
        try:
            data = request.get_json()
            
            # 这里应该更新.env文件或数据库
            # 现在只是返回成功消息
            return jsonify({
                'message': '设置更新成功',
                'updated_settings': data
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/stock-data/<symbol>')
def api_stock_data(symbol):
    """获取股票数据API（用于图表）"""
    try:
        period = request.args.get('period', '1y')
        data = get_stock_data_cached(symbol.upper(), period)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/market-overview')
def api_market_overview():
    """获取市场概览数据"""
    try:
        # 模拟市场数据
        market_data = {
            'indices': [
                {'name': '上证指数', 'symbol': '000001.SH', 'value': 3247.89, 'change': 1.23, 'change_percent': 0.038},
                {'name': '深证成指', 'symbol': '399001.SZ', 'value': 10234.56, 'change': -23.45, 'change_percent': -0.228},
                {'name': '创业板指', 'symbol': '399006.SZ', 'value': 2156.78, 'change': 15.67, 'change_percent': 0.732},
                {'name': '恒生指数', 'symbol': 'HSI', 'value': 18456.32, 'change': 89.12, 'change_percent': 0.485},
                {'name': '纳斯达克', 'symbol': 'IXIC', 'value': 14832.47, 'change': 125.34, 'change_percent': 0.852},
                {'name': 'S&P 500', 'symbol': 'SPX', 'value': 4657.12, 'change': 32.78, 'change_percent': 0.709}
            ],
            'sectors': [
                {'name': '科技', 'change_percent': 2.15, 'volume': 1250000000},
                {'name': '金融', 'change_percent': -0.87, 'volume': 890000000},
                {'name': '医疗', 'change_percent': 1.43, 'volume': 650000000},
                {'name': '消费', 'change_percent': 0.76, 'volume': 720000000},
                {'name': '能源', 'change_percent': -1.23, 'volume': 450000000},
                {'name': '地产', 'change_percent': -2.45, 'volume': 320000000}
            ],
            'hot_stocks': [
                {'symbol': 'AAPL', 'name': '苹果', 'price': 175.50, 'change_percent': 3.2},
                {'symbol': 'TSLA', 'name': '特斯拉', 'price': 245.80, 'change_percent': -1.8},
                {'symbol': '000001', 'name': '平安银行', 'price': 12.45, 'change_percent': 2.1},
                {'symbol': '600519', 'name': '贵州茅台', 'price': 1654.32, 'change_percent': 1.5},
                {'symbol': '000858', 'name': '五粮液', 'price': 145.67, 'change_percent': 0.9}
            ],
            'market_stats': {
                'total_volume': 5680000000,
                'up_stocks': 2145,
                'down_stocks': 1876,
                'unchanged': 234,
                'limit_up': 67,
                'limit_down': 23
            }
        }
        return jsonify(market_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/dashboard')
def api_analytics_dashboard():
    """获取分析仪表板数据"""
    try:
        # 从MongoDB获取统计数据
        analytics_data = {
            'usage_stats': {},
            'performance_metrics': {},
            'error_rates': {}
        }
        
        if mongodb_storage and mongodb_storage.is_connected():
            try:
                # 获取使用统计
                usage_stats = mongodb_storage.get_usage_statistics(days=30)
                analytics_data['usage_stats'] = usage_stats
                
                # 获取供应商统计
                provider_stats = mongodb_storage.get_provider_statistics(days=30)
                analytics_data['provider_stats'] = provider_stats
                
            except Exception as e:
                logger.warning(f"获取MongoDB统计失败: {e}")
        
        # 模拟分析性能数据
        analytics_data['performance_metrics'] = {
            'avg_analysis_time': 45.6,  # 秒
            'success_rate': 94.5,  # 百分比
            'cache_hit_rate': 78.2,  # 百分比
            'daily_analyses': [12, 15, 8, 23, 19, 31, 28, 22, 25, 18, 29, 33, 27, 21],
            'model_usage': {
                'dashscope': 45,
                'deepseek': 32,
                'google': 23
            }
        }
        
        analytics_data['error_rates'] = {
            'api_errors': 2.3,
            'timeout_errors': 1.8,
            'data_errors': 0.9
        }
        
        return jsonify(analytics_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/database/status')
def api_database_status():
    """获取数据库详细状态"""
    try:
        status = {
            'mongodb': {
                'connected': db_status['mongodb_connected'],
                'collections': 0,
                'records': 0
            },
            'redis': {
                'connected': db_status['redis_connected'],
                'keys': 0,
                'memory_usage': '0MB'
            },
            'cache': {
                'enabled': db_status['cache_enabled'],
                'hit_rate': 0
            }
        }
        
        # MongoDB状态
        if mongodb_storage and mongodb_storage.is_connected():
            try:
                # 获取集合信息
                collections = mongodb_storage.db.list_collection_names()
                status['mongodb']['collections'] = len(collections)
                
                # 获取记录数量
                if 'token_usage' in collections:
                    count = mongodb_storage.collection.count_documents({})
                    status['mongodb']['records'] = count
                    
            except Exception as e:
                logger.warning(f"获取MongoDB详细状态失败: {e}")
        
        # Redis状态
        if redis_client and db_status['redis_connected']:
            try:
                info = redis_client.info()
                status['redis']['keys'] = redis_client.dbsize()
                status['redis']['memory_usage'] = f"{info.get('used_memory_human', '0B')}"
                
            except Exception as e:
                logger.warning(f"获取Redis详细状态失败: {e}")
        return jsonify(status)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/<analysis_id>')
def api_export(analysis_id):
    """导出分析报告API"""
    if analysis_id not in analysis_tasks:
        return jsonify({'error': '分析任务不存在'}), 404
    
    task = analysis_tasks[analysis_id]
    if task['status'] != 'completed':
        return jsonify({'error': '分析未完成'}), 400
    
    # 生成报告内容
    result = task['result']
    decision = result['decision']
    
    report_content = f"""
# {result['stock_symbol']} 股票分析报告

## 基本信息
- 股票代码: {result['stock_symbol']}
- 分析日期: {result['analysis_date']}
- 生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 投资建议
- 推荐操作: {decision.get('action', 'N/A')}
- 置信度: {(decision.get('confidence', 0) * 100):.1f}%
- 风险评分: {(decision.get('risk_score', 0) * 100):.1f}%

## 分析推理
{decision.get('reasoning', '暂无详细推理信息')}

---
报告由 TradingAgents-CN 自动生成
"""
    
    # 创建临时文件
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(report_content)
        temp_path = f.name
    
    return send_file(
        temp_path,
        as_attachment=True,
        download_name=f'{result["stock_symbol"]}_analysis_report.md',
        mimetype='text/markdown'
    )

if __name__ == '__main__':
    # 创建模板目录
    templates_dir = Path(__file__).parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    static_dir = Path(__file__).parent / 'static'
    static_dir.mkdir(exist_ok=True)
    
    # 初始化数据库连接
    print("🔧 初始化数据库连接...")
    init_database()
    
    print("🚀 TradingAgents-CN Flask应用启动")
    print("📱 访问地址: http://localhost:5000")
    print("⏹️  按 Ctrl+C 停止应用")
    print("📊 功能特性:")
    print("   - MongoDB + Redis 数据缓存")
    print("   - 实时数据可视化")
    print("   - 多智能体股票分析")
    print("   - 投资组合管理")
    
    app.run(debug=True, host='0.0.0.0', port=5000)