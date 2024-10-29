import click
import asyncio
from pathlib import Path
import importlib.util
import sys
from typing import Any
import json
from datetime import datetime


@click.group()
def cli():
    """Pynions CLI - AI Automation Framework"""
    pass


@cli.command()
@click.argument("project_name")
def init(project_name: str):
    """Initialize a new project"""
    project_dir = Path(project_name)
    project_dir.mkdir(exist_ok=True)

    # Create project structure
    (project_dir / "flows").mkdir(exist_ok=True)
    (project_dir / "data").mkdir(exist_ok=True)
    (project_dir / "logs").mkdir(exist_ok=True)
    (project_dir / ".cache").mkdir(exist_ok=True)

    # Create example flow
    example = """from pynions import Flow, State
from typing import Dict, Any

class ExampleState(State):
    query: str = ""
    result: Dict[str, Any] = {}

class ExampleFlow(Flow[ExampleState]):
    async def run(self):
        self.logger.info(f"Processing query: {self.state.query}")
        
        async with self.step("process"):
            # Your processing logic here
            self.state.result = {"status": "success"}
        
        return self.state.result

if __name__ == "__main__":
    import asyncio
    flow = ExampleFlow(query="test")
    result = asyncio.run(flow.run())
    print(result)
"""

    (project_dir / "flows" / "example.py").write_text(example)

    # Create requirements.txt
    reqs = """pynions
python-dotenv>=1.0.0
"""
    (project_dir / "requirements.txt").write_text(reqs)

    # Create .env.example
    env = """# API Keys
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
"""
    (project_dir / ".env.example").write_text(env)

    click.echo(f"Created project: {project_name}")
    click.echo("Next steps:")
    click.echo("1. cd " + project_name)
    click.echo("2. python -m venv .venv")
    click.echo("3. source .venv/bin/activate")
    click.echo("4. pip install -r requirements.txt")
    click.echo("5. cp .env.example .env")
    click.echo("6. Edit .env with your API keys")


@cli.command()
@click.argument("flow_path")
@click.option(
    "--kwargs", "-k", multiple=True, help="Key=value pairs for flow initialization"
)
def run(flow_path: str, kwargs):
    """Run a flow"""
    try:
        # Parse kwargs
        flow_kwargs = {}
        for kw in kwargs:
            key, value = kw.split("=", 1)
            try:
                # Try to parse as JSON
                flow_kwargs[key] = json.loads(value)
            except json.JSONDecodeError:
                # Fall back to string
                flow_kwargs[key] = value

        # Import flow class
        if ":" not in flow_path:
            click.echo("Error: Flow path must be in format: path/to/file.py:FlowClass")
            return

        file_path, class_name = flow_path.split(":")

        # Import module
        spec = importlib.util.spec_from_file_location("flow_module", file_path)
        if not spec or not spec.loader:
            click.echo(f"Error: Could not load {file_path}")
            return

        module = importlib.util.module_from_spec(spec)
        sys.modules["flow_module"] = module
        spec.loader.exec_module(module)

        # Get flow class
        flow_class = getattr(module, class_name)

        # Create and run flow
        flow = flow_class(**flow_kwargs)
        result = asyncio.run(flow.run())

        # Print result
        click.echo(json.dumps(result, indent=2, default=str))

    except Exception as e:
        click.echo(f"Error running flow: {str(e)}")
