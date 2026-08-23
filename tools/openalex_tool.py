import requests
from agents import function_tool


@function_tool
def search_openalex(query: str, max_results: int = 5) -> str:
    """Search OpenAlex for scholarly works and return source-backed metadata."""
    try:
        response = requests.get(
            "https://api.openalex.org/works",
            params={"search": query, "per-page": max_results},
            timeout=15,
            headers={"User-Agent": "AI-Research-Scientist/1.0"},
        )
        response.raise_for_status()
        works = response.json().get("results", [])
        if not works:
            return "No OpenAlex results were found."

        results = []
        for work in works:
            authors = ", ".join(
                a.get("author", {}).get("display_name", "Unknown")
                for a in work.get("authorships", [])[:8]
            )
            results.append(
                "Title: {title}\nAuthors: {authors}\nYear: {year}\nDOI: {doi}\nURL: {url}".format(
                    title=work.get("display_name", "Unknown title"),
                    authors=authors or "Unknown",
                    year=work.get("publication_year", "Unknown"),
                    doi=work.get("doi", "Not available"),
                    url=work.get("id", "Not available"),
                )
            )
        return "\n\n".join(results)
    except Exception as exc:
        return f"OpenAlex search failed: {exc}"
