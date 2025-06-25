



# Imports
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import ConnectedAgentTool, OpenApiTool, OpenApiAnonymousAuthDetails
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from tools.openapi_azurefx_configurator import parse_azure_function_url_and_modify_spec
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ag_card_generator'))
import ag_card_generator


# Global variables to store instances
_web_gen_agent = None
_agents_client = None




# Agents client (Create or retrieve)
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


# ag-web-gen (Create or retrieve - main agent)
def _create_web_gen_agent():
    """Create or retrieve the web generator agent with connected card generator tool."""
    global _web_gen_agent
    
    # Check if in memory agent instance already exists (Singleton pattern)
    # If it exists, return the existing instance
    if _web_gen_agent is not None:
        return _web_gen_agent
    


    # Create agents client
    # This will create a new client if it doesn't exist
    client = _get_agents_client()
    agent_name = "ag-web-gen"
    


    # Check if agent already exists in AI Foundry
    # List all agents and check if the agent with the given name already exists
    # If it exists, return the existing agent instance
    # If it doesn't exist, create a new agent instance
    agents = list(client.list_agents())
    for agent in agents:
        if agent.name == agent_name:
            _web_gen_agent = agent
            return _web_gen_agent
    

    # If agent doesn't exist, create a new one


    #TOOLS
    #====================================


    # Tool 1: ConnectedAgentTool for the card generator
    # Get the card generator agent instance
    card_generator_agent = ag_card_generator.instance
    # Create a ConnectedAgentTool for the card generator
    card_generator_tool = ConnectedAgentTool(
        id=card_generator_agent.id,
        name="card_generator",
        description="Generates creative business card data in JSON format with title, name, city, profession, message, and date fields according to the instructions given"
    )




    # Tool 2: OpenApiTool for the HTML template filler Azure Function
    # Get configured OpenAPI spec using our configurator
    openapi_spec_path = os.path.join(os.path.dirname(__file__), "tools", "html_template_filler_openapi_spec.json")
    openapi_spec = parse_azure_function_url_and_modify_spec(openapi_spec_path)    
    # Register the Azure Function as an OpenAPI tool
    azure_function_tool = OpenApiTool(
        name="html_template_filler",
        description="Fills HTML template with JSON card data and publishes it to the web, returning the final URL",
        spec=openapi_spec,
        auth=OpenApiAnonymousAuthDetails()
    )


    
    # Create new agent if it doesn't exist
    instructions = """You are an agent that receives requests for publishing personal cards. These cards contain title, name, city, profession, message and date. For this publishing, it is required that an html template be filled with the person's information in json format. After this, the resulting html is published in a given URL. That URL will be the only response you give to your users."""    
    # Combine all tools
    all_tools = card_generator_tool.definitions + azure_function_tool.definitions    
    # Create the web generator agent with the connected tools
    _web_gen_agent = client.create_agent(
        model=os.environ.get("MODEL_DEPLOYMENT_NAME"),
        name=agent_name,
        description="Generates JSON data for personal cards and publishes them to the web using HTML templates",
        instructions=instructions,
        tools=all_tools
    )
    
    return _web_gen_agent


# Make instance and client accessible (To use the agent)
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