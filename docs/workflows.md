---
title: "Workflows"
publishedAt: "2024-10-30"
updatedAt: "2024-11-03"
summary: "Learn how to create and run marketing automation workflows by combining plugins into reusable sequences that execute locally on your machine."
kind: "detailed"
---

## Workflow System Overview

Workflows in Pynions are sequences of steps that:
- Execute plugins in order
- Pass data between steps
- Handle errors gracefully
- Store results

## Basic Workflow Structure

```python
from pynions.core import Workflow, WorkflowStep
from pynions.plugins.serper import SerperWebSearch
from pynions.plugins.litellm import LiteLLMPlugin

# Create workflow
workflow = Workflow(
    name="content_research",
    description="Research and analyze content"
)

# Add steps
workflow.add_step(WorkflowStep(
    plugin=SerperWebSearch({"max_results": 10}),
    name="search",
    description="Search for content"
))

workflow.add_step(WorkflowStep(
    plugin=LiteLLMPlugin(config),
    name="analyze",
    description="Analyze content"
))

# Execute
results = await workflow.execute({"query": "your search query"})
```

## Example Workflows

### 1. SERP Analysis Workflow
```python
async def serp_analysis_workflow():
    # Initialize components
    config = Config()
    data_store = DataStore()
    
    # Setup plugins
    serper = SerperWebSearch({
        "max_results": 10
    })
    llm = LiteLLMPlugin(config.get_plugin_config('litellm'))
    
    # Create workflow
    workflow = Workflow("serp_analysis")
    
    # Add steps
    workflow.add_step(WorkflowStep(
        plugin=serper,
        name="fetch_serp",
        description="Fetch search results"
    ))
    
    workflow.add_step(WorkflowStep(
        plugin=llm,
        name="analyze_results",
        description="Analyze SERP data"
    ))
    
    # Execute
    results = await workflow.execute({
        'query': 'best marketing automation tools 2024'
    })
    
    # Save results
    data_store.save(results, "serp_analysis")
    
    return results
```

### 2. Content Research Workflow
```python
async def content_research_workflow():
    workflow = Workflow("content_research")
    
    # SERP research step
    workflow.add_step(WorkflowStep(
        plugin=SerperWebSearch({"max_results": 10}),
        name="search",
        description="Search for relevant content"
    ))
    
    # Content extraction step
    workflow.add_step(WorkflowStep(
        plugin=JinaAIReader(config),
        name="extract",
        description="Extract content from top results"
    ))
    
    # Analysis step
    workflow.add_step(WorkflowStep(
        plugin=LiteLLMPlugin(config),
        name="analyze",
        description="Analyze extracted content"
    ))
    
    return await workflow.execute({
        "query": "marketing automation trends 2024"
    })
```

## Workflow Best Practices

1. Planning
   - Define clear objectives
   - Map out data flow
   - Identify required plugins
   - Plan error handling

2. Implementation
   - Single responsibility steps
   - Clear step names
   - Proper error handling
   - Data validation

3. Testing
   - Test individual steps
   - Test complete workflow
   - Test error cases
   - Validate results

4. Monitoring
   - Log important events
   - Track execution time
   - Monitor resource usage
   - Save results

## Advanced Workflow Features

### 1. Conditional Steps
```python
class ConditionalStep(WorkflowStep):
    def __init__(self, condition, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.condition = condition
        
    async def execute(self, input_data):
        if self.condition(input_data):
            return await super().execute(input_data)
        return input_data
```

### 2. Parallel Execution
```python
class ParallelSteps(WorkflowStep):
    def __init__(self, steps, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.steps = steps
        
    async def execute(self, input_data):
        tasks = [step.execute(input_data) for step in self.steps]
        return await asyncio.gather(*tasks)
```

### 3. Retry Logic
```python
class RetryStep(WorkflowStep):
    def __init__(self, max_retries=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_retries = max_retries
        
    async def execute(self, input_data):
        for i in range(self.max_retries):
            try:
                return await super().execute(input_data)
            except Exception as e:
                if i == self.max_retries - 1:
                    raise
                await asyncio.sleep(2 ** i)
```

## Error Handling

### 1. Step-Level Errors
```python
try:
    result = await step.execute(input_data)
except Exception as e:
    logger.error(f"Step {step.name} failed: {str(e)}")
    if isinstance(e, ValueError):
        # Handle validation errors
        pass
    elif isinstance(e, aiohttp.ClientError):
        # Handle API errors
        pass
    raise
```

### 2. Workflow-Level Errors
```python
try:
    results = await workflow.execute(input_data)
except Exception as e:
    logger.error(f"Workflow failed: {str(e)}")
    # Cleanup or rollback if needed
    raise
```

## Data Handling

### 1. Input Validation
```python
def validate_serp_input(input_data: Dict[str, Any]) -> bool:
    """Validate input for SERP analysis workflow"""
    if not isinstance(input_data, dict):
        return False
    if 'query' not in input_data:
        return False
    return True
```

### 2. Result Storage
```python
def store_results(results: Dict[str, Any], workflow_name: str):
    """Store workflow results with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/{workflow_name}_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    return filename
```
