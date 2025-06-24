# example_agent_usage.py
"""
Example of how to use the webgen agent from other files.
This demonstrates the transparent instantiation pattern.
"""

import sys
import os

# Add path for ag_webgen imports
sys.path.append(os.path.join(os.path.dirname(__file__), "agents", "ag_webgen"))

# Import the public interface functions
from ag_webgen import (
    get_webgen_agent,
    get_agents_client, 
    create_conversation_with_webgen_agent,
    generate_card_from_data,
    generate_card_with_random_data,
    get_agent_info,
    is_webgen_agent_initialized
)

def example_basic_usage():
    """Example of basic agent usage."""
    print("🔍 Example 1: Basic Agent Information")
    
    # Check if agent is already initialized
    if is_webgen_agent_initialized():
        print("✅ Agent already initialized in this session")
    else:
        print("🆕 Agent will be created/fetched on first use")
    
    # Get agent info (this will create/fetch the agent transparently)
    info = get_agent_info()
    print(f"📊 Agent Info: {info}")
    
    return True

def example_direct_conversation():
    """Example of having a direct conversation with the agent."""
    print("\n🗣️  Example 2: Direct Conversation")
    
    # Have a conversation with the agent
    user_message = "Genera una tarjeta para un desarrollador de software en Madrid"
    response = create_conversation_with_webgen_agent(user_message)
    print(f"🤖 Agent Response: {response}")
    
    return response

def example_card_generation():
    """Example of using the specific card generation functions."""
    print("\n🎴 Example 3: Card Generation Functions")
    
    # Generate card with specific data
    card_data = {
        "title": "Tarjeta de Ingeniero",
        "name": "Ana García",
        "city": "Barcelona",
        "profession": "Data Scientist",
        "message": "Especialista en Machine Learning e IA",
        "date": "2025-06-24"
    }
    
    print("🔄 Generating card with specific data...")
    url1 = generate_card_from_data(card_data)
    print(f"📍 Card URL: {url1}")
    
    # Generate card with random data
    print("\n🎲 Generating card with random data...")
    url2 = generate_card_with_random_data()
    print(f"📍 Random Card URL: {url2}")
    
    return url1, url2

def example_agent_management():
    """Example of agent management operations."""
    print("\n⚙️  Example 4: Agent Management")
    
    # Get direct access to the agent (if needed for advanced operations)
    try:
        agent = get_webgen_agent()
        print(f"🤖 Direct agent access - ID: {agent.id}, Name: {agent.name}")
        
        # Get direct access to the client (if needed for advanced operations)
        client = get_agents_client()
        print(f"🔌 Direct client access available")
        
        return True
    except Exception as e:
        print(f"❌ Error in agent management: {e}")
        return False

def main():
    """Run all examples."""
    print("🚀 Webgen Agent Usage Examples")
    print("=" * 50)
    
    try:
        # Run examples
        example_basic_usage()
        example_direct_conversation()
        example_card_generation()
        example_agent_management()
        
        print("\n✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error in examples: {e}")
        print("💡 Make sure your environment variables are set correctly:")
        print("   - PROJECT_ENDPOINT")
        print("   - MODEL_DEPLOYMENT_NAME") 
        print("   - AZURE_FUNCTION_URL")

if __name__ == "__main__":
    main()
