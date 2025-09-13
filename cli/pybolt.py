import typer
from pathlib import Path
from cli.generator import generate_project
from rich.logging import RichHandler
import logging

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("pybolt")

app = typer.Typer(help="PyBolt - Scaffold Python backend projects instantly.")


@app.command()
def create(
    name: str = typer.Argument(..., help="Name of your project"),
    framework: str = typer.Option(..., "--framework", "-f", case_sensitive=False, help="Backend framework"),
    output: Path = typer.Option(".", "--output", "-o", help="Output directory"),
    skip_install: bool = typer.Option(False, "--skip-install", help="Skip installing dependencies"),
):
    frameworks = {
        "fastapi": "cli/templates/fastapi",
        "flask": "cli/templates/flask",
        "django": "cli/templates/django"
        }

    if framework.lower() not in frameworks:
        logger.error("❌ Invalid framework. Choose from: fastapi, flask, django.")
        raise typer.Exit(code=1)

    template_path = frameworks[framework.lower()]
    generate_project(template_path, name, output_dir=output, skip_install=skip_install)


if __name__ == "__main__":
    app()
