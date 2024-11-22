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

        # Create project directory and copy example files
        project_dir = Path.cwd()
        
        # Copy example files if they don't exist
        example_files = [
            (".env.example", ".env"),
            ("pynions.example.json", "pynions.json")
        ]
        
        for src_name, dst_name in example_files:
            src = project_dir / src_name
            dst = project_dir / dst_name
            if src.exists() and not dst.exists():
                shutil.copy2(src, dst)

        print("\n Pynions installed successfully!")
        print("\n Quick Setup:")
        print("1. Add your OpenAI API key to .env")
        print("2. (Optional) Customize settings in pynions.json")
        print("\n Optional API keys for specific features:")
        print("- SERPER_API_KEY (search)")
        print("- ANTHROPIC_API_KEY (Claude)")
        print("- JINA_API_KEY (embeddings)")
        print("\n Documentation: https://pynions.com")


setup(
    name="pynions",
    version="0.2.26",
    author="Tomas Laurinavicius",
    author_email="tom@pynions.com",
    description="Simple marketing automation framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tomaslau/pynions",
    packages=find_namespace_packages(include=["pynions", "pynions.*"]),
    install_requires=requirements,
    cmdclass={
        "install": PostInstallCommand,
    },
    package_data={
        "pynions": ["*.example.json", "*.example"],
    },
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
