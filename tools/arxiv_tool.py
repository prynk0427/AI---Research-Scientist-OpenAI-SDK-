import arxiv
from agents import function_tool


@function_tool
def search_arxiv(query: str, max_results: int = 5) -> str:
    """Search arXiv for relevant research papers."""
    try:
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        client = arxiv.Client()
        papers = []
        for paper in client.results(search):
            authors = ", ".join(author.name for author in paper.authors)
            papers.append(
                f"Title: {paper.title}\n"
                f"Authors: {authors}\n"
                f"Published: {paper.published.strftime('%Y-%m-%d')}\n"
                f"Abstract:\n{paper.summary}\n"
                f"URL: {paper.entry_id}"
            )
        return "\n\n".join(papers) if papers else "No relevant papers were found on arXiv."
    except Exception as exc:
        return f"arXiv search failed: {exc}"
