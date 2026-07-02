from rich.console import Console
from rich.theme import Theme
from rich.tree import Tree
from rich.text import Text
from rich.panel import Panel
from rich import box

theme = Theme({
    "confirmed": "bold green",
    "likely": "bold yellow",
    "suspected": "dim white",
})

console = Console(theme=theme)

CONF_ICON = {"Confirmed": "[green]+[/green]", "Likely": "[yellow]~[/yellow]", "Suspected": "[dim]?[/dim]"}
CONF_LABEL = {"Confirmed": "[confirmed]Confirmed[/confirmed]", "Likely": "[likely]Likely[/likely]", "Suspected": "[suspected]Suspected[/suspected]"}


def print_banner():
    console.print()
    console.print("[bold cyan]wtective[/bold cyan] [dim]v1.0[/dim]  Web Technology Detector")
    console.print("[dim]-[/dim]" * 50)


def print_results(results: dict):
    if not results:
        console.print("[red]No technologies detected.[/red]")
        return

    total = sum(len(v) for v in results.values())
    console.print()
    console.print(f"[bold]{total}[/bold] technologies detected across [bold]{len(results)}[/bold] categories")
    console.print()

    tree = Tree("[bold cyan]Scan Results[/bold cyan]", guide_style="dim")

    for category, techs in results.items():
        cat_branch = tree.add(f"[bold white]{category}[/bold white] [dim]({len(techs)})[/dim]")
        for t in techs:
            icon = CONF_ICON.get(t['confidence'], '?')
            label = CONF_LABEL.get(t['confidence'], t['confidence'])
            ver = f" [magenta]{t['version']}[/magenta]" if t.get('version') else ""
            tech_line = f"{icon}  [bold]{t['name']}[/bold]{ver}  {label}"
            node = cat_branch.add(tech_line)
            if t.get('evidence'):
                node.add(f"[dim]{t['evidence']}[/dim]")

    console.print(tree)
    console.print()

    confirmed = sum(1 for techs in results.values() for t in techs if t['confidence'] == 'Confirmed')
    likely = sum(1 for techs in results.values() for t in techs if t['confidence'] == 'Likely')
    suspected = sum(1 for techs in results.values() for t in techs if t['confidence'] == 'Suspected')

    legend = f"[green]+ Confirmed ({confirmed})[/green]  [yellow]~ Likely ({likely})[/yellow]  [dim]? Suspected ({suspected})[/dim]"
    console.print(legend)
    console.print()


