#!/usr/bin/env python3
"""
检查新页面文件的语法
"""

import ast
import sys
from pathlib import Path

def check_syntax(file_path):
    """检查文件语法"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 尝试解析AST
        ast.parse(content)
        print(f"✅ {file_path.name} - 语法正确")
        return True
        
    except SyntaxError as e:
        print(f"❌ {file_path.name} - 语法错误:")
        print(f"   行 {e.lineno}: {e.text.strip() if e.text else ''}")
        print(f"   错误: {e.msg}")
        return False
    except Exception as e:
        print(f"⚠️ {file_path.name} - 检查失败: {e}")
        return False

def main():
    """主函数"""
    print("🔍 检查新页面文件语法")
    print("=" * 40)
    
    # 要检查的文件列表
    files_to_check = [
        "web/app.py",
        "web/pages/dashboard.py",
        "web/pages/stock_analysis.py",
        "web/pages/portfolio_management.py", 
        "web/pages/analysis_history.py",
        "web/pages/market_monitor.py",
        "web/pages/system_settings.py",
        "web/components/sidebar.py"
    ]
    
    all_good = True
    
    for file_path in files_to_check:
        path = Path(file_path)
        if path.exists():
            if not check_syntax(path):
                all_good = False
        else:
            print(f"⚠️ {file_path} - 文件不存在")
            all_good = False
    
    print("=" * 40)
    if all_good:
        print("🎉 所有文件语法检查通过！")
    else:
        print("❌ 发现语法错误，请修复后重试")
        sys.exit(1)

if __name__ == "__main__":
    main()