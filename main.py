import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Optional
from datetime import datetime

from models import Product, Launch, Feedback, Platform
from generator import ContentGenerator
from tracker import LaunchTracker
from feedback_manager import FeedbackManager

app = typer.Typer(help="Help indie developers find early users and collect feedback safely")
console = Console()

generator = ContentGenerator()
tracker = LaunchTracker()
feedback_mgr = FeedbackManager()


@app.command()
def init(
    name: str = typer.Option(..., "--name", "-n", help="Product name"),
    description: str = typer.Option(..., "--desc", "-d", help="Product description"),
    url: str = typer.Option("", "--url", "-u", help="Product URL"),
):
    """Initialize a new product profile"""
    product = Product(name=name, description=description, url=url)
    tracker.save_product(product)
    console.print(Panel(f"[green]Product '{name}' initialized successfully![/green]"))


@app.command()
def generate(
    platform: Platform = typer.Argument(..., help="Target platform"),
    tone: str = typer.Option("friendly", "--tone", "-t", help="Content tone: friendly/professional/casual"),
):
    """Generate launch content for specific platform"""
    product = tracker.load_product()
    if not product:
        console.print("[red]No product found. Run 'init' first.[/red]")
        raise typer.Exit(1)
    
    content = generator.generate_content(product, platform, tone)
    
    console.print(Panel(f"[bold cyan]{platform.value} Launch Content[/bold cyan]"))
    console.print(content)
    console.print("\n[dim]Tip: Copy and customize before posting[/dim]")


@app.command()
def launch(
    platform: Platform = typer.Argument(..., help="Platform where you launched"),
    url: str = typer.Option("", "--url", "-u", help="Launch post URL"),
    notes: str = typer.Option("", "--notes", "-n", help="Additional notes"),
):
    """Record a product launch"""
    product = tracker.load_product()
    if not product:
        console.print("[red]No product found. Run 'init' first.[/red]")
        raise typer.Exit(1)
    
    launch_record = Launch(
        platform=platform,
        url=url,
        notes=notes,
        launched_at=datetime.now()
    )
    tracker.add_launch(launch_record)
    console.print(f"[green]Launch on {platform.value} recorded![/green]")


@app.command()
def launches():
    """List all product launches"""
    records = tracker.get_launches()
    if not records:
        console.print("[yellow]No launches recorded yet.[/yellow]")
        return
    
    table = Table(title="Launch History")
    table.add_column("Platform", style="cyan")
    table.add_column("Date", style="green")
    table.add_column("URL", style="blue")
    table.add_column("Notes")
    
    for launch in records:
        table.add_row(
            launch.platform.value,
            launch.launched_at.strftime("%Y-%m-%d %H:%M"),
            launch.url or "-",
            launch.notes or "-"
        )
    
    console.print(table)


@app.command()
def add_feedback(
    source: str = typer.Option(..., "--source", "-s", help="Feedback source (username/email)"),
    content: str = typer.Option(..., "--content", "-c", help="Feedback content"),
    platform: Optional[Platform] = typer.Option(None, "--platform", "-p", help="Platform"),
    rating: Optional[int] = typer.Option(None, "--rating", "-r", help="Rating 1-5"),
):
    """Add user feedback"""
    feedback = Feedback(
        source=source,
        content=content,
        platform=platform,
        rating=rating,
        created_at=datetime.now()
    )
    feedback_mgr.add_feedback(feedback)
    console.print("[green]Feedback added successfully![/green]")


@app.command()
def feedbacks(
    platform: Optional[Platform] = typer.Option(None, "--platform", "-p", help="Filter by platform"),
):
    """List all feedback"""
    all_feedback = feedback_mgr.get_all_feedback()
    
    if platform:
        all_feedback = [f for f in all_feedback if f.platform == platform]
    
    if not all_feedback:
        console.print("[yellow]No feedback yet.[/yellow]")
        return
    
    table = Table(title="User Feedback")
    table.add_column("Date", style="cyan")
    table.add_column("Source", style="green")
    table.add_column("Platform")
    table.add_column("Rating")
    table.add_column("Content")
    
    for fb in all_feedback:
        table.add_row(
            fb.created_at.strftime("%Y-%m-%d"),
            fb.source,
            fb.platform.value if fb.platform else "-",
            str(fb.rating) if fb.rating else "-",
            fb.content[:50] + "..." if len(fb.content) > 50 else fb.content
        )
    
    console.print(table)


@app.command()
def report():
    """Generate feedback analysis report"""
    analysis = feedback_mgr.generate_report()
    
    console.print(Panel("[bold cyan]Feedback Analysis Report[/bold cyan]"))
    console.print(f"\n[bold]Total Feedback:[/bold] {analysis['total']}")
    console.print(f"[bold]Average Rating:[/bold] {analysis['avg_rating']:.1f}/5.0")
    
    if analysis['by_platform']:
        console.print("\n[bold]Feedback by Platform:[/bold]")
        for platform, count in analysis['by_platform'].items():
            console.print(f"  • {platform}: {count}")
    
    if analysis['recent']:
        console.print("\n[bold]Recent Feedback:[/bold]")
        for fb in analysis['recent'][:5]:
            console.print(f"  • [{fb.created_at.strftime('%Y-%m-%d')}] {fb.source}: {fb.content[:60]}...")


if __name__ == "__main__":
    app()
