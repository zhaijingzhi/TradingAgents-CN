"""
缓存管理页面
"""

import streamlit as st
import os
import shutil
from pathlib import Path

def show_cache_management():
    """显示缓存管理页面"""
    st.title("🧹 缓存管理")
    
    # 缓存目录列表
    cache_dirs = [
        ("./cache", "系统缓存"),
        ("./data", "数据缓存"),
        ("./logs", "日志文件"),
        ("./results", "分析结果"),
        ("interfaces/streamlit/utils/__pycache__", "Python缓存"),
    ]
    
    st.subheader("📁 缓存目录状态")
    
    total_size = 0
    for cache_dir, description in cache_dirs:
        if os.path.exists(cache_dir):
            size = get_dir_size(cache_dir)
            total_size += size
            size_str = format_size(size)
            st.info(f"**{description}** (`{cache_dir}`): {size_str}")
        else:
            st.warning(f"**{description}** (`{cache_dir}`): 不存在")
    
    st.metric("总缓存大小", format_size(total_size))
    
    st.markdown("---")
    
    # 清理选项
    st.subheader("🗑️ 清理选项")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧹 清理系统缓存", help="清理 ./cache 目录", use_container_width=True):
            if clear_directory("./cache"):
                st.success("✅ 系统缓存已清理")
            else:
                st.error("❌ 清理失败")
            st.rerun()
    
    with col2:
        if st.button("📊 清理分析结果", help="清理 ./results 目录", use_container_width=True):
            if clear_directory("./results"):
                st.success("✅ 分析结果已清理")
            else:
                st.error("❌ 清理失败")
            st.rerun()
    
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("📝 清理日志文件", help="清理 ./logs 目录", use_container_width=True):
            if clear_directory("./logs"):
                st.success("✅ 日志文件已清理")
            else:
                st.error("❌ 清理失败")
            st.rerun()
    
    with col4:
        if st.button("🐍 清理Python缓存", help="清理 __pycache__ 目录", use_container_width=True):
            cleared = clear_python_cache()
            if cleared > 0:
                st.success(f"✅ 已清理 {cleared} 个Python缓存目录")
            else:
                st.info("ℹ️ 没有找到Python缓存")
            st.rerun()
    
    # 危险操作
    st.markdown("---")
    st.subheader("⚠️ 危险操作")
    
    with st.expander("🚨 清理所有缓存", expanded=False):
        st.warning("此操作将清理所有缓存文件，包括分析结果和日志。操作不可逆！")
        
        if st.button("🗑️ 确认清理所有缓存", type="secondary"):
            cleared_count = 0
            for cache_dir, _ in cache_dirs:
                if clear_directory(cache_dir):
                    cleared_count += 1
            
            cleared_count += clear_python_cache()
            
            if cleared_count > 0:
                st.success(f"✅ 已清理 {cleared_count} 个目录")
            else:
                st.info("ℹ️ 没有需要清理的内容")
            st.rerun()
    
    # 返回主页按钮
    if st.button("🏠 返回主页", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()

def get_dir_size(path):
    """获取目录大小"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
    except Exception:
        pass
    return total_size

def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def clear_directory(path):
    """清理目录"""
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
            os.makedirs(path, exist_ok=True)
            return True
    except Exception as e:
        st.error(f"清理失败: {e}")
    return False

def clear_python_cache():
    """清理Python缓存"""
    cleared = 0
    try:
        for root, dirs, files in os.walk("."):
            if "__pycache__" in dirs:
                cache_path = os.path.join(root, "__pycache__")
                shutil.rmtree(cache_path)
                cleared += 1
    except Exception:
        pass
    return cleared