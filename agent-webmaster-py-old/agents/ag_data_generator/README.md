# AG Data Generator Agent

## Overview

The AG Data Generator is an Azure AI Foundry agent that generates creative, diverse professional business card data. It's designed to work seamlessly with the main card publishing system and ensures only one instance is created in Azure AI Foundry.

## Key Features

- **Single Instance Creation**: Checks for existing agents in Azure AI Foundry and only creates a new one if it doesn't exist
- **Creative AI Generation**: Uses AI to generate diverse, realistic professional card data
- **International Diversity**: Generates names, cities, and professions from various cultures and countries
- **Validated Output**: Returns properly formatted JSON with required fields
- **ConnectedAgentTool Integration**: Can be used as a tool by other agents in the system

## Generated Data Fields

Each generated card contains exactly these 5 fields:

- **title**: Professional card title (e.g., "Business Card", "Professional Profile")
- **name**: Realistic full name (diverse, international names)
- **city**: Real city name from any country
- **profession**: Realistic job title/profession
- **message**: Professional message/bio (1-2 sentences)

## Usage

### Direct Usage

```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "agents", "ag_data_generator"))
from ag_data_generator import generate_random_card_data

# Generate random card data
card_data = generate_random_card_data()
print(card_data)
```

### As ConnectedAgentTool

```python
import sys
import os
from azure.ai.agents.models import ConnectedAgentTool
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "agents", "ag_data_generator"))
from ag_data_generator import _create_data_generator_agent

# Create the agent and tool
data_generator_agent = _create_data_generator_agent()
data_generator_tool = ConnectedAgentTool(
    id=data_generator_agent.id,
    name="generate_random_card_data",
    description="Generates creative, random professional card data..."
)
```

## Environment Variables

Required environment variables:
- `PROJECT_ENDPOINT`: Azure AI Foundry project endpoint
- `MODEL_DEPLOYMENT_NAME`: Azure OpenAI model deployment name

## Example Output

```json
{
  "title": "Professional Card",
  "name": "Elena Rodriguez",
  "city": "Madrid",
  "profession": "Architect",
  "message": "Dedicated to creating sustainable and innovative architectural designs that enrich communities."
}
```

## Functions

- `generate_random_card_data()`: Main function to generate card data
- `get_agent_info()`: Get information about the agent instance
- `list_all_agents()`: List all agents in the project
- `delete_data_generator_agent()`: Delete the agent (use with caution)

## Testing

Run the agent directly to test functionality:

```bash
python agents/ag-data-generator/ag_data_generator.py
```

This will show existing agents, generate test data, and verify agent reuse.
