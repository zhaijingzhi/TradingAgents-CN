#!/bin/bash

# TradingAgents-CN 临时文件清理脚本
# 使用方法: ./cleanup_temp_files.sh [选项]

echo "🧹 TradingAgents-CN 临时文件清理工具"
echo "=" * 50

# 显示帮助信息
show_help() {
    echo "使用方法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --logs          清理日志文件"
    echo "  --packages      清理安装包"
    echo "  --tests         清理测试脚本"
    echo "  --docs-delete   删除重复文档"
    echo "  --archived      删除归档文档"
    echo "  --all           清理所有临时文件"
    echo "  --help          显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 --logs                # 只清理日志文件"
    echo "  $0 --docs-delete         # 只删除重复文档"
    echo "  $0 --all                 # 清理所有临时文件"
}

# 清理日志文件
cleanup_logs() {
    echo "🗑️ 清理日志文件..."
    if [ -d "temp_files/logs" ]; then
        rm -rf temp_files/logs/*
        echo "✅ 日志文件已清理"
    else
        echo "ℹ️ 没有找到日志文件"
    fi
}

# 清理安装包
cleanup_packages() {
    echo "📦 清理安装包..."
    if [ -d "temp_files/packages" ]; then
        rm -rf temp_files/packages/*
        echo "✅ 安装包已清理"
    else
        echo "ℹ️ 没有找到安装包"
    fi
}

# 清理测试脚本
cleanup_tests() {
    echo "🧪 清理测试脚本..."
    if [ -d "temp_files/test_scripts" ]; then
        echo "📋 测试脚本列表:"
        ls -la temp_files/test_scripts/
        read -p "确认删除这些测试脚本? (y/N): " confirm
        if [[ $confirm == [yY] ]]; then
            rm -rf temp_files/test_scripts/*
            echo "✅ 测试脚本已清理"
        else
            echo "ℹ️ 跳过测试脚本清理"
        fi
    else
        echo "ℹ️ 没有找到测试脚本"
    fi
}

# 删除重复文档
cleanup_docs_delete() {
    echo "📄 删除重复文档..."
    if [ -d "temp_files/docs_to_delete" ]; then
        echo "📋 待删除文档列表:"
        ls -la temp_files/docs_to_delete/
        read -p "确认删除这些重复文档? (y/N): " confirm
        if [[ $confirm == [yY] ]]; then
            rm -rf temp_files/docs_to_delete/*
            echo "✅ 重复文档已删除"
        else
            echo "ℹ️ 跳过重复文档删除"
        fi
    else
        echo "ℹ️ 没有找到待删除文档"
    fi
}

# 删除归档文档
cleanup_archived() {
    echo "📚 删除归档文档..."
    if [ -d "temp_files/archived_docs" ]; then
        echo "📋 归档文档列表:"
        ls -la temp_files/archived_docs/
        echo ""
        echo "⚠️ 警告: 这些文档包含项目历史信息，删除前请确认不再需要"
        read -p "确认删除这些归档文档? (y/N): " confirm
        if [[ $confirm == [yY] ]]; then
            rm -rf temp_files/archived_docs/*
            echo "✅ 归档文档已删除"
        else
            echo "ℹ️ 跳过归档文档删除"
        fi
    else
        echo "ℹ️ 没有找到归档文档"
    fi
}

# 清理所有临时文件
cleanup_all() {
    echo "🗑️ 清理所有临时文件..."
    echo ""
    echo "⚠️ 警告: 这将删除temp_files目录中的所有内容"
    echo "包括: 日志、安装包、测试脚本、重复文档、归档文档等"
    echo ""
    read -p "确认删除所有临时文件? (y/N): " confirm
    if [[ $confirm == [yY] ]]; then
        rm -rf temp_files/
        echo "✅ 所有临时文件已清理"
        echo "📁 temp_files目录已删除"
    else
        echo "ℹ️ 取消清理操作"
    fi
}

# 显示当前状态
show_status() {
    echo "📊 当前临时文件状态:"
    echo ""
    if [ -d "temp_files" ]; then
        echo "📁 temp_files/ 目录内容:"
        du -sh temp_files/* 2>/dev/null | sort -hr
        echo ""
        echo "📈 总大小: $(du -sh temp_files/ | cut -f1)"
    else
        echo "✅ 没有临时文件目录"
    fi
}

# 主逻辑
case "$1" in
    --logs)
        cleanup_logs
        ;;
    --packages)
        cleanup_packages
        ;;
    --tests)
        cleanup_tests
        ;;
    --docs-delete)
        cleanup_docs_delete
        ;;
    --archived)
        cleanup_archived
        ;;
    --all)
        cleanup_all
        ;;
    --status)
        show_status
        ;;
    --help|"")
        show_help
        ;;
    *)
        echo "❌ 未知选项: $1"
        echo ""
        show_help
        exit 1
        ;;
esac

echo ""
echo "🎉 清理操作完成！"
echo ""
echo "💡 提示:"
echo "  - 使用 '$0 --status' 查看当前状态"
echo "  - 使用 '$0 --help' 查看所有选项"
echo "  - 重要文档建议先备份再删除"