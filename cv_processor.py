import io
from fastapi import UploadFile
import PyPDF2

def extract_text_from_file(file: UploadFile) -> str:
    """
    Extracts text from an uploaded file.
    Supports PDF and plain text files.
    """
    filename = file.filename.lower()
    content = file.file.read()
    
    if filename.endswith('.pdf'):
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Error reading PDF: {e}")
    elif filename.endswith('.txt'):
        try:
            return content.decode("utf-8")
        except Exception as e:
            raise ValueError(f"Error decoding text file: {e}")
    else:
        try:
            return content.decode("utf-8")
        except Exception as e:
            raise ValueError("Unsupported file type or encoding error.")
