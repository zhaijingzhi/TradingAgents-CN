"""
API密钥检查工具
"""

import os
from dotenv import load_dotenv

# 确保加载.env文件
load_dotenv()

def check_api_keys():
    """检查所有必要的API密钥是否已配置"""

    # 检查各个API密钥，过滤掉占位符值
    dashscope_key = os.getenv("DASHSCOPE_API_KEY")
    finnhub_key = os.getenv("FINNHUB_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    tushare_token = os.getenv("TUSHARE_TOKEN")
    
    # 定义占位符值，这些不算有效配置
    placeholder_values = {
        "your_finnhub_api_key_here",
        "your_openai_api_key_here", 
        "your_google_api_key_here",
        "your_anthropic_api_key_here",
        "your_deepseek_api_key_here"
    }
    
    # 过滤掉占位符值
    def is_valid_key(key):
        return key and key not in placeholder_values and len(key.strip()) > 10
    
    dashscope_key = dashscope_key if is_valid_key(dashscope_key) else None
    finnhub_key = finnhub_key if is_valid_key(finnhub_key) else None
    openai_key = openai_key if is_valid_key(openai_key) else None
    anthropic_key = anthropic_key if is_valid_key(anthropic_key) else None
    google_key = google_key if is_valid_key(google_key) else None
    deepseek_key = deepseek_key if is_valid_key(deepseek_key) else None
    tushare_token = tushare_token if is_valid_key(tushare_token) else None
    
    # 构建详细状态
    details = {
        "DASHSCOPE_API_KEY": {
            "configured": bool(dashscope_key),
            "display": f"{dashscope_key[:12]}..." if dashscope_key else "未配置",
            "required": False,  # 不是必需的，因为可以用其他AI模型
            "description": "阿里百炼API密钥",
            "category": "AI模型"
        },
        "DEEPSEEK_API_KEY": {
            "configured": bool(deepseek_key),
            "display": f"{deepseek_key[:12]}..." if deepseek_key else "未配置",
            "required": False,  # 不是必需的，因为可以用其他AI模型
            "description": "DeepSeek API密钥",
            "category": "AI模型"
        },
        "OPENAI_API_KEY": {
            "configured": bool(openai_key),
            "display": f"{openai_key[:12]}..." if openai_key else "未配置",
            "required": False,
            "description": "OpenAI API密钥",
            "category": "AI模型"
        },
        "ANTHROPIC_API_KEY": {
            "configured": bool(anthropic_key),
            "display": f"{anthropic_key[:12]}..." if anthropic_key else "未配置",
            "required": False,
            "description": "Anthropic API密钥",
            "category": "AI模型"
        },
        "GOOGLE_API_KEY": {
            "configured": bool(google_key),
            "display": f"{google_key[:12]}..." if google_key else "未配置",
            "required": False,
            "description": "Google AI API密钥",
            "category": "AI模型"
        },
        "TUSHARE_TOKEN": {
            "configured": bool(tushare_token),
            "display": f"{tushare_token[:12]}..." if tushare_token else "未配置",
            "required": False,  # 不是必需的，但推荐用于A股数据
            "description": "Tushare数据API密钥",
            "category": "数据源"
        },
        "FINNHUB_API_KEY": {
            "configured": bool(finnhub_key),
            "display": f"{finnhub_key[:12]}..." if finnhub_key else "未配置",
            "required": False,  # 改为非必需，因为有Tushare作为替代
            "description": "FinnHub金融数据API密钥",
            "category": "数据源"
        }
    }
    
    # 检查是否至少有一个AI模型API密钥配置
    ai_keys_configured = any([dashscope_key, deepseek_key, openai_key, anthropic_key, google_key])
    
    # 如果没有AI模型密钥，将第一个可用的设为必需
    if not ai_keys_configured:
        if dashscope_key is not None:
            details["DASHSCOPE_API_KEY"]["required"] = True
        elif deepseek_key is not None:
            details["DEEPSEEK_API_KEY"]["required"] = True
        else:
            # 如果都没有，建议配置DeepSeek（性价比高）
            details["DEEPSEEK_API_KEY"]["required"] = True
    
    # 检查必需的API密钥
    required_keys = [key for key, info in details.items() if info["required"]]
    missing_required = [key for key in required_keys if not details[key]["configured"]]
    
    return {
        "all_configured": len(missing_required) == 0,
        "required_configured": len(missing_required) == 0,
        "missing_required": missing_required,
        "details": details,
        "summary": {
            "total": len(details),
            "configured": sum(1 for info in details.values() if info["configured"]),
            "required": len(required_keys),
            "required_configured": len(required_keys) - len(missing_required)
        }
    }

def get_api_key_status_message():
    """获取API密钥状态消息"""
    
    status = check_api_keys()
    
    if status["all_configured"]:
        return "✅ 所有必需的API密钥已配置完成"
    elif status["required_configured"]:
        return "✅ 必需的API密钥已配置，可选API密钥未配置"
    else:
        missing = ", ".join(status["missing_required"])
        return f"❌ 缺少必需的API密钥: {missing}"

def validate_api_key_format(key_type, api_key):
    """验证API密钥格式"""
    
    if not api_key:
        return False, "API密钥不能为空"
    
    # 基本长度检查
    if len(api_key) < 10:
        return False, "API密钥长度过短"
    
    # 特定格式检查
    if key_type == "DASHSCOPE_API_KEY":
        if not api_key.startswith("sk-"):
            return False, "阿里百炼API密钥应以'sk-'开头"
    elif key_type == "OPENAI_API_KEY":
        if not api_key.startswith("sk-"):
            return False, "OpenAI API密钥应以'sk-'开头"
    
    return True, "API密钥格式正确"

def test_api_connection(key_type, api_key):
    """测试API连接（简单验证）"""
    
    # 这里可以添加实际的API连接测试
    # 为了简化，现在只做格式验证
    
    is_valid, message = validate_api_key_format(key_type, api_key)
    
    if not is_valid:
        return False, message
    
    # 可以在这里添加实际的API调用测试
    # 例如：调用一个简单的API端点验证密钥有效性
    
    return True, "API密钥验证通过"
