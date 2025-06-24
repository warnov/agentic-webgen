# AG WebGen Agent

This agent is responsible for generating web cards and managing web-related functionality. It integrates with Azure Functions and can work with both specific and random card data.

## Features

- **Web Card Generation**: Creates professional cards using Azure Functions
- **Random Data Integration**: Uses the data generator agent for creative card content
- **Flexible Input**: Accepts both specific card data and random generation requests
- **Azure Integration**: Connects to Azure AI Foundry and Azure Functions

## Functions

### `generate_card_from_data(card_data: dict) -> str`
Generates a card using specific card data provided by the user.

**Parameters:**
- `card_data`: Dictionary with keys: title, name, city, profession, message

**Returns:**
- URL string of the generated card

### `generate_card_with_random_data() -> str`
Generates a card using random, AI-generated data.

**Returns:**
- URL string of the generated card

### `get_agent_info() -> dict`
Returns information about the webgen agent.

### `list_all_agents() -> list`
Lists all agents in the current project.

### `delete_webgen_agent() -> dict`
Deletes the webgen agent from Azure AI Foundry (use with caution).

## Tools Used

- **Azure Function Tool**: For card generation and web publishing
- **Data Generator Agent**: For creating random card data
- **OpenAPI Integration**: For connecting to external services

## Configuration

The agent uses the same configuration file (`config.json`) as the main application and requires the following environment variables:

- `PROJECT_ENDPOINT`: Azure AI Foundry project endpoint
- `MODEL_DEPLOYMENT_NAME`: AI model deployment name
- `AZURE_FUNCTION_URL`: Azure Function endpoint for card generation

## Usage

```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "agents", "ag_webgen"))
from ag_webgen import generate_card_from_data, generate_card_with_random_data

# Generate with specific data
card_data = {
    "title": "Professional Card",
    "name": "John Doe",
    "city": "San Francisco",
    "profession": "Software Engineer",
    "message": "Passionate about building scalable solutions."
}
url = generate_card_from_data(card_data)

# Generate with random data
random_url = generate_card_with_random_data()
```
