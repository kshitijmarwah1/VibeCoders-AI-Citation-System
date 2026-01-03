from services.core.input.text import extract_text_from_text
from services.core.input.pdf import extract_text_from_pdf
from services.core.input.docx import extract_text_from_docx
from services.core.input.url import extract_text_from_url
from services.core.input.batch import merge_texts
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def normalize_input(
    text: str | None = None,
    files: list[str] | None = None,
    urls: list[str] | None = None
) -> str:
    """
    Normalize input from various formats into a single text string.
    Handles errors gracefully and continues processing other inputs.
    """
    extracted = []

    if text:
        try:
            extracted.append(extract_text_from_text(text))
        except Exception as e:
            logger.error(f"Failed to extract text: {e}")

    if files:
        for file_path in files:
            try:
                file_path_obj = Path(file_path)
                if not file_path_obj.exists():
                    logger.warning(f"File not found: {file_path}")
                    continue

                if file_path.endswith(".pdf"):
                    extracted.append(extract_text_from_pdf(file_path))
                elif file_path.endswith(".docx") or file_path.endswith(".doc"):
                    extracted.append(extract_text_from_docx(file_path))
                else:
                    logger.warning(f"Unsupported file type: {file_path}")
            except Exception as e:
                logger.error(f"Failed to extract text from file {file_path}: {e}")
                continue

    if urls:
        for url in urls:
            try:
                extracted.append(extract_text_from_url(url))
            except Exception as e:
                logger.error(f"Failed to extract text from URL {url}: {e}")
                continue

    normalized = merge_texts(extracted)
    
    if not normalized or not normalized.strip():
        raise ValueError("No text content could be extracted from the provided inputs")

    return normalized
