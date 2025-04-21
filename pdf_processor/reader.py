import pdfplumber
from .interfaces.i_reader import IReader

class PDFReader(IReader):
    def read(self, file_path: str) -> str:
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(p.extract_text() for p in pdf.pages if p.extract_text())
