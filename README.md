# 🏆 Alpha Arena - Ollama Model Trading Bot

灵感来自 [nof1.ai](https://nof1.ai) 的 Alpha Arena 实验，这是一个使用 Ollama Model 驱动的永不停机的加密货币量化交易系统。

## 📖 项目简介

Alpha Arena 是一个完全自主的 AI 交易机器人，它：
- 🤖 使用 Ollama Model 进行智能交易决策
- 📊 实时分析市场技术指标（RSI、MACD、布林带等）
- ⚡ 自动执行交易（开多、开空、止损、止盈）
- 📈 追踪性能指标（夏普比率、最大回撤、胜率等）
- 🌐 提供 Web 仪表板实时监控
- 🔄 **永不停机** - 24/7 持续运行
- 🎯 高级仓位管理（浮盈滚仓、追踪止损等）
- 🛡️ 完善的风险管理和健康监控
- 📝 专业的日志记录和决策分析

### 与 nof1.ai Alpha Arena 的对比

nof1.ai 的 Alpha Arena 让 6 个 AI 模型（GPT-5、Gemini 2.5、Grok-4、Claude Sonnet 4.5、DeepSeek-V3、Qwen3 Max）各自使用 $10,000 在 Hyperliquid 交易所进行真实交易竞赛。

**我们的系统**：
- 在 Binance 交易所运行
- 完全开源，可自定义
- 永久运行，持续优化
- 支持高级交易策略（浮盈滚仓、追踪止损等）
- 提供双版本仪表板（Flask + Next.js）

## 🎯 核心功能

### 1. AI 驱动的交易决策
- 基于技术指标和趋势分析做出决策
- 动态调整仓位和杠杆
- 智能止损止盈
- 增强决策引擎，整合市场上下文信息
- 支持推理模型的智能调用策略

### 2. 性能追踪系统
类似 nof1.ai 的 SharpeBench，追踪：
- ✅ 账户价值和收益率
- ✅ 夏普比率（风险调整后收益）
- ✅ 最大回撤
- ✅ 胜率
- ✅ 交易次数和手续费
- ✅ 每日收益

### 3. 高级仓位管理
- 浮盈滚仓功能，最大化盈利空间
- 追踪止损管理器，锁定盈利
- ROLL状态追踪器，监控持仓状态
- 高级仓位策略配置

### 4. Web 仪表板
#### Flask 仪表板（快速启动）
- 实时显示交易表现
- 资金曲线图表
- 交易历史记录
- 自动刷新（每 10 秒）

#### Next.js 仪表板（Framer风格）
- ✨ 现代暗黑主题设计
- 📊 实时数据可视化
- 🎨 平滑动画效果
- 📱 响应式设计，支持移动设备

### 5. 风险管理
- 仓位大小控制
- 自动止损止盈
- 最大回撤保护
- 每日亏损限制
- 高波动市场保护
- 大额亏损持仓管理

### 6. 系统管理
- 健康监控和自动恢复
- 数据备份和恢复功能
- 专业的日志系统
- 彩色交易日志，便于分析
- 决策记录和查看工具

### 7. 监控工具
- 滚仓状态监控
- 系统状态监控
- 一键重启和清理脚本

## 🚀 快速开始

### 1. 前置要求

- Python 3.8+
- Binance 账户和 API 密钥
- Ollama Model API 密钥

### 2. 安装依赖

```bash
# 安装 Python 依赖
pip3 install -r requirements.txt

# 如需使用 Next.js 仪表板，额外安装前端依赖
cd framer-dashboard
npm install
```

### 3. 配置

#### 3.1 主要配置文件

**环境变量文件 (.env)**：
```bash
# Binance API
BINANCE_API_KEY=your_binance_api_key
BINANCE_API_SECRET=your_binance_secret
BINANCE_TESTNET=false

# v2ray proxy
USING_V2RAY_PROXY=1
V2RAY_PORT=10808

# Ollama API
OLLAMA_API_KEY=your_ollama_api_key
OLLAMA_MODEL_NAME=qwen2.5:14b-instruct-q8_0

# 交易配置
INITIAL_CAPITAL=500
MAX_POSITION_PCT=10             # 最大单次仓位占比
DEFAULT_LEVERAGE=3              # 默认杠杆
TRADING_INTERVAL_SECONDS=180    # 交易间隔（默认180秒）

# 交易对（多个用逗号分隔）
TRADING_SYMBOLS=BTCUSDT,ETHUSDT,SOLUSDT,BNBUSDT,DOGEUSDT,XRPUSDT
```

**高级配置文件 (config.py)**：

```python
# ==================== AI 模型配置 ====================
REASONER_INTERVAL_SECONDS = 600  # 推理模型最小调用间隔（秒）- 默认10分钟
USE_REASONER_FOR_OPENING = True  # 开仓决策使用推理模型
USE_REASONER_FOR_HIGH_VOLATILITY = True  # 高波动市场（24h>5%）使用推理模型
USE_REASONER_FOR_LARGE_LOSS = True  # 大额亏损持仓（>10%）使用推理模型

# ==================== 日志管理配置 ====================
MIN_TRADES_FOR_WINRATE = 20  # 最少多少笔交易才显示胜率
SHOW_WINRATE_IN_PROMPT = False  # 是否在AI prompt中显示胜率

# ==================== 风险管理配置 ====================
MAX_PORTFOLIO_RISK = 0.02  # 单笔交易最大风险（2%）
MAX_DRAWDOWN = 0.15  # 最大回撤（15%）
MAX_DAILY_LOSS = 0.05  # 每日最大亏损（5%）
MAX_POSITIONS = 10  # 最大持仓数量

# ==================== 高级功能配置 ====================
ENABLE_ADVANCED_STRATEGIES = True  # 是否启用高级策略（ROLL, PYRAMID等）
```

### 4. 启动机器人

```bash
./start.sh
```

或者直接运行：

```bash
python3 alpha_arena_bot.py
```

### 5. 启动 Web 仪表板

#### 5.1 Flask 仪表板（快速启动）

在另一个终端窗口：

```bash
python3 web_dashboard.py
```

然后访问：http://localhost:5000

#### 5.2 Next.js 仪表板（Framer风格）

**安装依赖：**
```bash
cd framer-dashboard
npm install
```

**配置环境变量：**
```bash
cp .env.local.example .env.local
# 编辑 .env.local 文件，填入 Binance API 密钥
```

**启动开发服务器：**
```bash
npm run dev
```

然后访问：http://localhost:3000

**构建生产版本：**
```bash
npm run build
npm run start
```

## 📊 项目结构

```
AlphaArena-local-ollama/
├── alpha_arena_bot.py            # 主交易机器人
├── ollama_client.py              # Ollama Model API 客户端
├── ai_trading_engine.py          # AI 交易引擎
├── enhanced_decision_engine.py   # 增强决策引擎
├── performance_tracker.py        # 性能追踪系统
├── web_dashboard.py              # Flask Web 仪表板
├── binance_client.py             # Binance API 客户端
├── market_analyzer.py            # 市场分析器
├── risk_manager.py               # 风险管理器
├── advanced_position_manager.py  # 高级仓位管理
├── rolling_position_manager.py   # 浮盈滚仓管理器
├── trailing_stop_manager.py      # 追踪止损管理器
├── roll_tracker.py               # ROLL状态追踪器
├── health_monitor.py             # 健康监控器
├── backup_manager.py             # 备份管理器
├── log_manager.py                # 日志管理器
├── colored_log_formatter.py      # 彩色日志格式化器
├── pro_log_formatter.py          # 专业交易日志格式化器
├── colored_logger.py             # 彩色日志记录器
├── config.py                     # 配置文件
├── manage.sh                     # 管理脚本
├── monitor_rolling.sh            # 滚仓监控脚本
├── monitor_status.sh             # 状态监控脚本
├── restart_clean.sh              # 重启清理脚本
├── view_decisions.py             # 决策查看工具
├── verify_enhanced_data.py       # 数据验证工具
├── remove_stat_card_tooltips.py  # 移除统计卡片提示工具
├── .env                          # 环境配置文件
├── requirements.txt              # Python 依赖
├── start.sh                      # 启动脚本
├── performance_data.json         # 性能数据（自动生成）
├── ai_decisions.json             # AI决策记录（自动生成）
├── logs/                         # 日志目录
├── templates/                    # Flask 模板
│   ├── dashboard.html
│   └── dashboard.html.backup
├── static/                       # 静态文件
│   └── sw.js
├── tests/                        # 测试文件
│   ├── test_advanced_strategies.py
│   ├── test_enhanced_system.py
│   ├── test_integration.py
│   ├── test_production_readiness.py
│   └── test_rolling_live.py
└── framer-dashboard/             # Next.js 仪表板
    ├── app/                      # Next.js App Router
    ├── components/               # React 组件
    ├── .env.local.example
    ├── package.json
    └── ...
```

## 🎮 使用说明

### 永不停机运行

系统设计为 24/7 持续运行：

1. **自动重试**：遇到错误自动重试
2. **优雅关闭**：支持 Ctrl+C 优雅退出
3. **数据持久化**：所有交易和性能数据自动保存
4. **日志记录**：详细的日志文件

### 后台运行（推荐）

使用 `screen` 或 `tmux` 在后台运行：

```bash
# 使用 screen
screen -S alpha_arena
./start.sh
# 按 Ctrl+A 然后 D 脱离会话

# 重新连接
screen -r alpha_arena
```

或使用 `nohup`：

```bash
nohup ./start.sh > output.log 2>&1 &
```

### 监控运行状态

```bash
# 查看实时日志
tail -f logs/alpha_arena_*.log

# 查看 Web 仪表板
# 访问 http://localhost:5000
```

## 📈 性能指标说明

### Sharpe Ratio（夏普比率）
- 衡量风险调整后的收益
- > 1.0 = 良好
- > 2.0 = 优秀
- > 3.0 = 卓越

### Max Drawdown（最大回撤）
- 从峰值到谷底的最大跌幅
- 越小越好
- < 10% = 优秀
- < 20% = 良好

### Win Rate（胜率）
- 盈利交易占总交易的百分比
- > 50% = 不错
- > 60% = 良好
- > 70% = 优秀

## ⚠️ 风险警告

**重要提示**：

1. ⚠️ 加密货币交易存在高风险，可能导致资金损失
2. 🧪 建议先在 Binance 测试网测试（设置 `BINANCE_TESTNET=true`）
3. 💰 只投入你能承受损失的资金
4. 📊 定期监控机器人运行状态
5. 🔐 妥善保管 API 密钥，不要分享给他人
6. 🛡️ 建议设置 IP 白名单限制 API 访问

## 🔧 高级配置

### 调整交易频率

在 `.env` 中修改：
```bash
TRADING_INTERVAL_SECONDS=300  # 5分钟
```

### 调整仓位和杠杆

```bash
MAX_POSITION_PCT=5      # 最大单次仓位 5%
DEFAULT_LEVERAGE=2      # 默认杠杆 2x
```

### 修改交易对

```bash
TRADING_SYMBOLS=BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,ADAUSDT
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- 灵感来自 [nof1.ai](https://nof1.ai) 的 Alpha Arena 实验
- 基于 [Binance](https://www.binance.com) 交易所

---

**祝交易顺利！🚀**
