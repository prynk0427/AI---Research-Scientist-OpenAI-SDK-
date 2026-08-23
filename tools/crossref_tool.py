import requests
from agents import function_tool


@function_tool
def search_crossref(query: str, max_results: int = 5) -> str:
    """Search Crossref for scholarly publication metadata."""
    try:
        response = requests.get(
            "https://api.crossref.org/works",
            params={"query.bibliographic": query, "rows": max_results},
            timeout=15,
            headers={"User-Agent": "AI-Research-Scientist/1.0 (mailto:research@example.com)"},
        )
        response.raise_for_status()
        items = response.json().get("message", {}).get("items", [])
        if not items:
            return "No Crossref results were found."

        results = []
        for item in items:
            authors = ", ".join(
                " ".join(filter(None, [a.get("given"), a.get("family")]))
                for a in item.get("author", [])[:8]
            )
            results.append(
                "Title: {title}\nAuthors: {authors}\nPublished: {date}\nDOI: {doi}\nURL: {url}".format(
                    title=(item.get("title") or ["Unknown title"])[0],
                    authors=authors or "Unknown",
                    date=(item.get("published-print") or item.get("published-online") or {}).get("date-parts", [["Unknown"]])[0][0],
                    doi=item.get("DOI", "Not available"),
                    url=item.get("URL", "Not available"),
                )
            )
        return "\n\n".join(results)
    except Exception as exc:
        return f"Crossref search failed: {exc}"
