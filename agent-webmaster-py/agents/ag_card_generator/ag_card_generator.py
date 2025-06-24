import os
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Global variables to store instances
_card_generator_agent = None
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

def _create_card_generator_agent():
    """Create or retrieve the card generator agent."""
    global _card_generator_agent
    
    if _card_generator_agent is not None:
        return _card_generator_agent
    
    client = _get_agents_client()
    agent_name = "ag-card-generator"
    
    # Check if agent already exists
    agents = list(client.list_agents())
    for agent in agents:
        if agent.name == agent_name:
            _card_generator_agent = agent
            return _card_generator_agent
    
    # Create new agent if it doesn't exist
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
    
    _card_generator_agent = client.create_agent(
        model=os.environ.get("MODEL_DEPLOYMENT_NAME"),
        name=agent_name,
        description="Generates creative business card data in JSON format",
        instructions=instructions
    )
    
    return _card_generator_agent

# Make instance and client accessible
class AgentModule:
    @property
    def instance(self):
        return _create_card_generator_agent()
    
    @property
    def client(self):
        return _get_agents_client()

# Create module instance
import sys
sys.modules[__name__] = AgentModule()
