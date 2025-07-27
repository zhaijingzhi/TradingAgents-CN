# 模型切换和历史记录修复指南

## 问题描述

用户反馈了两个主要问题：
1. **模型切换问题**: 切换到DeepSeek模型时没有正确切换
2. **历史记录显示问题**: 查看分析历史记录时显示有问题

## 修复方案

### 1. 修复模型切换问题

**问题原因**: 侧边栏中有两套模型配置系统，导致配置不同步

**修改文件**: `interfaces/streamlit/components/sidebar.py`

#### 修复内容

1. **统一模型配置逻辑**:
```python
# 从session state获取当前配置
current_config = st.session_state.get('sidebar_config', {})
current_provider = current_config.get('llm_provider', 'dashscope')

provider_options = ["dashscope", "deepseek", "google"]
try:
    provider_index = provider_options.index(current_provider)
except ValueError:
    provider_index = 0

llm_provider = st.selectbox(
    "LLM提供商",
    options=provider_options,
    index=provider_index,
    format_func=lambda x: {
        "dashscope": "阿里百炼",
        "deepseek": "DeepSeek V3",
        "google": "Google AI"
    }[x],
    help="选择AI模型提供商",
    key="sidebar_llm_provider"
)
```

2. **为每个模型提供商添加状态同步**:
```python
# DeepSeek模型选择
elif llm_provider == "deepseek":
    deepseek_options = ["deepseek-chat"]
    try:
        model_index = deepseek_options.index(current_model) if current_model in deepseek_options else 0
    except ValueError:
        model_index = 0
        
    llm_model = st.selectbox(
        "选择DeepSeek模型",
        options=deepseek_options,
        index=model_index,
        format_func=lambda x: {
            "deepseek-chat": "DeepSeek Chat - 通用对话模型，适合股票分析"
        }[x],
        help="选择用于分析的DeepSeek模型",
        key="sidebar_deepseek_model"
    )
```

### 2. 修复历史记录显示问题

**问题原因**: 历史记录页面只显示模拟数据，没有获取真实的分析历史

**修改文件**: 
- `interfaces/streamlit/pages/analysis_history.py`
- `interfaces/streamlit/utils/async_progress_tracker.py`

#### 修复内容

1. **添加真实历史数据获取函数**:
```python
def get_all_analysis_history() -> Dict[str, Any]:
    """获取所有分析历史记录"""
    history = {}
    
    try:
        # 检查REDIS_ENABLED环境变量
        redis_enabled = os.getenv('REDIS_ENABLED', 'false').lower() == 'true'

        # 如果Redis启用，先尝试从Redis获取
        if redis_enabled:
            # Redis获取逻辑...
            
        # 如果Redis失败或未启用，尝试从文件获取
        data_dir = Path("data")
        if data_dir.exists():
            # 文件获取逻辑...
            
        return history
    except Exception as e:
        logger.error(f"📊 [历史记录] 获取历史记录失败: {e}")
        return {}
```

2. **改进历史记录格式化**:
```python
def get_filtered_history():
    """获取筛选后的历史记录"""
    try:
        # 尝试从Redis获取真实的分析历史数据
        from interfaces.streamlit.utils.async_progress_tracker import get_all_analysis_history
        real_history = get_all_analysis_history()
        
        if real_history:
            # 转换真实数据格式
            formatted_history = []
            for analysis_id, data in real_history.items():
                # 解析分析结果
                raw_results = data.get('raw_results', {})
                decision = raw_results.get('decision', {}) if raw_results else {}
                
                # 格式化记录
                record = {
                    'id': analysis_id,
                    'stock_symbol': data.get('stock_symbol', 'N/A'),
                    'market_type': data.get('market_type', '未知'),
                    'date': data.get('timestamp', '未知时间'),
                    'duration': calculate_duration(data.get('start_time'), data.get('end_time')),
                    'status': data.get('status', 'unknown'),
                    'recommendation': decision.get('action', 'N/A'),
                    'confidence': f"{decision.get('confidence', 0)*100:.0f}%" if isinstance(decision.get('confidence'), (int, float)) else 'N/A',
                    'risk_score': decision.get('risk_score', 'N/A'),
                    'model': format_model_name(data.get('llm_provider', 'unknown')),
                    'analysts_count': len(data.get('analysts', [])),
                    'detailed_analysis': format_detailed_analysis(raw_results)
                }
                formatted_history.append(record)
            
            return apply_filters(formatted_history, filters)
    except Exception as e:
        st.warning(f"获取历史数据时出错: {e}")
    
    # 如果没有真实数据，返回演示数据
    return apply_filters(sample_data, filters)
```

3. **添加辅助函数**:
```python
def calculate_duration(start_time, end_time):
    """计算分析持续时间"""
    # 时间计算逻辑...

def format_model_name(llm_provider):
    """格式化模型名称"""
    model_names = {
        'dashscope': '阿里百炼',
        'deepseek': 'DeepSeek V3',
        'google': 'Google AI',
        'anthropic': 'Claude',
        'openai': 'OpenAI'
    }
    return model_names.get(llm_provider, llm_provider)

def format_detailed_analysis(raw_results):
    """格式化详细分析内容"""
    # 分析内容格式化逻辑...

def apply_filters(data, filters):
    """应用筛选条件"""
    # 筛选逻辑...
```

## 修复效果

### ✅ 模型切换修复
- 现在可以正确切换到DeepSeek V3模型
- 模型选择状态在页面间保持同步
- 支持所有配置的模型提供商（阿里百炼、DeepSeek、Google AI）

### ✅ 历史记录修复
- 现在显示真实的分析历史数据（从Redis或文件获取）
- 支持按市场类型、状态、模型等条件筛选
- 显示准确的分析时长、置信度、风险评分等信息
- 如果没有真实数据，会显示演示数据作为示例

## 测试验证

```bash
# 启动应用
source activate_env.sh
python -m streamlit run interfaces/streamlit/app.py --server.port 8501
```

### 测试步骤

1. **测试模型切换**:
   - 在侧边栏中选择"DeepSeek V3"
   - 确认模型选择器显示"DeepSeek Chat"
   - 开始分析，验证使用的是DeepSeek模型

2. **测试历史记录**:
   - 导航到"📋 分析历史"页面
   - 查看是否显示真实的历史分析记录
   - 测试筛选功能（按市场、状态、模型筛选）
   - 点击"查看"按钮查看详细分析报告

## 技术要点

### 模型配置同步
- 使用session state作为配置的统一存储
- 确保侧边栏配置与实际使用的配置一致
- 为每个selectbox添加唯一的key避免冲突

### 历史数据获取
- 优先从Redis获取实时数据
- Redis失败时回退到文件存储
- 数据格式化确保显示的一致性
- 错误处理确保页面不会崩溃

### 数据筛选和显示
- 支持多维度筛选（日期、市场、状态、模型）
- 分页显示避免性能问题
- 友好的错误提示和空数据处理

---

**修复完成时间**: 2025-07-27  
**测试状态**: ✅ 所有功能正常  
**影响范围**: 模型切换、历史记录显示  
**向后兼容**: ✅ 完全兼容

## 使用建议

1. **模型切换**: 建议在开始分析前先在侧边栏选择合适的模型
2. **历史查看**: 可以通过筛选条件快速找到特定的分析记录
3. **数据备份**: 重要的分析结果会自动保存到Redis和文件中
4. **性能优化**: 历史记录较多时建议使用筛选功能提高加载速度