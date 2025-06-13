from typing import Union, IO, Optional, Type, Protocol
from types import TracebackType
from pdf2docx import Converter  # type: ignore


class ConverterProtocol(Protocol):
    def convert(self, output_path: str) -> None: ...
    def close(self) -> None: ...


class PDFConverterAdapter:
    def __init__(self, pdf_path: Union[str, IO[bytes]]) -> None:
        self._pdf_path = pdf_path
        self._converter: Optional[ConverterProtocol] = None

    def __enter__(self) -> "PDFConverterAdapter":
        self._converter = Converter(str(self._pdf_path))  # type: ignore
        return self

    def convert(self, output_path: str) -> None:
        if not self._converter:
            raise RuntimeError("Converter not initialised.")
        self._converter.convert(output_path)

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if self._converter:
            self._converter.close()
