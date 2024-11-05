from setuptools import setup, find_packages
import sys
import subprocess
from setuptools.command.install import install

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
        print("\n🎉 Pynions installed successfully!")
        print("📝 Next steps:")
        print("1. Create a .env file with your API keys")
        print("2. Copy config.example.json to config.json")
        print("3. Run: playwright install")

def run_playwright_install():
    try:
        subprocess.check_call(["playwright", "install"])
    except Exception as e:
        print("⚠️  Playwright browsers not installed. Run: playwright install")

setup(
    name="pynions",
    version="0.2.13",
    author="Tomas Laurinavicius",
    author_email="tom@pynions.com",
    description="Simple AI automation framework for marketers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tomaslau/pynions",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "pynions": ["py.typed"],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
)
