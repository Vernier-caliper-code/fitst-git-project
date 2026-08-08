"""真实的新闻抓取函数：调用 Hacker News 公开 API（免费、无需 key）.

记忆点：工具调用 = LLM 只出「意图 JSON」，真正抓数据的是这里的 Python 函数。
"""

import requests

# Hacker News 公开 API（Firebase 托管，免费无需 key）
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"

TIMEOUT_SECONDS = 10


def fetch_top_stories(limit: int = 10) -> list[dict]:
    """抓取 Hacker News 当前 top 头条。

    Args:
        limit: 返回头条条数（默认 10）。

    Returns:
        list[dict]: 每条含 id / title / url / score。

    Raises:
        requests.RequestException: 网络或 API 异常（由上层工具兜底处理）。
    """
    resp = requests.get(TOP_STORIES_URL, timeout=TIMEOUT_SECONDS)
    resp.raise_for_status()
    story_ids = resp.json()[:limit]

    stories: list[dict] = []
    for sid in story_ids:
        item = requests.get(ITEM_URL.format(id=sid), timeout=TIMEOUT_SECONDS).json()
        # 过滤非 story 类型或无标题的条目
        if item and item.get("type") == "story" and item.get("title"):
            stories.append(
                {
                    "id": item["id"],
                    "title": item["title"],
                    "url": item.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                    "score": item.get("score", 0),
                }
            )
    return stories


if __name__ == "__main__":
    # 自检：抓 5 条，断言字段齐全
    data = fetch_top_stories(5)
    assert len(data) > 0, "应至少抓到 1 条"
    for story in data:
        assert set(story) == {"id", "title", "url", "score"}, "字段不齐"
        print(f"- [{story['score']:>3}] {story['title']}")
    print(f"\n自检通过，共 {len(data)} 条")
