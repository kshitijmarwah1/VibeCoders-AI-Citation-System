import pdfplumber
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF file with error handling.
    """
    if not file_path or not Path(file_path).exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    text_chunks = []

    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    content = page.extract_text()
                    if content:
                        text_chunks.append(content)
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {page_num}: {e}")
                    continue
    except Exception as e:
        logger.error(f"Failed to open PDF {file_path}: {e}")
        raise ValueError(f"Invalid or corrupted PDF file: {file_path}")

    if not text_chunks:
        raise ValueError(f"No text content found in PDF: {file_path}")

    return "\n".join(text_chunks)
