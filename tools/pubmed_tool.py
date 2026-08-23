import requests
from agents import function_tool


@function_tool
def search_pubmed(query: str, max_results: int = 5) -> str:
    """Search PubMed through NCBI E-utilities and return verified paper metadata."""
    try:
        params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": max_results,
            "sort": "relevance",
        }
        response = requests.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
            params=params,
            timeout=15,
        )
        response.raise_for_status()
        ids = response.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return "No PubMed results were found."

        fetch = requests.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
            params={"db": "pubmed", "id": ",".join(ids), "retmode": "json"},
            timeout=15,
        )
        fetch.raise_for_status()
        data = fetch.json().get("result", {})

        results = []
        for pmid in ids:
            item = data.get(pmid, {})
            results.append(
                "Title: {title}\nJournal: {journal}\nPublished: {date}\nPMID: {pmid}\nURL: https://pubmed.ncbi.nlm.nih.gov/{pmid}/".format(
                    title=item.get("title", "Unknown title"),
                    journal=item.get("fulljournalname", "Unknown journal"),
                    date=item.get("pubdate", "Unknown date"),
                    pmid=pmid,
                )
            )
        return "\n\n".join(results)
    except Exception as exc:
        return f"PubMed search failed: {exc}"
