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
        console.print("[bold red]Useage:[/] gusto <file>")
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
    
    

if __name__=='__main__':
    main()
