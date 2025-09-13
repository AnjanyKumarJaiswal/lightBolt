from __future__ import annotations
import sys
import time
import subprocess
from pathlib import Path
from typing import Optional, Union
from cookiecutter.main import cookiecutter
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.traceback import install as enable_rich_traceback
import logging

enable_rich_traceback()
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("pybolt")


def install_dependencies(project_path: Union[str, Path], python_executable: Optional[str] = None) -> bool:
    project_path = Path(project_path)
    req_file = project_path / "requirements.txt"

    if not req_file.exists():
        logger.warning("No requirements.txt found — skipping dependency installation.")
        return True

    python_executable = python_executable or sys.executable
    logger.info(f"Installing dependencies with: {python_executable} -m pip install -r {req_file}")

    try:
        subprocess.run(
            [python_executable, "-m", "pip", "install", "-r", str(req_file)],
            cwd=str(project_path),
            check=True
        )
        logger.info("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as exc:
        logger.error(f"Dependency installation failed (exit code: {exc.returncode}).")
        logger.warning(f"Run manually: {python_executable} -m pip install -r {req_file}")
        return False


def _find_created_project_dir(output_dir: Path, expected_name: str, start_time: float) -> Path | None:
    candidates = [p for p in output_dir.iterdir() if p.is_dir() and expected_name in p.name]
    if candidates:
        return max(candidates, key=lambda p: p.stat().st_mtime)

    recent = [p for p in output_dir.iterdir() if p.is_dir() and p.stat().st_mtime >= start_time - 1]
    if recent:
        return max(recent, key=lambda p: p.stat().st_mtime)
    return None


def generate_project(
    template_path: Union[str, Path],
    project_name: str,
    output_dir: Union[str, Path] = ".",
    skip_install: bool = False,
    python_executable: Optional[str] = None,
) -> Path:
    template_path = Path(template_path).resolve()
    output_dir = Path(output_dir).resolve()

    if not template_path.exists():
        raise FileNotFoundError(f"Template path does not exist: {template_path}")

    target_dir = output_dir / project_name
    if target_dir.exists():
        raise FileExistsError(f"Target directory already exists: {target_dir}")

    logger.info(f"Generating project {project_name} from template {template_path}")
    start_time = time.time()

    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        BarColumn(bar_width=None),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task("Scaffolding project...", total=100)

        try:
            cookiecutter(
                str(template_path),
                no_input=True,
                extra_context={"project_name": project_name},
                output_dir=str(output_dir),
            )
        except Exception as exc:
            logger.error(f"Failed to scaffold project: {exc}")
            raise RuntimeError("Cookiecutter generation failed") from exc

        progress.update(task, advance=60)

        created_dir = target_dir if target_dir.exists() else _find_created_project_dir(output_dir, project_name, start_time)
        if created_dir is None:
            logger.warning("Could not find generated project folder automatically.")
            created_dir = target_dir

        if not skip_install:
            if (created_dir / "requirements.txt").exists():
                progress.update(task, description="Installing dependencies...")
                success = install_dependencies(created_dir, python_executable=python_executable)
                progress.update(task, advance=40)
                if not success:
                    logger.warning("Installation completed with issues.")
            else:
                progress.update(task, advance=40)
                logger.info("No requirements.txt found — skipped install.")
        else:
            progress.update(task, advance=40)
            logger.info("Skipped installing dependencies (user requested).")

    logger.info(f"Project ready: {created_dir}")
    logger.info(f"cd {created_dir.name}")
    return created_dir
