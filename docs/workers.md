---
title: "Workers"
publishedAt: "2024-11-10"
updatedAt: "2025-02-17"
summary: "Standalone task executors that perform single, focused operations using plugins."
kind: "detailed"
---

## Overview
Workers are specialized task executors that follow the single responsibility principle. Each worker is designed to do one thing and do it well, making them reliable, maintainable, and easily testable.

Unlike workflows that chain multiple steps together, workers are focused on a single, specific task. This makes them:
- More reliable (fewer points of failure)
- Easier to test and debug
- More maintainable over time
- Reusable across different workflows

## Key Principles
1. **Single Responsibility**
   - Each worker does exactly one thing
   - Clear, focused purpose
   - No task overlap between workers

2. **Independence**
   - Workers operate independently
   - No direct dependencies on other workers
   - Self-contained functionality

3. **Reliability**
   - Focused scope means fewer failure points
   - Easier to test and validate
   - Clear success/failure conditions

4. **Reusability**
   - Can be used in multiple workflows
   - Consistent interface
   - Well-defined inputs and outputs

## Available Workers

### PerplexityFeaturesWorker
Extracts feature information using Perplexity AI:
- Single focus: Feature extraction
- Uses official sources
- Saves raw responses for verification

#### Usage
```python
from pynions.workers import PerplexityFeaturesWorker

async def analyze_features():
    worker = PerplexityFeaturesWorker()
    result = await worker.execute({"domain": "example.com"})
```

### PerplexityPricingWorker
Advanced pricing data extraction using Perplexity AI's research capabilities:
1. **Direct URL Analysis**: Finds and validates official pricing pages
2. **First-Party Data**: Prioritizes data from official sources
3. **Cross-Reference**: Validates with trusted third-party sources
4. **Structured Output**: Clean, validated JSON with source tracking

#### Usage
```python
from pynions.workers import PerplexityPricingWorker

async def analyze_pricing():
    worker = PerplexityPricingWorker()
    result = await worker.execute({"domain": "example.com"})
```

## Creating Custom Workers

1. Inherit from base Worker class
```python
from pynions import Worker

class CustomWorker(Worker):
    """Worker with a single, focused purpose"""
    
    def __init__(self):
        # Initialize required plugin
        self.plugin = Plugin()

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Implement single focused task
        pass
```

## Best Practices

1. **Single Purpose**
   - One clear task per worker
   - Avoid feature creep
   - Clear documentation of purpose

2. **Error Handling**
   - Handle errors specific to the task
   - Clear error messages
   - Proper error propagation

3. **Data Management**
   - Save raw responses
   - Clear data structure
   - Proper file organization

4. **Testing**
   - Test single responsibility
   - Verify error cases
   - Validate output format

## Common Issues
- Scope creep (trying to do too much)
- Unclear responsibility boundaries
- Insufficient error handling
- Poor data organization

Need help? Check our [debugging guide](https://pynions.com/docs/debugging) for solutions.