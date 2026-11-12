
import arxiv
from mcp.server import MCPServer

mcp = MCPServer("research-paper-server")
client = arxiv.Client()


def serialize_paper(paper: arxiv.Result) -> dict:
    return {
        "id": paper.get_short_id(),
        "title": paper.title,
        "authors": [a.name for a in paper.authors],
        "published": paper.published.date().isoformat(),
        "abstract": paper.summary,
        "url": paper.entry_id,
        "pdf_url": paper.pdf_url,
    }


@mcp.tool()
def search_papers(query: str, max_results: int = 5) -> list[dict]:
    """Search arXiv for research papers, newest first."""
    if not query.strip() or not 1 <= max_results <= 10:
        raise ValueError("Provide a query and 1-10 results.")

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    return [serialize_paper(p) for p in client.results(search)]


@mcp.tool()
def get_paper(arxiv_id: str) -> dict | None:
    """Get a paper's metadata and abstract by arXiv ID."""
    search = arxiv.Search(id_list=[arxiv_id], max_results=1)
    paper = next(client.results(search), None)
    return serialize_paper(paper) if paper else None


if __name__ == "__main__":
    mcp.run()
