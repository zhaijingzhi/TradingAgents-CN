# 临时文件整理说明

本文件夹包含了从项目根目录整理出来的临时文件、测试文件和文档。

## 文件夹结构

### 📋 fix_guides/ - 修复指南文档
包含项目开发过程中创建的各种修复指南：
- `API_CHECK_FIX_GUIDE.md` - API状态检查修复指南
- `MODEL_HISTORY_FIX_GUIDE.md` - 模型切换和历史记录修复指南  
- `NAVIGATION_FIX_GUIDE.md` - Streamlit导航修复指南

**用途**: 这些文档记录了重要的修复过程，可以作为参考保留，或者整合到主要文档中。

### 📊 logs/ - 日志文件
包含测试和开发过程中产生的日志文件：
- `streamlit_final_test.log` - 最终测试日志
- `streamlit_test.log` - 测试日志
- `streamlit.log` - Streamlit运行日志

**用途**: 这些日志文件可以用于调试和问题排查，建议定期清理。

### 🧪 test_scripts/ - 测试脚本
包含开发过程中创建的临时测试脚本：
- `test_new_interface.py` - 新界面测试脚本
- `test_page_navigation.py` - 页面导航测试脚本

**用途**: 这些脚本用于特定功能的测试，可以保留作为回归测试的参考。

### 🔧 utility_scripts/ - 工具脚本
包含开发过程中创建的实用工具脚本：
- `check_app_status.py` - 应用状态检查脚本
- `check_syntax.py` - 语法检查脚本

**用途**: 这些工具脚本可以用于开发和维护，建议保留或移动到scripts目录。

### 📚 docs_to_merge/ - 待合并文档
包含内容重复需要合并的文档：
- `DATABASE_SETUP_GUIDE.md` - 数据库设置指南
- `database_setup.md` - 数据库配置指南  
- `installation.md` - 安装指南(来自overview目录)
- `BRANCH_GUIDE.md` - 分支指南
- `BRANCH_MANAGEMENT_STRATEGY.md` - 分支管理策略

**用途**: 这些文档内容重复，需要合并成统一的文档。

### 🗑️ docs_to_delete/ - 待删除文档
包含重复或过时的文档：
- `QUICK_START.md` - 与根目录新建的快速开始指南重复
- `VERSION_0.1.7_RELEASE_NOTES.md` - 重复的版本发布说明

**用途**: 这些文档已有更好的替代版本，可以安全删除。

### 📄 docs_duplicates/ - 重复文档备份
包含原始的重复文档备份：
- `QUICKSTART.md` - 原根目录快速开始指南
- `QUICK_START_NEW_UI.md` - 新UI快速开始指南
- `QUICK_START.md` - docs目录快速开始指南

**用途**: 作为合并参考的备份文件，合并完成后可删除。

### 📦 packages/ - 安装包
包含下载的软件安装包：
- `pandoc-3.7.0.2-1-amd64.deb` - Pandoc安装包

**用途**: 安装包在安装完成后可以删除，或者保留用于其他环境的部署。

### 📚 archived_docs/ - 归档文档
包含可能过时或重复的文档：
- `README-ORIGINAL.md` - 原始README文档
- `FLASK_MIGRATION_GUIDE.md` - Flask迁移指南

**用途**: 这些文档可能包含有用的历史信息，建议审查后决定是否保留。

## 建议处理方式

### 🔄 可以整合的文件
- **修复指南**: 考虑将重要的修复信息整合到主要的开发文档中
- **测试脚本**: 有价值的测试可以移动到 `tests/` 目录

### 🗑️ 可以删除的文件
- **日志文件**: 如果不需要调试，可以定期清理
- **安装包**: 软件安装完成后可以删除
- **过时文档**: 确认不再需要后可以删除

### 📁 建议保留的文件
- **修复指南**: 作为开发历史记录保留
- **测试脚本**: 可能用于未来的回归测试

## 清理命令

如果确认不再需要这些文件，可以使用以下命令清理：

```bash
# 删除日志文件
rm -rf temp_files/logs/

# 删除安装包
rm -rf temp_files/packages/

# 删除整个临时文件夹（谨慎使用）
rm -rf temp_files/
```

## 整合建议

1. **将有价值的修复指南整合到主文档**
2. **将测试脚本移动到正式的测试目录**
3. **定期清理日志和临时文件**
4. **建立文件管理规范，避免根目录堆积临时文件**

---

**整理时间**: 2025-07-27  
**整理范围**: 项目根目录临时文件  
**建议**: 定期进行类似整理，保持项目结构清洁