# Agentic Webgen - Agent-based Card Generation System

## Project Overview

This project implements GenAI Web Content generation using as an example a professional card generation and publishing system using Azure AI Foundry agents. The system supports both AI-generated random data and user-specified information, integrating multiple agents through the ConnectedAgentTool pattern.

## 🏗️ Project Structure

```
agent-webmaster-py/
├── agents/                           # Agents folder
│   ├── ag_data_generator/            # Data Generator Agent
│   │   ├── ag_data_generator.py      # Main agent implementation
│   │   └── README.md                 # Agent documentation
│   └── ag_webgen/                    # Web Generation Agent
│       ├── ag_webgen.py               # Web agent with Azure Function
│       ├── README.md                 # Agent documentation
│       └── tools/                    # Agent-specific tools
│           ├── card_generator.py     # Local random card generation
│           └── html_tools.py         # HTML processing utilities
├── utils/                            # Utility functions
│   ├── openapi_loader.py             # OpenAPI spec utilities
│   └── test_storage.py               # Storage testing utilities
├── config.json                       # Agent configuration
├── openapi_spec.json                 # Azure Function OpenAPI spec
├── azfx-tool-main.py                 # Main agent with integrations
├── test_integration.py               # Integration testing suite
├── interactive_demo.py               # Interactive demo interface
├── example_agent_usage.py            # Agent transparent instantiation examples
├── WEBGEN_AGENT_GUIDE.md             # Webgen agent usage guide
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

## 🚀 Key Features

### 1. Multi-Agent Architecture
- **Main Agent (`html-template-agent`)**: Orchestrates card generation and publishing
- **Data Generator Agent (`card-data-generator`)**: Creates AI-generated random card data
- **ConnectedAgentTool Integration**: Seamless agent-to-agent communication

### 2. Dual Data Sources
- **AI-Generated Data**: Creative, diverse professional card data via Azure AI
- **User-Specified Data**: Direct input processing for custom cards
- **Hybrid Approach**: Intelligent mixing of provided and generated data

### 3. Smart Agent Management
- **Single Instance Creation**: Agents are only created once in Azure AI Foundry
- **Agent Discovery**: Automatic detection of existing agents
- **Resource Optimization**: Reuses existing agents to prevent duplicates

### 4. Production-Ready Features
- **Modular Design**: Clean separation of concerns
- **Error Handling**: Robust error management and recovery
- **Configuration Management**: Externalized configuration
- **Comprehensive Testing**: Full integration test suite

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.8+
- Azure AI Foundry project
- Azure OpenAI deployment
- Azure Function for HTML template processing

### Environment Variables
```bash
PROJECT_ENDPOINT=<your-azure-ai-foundry-endpoint>
MODEL_DEPLOYMENT_NAME=<your-openai-model-deployment>
AZURE_FUNCTION_URL=<your-azure-function-url>
```

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd agent-webmaster-py

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Azure credentials
```

## 🎯 Usage

### Quick Start
```bash
# Run the main integrated system
python azfx-tool-main.py

# Run integration tests
python test_integration.py

# Interactive demo
python interactive_demo.py
```

### Programming Interface

#### Generate Random Cards
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "agents", "ag_data_generator"))
from ag_data_generator import generate_random_card_data

# Generate AI-powered random card data
card_data = generate_random_card_data()
print(card_data)
```

#### Use as ConnectedAgentTool
```python
import sys
import os
from azure.ai.agents.models import ConnectedAgentTool
sys.path.append(os.path.join(os.path.dirname(__file__), "agents", "ag_data_generator"))
from ag_data_generator import _create_data_generator_agent

# Create connected tool
data_generator_agent = _create_data_generator_agent()
tool = ConnectedAgentTool(
    id=data_generator_agent.id,
    name="generate_random_card_data",
    description="Generates random professional card data"
)
```

#### Local Random Generation
```python
from tools.card_generator import generate_random_card

# Generate using local data
local_card = generate_random_card()
print(local_card)
```

## 🧪 Testing

### Run All Tests
```bash
# Comprehensive integration tests
python test_integration.py

# Test data generator agent directly
python agents/ag_data_generator/ag_data_generator.py

# Test local tools
python tools/card_generator.py
```

### Test Scenarios
1. **Random AI Generation**: Generates creative, diverse card data
2. **Specific User Data**: Processes provided information
3. **Partial Data Completion**: Fills missing details with AI
4. **Agent Reuse**: Verifies single instance creation

## 🔧 Configuration

### Agent Configuration (`config.json`)
```json
{
  "agent": {
    "name": "html-template-agent",
    "instructions": "Agent instructions with dual capabilities..."
  },
  "tool": {
    "name": "fill_template_from_json",
    "description": "HTML template filling tool",
    "openapi_spec_file": "openapi_spec.json"
  }
}
```

### Key Configuration Points
- **Agent Instructions**: Support both random and specific data modes
- **Tool Descriptions**: Clear descriptions for ConnectedAgentTool
- **OpenAPI Specs**: External Azure Function integration

## 📊 Architecture Patterns

### ConnectedAgentTool Pattern
- **Agent Discovery**: Check for existing agents before creation
- **Tool Registration**: Register agents as tools for other agents
- **Message Passing**: Structured communication between agents

### Error Handling Strategy
- **Graceful Degradation**: Fallback to local tools if AI fails
- **Validation**: JSON schema validation for generated data
- **Logging**: Comprehensive logging for debugging

### Resource Management
- **Singleton Agents**: Prevent duplicate agent creation
- **Connection Pooling**: Reuse Azure AI client connections
- **Memory Management**: Efficient global variable usage

## 🎨 Example Outputs

### AI-Generated Card Data
```json
{
  "title": "Executive Profile",
  "name": "Sofia Almeida",
  "city": "Lisbon",
  "profession": "Marketing Manager",
  "message": "Experienced professional specialized in digital marketing strategies for global brands."
}
```

### Generated HTML URLs
- `https://saimpartnerdemo.blob.core.windows.net/templates/filled_template_20250624031046.html`
- Professional card templates with responsive design
- Direct access to published cards

## 🔄 Development Workflow

### Adding New Agents
1. Create folder in `agents/` directory
2. Implement agent with discovery logic
3. Create README documentation
4. Add integration tests
5. Update import paths as needed

### Extending Functionality
1. Update agent instructions in `config.json`
2. Add new ConnectedAgentTools
3. Update integration tests
4. Document new capabilities

## 🤝 Contributing

1. Follow the established folder structure
2. Implement single-instance creation for new agents
3. Add comprehensive error handling
4. Include integration tests
5. Update documentation

## 📝 License

[Your License Here]

---

## 🎉 Recent Updates

### v1.0.0 - Project Refactoring
- ✅ Reorganized into modular `agents/` structure
- ✅ Implemented proper Python package structure
- ✅ Added comprehensive documentation
- ✅ Maintained full backward compatibility
- ✅ Enhanced testing capabilities
- ✅ Improved code organization and maintainability
