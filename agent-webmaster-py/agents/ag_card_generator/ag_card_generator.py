"""
============================================
Agentic Web Generator: Card Generator Agent
============================================

This script demonstrates how to use Azure AI Foundry to create and manage an AI agent that generates creative business card data in JSON format. It is designed for absolute beginners and explains every step in detail.

What is Azure AI Foundry?
------------------------
Azure AI Foundry is a cloud platform from Microsoft that allows you to build, deploy, and manage intelligent agents powered by large language models (LLMs) like GPT. Agents are reusable AI components that can perform tasks, answer questions, or generate data.

What is an Agent?
-----------------
An agent is a program or service that uses AI to perform a specific task. In this script, the agent generates business card data (name, profession, city, etc.) in JSON format.

How does this script work?
--------------------------
- It connects to Azure AI Foundry using your credentials and project endpoint.
- It checks if a business card generator agent already exists; if not, it creates one.
- The agent is configured to always return a JSON object with business card details.
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

import os
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Global variables to store instances of the agent and client
_card_generator_agent = None
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


def _create_card_generator_agent():
    """
    Create or retrieve the card generator agent in Azure AI Foundry.
    This agent generates creative business card data in JSON format.
    - Checks if the agent already exists (by name).
    - If not, creates a new agent with specific instructions.
    Returns:
        Agent: The card generator agent instance.
    """
    global _card_generator_agent
    if _card_generator_agent is not None:
        return _card_generator_agent

    client = _get_agents_client()
    agent_name = "ag-card-generator"

    # Check if agent already exists in the Foundry project
    agents = list(client.list_agents())
    for agent in agents:
        if agent.name == agent_name:
            _card_generator_agent = agent
            return _card_generator_agent

    # Instructions for the agent: always return a JSON object with card details
    instructions = """You are a creative data generator for professional business cards. 
When asked to generate card data, return ONLY a valid JSON object with exactly these 6 fields:
- title: A professional card title (e.g., "Business Card", "Professional Profile", etc.)
- name: A realistic full name (diverse, international names)
- city: A real city name (from any country)
- profession: A realistic job title/profession
- message: A professional message/bio (1-2 sentences)
- date: Today's date in YYYY-MM-DD format

Be creative and diverse. Use different cultures, languages, and professions. 
Return ONLY the JSON object, no additional text or explanations.

Example format:
{
  "title": "Professional Card",
  "name": "Sarah Chen",
  "city": "Singapore", 
  "profession": "AI Research Scientist",
  "message": "Passionate about developing ethical AI solutions that transform healthcare.",
  "date": "2024-01-15"
}"""

    # Create the agent in Azure AI Foundry
    _card_generator_agent = client.create_agent(
        model=os.environ.get("MODEL_DEPLOYMENT_NAME"),
        name=agent_name,
        description="Generates creative business card data in JSON format",
        instructions=instructions
    )
    return _card_generator_agent


class AgentModule:
    """
    Helper class to access the card generator agent and the Azure AI Foundry client.
    Usage:
        from ag_card_generator import instance, client
        agent = instance  # Get the card generator agent
        client = client   # Get the Azure AI Foundry client
    """
    @property
    def instance(self):
        """
        Returns the card generator agent instance.
        """
        return _create_card_generator_agent()

    @property
    def client(self):
        """
        Returns the Azure AI Foundry Agents client.
        """
        return _get_agents_client()

# Make the module's instance and client accessible when imported
import sys
sys.modules[__name__] = AgentModule()
