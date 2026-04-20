"""
IMMUTABLE CORE CLI
The consolidated, professional entry point for the orchestrator.
"""

import asyncio
import click
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

# Add parent directory to path for core imports
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from modules.adk_agent import ADKOrchestrator

import logging
from rich.logging import RichHandler

console = Console()


def setup_logging(debug: bool = False):
    """Configure system-wide logging with Rich output."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, console=console)],
    )
    # Silencing verbose third-party libs
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("websockets").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)


PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DEFAULT_WORKSPACE = PROJECT_ROOT  # In ADK mode, the orchestrator handles the 'workspace/' subfolder internally


class InfiniteOrchestrator:
    def __init__(self, workspace_root: str = None):
        if workspace_root is None:
            workspace_root = str(PROJECT_ROOT)
        self.workspace_root = Path(workspace_root).resolve()
        self.brain = ADKOrchestrator(workspace_root=str(self.workspace_root))

    async def run_autoevolve(self, mission: str = None):
        """Primary loop for self-evolution via ADK."""
        title = f"EVOLVE: {mission}" if mission else "EVOLVE: Standard Maintenance"
        console.print(
            Panel(
                f"[bold green]STARTING ADK EVOLUTION LOOP[/bold green]\nTarget: {self.workspace_root}",
                title=title,
                border_style="green",
            )
        )

        # Initialize ADK
        await self.brain.initialize()

        # Trigger the mission logic from ADK orchestrator
        await self.brain.start_mission(
            mission or "Self-Evolution: Standard optimization and health check."
        )
        console.print("[bold cyan]Mission cycle complete.[/bold cyan]")


@click.group()
@click.option(
    "--workspace", default=str(DEFAULT_WORKSPACE), help="Path to workspace root"
)
@click.option(
    "--debug", is_flag=True, default=True, help="Enable verbose debug logging"
)
@click.pass_context
def main(ctx, workspace, debug):
    """IMMUTABLE CORE CLI - Autonomous Intelligence Orchestrator"""
    # Fix for Windows Unicode output crashes
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (AttributeError, Exception):
            pass  # Fallback for non-standard streams

    setup_logging(debug)
    ctx.obj = InfiniteOrchestrator(workspace)


@main.command()
@click.option(
    "--mission", default=None, help="Specific directive for the evolution cycle"
)
@click.pass_obj
def autoevolve(orchestrator, mission):
    """Launch the self-evolution loop for the IMMUTABLE CORE app."""
    asyncio.run(orchestrator.run_autoevolve(mission))


@main.command()
def project():
    """[TODO] Create or work on external projects or application scaffolds."""
    console.print(
        "[bold yellow]PROJECT COMMAND (External) is currently a placeholder.[/bold yellow]"
    )
    console.print(
        "Focus is currently on [bold cyan]autoevolve[/bold cyan] for self-optimization."
    )


if __name__ == "__main__":
    main()
