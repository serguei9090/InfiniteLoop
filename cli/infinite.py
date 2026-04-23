"""
IMMUTABLE CORE CLI
The consolidated, professional entry point for the orchestrator.
"""

import asyncio
import click
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

# Add parent directory to path for core imports
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from modules.brain import BrainOrchestrator

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
    def __init__(self, workspace_root: str = None, target_workspace: str = "workspace"):
        if workspace_root is None:
            workspace_root = str(PROJECT_ROOT)
        self.workspace_root = Path(workspace_root).resolve()
        self.brain = BrainOrchestrator(workspace_root=str(self.workspace_root), target_workspace=target_workspace)

    async def run_evolve(self, mission: str = None):
        """Primary loop for evolution via Hybrid Architecture."""
        mode = "SELF-EVOLUTION" if self.brain.target_workspace == "workspace" else f"APP-BUILDING: {self.brain.target_workspace}"
        title = f"EVOLVE [{mode}]: {mission}" if mission else f"EVOLVE [{mode}]: Standard Maintenance"
        
        console.print(
            Panel(
                f"[bold green]STARTING HYBRID EVOLUTION LOOP[/bold green]\nTarget Workspace: [cyan]{self.brain.workspace_root}[/cyan]",
                title=title,
                border_style="green",
            )
        )

        # Initialize
        await self.brain.initialize()

        # Trigger the mission logic
        await self.brain.start_mission(
            mission or "Self-Evolution: Standard optimization and health check."
        )
        console.print("[bold cyan]Mission cycle complete.[/bold cyan]")


@click.group()
@click.option(
    "--workspace", default=str(DEFAULT_WORKSPACE), help="Path to project root"
)
@click.option(
    "--debug", is_flag=True, default=True, help="Enable verbose debug logging"
)
@click.pass_context
def main(ctx, workspace, debug):
    """IMMUTABLE CORE CLI - Hybrid Autonomous Orchestrator"""
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (AttributeError, Exception):
            pass

    setup_logging(debug)
    ctx.ensure_object(dict)
    ctx.obj['workspace_root'] = workspace


@main.command()
@click.option(
    "--mission", default=None, help="Specific directive for the evolution cycle"
)
@click.option(
    "--self", "is_self", is_flag=True, default=False, help="Target the core 'workspace' for self-evolution"
)
@click.option(
    "--app", default="main_app", help="Target app in 'UserWorkspace/' (ignored if --self is set)"
)
@click.pass_context
def evolve(ctx, mission, is_self, app):
    """Launch the evolution loop for the IMMUTABLE CORE app or a user application."""
    target = "workspace" if is_self else f"UserWorkspace/{app}"
    orchestrator = InfiniteOrchestrator(ctx.obj['workspace_root'], target_workspace=target)

    # Configure env vars for PydanticAI / LiteLLM Proxy
    os.environ["OPENAI_API_KEY"] = "test"
    os.environ["OPENAI_BASE_URL"] = "http://127.0.0.1:4000/v1"

    asyncio.run(orchestrator.run_evolve(mission))


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
