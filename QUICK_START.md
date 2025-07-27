# 🚀 TradingAgents-CN 快速开始指南

> 📋 **版本**: cn-0.1.10 | **更新时间**: 2025-07-27  
> 🎯 **目标**: 5分钟内完成部署并开始股票分析  
> 💡 **适用**: 所有用户，特别推荐新手用户

## 🎯 选择部署方式

### 🐳 方式一：Docker部署 (强烈推荐)

**适用场景**: 生产环境、快速体验、零配置启动

```bash
# 1. 克隆项目
git clone https://github.com/hsliuping/TradingAgents-CN.git
cd TradingAgents-CN

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入API密钥（详见下方配置说明）

# 3. 构建并启动服务
docker-compose up -d --build

# 4. 访问应用
# Web界面: http://localhost:8501
# Redis管理: http://localhost:8081
# MongoDB管理: http://localhost:8082
```

**首次运行说明**:
- 构建时间: 5-10分钟（下载依赖和构建镜像）
- 镜像大小: ~800MB
- 包含工具: pandoc, wkhtmltopdf等报告导出工具

### 💻 方式二：本地开发部署

**适用场景**: 开发环境、自定义配置、学习研究

```bash
# 1. 克隆项目
git clone https://github.com/hsliuping/TradingAgents-CN.git
cd TradingAgents-CN

# 2. 创建虚拟环境
python -m venv env
source env/bin/activate  # Linux/Mac
# 或 env\\Scripts\\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 5. 启动应用
python -m streamlit run interfaces/streamlit/app.py --server.port 8501
# 或使用便捷脚本
./start_web.sh  # Linux/Mac
# start_web.bat  # Windows
```

### 🚀 方式三：统一启动器 (推荐开发者)

```bash
# 使用新的统一启动器
python start_app.py --ui streamlit  # 启动Streamlit界面
python start_app.py --ui flask      # 启动Flask界面
python start_app.py --ui auto       # 自动选择界面
```

## 🔑 API密钥配置

### 必需配置 (至少配置一个AI模型)

#### 🇨🇳 DeepSeek V3 (推荐，性价比最高)
```bash
# 获取地址: https://platform.deepseek.com/
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_ENABLED=true
```

#### 🇨🇳 阿里百炼 (国产稳定)
```bash
# 获取地址: https://dashscope.aliyun.com/
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 🌍 其他AI模型 (可选)
```bash
# OpenAI
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Anthropic Claude
ANTHROPIC_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Google AI
GOOGLE_API_KEY=AIxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 数据源配置 (推荐配置)

#### 📈 Tushare (A股数据，推荐)
```bash
# 获取地址: https://tushare.pro/
TUSHARE_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TUSHARE_ENABLED=true
```

#### 📊 FinnHub (美股数据)
```bash
# 获取地址: https://finnhub.io/
FINNHUB_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 🎯 快速验证

### 1. 检查配置状态
```bash
# 激活环境
source env/bin/activate  # 或 source activate_env.sh

# 检查配置
python -m cli.main config

# 测试配置
python -m cli.main test
```

### 2. 访问Web界面
- 打开浏览器访问: http://localhost:8501
- 选择股票代码进行分析测试
- 推荐测试股票: AAPL (美股) 或 000001 (A股)

### 3. 功能验证清单
- [ ] 页面正常加载
- [ ] API状态检查通过
- [ ] 能够选择AI模型
- [ ] 能够输入股票代码
- [ ] 分析进度正常显示
- [ ] 能够查看分析报告

## 📚 进阶使用

### 🔧 系统配置
- **模型配置**: 在Web界面的"🤖 模型配置"页面切换AI模型
- **系统设置**: 在"⚙️ 系统设置"页面查看API状态和系统信息
- **分析历史**: 在"📋 分析历史"页面查看历史分析记录

### 📊 分析功能
- **股票分析**: 支持美股、A股、港股分析
- **多维度分析**: 技术面、基本面、新闻面、社交媒体情绪
- **报告导出**: 支持PDF、Word、Markdown格式导出
- **实时进度**: 异步进度跟踪，实时显示分析状态

### 🛠️ 开发功能
- **CLI工具**: 使用`python -m cli.main`进行命令行操作
- **API接口**: 支持程序化调用分析功能
- **自定义配置**: 支持自定义分析深度和分析师组合

## 🆘 常见问题

### Q: Docker构建失败怎么办？
A: 检查Docker版本(>=20.10)，确保网络连接正常，可以使用国内镜像源。

### Q: API密钥配置后仍然报错？
A: 检查密钥格式是否正确，确认API服务可用，查看系统设置页面的API状态。

### Q: 分析速度很慢？
A: 建议使用DeepSeek V3模型（速度快、成本低），检查网络连接，降低分析深度。

### Q: 如何切换不同的AI模型？
A: 在Web界面侧边栏选择模型，或在"🤖 模型配置"页面进行详细配置。

## 📖 更多资源

- **详细文档**: [docs/](./docs/) 目录
- **安装指南**: [docs/INSTALLATION_GUIDE.md](./docs/INSTALLATION_GUIDE.md)
- **Docker部署**: [docs/features/docker-deployment.md](./docs/features/docker-deployment.md)
- **API配置**: [docs/configuration/](./docs/configuration/)
- **故障排除**: [docs/troubleshooting/](./docs/troubleshooting/)

## 🎉 开始使用

配置完成后，您就可以开始使用TradingAgents-CN进行专业的股票分析了！

1. 访问 http://localhost:8501
2. 在侧边栏选择AI模型
3. 输入股票代码（如AAPL、000001）
4. 选择分析师和分析深度
5. 点击"开始分析"
6. 等待分析完成并查看报告

祝您投资顺利！📈

---

**需要帮助？** 
- 📧 提交Issue: [GitHub Issues](https://github.com/hsliuping/TradingAgents-CN/issues)
- 💬 讨论交流: [GitHub Discussions](https://github.com/hsliuping/TradingAgents-CN/discussions)
- 📖 查看文档: [完整文档](./docs/)