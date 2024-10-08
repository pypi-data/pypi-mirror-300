import re
import click
import os
import shutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.text import Text
from rich.traceback import install
from rich.prompt import Prompt, Confirm

# Install rich traceback handler
install()

console = Console()

# Path to the directory containing templates
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

INIT_PATH = os.path.join(os.path.dirname(__file__), "__init__.py")


def get_version():
    with open(INIT_PATH, "r") as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        # Start the interactive wizard
        display_banner()
        console.print(
            "[bold blue]Welcome to the whiteduck project scaffolding wizard![/]\n"
        )
        # Ask the user to select an action
        action = Prompt.ask(
            "[bold cyan]> Choose an action[/]",
            choices=["create", "list_templates", "template_info", "exit"],
            default="create",
        )

        if action == "create":
            interactive_create()
        elif action == "list_templates":
            list_templates()
        elif action == "template_info":
            template_info_interactive()
        else:
            console.print("[yellow]Goodbye![/]")
            return


@cli.command()
@click.option(
    "-o",
    "--output",
    default=".",
    type=click.Path(),
    help="Output path for the new project (defaults to current directory)",
)
@click.option(
    "-t",
    "--template",
    default="shiny-default",
    required=True,
    help="Name of the template to use",
)
def create(output, template):
    """Create a new project scaffold."""
    display_banner()
    try:
        create_project(output, template)
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/] {e}")


@cli.command()
def list_templates():
    """List available templates."""
    display_banner()
    templates = get_available_templates()
    if templates:
        table = Table(
            title="Available Templates", box=box.ROUNDED, title_style="bold green"
        )
        table.add_column("Template Name", style="cyan", no_wrap=True)
        for tmpl in templates:
            table.add_row(tmpl)
        console.print(table)
    else:
        console.print("[yellow]No templates found.[/]")


@cli.command()
@click.argument("template")
def template_info(template):
    """Display information about a template."""
    display_banner()
    readme_path = os.path.join(TEMPLATES_DIR, template, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            content = f.read()
            panel = Panel(
                content,
                title=f"[bold green]Template: {template}[/]",
                border_style="green",
            )
            console.print(panel)
    else:
        console.print(f"[yellow]No README.md found for template '{template}'[/]")


def interactive_create():
    """Interactive create command within the wizard."""
    # Get the output path
    output = Prompt.ask(
        "[bold cyan]> Enter the output path[/]",
        default=".",
    )
    # Get the available templates
    templates = get_available_templates()
    if not templates:
        console.print("[red]No templates available.[/]")
        return
    # Display the templates
    console.print("\n[bold green]Available templates:[/]")
    for idx, tmpl in enumerate(templates, start=1):
        console.print(f" [cyan]{idx}[/]. {tmpl}")
    # Ask the user to select a template
    template_index = Prompt.ask(
        "[bold cyan]> Choose a template by number[/]",
        choices=[str(i) for i in range(1, len(templates) + 1)],
    )
    template = templates[int(template_index) - 1]

    # Display the template's README.md
    readme_path = os.path.join(TEMPLATES_DIR, template, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            content = f.read()
            panel = Panel(
                content,
                title=f"[bold green]Template: {template}[/]",
                border_style="green",
            )
            console.print(panel)
    else:
        console.print(f"[yellow]No README.md found for template '{template}'[/]")

    # Confirm and create the project
    confirm = Confirm.ask(
        f"[bold green]Proceed to create the project '{template}' at '{output}'?[/]"
    )
    if confirm:
        try:
            create_project(output, template)
        except Exception as e:
            console.print(f"[bold red]An error occurred:[/] {e}")
    else:
        console.print("[yellow]Operation cancelled.[/]")


def template_info_interactive():
    """Interactive template_info command within the wizard."""
    templates = get_available_templates()
    if not templates:
        console.print("[red]No templates available.[/]")
        return
    # Display the templates
    console.print("\n[bold green]Available templates:[/]")
    for idx, tmpl in enumerate(templates, start=1):
        console.print(f" [cyan]{idx}[/]. {tmpl}")
    # Ask the user to select a template
    template_index = Prompt.ask(
        "[bold cyan]> Choose a template to view information[/]",
        choices=[str(i) for i in range(1, len(templates) + 1)],
    )
    template = templates[int(template_index) - 1]
    # Display the template's README.md
    readme_path = os.path.join(TEMPLATES_DIR, template, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            content = f.read()
            panel = Panel(
                content,
                title=f"[bold green]Template: {template}[/]",
                border_style="green",
            )
            console.print(panel)
    else:
        console.print(f"[yellow]No README.md found for template '{template}'[/]")


def display_banner():
    banner_text = Text(
        """
              WWW      dWb WWW                 WWW                   WWW      
              WWW      YWP WWW                 WWW                   WWW      
              WWW          WWW                 WWW                   WWW      
WWW  WWW  WWW WWWWWb.  WWW WWWWWW .dWWb.   .dWWWWW WWW  WWW  .dWWWWb WWW  WWW 
WWW  WWW  WWW WWW "WWb WWW WWW   dWP  YWb dWW" WWW WWW  WWW dWWP"    WWW .WWP 
WWW  WWW  WWW WWW  WWW WWW WWW   WWWWWWWW WWW  WWW WWW  WWW WWW      WWWWWWK  
YWWb WWW dWWP WWW  WWW WWW YWWb. YWb.     YWWb WWW YWWb WWW YWWb.    WWW "WWb 
 "YWWWWWWWP"  WWW  WWW WWW  "YWWW "YWWWW   "YWWWWW  "YWWWWW  "YWWWWP WWW  WWW 
""",
        justify="center",
        style="bold orange3",
    )
    console.print(banner_text)
    console.print(
        f"[bold]v{get_version()}[/] - [bold]whiteduck GmbH[/] - [cyan]https://whiteduck.de[/]\n"
    )


def get_available_templates():
    if os.path.exists(TEMPLATES_DIR):
        return [
            name
            for name in os.listdir(TEMPLATES_DIR)
            if os.path.isdir(os.path.join(TEMPLATES_DIR, name))
        ]
    return []


def create_project(output_path, template_name):
    console.print(
        f"[bold green]Creating project at[/] '{output_path}' [bold green]using template[/] '{template_name}'\n"
    )

    template_path = os.path.join(TEMPLATES_DIR, template_name)

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template '{template_name}' not found.")

    shutil.copytree(template_path, output_path, dirs_exist_ok=True)

    # Rename .env_example to .env if it exists
    env_example_path = os.path.join(output_path, ".env_example")
    env_path = os.path.join(output_path, ".env")
    if os.path.exists(env_example_path):
        os.rename(env_example_path, env_path)
        console.print("[cyan]Renamed .env_example to .env[/]")

    console.print("[bold green]Project scaffold created successfully.[/]")


if __name__ == "__main__":
    cli()
