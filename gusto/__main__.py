import sys
from typing import Final

import os

from rich.console import Console
from rich.table import Table
from rich import box

from gusto.analysis import DocumentAnalysis, FileAnalyser, AnalyserFactory


def main() -> None:
    console = Console()
    
    if len(sys.argv) != 2:
        console.print("[bold red]Usage:[/] gusto <file>")
        sys.exit(1)
    
    path: Final[str] = sys.argv[1]
    
    if not os.path.exists(path):
        console.print(f"[bold red]Error:[/] file not found: {path}")
        sys.exit(1)
    
    if not path.lower().endswith('.pdf'):
        console.print(f"[bold red]Error:[/] file type not supported.")
        sys.exit(1)
    
    console.print('[bold green]Reading file...[/]\n\n')
    
    analyser: FileAnalyser = AnalyserFactory.get_analyser(path)
    
    analysis: DocumentAnalysis = analyser.analyse()
    
    stats = Table(title="Analysis", show_header=False, show_lines=True, box=box.SQUARE)
    stats.add_column("Name", justify="right", width=20, style="bold")
    stats.add_column("Value", justify="left", width=40)

    stats.add_row("Word count", f"{analysis.word_count:,}")
    stats.add_row("Character count", f"{analysis.char_count:,}")
    stats.add_row("Page count", f"{analysis.page_count}")

    console.print(stats)

    meta = Table(title="Metadata", show_header=False, show_lines=True, box=box.SQUARE)
    meta.add_column("Name", justify="right", width=20, style="bold")
    meta.add_column("Value", justify="left", width=40)

    if analysis.title:
        meta.add_row("Title", analysis.title)
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
        console.print("\n[italic yellow]No metadata found in the PDF.[/]\n")

    print("\n\n")

if __name__=='__main__':
    main()
