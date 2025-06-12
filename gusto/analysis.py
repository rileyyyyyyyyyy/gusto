from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional


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


class FileAnalyser(ABC):
    @abstractmethod
    def analyse_content(self):
        pass
    
    @abstractmethod
    def read_metadata(self):
        pass


class PDFAnalyser(FileAnalyser):
    def analyse_content(self):
        pass
    
    def read_metadata(self):
        pass
    

class AnalyserFactory:
    @staticmethod
    def get_analyser(path: str) -> FileAnalyser:
        if path.lower().endswith('pdf'):
            return PDFAnalyser()
        else:
            raise ValueError("File type not supported.")
        return PDFAnalyser()
