---
title: "Data Organization"
publishedAt: "2024-11-09"
updatedAt: "2024-11-14"
summary: "Learn how to organize data and content workflows in Pynions."
kind: "detailed"
---

Pynions uses a structured approach to organize data and content workflows.

## Directory Structure

```
data/
├── output/           # All workflow outputs
│   └── [project]/    # Project-specific folders
│       ├── assets/    # Project-specific assets
│       └── [status]_[project]_[date].[ext]
└── raw/              # Original, unmodified data
    ├── scraped_data/ # Raw scraped content
    └── logs/         # Application logs
```

## Data Folders

- `data`: Processed data files
- `assets`: Related assets and resources

## Workflow Status Types

Content goes through six (optional) stages in a typical workflow:

- `1_research`: Initial research and data gathering
- `2_brief`: Content brief or outline
- `3_outline`: Detailed content structure
- `4_draft`: First version of content
- `5_review`: Content under review
- `6_final`: Final approved version

## File Naming Convention

Files are automatically named using the following pattern:
`[status]_[project]_[YYYY_MM_DD].[extension]`

Examples:

```
1_research_best_mailchimp_alternatives_2024_ 03_09.md
2_brief_best_mailchimp_alternatives_2024_03_09.md
4_draft_best_mailchimp_alternatives_2024_03_09.md
```

## Usage

Save content at different stages of your workflow:

```python
from pynions.core.utils import save_result

# Save research content
save_result(
    content="Research findings...",
    project_name="best-mailchimp-alternatives",
    status="research"
)

# Save draft content
save_result(
    content="Draft content...",
    project_name="best-mailchimp-alternatives",
    status="draft"
)

# Save related data
save_result(
    content='{"data": "metrics"}',
    project_name="best-mailchimp-alternatives",
    status="data",
    extension="json"
)
```

## Raw Data Storage

For storing raw data from various sources:

```python
from pynions.core.utils import save_raw_data

# Save scraped content
save_raw_data(
    content="Raw scraped content...",
    source="serper",
    data_type="scraped_data"
)

# Save log data
save_raw_data(
    content="Log entry...",
    source="workflow",
    data_type="logs"
)
```

## Configuration

Status types and their properties are configured in `settings.json`:

```json
{
  "workflow": {
    "status_types": {
      "research": {
        "description": "Initial research and data gathering",
        "extensions": ["md", "txt"]
      },
      "brief": {
        "description": "Content brief or outline",
        "extensions": ["md"]
      },
      "draft": {
        "description": "First version of content",
        "extensions": ["md"]
      }
      // ... other status types
    }
  }
}
```

## Best Practices

1. **Project Names**

   - Use descriptive, hyphen-separated names
   - Keep names consistent across related content
   - Example: "best-mailchimp-alternatives"

2. **Content Organization**

   - Create a new project folder for each content initiative
   - Keep all related files within the project folder
   - Use appropriate status types to track progress

3. **Raw Data**

   - Always save original, unmodified data in the raw directory
   - Use descriptive source names
   - Include timestamps for tracking

4. **File Extensions**
   - Use `.md` for content files (research, briefs, drafts)
   - Use `.json` for structured data
   - Use `.txt` for plain text and logs

## Data Lifecycle

1. **Creation**

   - Raw data is saved in appropriate raw/ subdirectories
   - New project folders are created as needed

2. **Processing**

   - Content moves through various status types
   - Each stage saved with appropriate status

3. **Completion**

   - Final content marked with 'final' status
   - Raw data retained for reference

4. **Maintenance**
   - Regular cleanup of old raw data
   - Archive completed projects as needed
