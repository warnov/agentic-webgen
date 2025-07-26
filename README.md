# 🧠 Agentic Business Card Generator on Azure AI Foundry

This repository contains a hands-on example of an **agent-based application built with Azure AI Foundry**, focused on showcasing how intelligent agents can collaborate to generate and publish a fully customized personal business card.

## 🎯 Project Overview

This application demonstrates a **multi-agent architecture** in which a user interacts through natural language with an orchestrating agent, requesting the creation of a business card for a given person. The user can provide complete or partial information (name, location, profession, etc.), and the agents will intelligently infer and complete the rest to produce a realistic business card.

The final output is a **web-based HTML business card**, hosted publicly on Azure Blob Storage.

## 🧩 Architecture Summary

The system consists of two AI Foundry agents:

### 1. 🧠 Data Extraction Agent (powered by GPT-3.5)

- Receives raw, natural language input from the orchestrator agent.
- Extracts structured personal information from the input.
- Returns a clean JSON representation of the data.
- Does **not** use external tools — only a basic language model (GPT-3.5).

### 2. 🤖 Orchestrator Agent

- Serves as the main entry point for user interaction.
- Coordinates multiple steps using agent tools:
  - **Agent-to-Agent Tool:** Connects to the Data Extraction Agent to obtain structured data.
  - **Azure Function Tool:** Sends the resulting JSON to an Azure Function.
  - **Azure Function:** Fills an HTML template with the received data and uploads it to Azure Blob Storage.
- Finally, it returns the public URL of the generated HTML page (business card) to the user.

This demonstrates **tool-based orchestration**, **agent chaining**, and **integration with external services** like Azure Functions and Azure Storage — all within the AI Foundry framework.

## 🚀 What You'll Learn

- How to build and configure multi-agent solutions in Azure AI Foundry.
- How to create an agent that transforms unstructured input into structured JSON.
- How to orchestrate tools (like Azure Functions) from within an AI agent.
- How to deploy and publish HTML content via Azure Blob Storage.
- How to chain multiple agents for collaborative AI workflows.

---

## 🛠️ Installation & Requirements

This solution is fully **cross-platform** and works on **Windows, macOS, and Linux**. However, a convenience script is provided for **Windows** users to automate the installation process.

### ✅ Prerequisites

Make sure the following components are installed:

