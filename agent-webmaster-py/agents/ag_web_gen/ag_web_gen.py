import os
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import ConnectedAgentTool

from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ag_card_generator'))
import ag_card_generator

# Global variables to store instances
_web_gen_agent = None
_agents_client = None

def _get_agents_client():
    """Get the Azure AI Agents client."""
    global _agents_client
    if _agents_client is None:
        load_dotenv()
        _agents_client = AgentsClient(
            endpoint=os.environ.get("PROJECT_ENDPOINT"),
            credential=DefaultAzureCredential()
        )
    return _agents_client

def _create_web_gen_agent():
    """Create or retrieve the web generator agent with connected card generator tool."""
    global _web_gen_agent
    
    if _web_gen_agent is not None:
        return _web_gen_agent
    
    client = _get_agents_client()
    agent_name = "ag-web-gen"
    
    # Check if agent already exists
    agents = list(client.list_agents())
    for agent in agents:
        if agent.name == agent_name:
            _web_gen_agent = agent
            return _web_gen_agent
    
    # Get the card generator agent instance
    card_generator_agent = ag_card_generator.instance
      # Create ConnectedAgentTool for the card generator
    card_generator_tool = ConnectedAgentTool(
        id=card_generator_agent.id,
        name="card_generator",
        description="Generates creative business card data in JSON format with title, name, city, profession, message, and date fields according to the instructions given"
    )
      # Create new agent if it doesn't exist
    instructions = """You are an agent that receives requests for publishing personal cards. These cards contain title, name, city, profession, and message. For this publishing, it is required that an html template be filled with the person's information in json format."""
      
      
      # Create agent with the connected tool
    _web_gen_agent = client.create_agent(
        model=os.environ.get("MODEL_DEPLOYMENT_NAME"),
        name=agent_name,
        description="Generates JSON data for publishing personal cards to HTML templates",
        instructions=instructions,
        tools=card_generator_tool.definitions
    )
    
    return _web_gen_agent

# Make instance and client accessible
class AgentModule:
    @property
    def instance(self):
        return _create_web_gen_agent()
    
    @property
    def client(self):
        return _get_agents_client()

# Create module instance
import sys
sys.modules[__name__] = AgentModule()