# ag_data_generator.py

import os
import json
import re
from typing import Annotated, Optional
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Global variables to store the agent instance
_data_generator_agent = None
_agents_client = None

def _get_agents_client():
    """Get or create the agents client instance."""
    global _agents_client
    if _agents_client is None:
        load_dotenv()
        project_endpoint = os.environ.get("PROJECT_ENDPOINT")
        if not project_endpoint:
            raise EnvironmentError("Please set PROJECT_ENDPOINT as environment variable.")
        
        _agents_client = AgentsClient(
            endpoint=project_endpoint,
            credential=DefaultAzureCredential(),
        )
    return _agents_client

def _create_data_generator_agent():
    """Create or retrieve the data generator agent (only created once in Foundry)."""
    global _data_generator_agent
    
    if _data_generator_agent is not None:
        return _data_generator_agent
    
    model_deployment = os.environ.get("MODEL_DEPLOYMENT_NAME")
    if not model_deployment:
        raise EnvironmentError("Please set MODEL_DEPLOYMENT_NAME as environment variable.")
    
    agents_client = _get_agents_client()
    agent_name = "card-data-generator"
      # Check if agent already exists in Foundry
    try:
        # Try different methods to list agents
        try:
            existing_agents = agents_client.list_agents()
        except AttributeError:
            try:
                existing_agents = list(agents_client.list_agents())
            except AttributeError:
                # If listing doesn't work, skip the check and create
                print("⚠️  Cannot list existing agents, will create new one")
                existing_agents = []
        
        for agent in existing_agents:
            if hasattr(agent, 'name') and agent.name == agent_name:
                print(f"♻️  Found existing data generator agent with ID: {agent.id}")
                _data_generator_agent = agent
                return _data_generator_agent
    except Exception as e:
        print(f"Warning: Could not check for existing agents: {e}")
        print("Will create a new agent...")
      # Agent doesn't exist, create it
    try:
        _data_generator_agent = agents_client.create_agent(
            model=model_deployment,
            name=agent_name,
            instructions="""You are a creative data generator for professional business cards. 
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
        )
        
        print(f"✅ New data generator agent created with ID: {_data_generator_agent.id}")
        return _data_generator_agent
        
    except Exception as e:
        raise RuntimeError(f"Failed to create data generator agent: {str(e)}")

def generate_random_card_data() -> Annotated[str, "JSON string with AI-generated random card data"]:
    """
    Generates random professional card data using AI.
    
    Returns:
        JSON string containing AI-generated card data with title, name, city, profession, and message.
    """
    try:
        # Get or create the data generator agent (only created once)
        agent = _create_data_generator_agent()
        agents_client = _get_agents_client()
        
        # Create a conversation with the data generator agent
        thread = agents_client.threads.create()
        
        agents_client.messages.create(
            thread_id=thread.id,
            role="user",
            content="Generate random professional card data in JSON format"
        )
          # Run the agent
        run = agents_client.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id
        )
        
        if run.status == "completed":
            # Get the response
            messages = agents_client.messages.list(thread_id=thread.id)
            messages_list = list(messages)
            
            for msg in reversed(messages_list):
                if msg.role == "assistant":
                    # Extract content from the response
                    if hasattr(msg, 'content') and msg.content:
                        # Handle both text content and content arrays
                        if isinstance(msg.content, list) and len(msg.content) > 0:
                            content = str(msg.content[0].text.value if hasattr(msg.content[0], 'text') else msg.content[0])
                        else:
                            content = str(msg.content)
                    else:
                        continue
                    
                    # Clean up the content and try to find JSON
                    content = content.strip()
                    print(f"🔍 Raw agent response: {content[:200]}...")  # Debug info
                    
                    # Try to find JSON in the response (more robust)
                    json_patterns = [
                        r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Simple nested JSON
                        r'\{.*?\}',  # Basic JSON pattern
                    ]
                    
                    for pattern in json_patterns:
                        json_matches = re.findall(pattern, content, re.DOTALL)
                        for json_str in json_matches:
                            try:
                                # Try to parse the JSON
                                parsed = json.loads(json_str)                                # Validate it has the expected fields
                                required_fields = ['title', 'name', 'city', 'profession', 'message', 'date']
                                if all(field in parsed for field in required_fields):
                                    return json.dumps(parsed, indent=2)
                            except json.JSONDecodeError:
                                continue
            
            return json.dumps({"error": "No valid JSON found in agent response", "raw_response": content[:500]})
        else:
            return json.dumps({"error": f"Agent run failed with status: {run.status}"})
            
    except Exception as e:
        error_msg = f"Error generating random card data: {str(e)}"
        print(error_msg)
        return json.dumps({"error": error_msg})

def get_agent_info() -> dict:
    """
    Get information about the data generator agent.
    
    Returns:
        Dictionary with agent information.
    """
    try:
        agent = _create_data_generator_agent()
        return {
            "agent_id": agent.id,
            "agent_name": agent.name,
            "model": getattr(agent, 'model', 'N/A'),
            "created_in_session": _data_generator_agent is not None
        }
    except Exception as e:
        return {"error": str(e)}

def list_all_agents() -> list:
    """
    List all agents in the current project.
    
    Returns:
        List of agent information.
    """
    try:
        agents_client = _get_agents_client()
        # Try different methods to list agents
        try:
            agents = agents_client.list_agents()
        except AttributeError:
            return [{"info": "Agent listing not available with current API"}]
        
        return [{"id": agent.id, "name": getattr(agent, 'name', 'N/A'), "model": getattr(agent, 'model', 'N/A')} for agent in agents]
    except Exception as e:
        return [{"error": str(e)}]

def delete_data_generator_agent() -> dict:
    """
    Delete the data generator agent from Foundry (use with caution).
    
    Returns:
        Dictionary with deletion status.
    """
    global _data_generator_agent
    
    try:
        agents_client = _get_agents_client()
        agent_name = "card-data-generator"
        
        # Find and delete the agent
        try:
            existing_agents = agents_client.list_agents()
        except AttributeError:
            return {"success": False, "error": "Cannot list agents with current API"}
        
        for agent in existing_agents:
            if hasattr(agent, 'name') and agent.name == agent_name:
                agents_client.delete_agent(agent.id)
                _data_generator_agent = None  # Reset the global variable
                return {"success": True, "message": f"Agent {agent.id} deleted successfully"}
        
        return {"success": False, "message": "Agent not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Test function
if __name__ == "__main__":
    print("Testing data generator agent...")
    
    # Show all existing agents first
    print("\n📋 All agents in project:")
    all_agents = list_all_agents()
    for agent in all_agents:
        print(f"  - {agent}")
    
    # Test generating data (this will create or find the agent)
    print("\n🔄 Generating card data...")
    result = generate_random_card_data()
    print("Generated data:")
    print(result)
    
    # Show agent info
    print("\n📊 Agent info:")
    info = get_agent_info()
    print(info)
    
    # Test that subsequent calls use the same agent
    print("\n🔄 Generating data again (should use existing agent)...")
    result2 = generate_random_card_data()
    print("Generated data:")
    print(result2)
    
    # Show that agent is reused
    print("\n📊 Agent info after second call:")
    info2 = get_agent_info()
    print(info2)
    print(f"Same agent ID: {info['agent_id'] == info2['agent_id']}")
