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

        # Create ~/.pynions directory and copy config files
        home = Path.home()
        config_dir = home / ".pynions"
        config_dir.mkdir(exist_ok=True)

        # Copy config files from package to ~/.pynions
        pkg_config = Path(__file__).parent / "pynions/config"
        if pkg_config.exists():
            for file in [".env.example", "settings.json"]:
                src = pkg_config / file
                dst = config_dir / (file[:-8] if file.endswith(".example") else file)
                if src.exists() and not dst.exists():
                    shutil.copy2(src, dst)

        print("\n🎉 Pynions installed successfully!")
        print("\n💡 To use advanced features, add API keys to ~/.pynions/.env:")
        print("   - OPENAI_API_KEY (for AI features)")
        print("   - SERPER_API_KEY (for search features)")
        print("   - JINA_API_KEY (for content features)")
        print("\n🚀 Ready to go! Check docs at https://pynions.com")


setup(
    name="pynions",
    version="0.2.25",
    author="Tomas Laurinavicius",
    author_email="tom@pynions.com",
    description="Simple AI automation framework for marketers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pynions.com",
    packages=find_namespace_packages(include=["pynions*"]),
    include_package_data=True,
    package_data={
        "pynions.config": [".env.example", "settings.json"],
        "pynions.workers": ["*.py"],
        "pynions.plugins": ["*.py"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    cmdclass={
        "install": PostInstallCommand,
    },
)
