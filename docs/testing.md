---
title: "Testing"
publishedAt: "2024-11-03"
updatedAt: "2024-11-03"
summary: "A beginner's guide to testing in Pynions using pytest."
kind: "simple"
---

# Testing with pytest

## Quick Start

1. Make sure you're in your virtual environment:
```bash
source venv/bin/activate
```

2. Run all tests:
```bash
pytest
```

3. Run tests with output:
```bash
pytest -v  # verbose output
pytest -s  # show print statements
pytest -v -s  # both verbose and print statements
```

## Environment Setup

1. Install test dependencies:
```bash
pip install -e .
pip install pytest pytest-asyncio pytest-cov
```

2. Create basic test structure:
```bash
mkdir -p tests/test_plugins
touch tests/__init__.py tests/test_plugins/__init__.py
```

## Basic Test Structure

Create test files in the `tests/` directory:

```python
# tests/test_example.py
def test_basic_example():
    result = 1 + 1
    assert result == 2
```

## Testing Async Functions

For testing async functions (like our Serper plugin):

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

## Test Configuration

Create `pytest.ini` in your project root:

```ini
[pytest]
python_files = test_*.py
python_classes = Test*
python_functions = test_*
testpaths = tests
addopts = -v -s --tb=short
asyncio_mode = auto
```

## Common Testing Patterns

### 1. Setup and Teardown

Use fixtures for common setup:

```python
import pytest

@pytest.fixture
def sample_data():
    """Provide sample data for tests"""
    return {
        "query": "test query",
        "max_results": 10
    }

def test_with_fixture(sample_data):
    assert sample_data["query"] == "test query"
```

### 2. Testing Exceptions

```python
import pytest

def test_error_handling():
    with pytest.raises(ValueError):
        # This should raise ValueError
        raise ValueError("Expected error")
```

### 3. Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("test", "TEST"),
    ("hello", "HELLO"),
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```

## Running Specific Tests

```bash
# Run single test file
pytest tests/test_example.py

# Run specific test function
pytest tests/test_example.py::test_basic_example

# Run tests matching pattern
pytest -k "test_basic"
```

## Test Coverage

1. Run tests with coverage:
```bash
pytest --cov=pynions

# With detailed report
pytest --cov=pynions --cov-report=html
```

2. View coverage report:
```bash
open htmlcov/index.html
```

## Best Practices

1. **Test File Organization**
   - Keep tests in `tests/` directory
   - Match source file structure
   - Use clear test names

2. **Test Naming**
   - Prefix test files with `test_`
   - Use descriptive test function names
   - Example: `test_serper_search_returns_results`

3. **Assertions**
   - Use specific assertions
   - Test one thing per test
   - Include error messages

4. **Environment**
   - Use fixtures for setup
   - Clean up after tests
   - Don't modify production data

## Debugging Tests

1. Show print output:
```bash
pytest -s
```

2. Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

3. Use breakpoints:
```python
def test_debug_example():
    breakpoint()  # Starts debugger here
    assert True
```

## Common Issues

1. **Module Not Found**
   - Check virtual environment
   - Install package in editable mode: `pip install -e .`

2. **Async Test Failures**
   - Use `@pytest.mark.asyncio`
   - Configure `asyncio_mode = auto`

3. **Fixture Errors**
   - Check fixture scope
   - Verify fixture dependencies

Need help? Check the debugging guide: `markdown:docs/debugging.md`

## Unit Tests

1. Test successful responses
2. Test error handling
3. Test rate limiting
4. Test invalid API keys

See the Serper plugin documentation for specific examples: