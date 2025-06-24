import os
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

def delete_agents_by_name(agent_name):
    """Delete all agents with the specified name."""
    load_dotenv()
    
    # Get client
    client = AgentsClient(
        endpoint=os.environ.get("PROJECT_ENDPOINT"),
        credential=DefaultAzureCredential()
    )
    
    # Get all agents
    agents = list(client.list_agents())
    
    # Find and delete agents with matching name
    deleted_count = 0
    for agent in agents:
        if agent.name == agent_name:
            client.delete_agent(agent.id)
            deleted_count += 1
    
    return deleted_count

if __name__ == "__main__":
    agent_name = input("Enter the name of the agents to delete: ")
    count = delete_agents_by_name(agent_name)
    print(f"Deleted {count} agent(s) with name '{agent_name}'")