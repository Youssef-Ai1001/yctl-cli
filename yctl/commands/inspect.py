"""
yctl inspect command - Inspect and analyze datasets.
"""

import typer
from pathlib import Path
from rich.table import Table
from yctl.core.analyzers import analyze_dataset
from yctl.utils import (
    console,
    print_header,
    print_success,
    print_error,
    print_info,
    print_panel,
    create_table,
    format_size,
)


def inspect_command(
    dataset_path: str = typer.Argument(..., help="Path to dataset file (CSV, Excel, JSON, Parquet)"),
    show_sample: bool = typer.Option(False, "--sample", help="Show sample rows"),
) -> None:
    """
    Inspect a dataset and get insights.
    
    Analyzes dataset statistics, detects issues, and suggests preprocessing steps.
    """
    path = Path(dataset_path)
    
    if not path.exists():
        print_error(f"File not found: {dataset_path}")
        print_info("Please check the file path and try again.")
        raise typer.Exit(1)
    
    if not path.is_file():
        print_error(f"Path is not a file: {dataset_path}")
        print_info("Please provide a path to a dataset file (CSV, Excel, JSON, or Parquet).")
        raise typer.Exit(1)
    
    print_header(f"Inspecting Dataset: {path.name}")
    
    try:
        # Analyze dataset
        with console.status("[bold cyan]Analyzing dataset...", spinner="dots"):
            stats, preprocessing, models = analyze_dataset(path)
        
        # Display basic info
        console.print("\n[bold cyan]📊 Dataset Overview[/bold cyan]")
        info_table = Table(show_header=False, box=None)
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="white")
        
        info_table.add_row("Rows", f"{stats.num_rows:,}")
        info_table.add_row("Columns", f"{stats.num_cols:,}")
        info_table.add_row("Memory Usage", format_size(stats.memory_usage))
        info_table.add_row("Duplicates", f"{stats.duplicates:,}")
        
        console.print(info_table)
        
        # Display column information
        console.print("\n[bold cyan]📋 Column Information[/bold cyan]")
        col_table = create_table("Columns", ["Column", "Type", "Missing", "Missing %"])
        
        for col, dtype in stats.column_types.items():
            missing = stats.missing_values[col]
            missing_pct = stats.missing_percentages[col]
            
            # Color code missing percentages
            if missing_pct > 50:
                missing_str = f"[red]{missing:,}[/red]"
                pct_str = f"[red]{missing_pct:.1f}%[/red]"
            elif missing_pct > 20:
                missing_str = f"[yellow]{missing:,}[/yellow]"
                pct_str = f"[yellow]{missing_pct:.1f}%[/yellow]"
            else:
                missing_str = f"{missing:,}"
                pct_str = f"{missing_pct:.1f}%"
            
            col_table.add_row(col, dtype, missing_str, pct_str)
        
        console.print(col_table)
        
        # Display numeric statistics
        if stats.numeric_stats:
            console.print("\n[bold cyan]🔢 Numeric Columns Statistics[/bold cyan]")
            num_table = create_table("Statistics", ["Column", "Mean", "Std", "Min", "Max", "Median"])
            
            for col, stat in stats.numeric_stats.items():
                num_table.add_row(
                    col,
                    f"{stat['mean']:.2f}",
                    f"{stat['std']:.2f}",
                    f"{stat['min']:.2f}",
                    f"{stat['max']:.2f}",
                    f"{stat['median']:.2f}",
                )
            
            console.print(num_table)
        
        # Display categorical statistics
        if stats.categorical_stats:
            console.print("\n[bold cyan]📝 Categorical Columns Statistics[/bold cyan]")
            cat_table = create_table("Statistics", ["Column", "Unique Values", "Most Common", "Frequency"])
            
            for col, stat in stats.categorical_stats.items():
                cat_table.add_row(
                    col,
                    f"{stat['unique_count']:,}",
                    str(stat['most_common'])[:30],
                    f"{stat['most_common_freq']:,}",
                )
            
            console.print(cat_table)
        
        # Display potential issues
        if stats.potential_issues:
            console.print("\n[bold yellow]⚠️  Potential Issues[/bold yellow]")
            for issue in stats.potential_issues:
                console.print(f"  • {issue}")
        else:
            console.print("\n[bold green]✓ No major issues detected[/bold green]")
        
        # Display preprocessing suggestions
        console.print("\n[bold cyan]🔧 Preprocessing Suggestions[/bold cyan]")
        for i, suggestion in enumerate(preprocessing, 1):
            console.print(f"  {i}. {suggestion}")
        
        # Display model recommendations
        console.print("\n[bold cyan]🤖 Model Recommendations[/bold cyan]")
        
        if models['classification']:
            console.print("\n[bold]Classification Models:[/bold]")
            for model in models['classification']:
                console.print(f"  • {model}")
        
        if models['regression']:
            console.print("\n[bold]Regression Models:[/bold]")
            for model in models['regression']:
                console.print(f"  • {model}")
        
        if models['general']:
            console.print("\n[bold]General Advice:[/bold]")
            for advice in models['general']:
                console.print(f"  • {advice}")
        
        console.print()
        print_success("Dataset inspection complete!")
        console.print()
        
    except ValueError as e:
        print_error(f"Unsupported file format: {str(e)}")
        print_info("Supported formats: CSV, Excel (.xlsx, .xls), JSON, Parquet")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Failed to inspect dataset: {str(e)}")
        print_info("Please ensure the file is a valid dataset in a supported format.")
        raise typer.Exit(1)
