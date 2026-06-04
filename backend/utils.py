"""
Utility functions: text extraction from PDF/TXT/images, and text chunking.
"""
import io
import PyPDF2


def extract_text_from_pdf(content: bytes) -> str:
    try:
        pdf_file = io.BytesIO(content)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""


def extract_text_from_txt(content: bytes) -> str:
    try:
        return content.decode("utf-8").strip()
    except Exception:
        try:
            return content.decode("latin-1").strip()
        except Exception:
            return ""


def extract_text_from_image(content: bytes) -> str:
    """Extract text from image using PIL. Returns empty string if OCR not available."""
    try:
        from PIL import Image
        import pytesseract
        image = Image.open(io.BytesIO(content))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except ImportError:
        return "[Image uploaded - OCR not available. Install pytesseract to extract text.]"
    except Exception as e:
        print(f"Image OCR error: {e}")
        return ""


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list:
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start: start + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
