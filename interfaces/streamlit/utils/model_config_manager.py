"""
模型配置管理器
用于管理和切换不同的LLM模型配置
"""

import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class ModelConfig:
    """模型配置数据类"""
    name: str
    display_name: str
    provider: str
    api_key_env: str
    base_url_env: Optional[str] = None
    enabled_env: Optional[str] = None
    deep_think_model: str = ""
    quick_think_model: str = ""
    description: str = ""
    is_available: bool = False

class ModelConfigManager:
    """模型配置管理器"""
    
    def __init__(self):
        # 获取正确的配置文件路径（相对于项目根目录）
        current_file_path = Path(__file__)
        project_root = current_file_path.parent.parent.parent.parent
        self.config_file = project_root / "interfaces" / "streamlit" / "config" / "model_configs.json"
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self._init_default_configs()
    
    def _init_default_configs(self):
        """初始化默认模型配置"""
        default_configs = {
            "custom_anthropic": {
                "name": "custom_anthropic",
                "display_name": "自定义模型 (Anthropic兼容)",
                "provider": "anthropic",
                "api_key_env": "DEEPSEEK_API_KEY",
                "base_url_env": "DEEPSEEK_BASE_URL",
                "enabled_env": "DEEPSEEK_ENABLED",
                "deep_think_model": "claude-3-5-sonnet-20241022",
                "quick_think_model": "claude-3-5-haiku-20241022",
                "description": "使用自定义API端点的Anthropic兼容模型"
            },
            "dashscope": {
                "name": "dashscope",
                "display_name": "阿里百炼 (通义千问)",
                "provider": "dashscope",
                "api_key_env": "DASHSCOPE_API_KEY",
                "deep_think_model": "qwen-max",
                "quick_think_model": "qwen-plus",
                "description": "阿里云百炼平台的通义千问模型"
            },
            "openai": {
                "name": "openai",
                "display_name": "OpenAI GPT",
                "provider": "openai",
                "api_key_env": "OPENAI_API_KEY",
                "deep_think_model": "gpt-4o",
                "quick_think_model": "gpt-4o-mini",
                "description": "OpenAI的GPT系列模型"
            },
            "google": {
                "name": "google",
                "display_name": "Google Gemini",
                "provider": "google",
                "api_key_env": "GOOGLE_API_KEY",
                "deep_think_model": "gemini-2.0-flash",
                "quick_think_model": "gemini-2.0-flash",
                "description": "Google的Gemini系列模型"
            },
            "anthropic": {
                "name": "anthropic",
                "display_name": "Anthropic Claude",
                "provider": "anthropic",
                "api_key_env": "ANTHROPIC_API_KEY",
                "deep_think_model": "claude-3-5-sonnet-20241022",
                "quick_think_model": "claude-3-5-haiku-20241022",
                "description": "Anthropic的Claude系列模型"
            }
        }
        
        if not self.config_file.exists():
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_configs, f, indent=2, ensure_ascii=False)
    
    def get_available_models(self) -> List[ModelConfig]:
        """获取所有可用的模型配置"""
        with open(self.config_file, 'r', encoding='utf-8') as f:
            configs = json.load(f)
        
        models = []
        for config_data in configs.values():
            model = ModelConfig(**config_data)
            # 检查API密钥是否配置
            api_key = os.getenv(model.api_key_env)
            model.is_available = bool(api_key and api_key != "your_api_key_here" and api_key != "xxx")
            models.append(model)
        
        return models
    
    def get_current_model(self) -> str:
        """获取当前使用的模型"""
        # 检查环境变量中启用的模型
        if os.getenv("DEEPSEEK_ENABLED", "false").lower() == "true":
            return "custom_anthropic"
        elif os.getenv("DASHSCOPE_API_KEY") and os.getenv("DASHSCOPE_API_KEY") != "xxx":
            return "dashscope"
        elif os.getenv("OPENAI_API_KEY"):
            return "openai"
        elif os.getenv("GOOGLE_API_KEY"):
            return "google"
        elif os.getenv("ANTHROPIC_API_KEY"):
            return "anthropic"
        else:
            return "custom_anthropic"  # 默认使用自定义模型
    
    def get_model_config(self, model_name: str) -> Optional[ModelConfig]:
        """获取指定模型的配置"""
        models = self.get_available_models()
        for model in models:
            if model.name == model_name:
                return model
        return None
    
    def update_env_file(self, model_name: str) -> bool:
        """更新.env文件以启用指定模型"""
        try:
            model = self.get_model_config(model_name)
            if not model:
                return False
            
            # 读取当前.env文件
            env_file = Path(".env")
            if not env_file.exists():
                return False
            
            with open(env_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 更新配置
            updated_lines = []
            for line in lines:
                if line.startswith("DEEPSEEK_ENABLED="):
                    if model_name == "custom_anthropic":
                        updated_lines.append("DEEPSEEK_ENABLED=true\n")
                    else:
                        updated_lines.append("DEEPSEEK_ENABLED=false\n")
                else:
                    updated_lines.append(line)
            
            # 写回文件
            with open(env_file, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)
            
            return True
        except Exception as e:
            print(f"更新环境文件失败: {e}")
            return False
    
    def get_model_for_analysis(self, model_name: str) -> Dict[str, Any]:
        """获取用于分析的模型配置"""
        model = self.get_model_config(model_name)
        if not model:
            # 默认使用自定义模型
            model = self.get_model_config("custom_anthropic")
        
        if not model:
            raise ValueError("无法找到可用的模型配置")
        
        config = {
            "llm_provider": model.provider,
            "deep_think_llm": model.deep_think_model,
            "quick_think_llm": model.quick_think_model,
        }
        
        # 设置API端点
        if model.provider == "dashscope":
            config["backend_url"] = "https://dashscope.aliyuncs.com/api/v1"
        elif model.provider == "anthropic" and model.name == "custom_anthropic":
            # 自定义Anthropic兼容端点
            base_url = os.getenv("DEEPSEEK_BASE_URL", "https://anyrouter.top")
            config["backend_url"] = base_url
        elif model.provider == "google":
            config["backend_url"] = "https://generativelanguage.googleapis.com/v1"
        
        return config

# 全局实例
model_config_manager = ModelConfigManager()