#!/usr/bin/env python3
"""
检查应用状态
"""

import requests
import time
import sys

def check_app_status():
    """检查应用状态"""
    url = "http://localhost:8501"
    
    print("🔍 检查TradingAgents-CN Web应用状态...")
    print(f"📍 检查地址: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("✅ 应用运行正常！")
            print("🌐 请在浏览器中访问: http://localhost:8501")
            return True
        else:
            print(f"⚠️ 应用响应异常，状态码: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到应用，请检查:")
        print("   1. 应用是否已启动")
        print("   2. 端口8501是否被占用")
        print("   3. 防火墙设置")
        return False
        
    except requests.exceptions.Timeout:
        print("⏱️ 连接超时，应用可能正在启动中...")
        return False
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 TradingAgents-CN 应用状态检查器")
    print("=" * 50)
    
    # 等待几秒让应用完全启动
    print("⏳ 等待应用启动...")
    time.sleep(3)
    
    # 检查应用状态
    if check_app_status():
        print("\n🎉 应用检查通过！")
        print("\n📋 新界面功能:")
        print("   📊 仪表板 - 系统概览")
        print("   📈 股票分析 - 专业分析工具")
        print("   💼 投资组合 - 组合管理")
        print("   📋 分析历史 - 历史记录")
        print("   📊 市场监控 - 实时数据")
        print("   🤖 模型配置 - AI模型管理")
        print("   ⚙️ 系统设置 - 全面配置")
        print("   💾 缓存管理 - 数据清理")
        print("   💰 Token统计 - 成本跟踪")
        
    else:
        print("\n❌ 应用检查失败")
        print("\n🔧 故障排除建议:")
        print("   1. 检查终端是否有错误信息")
        print("   2. 确保在虚拟环境中运行")
        print("   3. 检查依赖是否完整安装")
        print("   4. 尝试重新启动应用")
        
        print("\n🚀 启动命令:")
        print("   source env/bin/activate")
        print("   python start_web.py")

if __name__ == "__main__":
    main()