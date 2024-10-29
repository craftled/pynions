import click
from rich import print
from dotenv import load_dotenv
import os
import sys
from pathlib import Path
import shutil


def main():
    """Entry point for CLI"""
    cli()  # Call our click group


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
@click.argument("project_name")
def new(project_name: str):
    """Create a new project from template"""
    try:
        template_dir = Path(__file__).parent / "templates" / "project"
        target_dir = Path.cwd() / project_name

        if not template_dir.exists():
            print(f"❌ Template directory not found: {template_dir}")
            sys.exit(1)

        print(f"📁 Creating project in {target_dir}")
        shutil.copytree(template_dir, target_dir)

        # Replace template variables
        for file in target_dir.rglob("*"):
            if file.is_file() and file.suffix in [".md", ".py", ".txt"]:
                content = file.read_text()
                content = content.replace("{{project_name}}", project_name)
                file.write_text(content)

        print(f"✨ Created new project: {project_name}")
        print("\n🚀 Next steps:")
        print("1. cd", project_name)
        print("2. Add your API keys to .env")
        print("3. python workflows/example.py")

    except Exception as e:
        print(f"❌ Error creating project: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
