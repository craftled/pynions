# Contributing to Pynions 🤖

Hey there! Thanks for considering contributing to Pynions. This guide will help you get started, even if you're new (like me) to coding or open source.

## 🎯 What We're Building

Pynions is a simple tool that helps marketers automate their tasks using AI. Think of it like building tiny minions that help you with your marketing work - like writing tweets, checking prices, or researching content.

## 🚀 Getting Started (Easy Mode)

### Step 1: Set Up Your Computer

1. **Install These Free Tools**

   - [VS Code](https://code.visualstudio.com/) or [Cursor](https://cursor.sh/) - These are like Microsoft Word but for code
   - [Python](https://www.python.org/downloads/) - The programming language we use
   - [Git](https://git-scm.com/downloads) - Helps us save and share code changes

2. **Get the Code**

   ```bash
   # Copy these commands into your terminal/command prompt
   git clone https://github.com/tomaslau/pynions.git
   cd pynions
   ```

3. **Set Up Your Development Space**

   ```bash
   # On Windows, use 'python' instead of 'python3'
   python3 -m venv venv

   # On Mac/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate

   # Install development tools
   pip install -e ".[dev]"
   ```

### Step 2: Make Changes

1. **Create Your Own Branch**

   ```bash
   git checkout -b feature/your-cool-feature
   ```

2. **Test Your Changes**

   ```bash
   # Run the tests
   pytest

   # Make your code pretty
   black .
   isort .
   ```

### Step 3: Share Your Changes

1. **Save Your Changes**

   ```bash
   git add .
   git commit -m "Describe what you changed"
   git push origin feature/your-cool-feature
   ```

2. **Create a Pull Request**
   - Go to [Pynions on GitHub](https://github.com/tomaslau/pynions)
   - Click "Pull Requests"
   - Click "New Pull Request"
   - Select your branch
   - Tell us what you changed and why

## 🎨 Style Guide

We keep things simple:

- Use clear, descriptive names
- Add comments to explain complex stuff
- Keep functions small and focused
- Add tests for new features

## 🤔 Need Help?

1. **Check the Examples**
   Look in the `examples/` folder for inspiration

2. **Ask Questions**
   - [Open an issue on GitHub](https://github.com/tomaslau/pynions/issues/new)
   - Explain what you're trying to do
   - Share any error messages you see

## 🎉 Your First Contribution Ideas

1. **Add Examples**

   - Create new workflow examples
   - Show how to solve real marketing problems

2. **Improve Documentation**

   - Fix typos
   - Make instructions clearer
   - Add more examples

3. **Add Features**
   - New AI tools
   - New marketing integrations
   - Better error messages

## 🛠 Project Structure

```bash
myproject/
├── workflows/          # Your workflows
├── data/              # Local storage
├── logs/              # Workflow logs
└── .cache/            # API cache
```

## 🔑 Environment Setup

1. **Required API Keys**
   ```bash
   OPENAI_API_KEY=your_openai_key_here          # Required
   SERPER_API_KEY=your_serper_key_here          # Optional, for search
   PERPLEXITY_API_KEY=your_perplexity_key_here  # Optional, for research
   ```

## 💻 CLI Commands

Our CLI makes it easy to work with workflows:

```bash
pynions run        # Run a workflow
pynions new        # Create a new workflow
pynions list       # List all workflows
pynions check      # Check a workflow
pynions check-all  # Check all workflows and sources
```

## 🔧 Development Tools

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",         # Testing framework
    "black>=23.0.0",         # Code formatting
    "isort>=5.0.0",         # Import sorting
    "mypy>=1.0.0",          # Type checking
    "build>=1.0.0",         # Package building
    "twine>=4.0.0",         # PyPI uploading
    "pytest-asyncio>=0.23.0" # Async test support
]
```

## 📚 Documentation Tools

We use these tools to keep our docs awesome:

- Markdown for all documentation
- Mintlify for hosting
- GitHub Actions for CI/CD

## 📝 Documentation

Our documentation lives in several places:

1. **Quick Start & Usage**

   - `README.md` - Main documentation and getting started guide
   - `examples/` - Real-world examples and use cases
   - Code comments - Inline documentation in Python files

2. **Contributing**

   - `CONTRIBUTING.md` (this file) - How to contribute
   - `CODE_OF_CONDUCT.md` - Community guidelines
   - GitHub Issue/PR templates - How to report issues and submit changes

3. **API Documentation**

   - Function and class docstrings
   - Type hints in code
   - Example outputs in comments

4. **How to Update Docs**

   - Update `README.md` for user-facing changes
   - Add examples to `examples/` for new features
   - Add docstrings to new functions/classes
   - Keep code comments clear and helpful
   - Follow our simple style:

     ```python
     def my_function(param: str) -> dict:
         """
         Short description of what this does.

         Args:
             param: What this parameter is for

         Returns:
             What this function returns
         """
     ```

5. **Documentation Tips**
   - Write for beginners
   - Include code examples
   - Explain the "why" not just the "how"
   - Keep it simple and clear
   - Test your examples

## ⚙️ Development Tools

We use these tools to keep our code nice:

- [pyproject.toml](pyproject.toml)
  [project.optional-dependencies]
  dev = [
  "pytest>=7.0.0", # Testing framework
  "black>=23.0.0", # Code formatting
  "isort>=5.0.0", # Import sorting
  "mypy>=1.0.0", # Type checking
  "build>=1.0.0", # Package building
  "twine>=4.0.0", # PyPI uploading
  "pytest-asyncio>=0.23.0" # Async test support
  ]

## 🌟 Recognition

- All contributors get added to our README
- We celebrate all contributions, big and small
- Your name gets added to our [Contributors](https://github.com/tomaslau/pynions/graphs/contributors) page

Remember: There's no such thing as a contribution too small. Even fixing a typo helps!

Need more help? Just ask! We're friendly. 😊

## 📦 Release Process

1. **Update Version**

   ```bash
   # Update version in src/pynions/__init__.py
   __version__ = "0.1.1"
   ```

2. **Build and Test Package**

   ```bash
   python -m build
   twine check dist/*
   ```

3. **Test Upload to TestPyPI**

   ```bash
   twine upload --repository testpypi dist/*
   ```

4. **Upload to PyPI**
   ```bash
   twine upload dist/*
   ```