- [Git](https://git-scm.com/downloads)
- [Python 3.12+](https://www.python.org/downloads/)
- [.NET SDK 8+](https://dotnet.microsoft.com/download)
- [Visual Studio Code](https://code.visualstudio.com/)


### 🔌 Recommended VSCode Extensions

We recommend installing the following VSCode extensions to enhance your development experience:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) – for Python development and debugging (`ms-python.python`)
- [Azure Functions](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) – for managing and editing Azure Functions projects (`ms-azuretools.vscode-azurefunctions`)
- [C#](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csharp) – required for .NET Function tools and IntelliSense (`ms-dotnettools.csharp`)
- [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) – to test APIs directly from `.http` files in VSCode (`humao.rest-client`)

> These extensions allow for smooth development, debugging, and testing of both AI agents and supporting services like Azure Functions.

To install them manually, just search by name in the VSCode Extensions Marketplace or use the command line:

```bash
code --install-extension ms-python.python
code --install-extension ms-azuretools.vscode-azurefunctions
code --install-extension ms-dotnettools.csharp
code --install-extension humao.rest-client
```

---

### 🪟 Quick Setup for Windows

For Windows users, we've included an automated setup script:

```powershell
misc/setup-dev-win.ps1
```

This script will:

- Install Visual Studio Code
- Install Git
- Install Python 3.12
- Install .NET SDK 8
- Install all recommended VSCode extensions

> 🟡 **After running the script**, restart your terminal to ensure all tools are available in the current session.

You can run the script from PowerShell with:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; ./misc/setup-dev-win.ps1
```

---

If you're on **macOS or Linux**, just ensure you manually install the same components listed above. The rest of the setup and execution steps remain identical across all platforms.

---





## 🏗️ Architecture Overview

The solution consists of three main components:

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   Python Agents    │───▶│   Azure Function    │───▶│   Azure Storage     │
│                     │    │                     │    │                     │
│ • Card Generator    │    │ • Template Filler   │    │ • HTML Templates    │
│ • Web Generator     │    │ • HTTP Endpoint     │    │ • Generated Cards   │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
```

### Components

1. **Python Agent System** (`agent-webmaster-py/`)
   - **Card Generator Agent**: Creates creative business card data in JSON format
   - **Web Generator Agent**: Orchestrates the entire workflow from data generation to web publishing
   - **OpenAPI Configurator**: Dynamically configures Azure Function endpoints

2. **Azure Function** (`AgenticWebGen.DotNetTools/`)
   - **Template Filler Function**: Processes JSON data and fills HTML templates
   - Built with .NET 8 and Azure Functions v4
   - Integrates with Azure Blob Storage for template and output management

3. **API Testing** (`requests/`)
   - Bruno collection for testing the Azure Function endpoints
   - Localhost and Azure environment configurations

## 🚀 Features

- **AI-Powered Content Generation**: Generates diverse, creative business card data using Azure AI
- **Dynamic Template Processing**: Fills HTML templates with JSON data using placeholder replacement
- **Web Publishing**: Automatically publishes generated cards to publicly accessible URLs
- **Multi-Environment Support**: Works with both local development and Azure cloud environments
- **RESTful API**: HTTP-based interface for easy integration
- **Scalable Architecture**: Built on Azure Functions for automatic scaling

## 📋 Prerequisites

- **Azure Account** with the following services:
  - Azure AI Studio/Foundry with deployed language model (GPT-3.5-turbo)
  - Azure Functions App
  - Azure Storage Account with blob containers
- **Development Environment**:
  - Python 3.8+ (for agent system)
  - .NET 8 SDK (for Azure Functions)
  - Azure Functions Core Tools
  - Visual Studio Code (recommended)

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd agentic-webgen
```

### 2. Python Agent Setup
```bash
cd agent-webmaster-py
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the `agent-webmaster-py` directory:
```env
PROJECT_ENDPOINT=https://your-ai-studio-endpoint.services.ai.azure.com/api/projects/your-project
MODEL_DEPLOYMENT_NAME=gpt-35-turbo
AZURE_FUNCTION_URL=https://your-function-app.azurewebsites.net/api/FxTemplateFiller?code=your-function-key
```

### 4. Azure Function Setup
```bash
cd AgenticWebGen.DotNetTools/AgenticWebGen.DotNetTools.Fx
# Update local.settings.json with your Azure credentials
dotnet restore
dotnet build
```

### 5. Azure Storage Setup
- Create a storage account
- Create a container named `templates`
- Upload an HTML template file named `template1.html` with placeholders like `{{title}}`, `{{name}}`, etc.

## 🎯 Usage

### Running the Python Agents

#### Test the Card Generator
```bash
cd agent-webmaster-py/agents/ag_card_generator
python ag_card_generator_tester.py
```

#### Test the Web Generator (Full Workflow)
```bash
cd agent-webmaster-py/agents/ag_web_gen
python ag_web_gen_tester.py
```

### Running the Azure Function Locally
```bash
cd AgenticWebGen.DotNetTools/AgenticWebGen.DotNetTools.Fx
func start
```

### API Testing with Bruno
1. Open the `requests/` folder in Bruno
2. Configure the environment variables
3. Test both localhost and Azure endpoints

## 📊 API Reference

### POST /api/FxTemplateFiller

Fills an HTML template with JSON data and publishes it to the web.

**Request Body:**
```json
{
  "title": "Professional Card",
  "name": "Alice Smith",
  "city": "New York",
  "profession": "Software Engineer", 
  "message": "Thank you for visiting this demo!",
  "date": "2024-06-07"
}
```

**Response:**
```json
{
  "url": "https://storage-account.blob.core.windows.net/templates/filled_template_20241207123456.html"
}
```

## 🏛️ Project Structure

```
agentic-webgen/
├── agent-webmaster-py/           # Python AI Agents
│   ├── agents/
│   │   ├── ag_card_generator/     # Data generation agent
│   │   └── ag_web_gen/           # Orchestration agent
│   │       └── tools/            # OpenAPI integration tools
│   ├── samples/                  # Example configurations
│   └── requirements.txt          # Python dependencies
├── AgenticWebGen.DotNetTools/     # Azure Functions
│   └── AgenticWebGen.DotNetTools.Fx/
│       ├── FxTemplateFiller.cs   # Main function logic
│       ├── Program.cs            # Function app configuration
│       └── Properties/           # Azure deployment configurations
├── requests/                     # API testing
│   ├── bruno.json               # Bruno collection
│   └── *.bru                    # Test requests
└── .vscode/                     # VS Code configuration
```

## 🔧 Configuration

### Key Configuration Files

- **`local.settings.json`**: Azure Function local development settings
- **`html_template_filler_openapi_spec.json`**: OpenAPI specification for the Azure Function
- **`final_openapi_spec.json`**: Complete API specification example
- **Bruno environment files**: API testing configurations

### Environment Variables

**Azure Function:**
- `AZURE_STORAGE_CONNECTION_STRING`: Connection string for blob storage
- `AzureWebJobsStorage`: Function app storage connection

**Python Agents:**
- `PROJECT_ENDPOINT`: Azure AI Studio project endpoint
- `MODEL_DEPLOYMENT_NAME`: Name of the deployed language model
- `AZURE_FUNCTION_URL`: Complete Azure Function URL with access key

## 🚀 Deployment

### Azure Function Deployment
1. Publish using Visual Studio Code Azure Functions extension
2. Or use Azure CLI:
```bash
func azure functionapp publish YourFunctionAppName
```

### Python Agents Deployment
- Agents can be deployed to any Python-compatible hosting platform
- Ensure environment variables are properly configured
- Consider using Azure Container Instances or App Service for hosting

## 🧪 Testing

### Unit Tests
```bash
# Test card generator
python agent-webmaster-py/agents/ag_card_generator/ag_card_generator_tester.py

# Test web generator  
python agent-webmaster-py/agents/ag_web_gen/ag_web_gen_tester.py
```

### API Tests
Use the Bruno collection in the `requests/` folder to test:
- Local development endpoints
- Azure production endpoints
- Different payload variations

## 🔍 Troubleshooting

### Common Issues

1. **Authentication Errors**: Verify Azure credentials and function keys
2. **Template Not Found**: Ensure template1.html exists in the storage container
3. **JSON Parsing Errors**: Validate JSON payload structure
4. **Storage Connection Issues**: Check storage connection strings

### Debug Logging
- Azure Function logs available in Azure Portal
- Python agent logs output to console
- Use Application Insights for production monitoring

## 📈 Performance & Scaling

- **Azure Functions**: Automatically scales based on demand
- **Storage**: Optimized for high-throughput operations
- **AI Agents**: Stateless design allows for horizontal scaling
- **Caching**: Consider implementing template caching for high-volume scenarios

## 🔒 Security Considerations

- Function keys protect Azure Function endpoints
- Azure AD authentication for AI Studio access
- Storage access keys secured in configuration
- Input validation prevents template injection attacks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review Azure Function and Python agent logs
3. Create an issue in the repository
4. Refer to Azure documentation for service-specific issues

---

**Built with ❤️ using Azure AI, Azure Functions, and Python**
