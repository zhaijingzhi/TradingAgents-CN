#!/bin/bash

# TradingAgents-CN 虚拟环境启动脚本
# 使用方法: source activate_env.sh 或 . activate_env.sh

echo "🚀 正在启动 TradingAgents-CN 虚拟环境..."

# 检查虚拟环境是否存在
if [ ! -d "env" ]; then
    echo "❌ 错误: 虚拟环境目录 'env' 不存在"
    echo "请先创建虚拟环境: python -m venv env"
    return 1 2>/dev/null || exit 1
fi

# 检查激活脚本是否存在
if [ ! -f "env/bin/activate" ]; then
    echo "❌ 错误: 虚拟环境激活脚本不存在"
    echo "请重新创建虚拟环境: python -m venv env"
    return 1 2>/dev/null || exit 1
fi

# 激活虚拟环境
source env/bin/activate

# 检查是否成功激活
if [ "$VIRTUAL_ENV" != "" ]; then
    echo "✅ 虚拟环境已成功激活"
    echo "📍 虚拟环境路径: $VIRTUAL_ENV"
    echo "🐍 Python 路径: $(which python)"
    echo "📦 Python 版本: $(python --version)"
    
    # 检查 .env 文件
    if [ -f ".env" ]; then
        echo "✅ 环境配置文件 .env 已找到"
    else
        echo "⚠️  警告: 环境配置文件 .env 不存在"
        echo "请复制 .env.example 为 .env 并配置API密钥"
    fi
    
    # 显示可用的启动命令
    echo ""
    echo "🎯 可用的启动命令:"
    echo "  • 启动新版Web界面: ./start_new_ui.sh"
    echo "  • 启动Web界面: ./start_web.sh"
    echo "  • 启动Flask应用: ./start_flask.sh"
    echo "  • 检查配置状态: python -m cli.main config"
    echo "  • 测试配置: python -m cli.main test"
    echo ""
    echo "💡 提示: 使用 'deactivate' 命令退出虚拟环境"
else
    echo "❌ 虚拟环境激活失败"
    return 1 2>/dev/null || exit 1
fi