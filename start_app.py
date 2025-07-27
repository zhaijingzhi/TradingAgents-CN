#!/usr/bin/env python3
"""
TradingAgents-CN 统一启动器
支持选择不同的Web界面类型
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def main():
    """主启动函数"""
    parser = argparse.ArgumentParser(description='TradingAgents-CN Web应用启动器')
    parser.add_argument(
        '--ui', 
        choices=['streamlit', 'flask', 'auto'], 
        default='auto',
        help='选择UI类型: streamlit(推荐), flask(传统), auto(自动检测)'
    )
    parser.add_argument('--port', type=int, help='指定端口号')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    
    args = parser.parse_args()
    
    print("🚀 TradingAgents-CN 统一启动器")
    print("=" * 50)
    
    # 项目根目录
    project_root = Path(__file__).parent
    
    # 检查虚拟环境
    in_venv = (
        hasattr(sys, 'real_prefix') or 
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )
    
    if not in_venv:
        print("⚠️ 建议在虚拟环境中运行")
        print("   Windows: .\\env\\Scripts\\activate")
        print("   Linux/macOS: source env/bin/activate")
        print()
    
    # 决定使用哪种UI
    ui_type = args.ui
    if ui_type == 'auto':
        # 自动检测：优先Streamlit，后备Flask
        try:
            import streamlit
            ui_type = 'streamlit'
            print("✅ 检测到Streamlit，使用Streamlit界面")
        except ImportError:
            try:
                import flask
                ui_type = 'flask'
                print("⚠️ Streamlit未安装，使用Flask界面")
            except ImportError:
                print("❌ 未安装Web框架，请安装streamlit或flask")
                return
    
    # 启动对应的应用
    if ui_type == 'streamlit':
        start_streamlit(project_root, args.port, args.debug)
    elif ui_type == 'flask':
        start_flask(project_root, args.port, args.debug)


def start_streamlit(project_root, port=None, debug=False):
    """启动Streamlit应用"""
    print("\n🌟 启动Streamlit界面")
    
    app_file = project_root / "interfaces" / "streamlit" / "app.py"
    if not app_file.exists():
        print(f"❌ 找不到Streamlit应用: {app_file}")
        return
    
    # 设置环境变量
    env = os.environ.copy()
    current_path = env.get('PYTHONPATH', '')
    if current_path:
        env['PYTHONPATH'] = f"{project_root}{os.pathsep}{current_path}"
    else:
        env['PYTHONPATH'] = str(project_root)
    
    # 构建命令
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(app_file),
        "--server.port", str(port or 8501),
        "--server.address", "localhost",
        "--browser.gatherUsageStats", "false"
    ]
    
    if not debug:
        cmd.extend([
            "--server.fileWatcherType", "none",
            "--server.runOnSave", "false"
        ])
    
    print(f"📱 浏览器将打开 http://localhost:{port or 8501}")
    print("⏹️  按 Ctrl+C 停止应用")
    
    try:
        subprocess.run(cmd, cwd=project_root, env=env)
    except KeyboardInterrupt:
        print("\n⏹️ Streamlit应用已停止")


def start_flask(project_root, port=None, debug=False):
    """启动Flask应用"""
    print("\n🌐 启动Flask界面")
    
    app_file = project_root / "interfaces" / "flask" / "app.py"
    if not app_file.exists():
        print(f"❌ 找不到Flask应用: {app_file}")
        return
    
    # 设置环境变量
    env = os.environ.copy()
    env['PYTHONPATH'] = str(project_root)
    env['FLASK_APP'] = str(app_file)
    if debug:
        env['FLASK_DEBUG'] = '1'
    
    print(f"📱 浏览器将打开 http://localhost:{port or 5000}")
    print("⏹️  按 Ctrl+C 停止应用")
    
    try:
        if port:
            subprocess.run([
                sys.executable, str(app_file), "--port", str(port)
            ], cwd=project_root, env=env)
        else:
            subprocess.run([sys.executable, str(app_file)], cwd=project_root, env=env)
    except KeyboardInterrupt:
        print("\n⏹️ Flask应用已停止")


if __name__ == "__main__":
    main()