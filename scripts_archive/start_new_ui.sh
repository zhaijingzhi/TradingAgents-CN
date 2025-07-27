#!/bin/bash
# TradingAgents-CN 新界面启动脚本

echo "🚀 TradingAgents-CN 新界面启动器"
echo "=================================================="

# 检查虚拟环境目录是否存在
if [ ! -d "env" ]; then
    echo "❌ 虚拟环境目录不存在，请先创建虚拟环境:"
    echo "   python3 -m venv env"
    echo "   source env/bin/activate"
    echo "   pip install -r requirements.txt"
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

# 检查文件是否存在
if [ ! -f "web/app.py" ]; then
    echo "❌ 找不到应用文件: web/app.py"
    exit 1
fi

# 检查streamlit是否安装
if ! python -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit未安装，请安装依赖:"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# 设置Python路径
export PYTHONPATH="$PWD:$PWD/web:$PYTHONPATH"

echo "🌐 启动Web应用..."
echo "📱 浏览器将自动打开 http://localhost:8501"
echo "⏹️  按 Ctrl+C 停止应用"
echo "=================================================="

# 启动应用
python -m streamlit run web/app.py \
    --server.port 8501 \
    --server.address localhost \
    --browser.gatherUsageStats false \
    --server.fileWatcherType none \
    --server.runOnSave false