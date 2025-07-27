#!/bin/bash
# TradingAgents-CN Flask版本启动脚本

echo "🚀 TradingAgents-CN Flask版本启动器"
echo "=================================================="

# 检查虚拟环境目录是否存在
if [ ! -d "env" ]; then
    echo "❌ 虚拟环境目录不存在，请先创建虚拟环境:"
    echo "   python3 -m venv env"
    echo "   source env/bin/activate"
    echo "   pip install -r requirements.txt"
    echo "   pip install flask"
    exit 1
fi

# 激活虚拟环境
echo "🔄 激活虚拟环境..."
source env/bin/activate

# 检查虚拟环境是否激活成功
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ 虚拟环境已激活: $VIRTUAL_ENV"
else
    echo "❌ 虚拟环境激活失败"
    exit 1
fi

# 检查Flask是否安装
if ! python -c "import flask" 2>/dev/null; then
    echo "🔄 安装Flask和相关依赖..."
    pip install flask gunicorn
fi

# 检查TradingAgents核心模块
if ! python -c "from tradingagents.graph.trading_graph import TradingAgentsGraph" 2>/dev/null; then
    echo "⚠️ TradingAgents核心模块未找到，某些功能可能不可用"
    echo "   请确保已正确安装项目依赖: pip install -e ."
fi

# 检查文件是否存在
if [ ! -f "flask_app/app.py" ]; then
    echo "❌ 找不到应用文件: flask_app/app.py"
    exit 1
fi

# 设置Python路径
export PYTHONPATH="$PWD:$PYTHONPATH"

echo "🌐 启动Flask Web应用..."
echo "📱 浏览器将自动打开 http://localhost:5000"
echo "⏹️  按 Ctrl+C 停止应用"
echo ""
echo "🎯 Flask版本特性:"
echo "   ✨ 传统Web架构 - 更稳定的页面导航"
echo "   ✨ RESTful API - 前后端分离设计"
echo "   ✨ 响应式界面 - Bootstrap 5 + jQuery"
echo "   ✨ 实时进度 - Ajax轮询显示分析进度"
echo "=================================================="

# 启动Flask应用
cd flask_app && python app.py