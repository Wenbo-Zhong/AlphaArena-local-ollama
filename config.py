"""
Alpha Arena 配置文件
集中管理所有可调参数
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==================== AI 模型配置 ====================

# 推理模型使用策略
REASONER_INTERVAL_SECONDS = 180  # 推理模型最小调用间隔（秒）- 默认5分钟，与REASONER_MODEL_INTERVAL_SECONDS保持一致

# 强制使用推理模型的场景（即使未到时间间隔）
USE_REASONER_FOR_OPENING = True  # 开仓决策使用推理模型
USE_REASONER_FOR_HIGH_VOLATILITY = True  # 高波动市场（24h>5%）使用推理模型
USE_REASONER_FOR_LARGE_LOSS = True  # 大额亏损持仓（>10%）使用推理模型

# ==================== 日志管理配置 ====================

# 胜率显示策略
MIN_TRADES_FOR_WINRATE = 20  # 最少多少笔交易才显示胜率（避免误导AI）
SHOW_WINRATE_IN_PROMPT = False  # 是否在AI prompt中显示胜率（开发阶段建议False）

# AI参考历史数据起始日期（格式：YYYY-MM-DD，None表示全部历史）
AI_REFERENCE_START_DATE = None  # 例如: '2025-10-22' 表示只让AI看这天之后的数据

# ==================== 交易配置 ====================

# Binance API
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
BINANCE_TESTNET = os.getenv('BINANCE_TESTNET', 'false').lower() == 'true'

# Ollama API
OLLAMA_API_KEY = os.getenv('OLLAMA_API_KEY')

# 交易参数
INITIAL_CAPITAL = float(os.getenv('INITIAL_CAPITAL', '20'))
MAX_POSITION_PCT = float(os.getenv('MAX_POSITION_PCT', '10'))
DEFAULT_LEVERAGE = int(os.getenv('DEFAULT_LEVERAGE', '3'))
TRADING_INTERVAL_SECONDS = int(os.getenv('TRADING_INTERVAL_SECONDS', '120'))

# 交易对
TRADING_SYMBOLS_STR = os.getenv('TRADING_SYMBOLS', 'BTCUSDT,ETHUSDT,SOLUSDT,BNBUSDT,DOGEUSDT,XRPUSDT')
TRADING_SYMBOLS = [s.strip() for s in TRADING_SYMBOLS_STR.split(',')]

# 交易冷却期
TRADE_COOLDOWN_SECONDS = 900  # 失败后冷却15分钟

# ==================== 风险管理配置 ====================

MAX_PORTFOLIO_RISK = 0.02  # 单笔交易最大风险（2%）
MAX_POSITION_SIZE = float(os.getenv('MAX_POSITION_PCT', 10)) / 100  # 最大持仓比例
MAX_LEVERAGE = 50  # 最大杠杆倍数
MAX_DRAWDOWN = 0.15  # 最大回撤（15%）
MAX_DAILY_LOSS = 0.05  # 每日最大亏损（5%）
MAX_POSITIONS = 10  # 最大持仓数量
MAX_DAILY_TRADES = 100  # 每日最大交易次数

# AI决策相关配置
MIN_TRADES_FOR_WINRATE = 5  # 计算胜率所需的最少交易次数
LOW_WINRATE_THRESHOLD = 0.4  # 低胜率阈值（40%）
HIGH_WINRATE_THRESHOLD = 0.6  # 高胜率阈值（60%）
DEFAULT_AI_STOP_LOSS_PCT = 0.01  # AI未提供止损时的默认值（1%）
DEFAULT_AI_TAKE_PROFIT_PCT = 0.02  # AI未提供止盈时的默认值（2%）

# AI模型配置
CHAT_MODEL_INTERVAL_SECONDS = 120  # 快速反应模型分析间隔（秒）
REASONER_MODEL_INTERVAL_SECONDS = 180  # 深度分析模型分析间隔（秒）

# 显示配置
ACCOUNT_DISPLAY_INTERVAL_SECONDS = 120  # 账户信息显示间隔（秒）
FORCE_CLOSE_PROFIT_TARGET_USD = 2.0  # 强制止盈目标（美元）

# ==================== 性能追踪配置 ====================

PERFORMANCE_DATA_FILE = 'performance_data.json'
AI_DECISIONS_FILE = 'ai_decisions.json'
LOG_CONFIG_FILE = 'log_config.json'

# ==================== Ollama 配置 ====================

# Ollama API 配置
OLLAMA_MAX_TOKENS = int(os.getenv('OLLAMA_MAX_TOKENS', '32768'))  # 最大令牌数
OLLAMA_TEMPERATURE = float(os.getenv('OLLAMA_TEMPERATURE', '0.3'))  # 温度参数
OLLAMA_API_TIMEOUT = int(os.getenv('OLLAMA_API_TIMEOUT', '150'))  # API超时时间（秒）
OLLAMA_API_PORT = int(os.getenv('OLLAMA_API_PORT', '11434'))  # API端口

# ==================== 高级功能配置 ====================

# 高级仓位管理策略
ENABLE_ADVANCED_STRATEGIES = True  # 是否启用高级策略（ROLL, PYRAMID等）

# ==================== 滚仓策略配置 ====================

# 激进滚仓配置
ROLLING_PROFIT_THRESHOLD_PCT = 0.8  # 盈利触发滚仓的百分比（%）
ROLLING_RATIO = 0.6  # 每次滚仓使用浮盈的比例
ROLLING_MAX_ROLLS = 3  # 最多滚仓次数
ROLLING_MIN_INTERVAL_MINUTES = 1  # 最少滚仓间隔（分钟）

# ==================== 止损止盈配置 ====================

# ATR动态止损
ATR_MULTIPLIER = 2.0  # ATR倍数

# 默认止损止盈百分比
DEFAULT_STOP_LOSS_PCT = 0.015  # 默认止损百分比（1.5%）
DEFAULT_TAKE_PROFIT_PCT = 0.05  # 默认止盈百分比（5%）
TRAILING_STOP_PCT = 0.01  # 移动止损百分比（1%）

# 风险阈值
MARGIN_CALL_THRESHOLD = 0.8  # 保证金率警戒阈值（80%）
MAX_CORRELATION = 0.7  # 最大相关性阈值（0.7）
