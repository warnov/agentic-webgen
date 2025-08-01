"""
============================================
Agentic Web Generator: Web Generation Agent
============================================

This script demonstrates how to use Azure AI Foundry to create and manage an AI agent that orchestrates the generation and publishing of personal business cards as web pages. It is designed for absolute beginners and explains every step in detail.

What is Azure AI Foundry?
------------------------
Azure AI Foundry is a Microsoft cloud platform for building, deploying, and managing intelligent agents powered by large language models (LLMs) like GPT. Agents are reusable AI components that can perform tasks, answer questions, or generate data.

What is an Agent?
-----------------
An agent is a program or service that uses AI to perform a specific task. In this script, the main agent coordinates the creation of business card data and its publication as a web page.

What is a Tool?
---------------
A tool is an external capability that an agent can use, such as another agent or an API. Here, the web generation agent uses two tools:
1. A connected agent tool (the card generator agent)
2. An OpenAPI tool (an Azure Function that fills and publishes HTML templates)

How does this script work?
--------------------------
- Connects to Azure AI Foundry using your credentials and project endpoint.
- Checks if the web generation agent already exists; if not, creates one.
- The agent is configured with two tools: a card generator agent and an Azure Function.
- The agent receives requests, generates card data, fills an HTML template, and publishes the result as a web page.
- You can access the agent and the client from other scripts using the `AgentModule` class.

How to use this script?
-----------------------
1. Set your Azure AI Foundry project endpoint and model name in a `.env` file:
   PROJECT_ENDPOINT=https://<your-foundry>.services.ai.azure.com/api/projects/<your-project>
   MODEL_DEPLOYMENT_NAME=gpt-35-turbo
2. Make sure you have Azure credentials set up (e.g., via `az login`).
3. Import this module in your Python code and use `instance` to get the agent, or `client` to interact with Azure AI Foundry.

Dependencies:
-------------
- azure-ai-agents
- azure-identity
- python-dotenv

"""

# Imports
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import ConnectedAgentTool, OpenApiTool, OpenApiAnonymousAuthDetails
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from tools.openapi_azurefx_configurator import parse_azure_function_url_and_modify_spec
import os
import sys
# Add the card generator agent module to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ag_card_generator'))
import ag_card_generator

# Global variables to store instances of the agent and client
_web_gen_agent = None
_agents_client = None


def _get_agents_client():
    """
    Get the Azure AI Agents client for communicating with Azure AI Foundry.
    Loads environment variables from .env and authenticates using your Azure account.
    Returns:
        AgentsClient: The client for managing agents in your Foundry project.
    """
    global _agents_client
    if _agents_client is None:
        load_dotenv()  # Load environment variables from .env file
        _agents_client = AgentsClient(
            endpoint=os.environ.get("PROJECT_ENDPOINT"),
            credential=DefaultAzureCredential()
        )
    return _agents_client


def _create_web_gen_agent():
    """
    Create or retrieve the web generation agent in Azure AI Foundry.
    This agent orchestrates the creation and publishing of business cards as web pages.
    - Checks if the agent already exists (by name).
    - If not, creates a new agent with two tools:
        1. ConnectedAgentTool: Uses the card generator agent to generate card data.
        2. OpenApiTool: Uses an Azure Function to fill and publish HTML templates.
    Returns:
        Agent: The web generation agent instance.
    """
    global _web_gen_agent
    # Singleton pattern: return existing instance if available
    if _web_gen_agent is not None:
        return _web_gen_agent

    client = _get_agents_client()
    agent_name = "ag-web-gen"

    # Check if agent already exists in the Foundry project
    agents = list(client.list_agents())
    for agent in agents:
        if agent.name == agent_name:
            _web_gen_agent = agent
            return _web_gen_agent

    # Tool 1: ConnectedAgentTool for the card generator agent
    card_generator_agent = ag_card_generator.instance
    card_generator_tool = ConnectedAgentTool(
        id=card_generator_agent.id,
        name="card_generator",
        description="Generates creative business card data in JSON format with title, name, city, profession, message, and date fields according to the instructions given"
    )

    # Tool 2: OpenApiTool for the HTML template filler Azure Function
    openapi_spec_path = os.path.join(os.path.dirname(__file__), "tools", "html_template_filler_openapi_spec.json")
    openapi_spec = parse_azure_function_url_and_modify_spec(openapi_spec_path)
    azure_function_tool = OpenApiTool(
        name="html_template_filler",
        description="Fills HTML template with JSON card data and publishes it to the web, returning the final URL",
        spec=openapi_spec,
        auth=OpenApiAnonymousAuthDetails()
    )

    # Instructions for the agent: orchestrate card generation and publishing
    instructions = """You are an agent that receives requests for publishing personal cards. These cards contain title, name, city, profession, message and date. For this publishing, it is required that an html template be filled with the person's information in json format. After this, the resulting html is published in a given URL. That URL will be the only response you give to your users."""
    # Combine all tools
    all_tools = card_generator_tool.definitions + azure_function_tool.definitions
    # Create the web generation agent with the connected tools
    _web_gen_agent = client.create_agent(
        model=os.environ.get("MODEL_DEPLOYMENT_NAME"),
        name=agent_name,
        description="Generates JSON data for personal cards and publishes them to the web using HTML templates",
        instructions=instructions,
        tools=all_tools
    )
    return _web_gen_agent


class AgentModule:
    """
    Helper class to access the web generation agent and the Azure AI Foundry client.
    Usage:
        from ag_web_gen import instance, client
        agent = instance  # Get the web generation agent
        client = client   # Get the Azure AI Foundry client
    """
    @property
    def instance(self):
        """
        Returns the web generation agent instance.
        """
        return _create_web_gen_agent()

    @property
    def client(self):
        """
        Returns the Azure AI Foundry Agents client.
        """
        return _get_agents_client()

# Make the module's instance and client accessible when imported
import sys
sys.modules[__name__] = AgentModule()