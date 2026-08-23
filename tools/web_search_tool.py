import re
from html import unescape
from urllib.parse import quote_plus

import requests
from agents import function_tool


@function_tool
def web_search(query: str, max_results: int = 5) -> str:
    """Search the public web using DuckDuckGo's HTML endpoint."""
    try:
        response = requests.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15,
        )
        response.raise_for_status()
        html = response.text
        blocks = re.findall(r'class="result__a"[^>]*>(.*?)</a>', html, flags=re.S)
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a?>', html, flags=re.S)
        if not blocks:
            return "No web search results were found."

        results = []
        for i, raw_title in enumerate(blocks[:max_results]):
            title = re.sub(r"<.*?>", "", raw_title)
            title = unescape(title).strip()
            snippet = ""
            if i < len(snippets):
                snippet = unescape(re.sub(r"<.*?>", "", snippets[i])).strip()
            results.append(f"Title: {title}\nSnippet: {snippet}")
        return "\n\n".join(results)
    except Exception as exc:
        return f"Web search failed: {exc}"
