import sys
import os
from typing import Final

from rich.console import Console
from rich.table import Table
from rich import box

from gusto.analysis import (
    DocumentAnalysis,
    FileAnalyser,
    AnalyserFactory,
    PDFOpenError,
    MetaDataReadError,
    analyse_directory,
)


def display_analysis(console: Console, path: str, analysis: DocumentAnalysis) -> None:
    console.print(f"[bold blue]\nFile: {path}[/]")

    stats = Table(title="Analysis", show_header=False, show_lines=True, box=box.SQUARE)
    stats.add_column("Name", justify="right", width=20, style="bold")
    stats.add_column("Value", justify="left", width=40)

    stats.add_row("Word count", f"{analysis.word_count:,}")
    stats.add_row("Character count", f"{analysis.char_count:,}")

    page_label = "Line count" if analysis.mime_type and analysis.mime_type.startswith("text/") else "Page count"
    stats.add_row(page_label, f"{analysis.page_count}")

    console.print(stats)

    meta = Table(title="Metadata", show_header=False, show_lines=True, box=box.SQUARE)
    meta.add_column("Name", justify="right", width=20, style="bold")
    meta.add_column("Value", justify="left", width=40)

    if analysis.title:
        meta.add_row("Title", analysis.title)
    if analysis.mime_type:
        meta.add_row("Type", analysis.mime_type)
    if analysis.author:
        meta.add_row("Author", analysis.author)
    if analysis.subject:
        meta.add_row("Subject", analysis.subject)
    if analysis.producer:
        meta.add_row("Producer", analysis.producer)
    if analysis.created:
        meta.add_row("Created", analysis.created)
    if analysis.modified:
        meta.add_row("Modified", analysis.modified)

    if meta.row_count > 0:
        console.print("\n", meta)
    else:
        console.print("\n[italic yellow]No metadata found in the document.[/]")


def main() -> None:
    console = Console()

    if len(sys.argv) != 2:
        console.print("[bold red]Usage:[/] gusto <file>")
        sys.exit(1)

    path: Final[str] = sys.argv[1]

    if not os.path.exists(path):
        console.print(f"[bold red]Error:[/] Path not found: {path}")
        sys.exit(1)

    if os.path.isdir(path):
        console.print("[bold green]Scanning directory...[/]")
        results = analyse_directory(path)
        if not results:
            console.print("[italic yellow]No supported files found in directory.[/]")
        for file_path, analysis in results.items():
            display_analysis(console, file_path, analysis)
    else:
        try:
            analyser: FileAnalyser = AnalyserFactory.get_analyser(path)
        except ValueError as e:
            console.print(f"[bold red]Error:[/] {e}")
            sys.exit(1)

        console.print("[bold green]Reading file...[/]\n")

        try:
            analysis: DocumentAnalysis = analyser.analyse()
        except (PDFOpenError, MetaDataReadError) as e:
            console.print(f"[bold red]Error analysing file:[/] {e}")
            sys.exit(1)

        display_analysis(console, path, analysis)


if __name__ == '__main__':
    main()
