"""真实的天气查询函数（mock 实现，不请求任何外部 API）.

记忆点：工具调用 = LLM 只出「意图 JSON」，真正干活的是这里的 Python 函数。
"""

# 模拟天气数据库：城市 -> 天气数据（写死，便于验证，不联网）
MOCK_WEATHER: dict[str, dict] = {
    "北京": {"temperature": 32, "condition": "晴", "feels_like": 35, "advice": "天气炎热，注意防晒补水，出门记得带伞"},
    "上海": {"temperature": 30, "condition": "多云", "feels_like": 32, "advice": "多云天气，体感偏热，适合穿短袖"},
    "广州": {"temperature": 33, "condition": "雷阵雨", "feels_like": 37, "advice": "有雷阵雨，记得带伞，注意防雷"},
    "深圳": {"temperature": 31, "condition": "小雨", "feels_like": 34, "advice": "小雨天气，带伞出行，路面湿滑注意安全"},
}

# 未收录城市的兜底数据
DEFAULT_WEATHER: dict[str, int | str] = {
    "temperature": 25,
    "condition": "多云",
    "feels_like": 26,
    "advice": "天气宜人，适合出行",
}


def query_weather(city: str) -> dict:
    """查询指定城市的当前天气（返回 mock 数据，不联网）。

    Args:
        city: 城市名称，如 "北京"。

    Returns:
        dict: 包含 city / temperature / condition / feels_like / advice 的天气数据。
    """
    data = MOCK_WEATHER.get(city, DEFAULT_WEATHER).copy()
    data["city"] = city
    return data
