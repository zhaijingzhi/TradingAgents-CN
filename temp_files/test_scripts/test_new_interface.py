#!/usr/bin/env python3
"""
测试新界面的启动脚本
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """主函数"""
    print("🚀 TradingAgents-CN 新界面测试启动器")
    print("=" * 50)
    
    # 检查项目结构
    project_root = Path(__file__).parent
    web_dir = project_root / "web"
    
    if not web_dir.exists():
        print("❌ web目录不存在")
        return
    
    # 检查新页面文件
    new_pages = [
        "pages/dashboard.py",
        "pages/stock_analysis.py", 
        "pages/portfolio_management.py",
        "pages/analysis_history.py",
        "pages/market_monitor.py",
        "pages/system_settings.py"
    ]
    
    print("📋 检查新页面文件:")
    for page in new_pages:
        page_path = web_dir / page
        if page_path.exists():
            print(f"  ✅ {page}")
        else:
            print(f"  ❌ {page} - 文件不存在")
    
    print("\n📖 新界面功能:")
    print("  📊 仪表板 - 系统概览和快速操作")
    print("  📈 股票分析 - 专门的分析工作台") 
    print("  💼 投资组合 - 组合管理和跟踪")
    print("  📋 分析历史 - 历史记录和统计")
    print("  📊 市场监控 - 实时市场数据")
    print("  🤖 模型配置 - AI模型管理")
    print("  ⚙️ 系统设置 - 全面的系统配置")
    print("  💾 缓存管理 - 数据清理工具")
    print("  💰 Token统计 - 成本跟踪")
    
    print("\n🎯 界面重构亮点:")
    print("  ✨ 功能分散化 - 每个页面专注特定功能")
    print("  ✨ 层次清晰 - 从概览到详细的信息架构")
    print("  ✨ 用户友好 - 简化操作流程，提升体验")
    print("  ✨ 可扩展性 - 便于后续功能模块添加")
    
    print("\n" + "=" * 50)
    
    # 询问是否启动
    try:
        choice = input("是否启动新界面进行测试? (y/n): ").lower().strip()
        if choice in ['y', 'yes', '是']:
            print("\n🌐 正在启动Web界面...")
            
            # 设置环境变量
            env = os.environ.copy()
            env['PYTHONPATH'] = str(project_root)
            
            # 启动命令
            cmd = [
                sys.executable, "-m", "streamlit", "run",
                str(web_dir / "app.py"),
                "--server.port", "8501",
                "--server.address", "localhost",
                "--browser.gatherUsageStats", "false"
            ]
            
            print("📱 浏览器将自动打开 http://localhost:8501")
            print("⏹️  按 Ctrl+C 停止应用")
            print("=" * 50)
            
            # 启动应用
            subprocess.run(cmd, cwd=project_root, env=env)
            
        else:
            print("\n👋 测试已取消")
            
    except KeyboardInterrupt:
        print("\n\n⏹️ 应用已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        print("\n💡 请尝试:")
        print("   1. 确保已安装streamlit: pip install streamlit")
        print("   2. 确保已安装项目依赖: pip install -r requirements.txt")
        print("   3. 手动启动: python start_web.py")

if __name__ == "__main__":
    main()