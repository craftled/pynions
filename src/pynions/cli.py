import click
import sys
from pathlib import Path
import shutil


@click.group()
def cli():
    """Pynions CLI - AI automation framework for marketers"""
    pass


@cli.command()
@click.argument("project_name")
def new(project_name: str):
    """Create a new project from template"""
    try:
        import pynions

        template_dir = Path(pynions.__file__).parent / "templates" / "project"
        target_dir = Path.cwd() / project_name

        if not template_dir.exists():
            print(f"❌ Template directory not found: {template_dir}")
            sys.exit(1)

        print(f"📁 Creating project in {target_dir}")
        target_dir.mkdir(parents=True, exist_ok=True)

        # Copy template files and create directories
        for src in template_dir.rglob("*"):
            rel_path = src.relative_to(template_dir)
            dst = target_dir / rel_path

            if src.is_dir():
                dst.mkdir(parents=True, exist_ok=True)
            elif src.is_file():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

                # Replace template variables
                if dst.suffix in [".md", ".py", ".txt"]:
                    content = dst.read_text()
                    content = content.replace("{{project_name}}", project_name)
                    dst.write_text(content)

        # Create empty directories
        for dir_name in ["data", "logs", ".cache"]:
            (target_dir / dir_name).mkdir(exist_ok=True)
            (target_dir / dir_name / ".gitkeep").touch()

        print(f"✨ Created new project: {project_name}")
        print("\n🚀 Next steps:")
        print(f"1. cd {project_name}")
        print("2. Add your API keys to .env")
        print("3. python workflows/tweet.py")

    except Exception as e:
        print(f"❌ Error creating project: {e}")
        sys.exit(1)


def main():
    cli()


if __name__ == "__main__":
    main()
