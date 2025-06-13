import sys
import re
import io
import logging
import unicodedata
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Any
from datetime import datetime
from PyPDF2 import PdfReader
from pdf2docx import Converter  # type: ignore
from docx import Document
import tempfile
import os

# suppress INFO logs from pdf2docx
logging.getLogger().setLevel(logging.ERROR)


@dataclass
class DocumentAnalysis:
    word_count: int
    char_count: int
    page_count: int
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    producer: Optional[str] = None
    created: Optional[str] = None
    modified: Optional[str] = None


def clean_meta(value: Any) -> Optional[str]:
    if value is None:
        return None
    try:
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="ignore").strip()
        return str(value).strip()
    except Exception:
        return None


def clean_text_for_counting(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = ''.join(c for c in text if unicodedata.category(c)[0] != 'C')
    return text.strip()


class FileAnalyser(ABC):
    @abstractmethod
    def analyse(self) -> DocumentAnalysis:
        pass

    @abstractmethod
    def _read_metadata(self) -> dict[str, Optional[str]]:
        pass


class PDFAnalyser(FileAnalyser):
    @staticmethod
    def parse_pdf_date(raw: Optional[str]) -> Optional[str]:
        if not raw:
            return None
        if raw.startswith("D:"):
            raw = raw[2:]
        try:
            dt = datetime.strptime(raw[:14], "%Y%m%d%H%M%S")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return raw

    def __init__(self, path: str):
        self.path = path
        self.reader: Optional[PdfReader] = None
        self.pages = []

        try:
            with open(self.path, 'rb') as file:
                data = file.read()
                self.reader = PdfReader(io.BytesIO(data))
                self.pages = self.reader.pages
        except Exception as e:
            logging.error(f"Error opening PDF: {e}")
            sys.exit(1)

    def analyse(self) -> DocumentAnalysis:
        word_count = 0
        char_count = 0

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            tmp.close()
            try:
                converter: Converter = Converter(self.path)
                converter.convert(tmp.name)  # type: ignore
                converter.close()

                doc = Document(tmp.name)

                text_parts = []
                text_parts.extend(p.text for p in doc.paragraphs)

                for table in doc.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            text_parts.append(cell.text)

                text = ' '.join(text_parts)
                cleaned = clean_text_for_counting(text)
                word_count = len(cleaned.split())
                char_count = len(cleaned.replace(" ", ""))
            finally:
                os.remove(tmp.name)

        meta = self._read_metadata()

        return DocumentAnalysis(
            word_count=word_count,
            char_count=char_count,
            page_count=len(self.pages),
            title=meta.get("title"),
            author=meta.get("author"),
            subject=meta.get("subject"),
            producer=meta.get("producer"),
            created=meta.get("created"),
            modified=meta.get("modified"),
        )

    def _read_metadata(self) -> dict[str, Optional[str]]:
        if not self.reader:
            return {}

        metadata: dict[str, Any] = dict(self.reader.metadata or {})
        return {
            "title": clean_meta(metadata.get('/Title')),
            "author": clean_meta(metadata.get('/Author')),
            "subject": clean_meta(metadata.get('/Subject')),
            "producer": clean_meta(metadata.get('/Producer')),
            "created": self.parse_pdf_date(clean_meta(metadata.get('/CreationDate'))),
            "modified": self.parse_pdf_date(clean_meta(metadata.get('/ModDate'))),
        }


class AnalyserFactory:
    @staticmethod
    def get_analyser(path: str) -> FileAnalyser:
        if path.lower().endswith('.pdf'):
            return PDFDocxAnalyser(path)
        raise ValueError("Unsupported file type.")
