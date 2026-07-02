import argparse
import time
from rich.console import Console
from .utils.logger import print_banner, print_results
from .core.scanner import Scanner

console = Console()


def main():
    parser = argparse.ArgumentParser(
        prog="wtect",
        description="Detect web technologies. Accepts example.com or https://www.example.com/"
    )
    parser.add_argument("-u", "--url", required=True, help="Target domain or URL (e.g. example.com)")
    args = parser.parse_args()

    print_banner()

    scanner = Scanner(args.url)
    console.print(f"[dim]Target: {scanner.target_url}[/dim]")
    start = time.time()
    with console.status("[dim]Scanning...[/dim]", spinner="dots"):
        results = scanner.run()
    elapsed = round(time.time() - start, 1)

    if not results:
        console.print("[red]Could not detect any technologies or failed to reach the target.[/red]")
    else:
        print_results(results)
        console.print(f"[dim]Completed in {elapsed}s[/dim]")


if __name__ == "__main__":
    main()

