"""
Alpha Arena 配置文件
集中管理所有可调参数
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """主配置类，包含所有子模块配置"""
    
    class AI:
        """AI 模型配置"""
        REASONER_INTERVAL_SECONDS = 180  # 推理模型最小调用间隔（秒）- 默认3分钟
        MIN_TRADES_FOR_WINRATE = 20  # 最少多少笔交易才显示胜率（避免误导AI）
        
    class Trading:
        """交易配置"""
        INITIAL_CAPITAL = float(os.getenv('INITIAL_CAPITAL', '20'))
        MAX_POSITION_PCT = float(os.getenv('MAX_POSITION_PCT', '10'))
        DEFAULT_LEVERAGE = int(os.getenv('DEFAULT_LEVERAGE', '3'))
        TRADING_INTERVAL_SECONDS = int(os.getenv('TRADING_INTERVAL_SECONDS', '120'))
        TRADING_SYMBOLS_STR = os.getenv('TRADING_SYMBOLS', 'BTCUSDT,ETHUSDT,SOLUSDT,BNBUSDT,DOGEUSDT,XRPUSDT')
        TRADING_SYMBOLS = [s.strip() for s in TRADING_SYMBOLS_STR.split(',')]
        TRADE_COOLDOWN_SECONDS = 900  # 失败后冷却15分钟
        ACCOUNT_DISPLAY_INTERVAL_SECONDS = 120  # 账户信息显示间隔（秒）
        
    class Binance:
        """Binance API 配置"""
        API_KEY = os.getenv('BINANCE_API_KEY')
        API_SECRET = os.getenv('BINANCE_API_SECRET')
        TESTNET = os.getenv('BINANCE_TESTNET', 'false').lower() == 'true'
        USING_V2RAY = os.getenv('USING_V2RAY_PROXY', 1)
        V2RAY_PORT = os.getenv('V2RAY_PORT', 10808)
        
    class Ollama:
        """Ollama API 配置"""
        API_KEY = os.getenv('OLLAMA_API_KEY')
        MAX_TOKENS = int(os.getenv('OLLAMA_MAX_TOKENS', '32768'))  # 最大令牌数
        TEMPERATURE = float(os.getenv('OLLAMA_TEMPERATURE', '0.3'))  # 温度参数
        API_TIMEOUT = int(os.getenv('OLLAMA_API_TIMEOUT', '150'))  # API超时时间（秒）
        API_PORT = int(os.getenv('OLLAMA_API_PORT', '11434'))  # API端口
        MODEL_NAME = os.getenv('OLLAMA_MODEL_NAME', '')
        
    class Risk:
        """风险管理配置"""
        MAX_PORTFOLIO_RISK = 0.02  # 单笔交易最大风险（2%）
        MAX_POSITION_SIZE = float(os.getenv('MAX_POSITION_PCT', '10')) / 100  # 最大持仓比例
        MAX_LEVERAGE = 50  # 最大杠杆倍数
        MAX_DRAWDOWN = 0.15  # 最大回撤（15%）
        MAX_DAILY_LOSS = 0.05  # 每日最大亏损（5%）
        MAX_POSITIONS = 10  # 最大持仓数量
        MAX_DAILY_TRADES = 100  # 每日最大交易次数
        ATR_MULTIPLIER = 2.0  # ATR倍数
        DEFAULT_STOP_LOSS_PCT = 0.015  # 默认止损百分比（1.5%）
        DEFAULT_TAKE_PROFIT_PCT = 0.05  # 默认止盈百分比（5%）
        TRAILING_STOP_PCT = 0.01  # 移动止损百分比（1%）
        MARGIN_CALL_THRESHOLD = 0.8  # 保证金率警戒阈值（80%）
        MAX_CORRELATION = 0.7  # 最大相关性阈值（0.7）
        
    class Rolling:
        """滚仓策略配置"""
        ROLLING_PROFIT_THRESHOLD_PCT = 0.8  # 盈利触发滚仓的百分比（%）
        ROLLING_RATIO = 0.6  # 每次滚仓使用浮盈的比例
        ROLLING_MAX_ROLLS = 3  # 最多滚仓次数
        ROLLING_MIN_INTERVAL_MINUTES = 1  # 最少滚仓间隔（分钟）

# 导出配置类，方便直接导入使用
AI = Config.AI
Trading = Config.Trading
Binance = Config.Binance
Ollama = Config.Ollama
Risk = Config.Risk
Rolling = Config.Rolling



