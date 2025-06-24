# Azure AI Foundry Agents with ConnectedAgentTool Integration

This project demonstrates how to build modular Azure AI Foundry agents in Python using the singleton pattern and ConnectedAgentTool for agent-to-agent communication.

## Architecture

### Agents

1. **ag_card_generator** - Generates creative business card data in JSON format
   - Location: `agents/ag_card_generator/`
   - Singleton pattern for efficient resource usage
   - Generates complete card data with: title, name, city, profession, message, date

2. **ag_web_gen** - Publishes cards as JSON for HTML templates
   - Location: `agents/ag_web_gen/`
   - Uses ConnectedAgentTool to access ag_card_generator
   - Can handle both complete and partial user data

### ConnectedAgentTool Integration

The `ag_web_gen` agent uses Azure AI Foundry's `ConnectedAgentTool` to communicate with `ag_card_generator`:

```python
from azure.ai.agents import ConnectedAgentTool

# Create ConnectedAgentTool for the card generator
card_generator_tool = ConnectedAgentTool(
    agent_id=card_generator_agent.id,
    name="card_generator",
    description="Generates creative business card data in JSON format"
)

# Create agent with the connected tool
web_agent = client.create_agent(
    model=os.environ.get("MODEL_DEPLOYMENT_NAME"),
    name="ag-web-gen",
    tools=[card_generator_tool]  # ConnectedAgentTool attached here
)
```

## Key Features

- **Singleton Pattern**: Each agent uses a singleton pattern for efficient resource management
- **ConnectedAgentTool**: Proper agent-to-agent communication following Azure AI Foundry best practices
- **Modular Design**: Clean separation of concerns with organized folder structure
- **Interactive Testing**: Comprehensive test scripts for validation

## Project Structure

```
agent-webmaster-py/
├── agents/
│   ├── ag_card_generator/
│   │   ├── ag_card_generator.py          # Card generator agent
│   │   └── ag_card_generator_tester.py   # Interactive tester
│   └── ag_web_gen/
│       ├── ag_web_gen.py                 # Web generator with ConnectedAgentTool
│       └── ag_web_gen_tester.py          # Interactive tester
├── .vscode/
│   └── settings.json                     # VS Code settings (hides __pycache__)
├── demo_connected_agents.py              # Demo script
├── test_agents_integration.py            # Integration tests
├── requirements.txt                      # Python dependencies
└── README.md                            # This file
```

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Azure Credentials**:
   Create a `.env` file with:
   ```
   PROJECT_ENDPOINT=https://your-ai-foundry-endpoint
   MODEL_DEPLOYMENT_NAME=your-model-deployment
   ```

3. **Azure Authentication**:
   Make sure you're authenticated with Azure CLI or have appropriate managed identity configured.

## Usage

### Testing Individual Agents

**Card Generator**:
```bash
# Interactive mode
python agents/ag_card_generator/ag_card_generator_tester.py

# JSON-only output
python agents/ag_card_generator/ag_card_generator_tester.py --json "Generate a card for a software engineer"
```

**Web Generator with ConnectedAgentTool**:
```bash
# Interactive mode
python agents/ag_web_gen/ag_web_gen_tester.py

# Direct usage
python agents/ag_web_gen/ag_web_gen_tester.py "Publish a card for Maria from Barcelona, generate missing details"
```

### Integration Testing

```bash
# Run full integration tests
python test_agents_integration.py

# Demo the connected agents setup
python demo_connected_agents.py
```

## How ConnectedAgentTool Works

1. **Agent Creation**: `ag_web_gen` is created with a `ConnectedAgentTool` that references `ag_card_generator`
2. **Tool Registration**: The ConnectedAgentTool is attached to the web generator agent's tools list
3. **Automatic Invocation**: When users request card publishing with missing data, the web generator automatically calls the card generator
4. **Seamless Integration**: The Azure AI Foundry service handles the agent-to-agent communication transparently

## Example Scenarios

### Scenario 1: Complete Data Provided
```
User: "Publish a card for John Doe, Software Engineer, New York, passionate about AI"
Web Gen: Returns formatted JSON directly
```

### Scenario 2: Partial Data - ConnectedAgentTool Triggered
```
User: "Publish a card for Maria from Barcelona, generate the rest"
Web Gen: Uses ConnectedAgentTool to call Card Generator for missing fields
Card Gen: Generates profession, message, etc.
Web Gen: Returns complete JSON with user data preserved
```

### Scenario 3: No Data - Full Generation
```
User: "Generate and publish a card for a creative professional"
Web Gen: Uses ConnectedAgentTool to call Card Generator
Card Gen: Creates complete creative card data
Web Gen: Returns formatted JSON ready for HTML template
```

## Benefits of This Architecture

1. **Modularity**: Each agent has a single responsibility
2. **Reusability**: Card generator can be used by multiple other agents
3. **Efficiency**: Singleton pattern prevents resource duplication
4. **Scalability**: Easy to add more connected agents
5. **Best Practices**: Follows Azure AI Foundry SDK patterns for agent communication

## VS Code Integration

The `.vscode/settings.json` file is configured to hide Python cache files:
- `__pycache__/` folders
- `.pyc` files
- `.pyo` files

This keeps the workspace clean and focused on source code.

## Error Handling

Both agents include comprehensive error handling:
- Azure authentication failures
- Network connectivity issues
- Invalid responses
- Tool execution errors
- JSON parsing errors

## Future Enhancements

- Add more specialized agents (image generator, template renderer, etc.)
- Implement agent orchestration patterns
- Add persistent storage for generated cards
- Create web interface for card publishing
- Add monitoring and logging capabilities
