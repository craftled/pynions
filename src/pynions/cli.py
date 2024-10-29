import click
from rich import print
from dotenv import load_dotenv
import importlib.util
import sys
from typing import Optional

@click.group()
def cli():
    """Pynions CLI - Simple AI automation framework"""
    load_dotenv()

@cli.command()
def version():
    """Show version"""
    from pynions import __version__
    print(f"📦 Pynions v{__version__}")

@cli.command()
@click.argument('workflow_path')
def run(workflow_path: str):
    """Run a workflow from a Python file"""
    try:
        # Import the workflow file
        spec = importlib.util.spec_from_file_location("workflow", workflow_path)
        if not spec or not spec.loader:
            raise ImportError(f"Could not load {workflow_path}")
        
        module = importlib.util.module_from_spec(spec)
        sys.modules["workflow"] = module
        spec.loader.exec_module(module)
        
        # Run the main function if it exists
        if hasattr(module, 'main'):
            import asyncio
            asyncio.run(module.main())
        else:
            print("❌ No main() function found in workflow file")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    cli()
