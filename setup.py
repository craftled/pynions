from setuptools import setup, find_namespace_packages
import sys
import subprocess
from setuptools.command.install import install
from pathlib import Path
import shutil

# Read requirements from requirements.txt
with open("requirements.txt") as f:
    requirements = [
        line.strip() for line in f if line.strip() and not line.startswith("#")
    ]

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


class PostInstallCommand(install):
    def run(self):
        install.run(self)

        # Get package directory
        pkg_dir = Path(__file__).parent
        
        # Get installation directory (where user ran pip install)
        install_dir = Path.cwd()
        
        # Files to copy
        core_dirs = ['pynions', 'workflows', 'docs', 'tests', 'data']
        config_files = [
            ('.env.example', '.env'),
            ('pynions.example.json', 'pynions.json'),
            ('README.md', 'README.md'),
            ('requirements.txt', 'requirements.txt'),
            ('pytest.ini', 'pytest.ini')
        ]
        
        # Copy core directories
        for dir_name in core_dirs:
            src_dir = pkg_dir / dir_name
            dst_dir = install_dir / dir_name
            if src_dir.exists() and not dst_dir.exists():
                shutil.copytree(src_dir, dst_dir)
        
        # Copy config files
        for src_name, dst_name in config_files:
            src = pkg_dir / src_name
            dst = install_dir / dst_name
            if src.exists() and not dst.exists():
                shutil.copy2(src, dst)

        print("\n✨ Pynions installed successfully!")
        print("\n🚀 Quick Start:")
        print("1. Add your API keys to .env:")
        print("   - OPENAI_API_KEY (required)")
        print("   - SERPER_API_KEY (for search)")
        print("   - ANTHROPIC_API_KEY (for Claude)")
        print("   - JINA_API_KEY (for embeddings)")
        print("\n2. Try an example workflow:")
        print("   python workflows/example_workflow.py")
        print("\n📚 Documentation: docs/")
        print("🔧 Configuration: pynions.json")
        print("🧪 Run tests: pytest")


setup(
    name="pynions",
    version="0.2.28",
    author="Tomas Laurinavicius",
    author_email="tom@pynions.com",
    description="Simple marketing automation framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/craftled/pynions",
    packages=find_namespace_packages(include=["pynions", "pynions.*"]),
    install_requires=requirements,
    cmdclass={
        "install": PostInstallCommand,
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.8",
)
