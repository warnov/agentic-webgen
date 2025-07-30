# 🧠 Agentic Web Generator on Azure AI Foundry

This repository provides a hands-on implementation of a multi-agent system built with **Azure AI Foundry**, demonstrating how intelligent agents can be orchestrated to generate and publish personalized business cards as web pages, starting from natural language input.

---

## Table of Contents

- [🧠 Agentic Web Generator on Azure AI Foundry](#-agentic-web-generator-on-azure-ai-foundry)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [What You'll Learn](#what-youll-learn)
  - [Architecture](#architecture)
    - [Execution Flow](#execution-flow)
    - [Visual Highlights in the Diagram](#visual-highlights-in-the-diagram)
  - [Installation \& Requirements](#installation--requirements)
    - [Prerequisites](#prerequisites)
    - [Recommended VSCode Extensions](#recommended-vscode-extensions)
    - [Quick Windows Setup](#quick-windows-setup)
  - [Solution Setup](#solution-setup)
    - [Required Components](#required-components)
    - [Configure Deployed Services](#configure-deployed-services)
      - [Azure Storage](#azure-storage)
      - [Azure Function](#azure-function)
---

## Project Overview

This application demonstrates a **multi-agent architecture** where the user interacts through a Python console app to request the creation of a business card for a given person. The user can provide full or partial data (name, profession, location, etc.), and the agents will intelligently complete the rest and generate a realistic business card.

The final output is a **web-based HTML card** hosted on Azure Blob Storage.

## What You'll Learn

- How to structure multi-agent solutions in Azure AI Foundry.
- How to connect agents through tools and chain them.
- How to invoke external services like Azure Functions and Blob Storage.
- How to separate model intelligence from system orchestration logic.

---

## Architecture

![Architecture](misc/agentic_webgen_arch.png)

The diagram above illustrates the complete solution architecture based on **Azure AI Foundry**, which enables generating and publishing personal business cards starting from natural language input, using a **multi-agent approach**. Each component is designed to show how agents, tools, and Azure services interact to produce the final result.

---

### Execution Flow

1. **Python Console App (Desktop Client)**  
   - The flow begins when a user enters a natural language message via a Python console application.  
   - This message can include complete or partial data about a person to build their business card.

2. **Orchestrator Agent in Azure AI Foundry**  
   - The message is sent to the **Orchestrator Agent**, which analyzes the user's intent.
   - This agent has multiple tools (**highlighted in green**), including:
     - A tool to invoke another agent (Agent-to-Agent Tool).
     - A tool to invoke an Azure Function (Azure Function Tool).

3. **Agent-to-Agent Tool → JSON Card Generator Agent**  
   - The Orchestrator uses its **agent tool** to delegate the task of understanding the message to a second agent: the **JSON Card Generator Agent**.
   - This agent uses a **GPT-3.5 model** (**connections shown in orange**) to extract structured information and convert it into a JSON object containing the business card fields (name, title, city, etc.).

4. **Azure Function: HTML Template Filler**  
   - Once the JSON is received, the Orchestrator decides to use the **Azure Function Tool**.
   - It invokes a function deployed as an **Azure App Service using Flex Consumption**, which receives the JSON as input.

5. **Azure Storage – Templates Container**  
   - The Azure Function downloads an HTML template (`Business Card Template.html`) from the Templates container in Azure Blob Storage.

6. **Template Replacement and Publication**  
   - Using the received information, the Azure Function dynamically fills the HTML template.
   - Then it saves a new version (`Card1.html`, `Card2.html`, etc.) in the Cards container with **public access** enabled.

7. **Response to the User**  
   - The Azure Function returns the public URL of the generated HTML file.
   - The Orchestrator receives this URL and returns it to the original client (the Python Console App), allowing the user to open their personalized card as a web page.

---

### Visual Highlights in the Diagram

- **Tools used by the Orchestrator Agent** are clearly shown in **green**, representing its orchestration capabilities and ability to delegate tasks.
- **Calls to GPT-3.5 models** are shown in **orange**, emphasizing that reasoning is powered by a language model.
- **Azure Function and Storage** are integrated as external components, accessible from agents via tools.
- **Separation of storage containers** (one for templates, one for generated cards) reflects a clean, scalable architecture.

This setup showcases a modular, extensible AI solution using LLM-based agents, multi-step orchestration, and cloud-native publishing.

---

## Installation & Requirements
🛠️ 

This solution works on **Windows, macOS, and Linux**. A script is provided for quick setup on Windows.

### Prerequisites

Install:

- [Git](https://git-scm.com/downloads)
- [Python 3.12+](https://www.python.org/downloads/)
- [.NET SDK 8+](https://dotnet.microsoft.com/download)
- [Visual Studio Code](https://code.visualstudio.com/)

### Recommended VSCode Extensions
🔌 

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Azure Functions](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
- [C#](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csharp)
- [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)

```bash
code --install-extension ms-python.python
code --install-extension ms-azuretools.vscode-azurefunctions
code --install-extension ms-dotnettools.csharp
code --install-extension humao.rest-client
```

### Quick Windows Setup

Run this PowerShell script:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; ./misc/setup-dev-win.ps1
```

---
## Solution Setup

This solution requires the deployment of a resource group that will contain all the core infrastructure components. Each element is configured to support the application's runtime, storage, and AI capabilities.

---

### Required Components

We have included the [infra](./infra) folder from where you can deploy all the necessary Azure infrastructure components for this solution. Please check its [readme](./infra/README.md).

The infrastructure includes:

- **A Resource Group**  
  A logical container to host all resources related to the solution. All deployments will target this group to ensure scoped management, billing, and lifecycle control.

- **Storage Account**  
  A central storage layer that supports both internal operations and public content exposure. The configuration includes:
  - **SKU**: `Standard_LRS`
  - **Kind**: `StorageV2`
  - **Access Tier**: `Hot`
  - **HTTPS Traffic Only**: Enabled
  
  Two blob containers will be created:
  - `templates`: private access; used to store internal templates.
  - `cards`: public (blob-level) access; intended for publish the generated card assets.

- **Azure Function App**  
  The compute component of the solution, responsible for executing backend logic. It is deployed with the following configuration:
  - **Plan**: Elastic Premium (EP1) on Linux (`elastic` kind with `ElasticPremium` tier)
  - **Runtime**: .NET 8 Isolated Worker (`DOTNET-ISOLATED|8.0`)  
  - **HTTPS Only**: Enabled
  - **App Settings**:
    (Besides the default ones)
    - `AZURE_STORAGE_CONNECTION_STRING`: Storage connection for custom operations set to the connection string of the created storage account

- **Azure AI Foundry (Cognitive Services)**  
  The AI orchestration platform that enables multi-agent workflows. It is deployed as a Cognitive Services resource with the following configuration:
  - **Resource Type**: `Microsoft.CognitiveServices/accounts`
  - **Kind**: `AIServices` (multi-service AI resource, **NOT** Azure Machine Learning AI Foundry Hub a it doesn't have Agents in GA yet)
  - **SKU**: `S0` (Standard pricing tier)
  - **Identity**: System-assigned managed identity enabled
  - **Network Access**: Public network access enabled with custom subdomain
  

> ⚠️ All resources should be deployed in the same Azure region to ensure compatibility, performance, and cost efficiency.

---

### Configure Deployed Services
At this point it is supposed that either using the provided ARM template or manually, you have deployed the necessary Azure resources. Now, you should have the [required components](#required-components) ready. With these components in place, you can proceed to configure the services as follows:

#### Azure Storage
Two storage containers were deployed:
- **`templates`**: Contains the HTML template for business cards, which is private and not publicly accessible. A sample template file called [`business_card_template.html`](./misc/business_card_template.html) is provided in the `misc` folder. You can upload it to the `templates` container using Azure Storage Explorer, the Azure Portal or this command (for this you need to have the Azure CLI installed, configured and authenticated):
 
```bash
az storage blob upload --account-name stagenticwebgenw --container-name templates --file ./misc/business_card_template.html --name business_card_template.html
```
That is the template that will be used by the Azure Function to generate the business cards.

- **`cards`**: Publicly accessible container where generated business cards will be stored by the Azure Function. The cards will be accessible via public URLs. No required action at this point.

#### Azure Function
The Azure Function App is already configured to use the storage account created in the infrastructure deployment. You can verify this in the Azure Portal under the Function App's **Configuration** settings.
We just need to upload the code for the Azure Function that will generate the business cards. You can do this by using any of the methods described [here](https://learn.microsoft.com/en-us/azure/azure-functions/functions-deployment-technologies?tabs=windows#deployment-methods). 
For example, opening the [function project](AgenticWebGen.DotNetTools/AgenticWebGen.DotNetTools.Fx) in Visual Studio Code and running the following command in the terminal:

```bash
func azure functionapp publish <YourFunctionAppName>
```