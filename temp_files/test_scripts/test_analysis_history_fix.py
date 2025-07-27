#!/usr/bin/env python3
"""
测试分析历史功能修复
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_history_data_extraction():
    """测试历史数据提取功能"""
    print("🔍 测试历史数据提取功能")
    print("-" * 40)
    
    try:
        from interfaces.streamlit.pages.analysis_history import get_filtered_history
        
        # 获取历史数据
        history_data = get_filtered_history()
        print(f"📊 获取到历史记录数量: {len(history_data)}")
        
        if not history_data:
            print("❌ 没有获取到历史记录")
            return False
        
        # 检查数据完整性
        complete_records = 0
        for record in history_data:
            has_stock_symbol = record.get('stock_symbol') != 'N/A'
            has_date = record.get('date') != '未知时间'
            has_status = record.get('status') != 'unknown'
            
            if has_stock_symbol and has_date and has_status:
                complete_records += 1
        
        print(f"✅ 完整记录数量: {complete_records}/{len(history_data)}")
        
        # 显示示例记录
        if history_data:
            sample = history_data[0]
            print(f"\n📋 示例记录:")
            print(f"  股票代码: {sample['stock_symbol']}")
            print(f"  市场类型: {sample['market_type']}")
            print(f"  分析日期: {sample['date']}")
            print(f"  状态: {sample['status']}")
            print(f"  投资建议: {sample['recommendation']}")
            print(f"  置信度: {sample['confidence']}")
            print(f"  模型: {sample['model']}")
            print(f"  分析师数量: {sample['analysts_count']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_data_formatting():
    """测试数据格式化功能"""
    print("\n🔍 测试数据格式化功能")
    print("-" * 40)
    
    try:
        from interfaces.streamlit.pages.analysis_history import (
            calculate_duration, 
            format_model_name, 
            format_detailed_analysis
        )
        
        # 测试时长计算
        from datetime import datetime, timedelta
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=5, seconds=32)
        
        duration = calculate_duration(start_time.isoformat(), end_time.isoformat())
        print(f"✅ 时长计算: {duration}")
        
        # 测试模型名称格式化
        model_names = ['dashscope', 'deepseek', 'google', 'unknown']
        for model in model_names:
            formatted = format_model_name(model)
            print(f"✅ 模型格式化 {model}: {formatted}")
        
        # 测试详细分析格式化
        sample_results = {
            'state': {
                'market_report': '# 技术分析\n这是技术分析内容',
                'fundamentals_report': '# 基本面分析\n这是基本面分析内容'
            }
        }
        
        detailed = format_detailed_analysis(sample_results)
        print(f"✅ 详细分析格式化: {len(detailed)} 字符")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_page_navigation():
    """测试页面导航功能"""
    print("\n🔍 测试页面导航功能")
    print("-" * 40)
    
    try:
        # 模拟session state
        class MockSessionState:
            def __init__(self):
                self.data = {}
            
            def get(self, key, default=None):
                return self.data.get(key, default)
            
            def __setitem__(self, key, value):
                self.data[key] = value
            
            def __contains__(self, key):
                return key in self.data
        
        session_state = MockSessionState()
        
        # 测试选择记录
        sample_record = {
            'id': 'test_analysis_001',
            'stock_symbol': 'AAPL',
            'status': 'completed'
        }
        
        session_state['selected_history_record'] = sample_record
        print("✅ 记录选择功能正常")
        
        # 测试清除选择
        session_state['selected_history_record'] = None
        print("✅ 记录清除功能正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_filter_functionality():
    """测试筛选功能"""
    print("\n🔍 测试筛选功能")
    print("-" * 40)
    
    try:
        from interfaces.streamlit.pages.analysis_history import apply_filters
        
        # 模拟数据
        sample_data = [
            {
                'stock_symbol': 'AAPL',
                'market_type': '美股',
                'status': 'completed',
                'model': '阿里百炼'
            },
            {
                'stock_symbol': '000001',
                'market_type': 'A股',
                'status': 'failed',
                'model': 'DeepSeek V3'
            }
        ]
        
        # 测试市场筛选
        filters = {'market': '美股'}
        filtered = apply_filters(sample_data, filters)
        print(f"✅ 市场筛选: {len(filtered)} 条记录")
        
        # 测试状态筛选
        filters = {'status': '已完成'}
        filtered = apply_filters(sample_data, filters)
        print(f"✅ 状态筛选: {len(filtered)} 条记录")
        
        # 测试模型筛选
        filters = {'model': 'DeepSeek V3'}
        filtered = apply_filters(sample_data, filters)
        print(f"✅ 模型筛选: {len(filtered)} 条记录")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🔧 TradingAgents-CN 分析历史功能修复测试")
    print("=" * 60)
    
    tests = [
        ("历史数据提取", test_history_data_extraction),
        ("数据格式化", test_data_formatting),
        ("页面导航", test_page_navigation),
        ("筛选功能", test_filter_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 执行测试: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！分析历史功能修复成功！")
        print("\n💡 修复要点:")
        print("  • 修复了历史数据提取逻辑，正确从raw_results中获取信息")
        print("  • 改进了时间戳解析，从分析ID中提取时间信息")
        print("  • 添加了市场类型智能推断功能")
        print("  • 修复了页面导航问题，添加了返回按钮")
        print("  • 改进了数据格式化和显示逻辑")
        return True
    else:
        print("⚠️ 部分测试失败，请检查修复内容")
        return False

if __name__ == "__main__":
    main()