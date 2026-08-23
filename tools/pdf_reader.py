from pathlib import Path

from agents import function_tool
from pypdf import PdfReader


@function_tool
def read_pdf(file_path: str, max_chars: int = 30000) -> str:
    """Extract text from an uploaded research PDF for grounded analysis."""
    path = Path(file_path)
    if not path.exists():
        return "PDF file not found."
    try:
        reader = PdfReader(str(path))
        pages = []
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(f"--- Page {page_number} ---\n{text}")
        content = "\n\n".join(pages)
        return content[:max_chars] if content else "No extractable text was found in the PDF."
    except Exception as exc:
        return f"PDF reading failed: {exc}"
