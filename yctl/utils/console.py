"""
Rich console utilities for beautiful terminal output.
"""

from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.syntax import Syntax
from rich.markdown import Markdown
from typing import List, Optional

# Custom theme for yctl
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "highlight": "bold magenta",
    "dim": "dim",
})

console = Console(theme=custom_theme)


def print_header(text: str) -> None:
    """Print a styled header."""
    console.print(f"\n[bold cyan]{'=' * 60}[/bold cyan]")
    console.print(f"[bold cyan]{text.center(60)}[/bold cyan]")
    console.print(f"[bold cyan]{'=' * 60}[/bold cyan]\n")


def print_success(text: str) -> None:
    """Print a success message."""
    console.print(f"✓ [success]{text}[/success]")


def print_error(text: str) -> None:
    """Print an error message."""
    console.print(f"✗ [error]{text}[/error]")


def print_warning(text: str) -> None:
    """Print a warning message."""
    console.print(f"⚠ [warning]{text}[/warning]")


def print_info(text: str) -> None:
    """Print an info message."""
    console.print(f"ℹ [info]{text}[/info]")


def print_panel(content: str, title: Optional[str] = None, style: str = "cyan") -> None:
    """Print content in a panel."""
    console.print(Panel(content, title=title, border_style=style))


def create_table(title: str, columns: List[str]) -> Table:
    """
    Create a Rich table with standard styling.
    
    Args:
        title: Table title
        columns: List of column names
        
    Returns:
        Configured Rich Table instance
    """
    table = Table(title=title, show_header=True, header_style="bold magenta")
    for column in columns:
        table.add_column(column)
    return table


def print_code(code: str, language: str = "python") -> None:
    """Print syntax-highlighted code."""
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    console.print(syntax)


def print_markdown(text: str) -> None:
    """Print markdown-formatted text."""
    md = Markdown(text)
    console.print(md)
