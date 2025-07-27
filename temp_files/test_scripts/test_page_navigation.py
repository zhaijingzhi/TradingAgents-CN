#!/usr/bin/env python3
"""
测试页面导航功能
"""

import streamlit as st
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "web"))

def test_navigation():
    """测试导航功能"""
    st.title("🧪 页面导航测试")
    
    st.markdown("### 当前Session State")
    st.write("current_page:", st.session_state.get('current_page', 'None'))
    
    st.markdown("### 测试按钮")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("跳转到股票分析"):
            st.session_state.current_page = "stock_analysis"
            st.success("已设置跳转到股票分析")
            st.rerun()
    
    with col2:
        if st.button("跳转到模型配置"):
            st.session_state.current_page = "model_config"
            st.success("已设置跳转到模型配置")
            st.rerun()
    
    with col3:
        if st.button("清除跳转状态"):
            st.session_state.current_page = None
            st.success("已清除跳转状态")
            st.rerun()
    
    st.markdown("### 侧边栏测试")
    st.info("请查看左侧侧边栏的选择是否会根据按钮点击而改变")

if __name__ == "__main__":
    test_navigation()