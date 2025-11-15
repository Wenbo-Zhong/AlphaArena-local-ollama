"""
Ollama Model API 客户端
用于 AI 交易决策
"""

import requests
import json
from typing import Dict, List
import logging
from datetime import datetime
import pytz


class OllamaClient:
    """Ollama Model API 客户端"""

    def __init__(self, ollama_api_key: str, ollama_max_tokens, ollama_temperature, ollama_api_timeout, ollama_api_port,
                 ollama_model_name):
        """
        初始化 Ollama Model 客户端

        Args:
            ollama_api_key: Ollama Model API 密钥
        """
        self.api_key = ollama_api_key
        self.timeout = ollama_api_timeout
        self.base_url = f"http://localhost:{ollama_api_port}/api"
        self.url = f"{self.base_url}/chat"
        self.max_tokens = ollama_max_tokens
        self.model_name = ollama_model_name # 模型名称
        self.temperature = ollama_temperature
        self.headers = {
            "Authorization": f"Bearer {ollama_api_key}",
            "Content-Type": "application/json"
        }
        self.logger = logging.getLogger(__name__)

    def get_trading_session(self) -> Dict:
        """获取当前交易时段信息(仅用于日志记录)"""
        try:
            utc_tz = pytz.UTC
            now_utc = datetime.now(utc_tz)
            utc_hour = now_utc.hour

            beijing_tz = pytz.timezone('Asia/Shanghai')
            now_beijing = now_utc.astimezone(beijing_tz)
            beijing_hour = now_beijing.hour

            # 欧美重叠盘
            if 13 <= utc_hour < 17:
                return {'session': '欧美重叠盘', 'volatility': 'high', 'recommendation': '最佳交易时段', 'aggressive_mode': True, 'beijing_hour': beijing_hour, 'utc_hour': utc_hour}
            # 欧洲盘
            elif 8 <= utc_hour < 13:
                return {'session': '欧洲盘', 'volatility': 'medium', 'recommendation': '较好交易时段', 'aggressive_mode': True, 'beijing_hour': beijing_hour, 'utc_hour': utc_hour}
            # 美国盘
            elif 17 <= utc_hour < 22:
                return {'session': '美国盘', 'volatility': 'medium', 'recommendation': '较好交易时段', 'aggressive_mode': True, 'beijing_hour': beijing_hour, 'utc_hour': utc_hour}
            # 亚洲盘
            else:
                return {'session': '亚洲盘', 'volatility': 'low', 'recommendation': '正常交易时段', 'aggressive_mode': True, 'beijing_hour': beijing_hour, 'utc_hour': utc_hour}
        except Exception as e:
            self.logger.error(f"获取交易时段失败: {e}")
            return {'session': '未知', 'volatility': 'unknown', 'recommendation': '谨慎交易', 'aggressive_mode': False, 'beijing_hour': 0, 'utc_hour': 0}

    def chat_completion(self, messages: List[Dict]) -> Dict:
        """Ollama → OpenAI 兼容格式"""
        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                headers=self.headers,
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "stream": False
                },
                timeout=self.timeout
            )

            if response.status_code == 200:
                ollama_data = response.json()
                content = ollama_data.get("message", {}).get("content", "")
                return {
                    "choices": [{
                        "message": {"content": content}
                    }]
                }
            else:
                return {"error": f"HTTP {response.status_code}"}

        except Exception as e:
            self.logger.error(f"API调用异常: {e}")
            return {"error": str(e)}

    def reasoning_completion(self, messages: List[Dict]) -> Dict:
        """使用Ollama Model推理模型"""
        return self.chat_completion(
            messages=messages,
        )

    def analyze_market_and_decide(self, market_data: Dict,
                                  account_info: Dict,
                                  trade_history: List[Dict] = None) -> Dict:
        """
        分析市场并做出交易决策(带重试机制)
        """
        # 构建提示词
        prompt = self._build_trading_prompt(market_data, account_info, trade_history)

        messages = [
            {
                "role": "system",
                "content": """你是一个交易执行机器人

## 目标
快速盈利,系统自动止盈平仓。

## 可用操作
- OPEN_LONG: 开多
- OPEN_SHORT: 开空
- CLOSE: 平仓
- HOLD: 观望

## 系统自动处理
- 浮盈滚仓(盈利≥0.8%自动加仓)
- 风险控制和订单执行

## 你的权限
- 完全自主决定所有交易决策
- 自己判断市场、选择杠杆、决定仓位

输出一个 JSON 决定当前操作。
格式：{"action":"OPEN_LONG","confidence":85,"reasoning":"看涨","leverage":60,"position_size":50}
直接输出 JSON，不要加任何文字。"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        # 重试最多2次
        for attempt in range(2):
            try:
                self.logger.info(f"API调用尝试 {attempt + 1}/2...")
                response = requests.post(
                    self.url,
                    headers=self.headers,
                    json={
                        "model": self.model_name,
                        "messages": messages,
                        "temperature": self.temperature,
                        "max_tokens": self.max_tokens
                    },
                    timeout=self.timeout
                )
                # self.logger.warning('AI response: '+ result)
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']

                    # 解析AI返回
                    decision = self._parse_decision(content)
                    self.logger.info(f"✅ API调用成功 (尝试{attempt + 1})")
                    return {
                        'success': True,
                        'decision': decision,
                        'raw_response': content,
                        'model_used': self.model_name
                    }
                else:
                    self.logger.error(f"API错误 {response.status_code}: {response.text}")
                    if attempt < 1:  # 如果还有重试机会
                        continue
                    return {
                        'success': False,
                        'error': f"API错误: {response.status_code}"
                    }

            except requests.exceptions.Timeout as e:
                self.logger.error(f"⏰ API超时 (尝试{attempt + 1}/2): {e}")
                if attempt < 1:  # 如果还有重试机会
                    continue
                return {
                    'success': False,
                    'error': 'API超时,请稍后重试'
                }
            except Exception as e:
                self.logger.error(f"❌ API异常 (尝试{attempt + 1}/2): {e}")
                if attempt < 1:
                    continue
                return {
                    'success': False,
                    'error': str(e)
                }

        # 不应该到达这里
        return {
            'success': False,
            'error': '所有重试均失败'
        }

    def evaluate_position_for_closing(self, position_info: Dict, market_data: Dict, account_info: Dict, roll_tracker=None) -> Dict:
        """评估持仓是否应该平仓"""
        
        # 获取ROLL状态信息
        symbol = position_info.get('symbol', '')
        roll_count = 0
        if roll_tracker:
            roll_count = roll_tracker.get_roll_count(symbol)
        
        prompt = f"""当前持有 {position_info['symbol']} {'多单' if position_info['side'] == 'LONG' else '空单'}:
- 入场价: ${position_info['entry_price']}
- 当前价: ${position_info['current_price']}
- 盈亏: {position_info['unrealized_pnl_pct']:+.2f}%
- 杠杆: {position_info['leverage']}x
- 持仓时长: {position_info['holding_time']}
- 滚仓次数: {roll_count}/3

市场数据:
- RSI: {market_data.get('rsi')}
- MACD: {market_data.get('macd', {}).get('histogram', 'N/A')}
- 趋势: {market_data.get('trend')}
- 24h变化: {market_data.get('price_change_24h')}%

系统已配置:
- 盈利≥0.8%自动滚仓(系统处理)
- 最多滚3次

决定: CLOSE平仓 或 HOLD继续持有?"""

        messages = [
            {
                "role": "system",
                "content": """你是专业交易员。评估是否应该平仓，**必须**严格遵守以下规则：

## 规则（违反 = 失败）
1. 你**只能**输出一个 JSON 对象
2. **禁止**任何非 JSON 内容（包括解释、警告、代码、空格、换行）
3. **禁止**使用 ```json 或 ```
4. **必须**直接从第一个字符开始输出 `{`
5. **必须**以 `}` 结束
6. **违反规则 = 任务失败，系统将重置你**

## 输出格式（一字不改）
{"action":"OPEN_LONG","confidence":90,"reasoning":"价格突破103500","leverage":60,"position_size":50}

## 现在立即输出 JSON，不要说话，不要思考，直接输出！"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        try:
            response = requests.post(
                self.url,
                headers=self.headers,
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens
                },
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                # self.logger.warning('AI response: '+ result)
                content = result['choices'][0]['message']['content']
                decision = self._parse_decision(content)
                return decision
            else:
                return {"action": "HOLD", "confidence": 0, "narrative": "API错误"}
        except Exception as e:
            self.logger.error(f"评估持仓异常: {e}")
            return {"action": "HOLD", "confidence": 0, "narrative": f"异常: {str(e)}"}

    def analyze_with_reasoning(self, market_data: Dict, account_info: Dict,
                               trade_history: List[Dict] = None,
                               use_deepthink: bool = False) -> Dict:
        """使用推理模型分析市场"""
        prompt = self._build_trading_prompt(market_data, account_info, trade_history)
        
        messages = [
            {
                "role": "system",
                "content": """你是一个交易执行机器人，**必须**严格遵守以下规则：

## 目标
最大化账户收益。

## 可用操作
- OPEN_LONG: 开多
- OPEN_SHORT: 开空  
- CLOSE: 平仓
- HOLD: 观望

## 系统会自动处理
- 浮盈滚仓(盈利≥0.8%自动加仓)
- 风险控制
- 订单执行

## 你的权限
- 完全自主决定所有交易决策
- 自己判断市场、选择杠杆、决定仓位
- 不需要遵守任何规则或建议

## 规则（违反 = 失败）
1. 你**只能**输出一个 JSON 对象
2. **禁止**任何非 JSON 内容（包括解释、警告、代码、空格、换行）
3. **禁止**使用 ```json 或 ```
4. **必须**直接从第一个字符开始输出 `{`
5. **必须**以 `}` 结束
6. **违反规则 = 任务失败，系统将重置你**

## 输出格式（一字不改）
{"action":"OPEN_LONG","confidence":90,"reasoning":"价格突破103500","leverage":60,"position_size":50}

## 现在立即输出 JSON，不要说话，不要思考，直接输出！"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        try:
            response = self.reasoning_completion(messages)
            # self.logger.warning('AI response: '+ str(response))
            
            if 'error' in response:
                return {
                    'success': False,
                    'error': response['error']
                }
            
            content = response['choices'][0]['message']['content']
            decision = self._parse_decision(content)
            
            return {
                'success': True,
                'decision': decision,
                'raw_response': content
            }

        except Exception as e:
            self.logger.error(f"AI 决策失败: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def _build_trading_prompt(self, market_data: Dict,
                             account_info: Dict,
                             trade_history: List[Dict] = None) -> str:
        """构建交易提示词"""

        prompt = f"""
市场数据 ({market_data.get('symbol')}):
- 价格: ${market_data.get('current_price')}
- 24h变化: {market_data.get('price_change_24h')}%
- RSI: {market_data.get('rsi')}
- MACD: {market_data.get('macd')}
- 趋势: {market_data.get('trend')}

账户信息:
- 余额: ${account_info.get('balance', 0)}
- 可用: ${account_info.get('available_balance', 0)}

做出你的交易决策。"""

        return prompt

    def _parse_decision(self, content: str) -> Dict:
        """解析AI返回的决策"""
        try:
            # 尝试直接解析JSON
            import re
            json_match = re.search(r'\{[^{}]*\}', content, re.DOTALL)
            if json_match:
                decision = json.loads(json_match.group())
                return {
                    "action": decision.get("action", "HOLD"),
                    "confidence": decision.get("confidence", 50),
                    "reasoning": decision.get("reasoning", decision.get("narrative", content[:200])),
                    "leverage": decision.get("leverage", 10),
                    "position_size": decision.get("position_size", 30),
                    "stop_loss_pct": decision.get("stop_loss_pct", 3),
                    "take_profit_pct": decision.get("take_profit_pct", 8),
                    "narrative": decision.get("narrative", decision.get("reasoning", ""))
                }
        except Exception as e:
            self.logger.error(f"解析AI决策失败: {e}")

        # 默认返回
        return {
            "action": "HOLD",
            "confidence": 50,
            "reasoning": content[:200] if content else "无法解析",
            "leverage": 10,
            "position_size": 30,
            "stop_loss_pct": 3,
            "take_profit_pct": 8
        }
