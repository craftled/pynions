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
from pynions.plugins.serper_plugin import SerperPlugin
from pynions.plugins.litellm_plugin import LiteLLMPlugin

# Create workflow
workflow = Workflow(
    name="content_research",
    description="Research and analyze content"
)

# Add steps
workflow.add_step(WorkflowStep(
    plugin=SerperPlugin(config),
    name="search",
    description="Search for content"
))

workflow.add_step(WorkflowStep(
    plugin=LiteLLMPlugin(config),
    name="analyze",
    description="Analyze content"
))

# Execute
results = await workflow.execute(initial_input)
```

## Example Workflows

### 1. SERP Analysis Workflow
```python
async def serp_analysis_workflow():
    # Initialize components
    config = Config()
    data_store = DataStore()
    
    # Setup plugins
    serper = SerperPlugin(config.get_plugin_config('serper'))
    llm = LiteLLMPlugin(config.get_plugin_config('litellm'))
    
    # Create workflow
    workflow = Workflow("serp_analysis")
    
    # Add steps
    workflow.add_step(WorkflowStep(
        plugin=serper,
        name="fetch_serp"
    ))
    
    workflow.add_step(WorkflowStep(
        plugin=llm,
        name="analyze_results"
    ))
    
    # Execute
    results = await workflow.execute({
        'query': 'best project management software'
    })
    
    # Save results
    data_store.save(results, "serp_analysis")
    
    return results
```

### 2. Content Creation Workflow
```python
async def content_creation_workflow():
    workflow = Workflow("content_creation")
    
    # Research step
    workflow.add_step(WorkflowStep(
        plugin=SerperPlugin(config),
        name="research"
    ))
    
    # Scraping step
    workflow.add_step(WorkflowStep(
        plugin=PlaywrightPlugin(config),
        name="scrape"
    ))
    
    # Analysis step
    workflow.add_step(WorkflowStep(
        plugin=JinaPlugin(config),
        name="extract"
    ))
    
    # Writing step
    workflow.add_step(WorkflowStep(
        plugin=LiteLLMPlugin(config),
        name="write"
    ))
    
    return await workflow.execute(initial_data)
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
def validate_input(input_data: Dict[str, Any]) -> bool:
    required_fields = ['query', 'max_results']
    return all(field in input_data for field in required_fields)
```

### 2. Result Storage
```python
def store_results(results: Dict[str, Any], workflow_name: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
