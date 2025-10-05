import typer
from pathlib import Path
from cli.generator import generate_project , run_server
from rich.logging import RichHandler
import logging
from importlib import resources

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("lightbolt")

app = typer.Typer(help="lightbolt - Scaffold Python backend projects instantly.")


@app.command()
def create(
    name: str = typer.Argument(..., help="Name of your project"),
    framework: str = typer.Option(..., "--framework", "-f", case_sensitive=False, help="Backend framework"),
    output: Path = typer.Option(".", "--output", "-o", help="Output directory"),
    skip_install: bool = typer.Option(False, "--skip-install", help="Skip installing dependencies"),
):
    frameworks = {
        "fastapi": "fastapi",
        "flask": "flask",
        "django": "django"
    }

    if framework.lower() not in frameworks:
        logger.error("Invalid framework. Choose from: fastapi, flask, django.")
        raise typer.Exit(code=1)

    framework_dir_name = frameworks[framework.lower()]
    template_path = Path(resources.files("cli") / "templates" / framework_dir_name)
    generated_project_dir = generate_project(
        template_path, 
        name, 
        output_dir=output, 
        skip_install=skip_install
    )
    run_server(generated_project_path=generated_project_dir)


if __name__ == "__main__":
    app()
