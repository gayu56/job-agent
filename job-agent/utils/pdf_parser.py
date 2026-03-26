import io

import PyPDF2


class PdfParserError(RuntimeError):
    """Raised when PDF text extraction fails."""


def extract_pdf_text(pdf_bytes: bytes) -> str:
    if not pdf_bytes:
        raise PdfParserError("Uploaded PDF is empty.")

    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    except Exception as exc:
        raise PdfParserError(f"Unable to parse PDF: {exc}") from exc

    page_texts: list[str] = []
    for page in reader.pages:
        page_texts.append((page.extract_text() or "").strip())

    text = "\n".join(block for block in page_texts if block).strip()
    if not text:
        raise PdfParserError("No readable text found in PDF (possibly scan-only document).")
    return text
