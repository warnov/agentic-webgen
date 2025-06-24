# test_integration.py
"""
Test script to demonstrate the integrated card generation and publishing system.
Shows both random AI-generated data and specific user-provided data.
"""

import os
import json
import re
import sys
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FunctionTool, ToolSet, OpenApiTool, OpenApiAnonymousAuthDetails, ConnectedAgentTool
from dotenv import load_dotenv

# Add paths for direct imports
sys.path.append(os.path.join(os.path.dirname(__file__), "utils"))
sys.path.append(os.path.join(os.path.dirname(__file__), "agents", "ag_data_generator"))

from openapi_loader import load_openapi_spec
from ag_data_generator import _create_data_generator_agent

load_dotenv()

# 📋 Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

# 🔧 Environment setup
PROJECT_ENDPOINT = os.environ.get("PROJECT_ENDPOINT")
MODEL_DEPLOYMENT_NAME = os.environ.get("MODEL_DEPLOYMENT_NAME")
AZURE_FUNCTION_URL = os.environ.get("AZURE_FUNCTION_URL")

if not PROJECT_ENDPOINT or not MODEL_DEPLOYMENT_NAME:
    raise EnvironmentError("Please set PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME as environment variables.")

if not AZURE_FUNCTION_URL:
    raise EnvironmentError("Please set AZURE_FUNCTION_URL as environment variable for the Azure Function endpoint.")

# 🧠 Initialize the agents client directly
agents_client = AgentsClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

# 🛠️ Register the Azure Function as an AI Foundry web tool
openapi_spec = load_openapi_spec(config["tool"]["openapi_spec_file"], AZURE_FUNCTION_URL)

azure_function_tool = OpenApiTool(
    name=config["tool"]["name"],
    description=config["tool"]["description"],
    spec=openapi_spec,
    auth=OpenApiAnonymousAuthDetails()
)

# 🧠 Get the data generator agent and create a ConnectedAgentTool
data_generator_agent = _create_data_generator_agent()
data_generator_tool = ConnectedAgentTool(
    id=data_generator_agent.id,
    name="generate_random_card_data",
    description="Generates creative, random professional card data using AI. Returns JSON with title, name, city, profession, and message fields. Use this when the user asks for random data or doesn't provide specific details."
)

toolset = ToolSet()
toolset.add(azure_function_tool)
toolset.add(data_generator_tool)

# 🤖 Create the agent
agent = agents_client.create_agent(
    model=MODEL_DEPLOYMENT_NAME,
    name=config["agent"]["name"],
    instructions=config["agent"]["instructions"],
    toolset=toolset,
)

def test_card_generation(user_input, test_name):
    """Test card generation and return the result URL."""
    print(f"\n🧪 {test_name}")
    print(f"📝 Input: {user_input}")
    
    # 🎯 Create conversation and run
    thread = agents_client.threads.create()

    agents_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    # Start the agent run
    run = agents_client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id
    )

    # Check results
    if run.status == "completed":
        messages = agents_client.messages.list(thread_id=thread.id)
        messages_list = list(messages)
        for msg in reversed(messages_list):
            if msg.role == "assistant":
                url_match = re.search(r'https://[^\s)]+', str(msg.content))
                if url_match:
                    url = url_match.group()
                    print(f"✅ Generated URL: {url}")
                    return url
        print("❌ No URL was generated")
        return None
    else:
        print(f"❌ Agent run failed with status: {run.status}")
        return None

if __name__ == "__main__":
    print("🚀 Testing Integrated Card Generation and Publishing System")
    print("=" * 60)
    
    # Test 1: Random AI-generated data
    test_card_generation(
        "Generate a random professional card and publish it",
        "Test 1: Random AI-Generated Card Data"
    )
    
    # Test 2: Specific user data
    test_card_generation(
        "Publica una tarjeta personal para Walter Novoa, que vive en New York y trabaja como Solutions Architect. El título debe ser 'Tarjeta Profesional' y el mensaje debe ser 'Especialista en arquitecturas de soluciones en la nube con más de 10 años de experiencia.'",
        "Test 2: Specific User-Provided Data"
    )
    
    # Test 3: Another random generation
    test_card_generation(
        "Create a random business card",
        "Test 3: Another Random Generation"
    )
    
    # Test 4: Mixed input - partial data requesting random fill
    test_card_generation(
        "Create a card for someone from Tokyo who works in technology, but make up the rest of the details",
        "Test 4: Partial Data with Random Fill"
    )
    
    print("\n🎉 Integration testing completed!")
    print(f"📊 Agent used: {agent.name} (ID: {agent.id})")
    print(f"🔗 Connected to data generator: {data_generator_agent.name} (ID: {data_generator_agent.id})")
