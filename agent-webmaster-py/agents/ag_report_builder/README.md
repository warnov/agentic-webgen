# AG Report Builder Agent

An intelligent agent that analyzes JSON datasets and creates comprehensive HTML reports with appropriate visualizations using predefined HTML templates.

## Features

- **Smart Format Detection**: Automatically determines the best way to present data (charts, tables, or formatted text)
- **Template Integration**: Uses local HTML templates for consistent styling and structure
- **Complete HTML Generation**: Returns full HTML documents ready to save and view
- **Multiple Visualization Types**: Supports charts, tables, and formatted text reports
- **External Library Support**: Can reference popular JavaScript charting libraries (Chart.js, D3.js, Plotly.js)
- **Template Loading**: Built-in functionality to load and inject content into HTML templates

## Architecture

The agent uses a template-based approach:
1. **Template Loading**: Local function loads HTML template from the tools folder
2. **Content Analysis**: Agent analyzes the JSON dataset structure
3. **Format Decision**: Determines the best visualization approach
4. **Template Injection**: Injects generated report content into the template
5. **Complete HTML**: Returns a full HTML document ready for use

## Tools Folder

The `tools/` folder contains:
- `template_loader.py`: Functions for loading HTML templates
- `template_example.html`: Default HTML template with styling

### Template Loader Functions

```python
from tools.template_loader import load_html_template, get_available_templates

# Load a template
template_content = load_html_template("template_example.html")

# Get available templates
templates = get_available_templates()
```

## Usage

### Basic Testing
```bash
python ag_report_builder_tester.py
```

### Programmatic Usage
```python
from agents.ag_report_builder import ag_report_builder
from agents.ag_report_builder.tools.template_loader import load_html_template
import json

# Get agent instance
agent = ag_report_builder.instance
client = ag_report_builder.client

# Prepare your dataset
dataset = {
    "sales": [
        {"month": "January", "revenue": 50000},
        {"month": "February", "revenue": 65000}
    ]
}

# Create conversation
thread = client.threads.create()
client.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"Build a report from this dataset: {json.dumps(dataset, indent=2)}"
)

# Run agent (template is automatically loaded and included)
run = client.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id
)

# Get results - will be complete HTML document
if run.status == "completed":
    messages = list(client.messages.list(thread_id=thread.id))
    for msg in reversed(messages):
        if msg.role == "assistant":
            complete_html = msg.content[0].text.value
            print(complete_html)
            break
```

## Dataset Examples

### Sales Data (Chart Recommended)
```json
{
    "sales": [
        {"month": "January", "revenue": 50000, "units_sold": 120},
        {"month": "February", "revenue": 65000, "units_sold": 150},
        {"month": "March", "revenue": 80000, "units_sold": 180}
    ]
}
```

### Employee Data (Table Recommended)
```json
{
    "employees": [
        {"name": "John Doe", "department": "Engineering", "salary": 95000},
        {"name": "Jane Smith", "department": "Marketing", "salary": 75000}
    ]
}
```

### Survey Results (Formatted Text + Chart Recommended)
```json
{
    "survey": {
        "title": "Customer Satisfaction Survey 2025",
        "total_responses": 1250,
        "satisfaction_rating": 4.2,
        "key_findings": [
            "85% of customers rate our service as excellent or good",
            "Response time is the most mentioned improvement area"
        ]
    }
}
```

## Template Integration

The agent now uses a sophisticated template loading strategy:

1. **Automatic Template Loading**: The HTML template is automatically loaded from the tools folder when the agent is created
2. **Complete Document Generation**: The agent returns a full HTML document with the report content injected into the template
3. **Template Structure**: The agent works with this template structure:

```html
<section class="report-card" id="report-container">
    <h2>Report Title Placeholder</h2>
    <!-- Inject table, chart, or text report here -->
</section>
```

The agent will:
- Load the complete HTML template
- Replace the title placeholder with an appropriate report title
- Inject the generated report content in place of the comment
- Add any necessary CSS or JavaScript for charts/visualizations
- Return the complete, ready-to-use HTML document

## Output Format

The agent returns a complete HTML document with:
- Full HTML structure (DOCTYPE, html, head, body)
- Embedded CSS styles from the template plus any additional styles needed
- Embedded JavaScript for charts (if needed)
- CDN references for external libraries (when appropriate)
- Professional styling and responsive design
- Report content seamlessly integrated into the template

## Tools Folder

The `tools/` folder contains:
- `template_loader.py`: Functions for loading HTML templates
- `template_example.html`: Default HTML template with styling
