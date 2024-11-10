---
title: "Debugging"
publishedAt: "2024-10-30"
updatedAt: "2024-11-10"
summary: "Learn how to debug and troubleshoot common issues when developing plugins and workflows in Pynions, including installation problems, API errors, and testing failures."
kind: "detailed"
---

## Common Issues & Solutions

### 1. Installation Issues

#### Module Not Found
```bash
Error: ModuleNotFoundError: No module named 'pynions'
```

Solution:
```bash
# Verify virtual environment is activated
which python

# Should show: ~/Documents/pynions/venv/bin/python
# If not, activate venv:
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

#### Playwright Issues
```bash
Error: Browser executable not found
```

Solution:
```bash
# Install browsers
playwright install

# If that fails, try with sudo
sudo playwright install

# Verify installation
playwright --version
```

### 2. API Issues

#### Serper API Issues

##### API Key Not Found
```python
Error: SERPER_API_KEY not found in environment variables
```

Solution:
```bash
# Check if environment variables are loaded
python -c "import os; print(os.getenv('SERPER_API_KEY'))"

# If None, verify .env file contains:
SERPER_API_KEY=your_serper_key_here

# Reload environment:
source venv/bin/activate
```

##### Invalid Response Format
```python
Error: Serper API error: 401 (Invalid API key)
```

Solution:
1. Verify API key is valid in Serper dashboard
2. Check API service status
3. Monitor credit usage

##### Rate Limits
```python
Error: 429 Too Many Requests
```

Solution:
```python
# Add retry logic to config.json
{
  "plugins": {
    "serper": {
      "max_results": 10,
      "retry_attempts": 3,
      "retry_delay": 5
    }
  }
}
```

### 3. Workflow Issues

#### Step Execution Failure
```python
Error: Step 'fetch_serp' failed: Connection timeout
```

Debug Steps:
1. Test SerperWebSearch independently:
```python
# Test search independently
async def test_search():
    searcher = SerperWebSearch({
        "max_results": 10
    })
    return await searcher.execute({
        "query": "test query"
    })

# Run test
await test_search()
```

2. Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 4. Data Storage Issues

#### Permission Errors
```bash
Error: Permission denied: './data/results.json'
```

Solution:
```bash
# Fix permissions
chmod 755 data
chmod 644 data/*.json

# Verify
ls -la data/
```

## Debugging Tools

### 1. Logging

Enable detailed logging:
```python
# In your script
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
```

### 2. Interactive Debugging

Using iPython:
```bash
# Install iPython
pip install ipython

# Start interactive session
ipython

# Import and test components
from pynions.core import *
```

### 3. Visual Studio Code Debugging

1. Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

2. Set breakpoints and run debugger

## Performance Analysis

### 1. Time Profiling
```python
import time

class TimingWorkflowStep(WorkflowStep):
    async def execute(self, input_data):
        start_time = time.time()
        result = await super().execute(input_data)
        duration = time.time() - start_time
        print(f"Step {self.name} took {duration:.2f} seconds")
        return result
```

### 2. Memory Profiling
```bash
# Install memory profiler
pip install memory_profiler

# Run with profiling
python -m memory_profiler your_script.py
```

## Testing

### 1. Unit Tests
```python
# tests/test_plugins/test_serper.py
import pytest
from pynions.plugins.serper import SerperWebSearch

@pytest.mark.asyncio
async def test_serper_search():
    searcher = SerperWebSearch({
        "max_results": 10
    })
    result = await searcher.execute({
        "query": "test query"
    })
    assert result is not None
    assert "organic" in result
    assert "peopleAlsoAsk" in result
    assert "relatedSearches" in result
```

### 2. Integration Tests
```python
# tests/test_workflows/test_serp_workflow.py
import pytest
from pynions.core import Workflow
from pynions.plugins.serper import SerperWebSearch

@pytest.mark.asyncio
async def test_serp_workflow():
    workflow = Workflow("serp_test")
    workflow.add_step(WorkflowStep(
        plugin=SerperWebSearch({"max_results": 10}),
        name="fetch_serp"
    ))
    result = await workflow.execute({
        "query": "test query"
    })
    assert result is not None
```

## Monitoring

### 1. Basic Monitoring
```python
class MonitoredWorkflow(Workflow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = None
        self.metrics = {}
    
    async def execute(self, input_data):
        self.start_time = time.time()
        try:
            result = await super().execute(input_data)
            self.metrics['duration'] = time.time() - self.start_time
            self.metrics['success'] = True
            return result
        except Exception as e:
            self.metrics['success'] = False
            self.metrics['error'] = str(e)
            raise
```

### 2. Resource Monitoring
```python
import psutil

def log_system_metrics():
    metrics = {
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent
    }
    logging.info(f"System metrics: {metrics}")
```

## Best Practices

1. Always use virtual environment
2. Keep logs for debugging
3. Test components individually
4. Monitor resource usage
5. Use version control
6. Document errors and solutions

## Getting Help

1. Check logs first
2. Review documentation
3. Test in isolation
4. Use debugging tools
5. Ask specific questions

## Common Serper Response Issues

### 1. Missing Data Fields
If certain fields are missing from the response:
```python
# Check if fields exist before accessing
if "peopleAlsoAsk" in result and result["peopleAlsoAsk"]:
    # Process people also ask data
    pass

if "relatedSearches" in result and result["relatedSearches"]:
    # Process related searches
    pass
```

### 2. Rate Limit Monitoring
```python
# Monitor credit usage
if "credits" in result:
    logging.info(f"Credits used: {result['credits']}")
    if result["credits"] > threshold:
        logging.warning("High credit usage detected")
```

### 3. Response Validation
```python
def validate_serper_response(result):
    """Validate Serper API response"""
    required_fields = ["searchParameters", "organic"]
    for field in required_fields:
        if field not in result:
            logging.error(f"Missing required field: {field}")
            return False
    return True
```
