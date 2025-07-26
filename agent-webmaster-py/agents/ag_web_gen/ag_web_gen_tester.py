#!/usr/bin/env python3
"""
Simple tester for the AG Web Generator agent.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Display current environment configuration
def display_environment_info():
    """Display current environment configuration and settings."""
    environment = os.getenv('ENVIRONMENT', 'unknown')
    
    print("╔" + "═" * 60 + "╗")
    print("║" + " 🚀 AGENTIC WEB GENERATOR TESTER ".center(60) + "║")
    print("╠" + "═" * 60 + "╣")
    
    # Environment indicator with colors
    if environment.lower() == 'public':
        env_indicator = "🌐 PUBLIC ENVIRONMENT"
        env_color = "🟢"
    elif environment.lower() == 'private':
        env_indicator = "🔒 PRIVATE ENVIRONMENT"
        env_color = "🔴"
    else:
        env_indicator = f"❓ UNKNOWN ENVIRONMENT ({environment})"
        env_color = "🟡"
    
    print(f"║ {env_color} {env_indicator:<50} ║")
    print("╠" + "─" * 60 + "╣")
    
    # Display key configuration details
    project_endpoint = os.getenv('PROJECT_ENDPOINT', 'Not set')
    function_url = os.getenv('AZURE_FUNCTION_URL', 'Not set')
    model_deployment = os.getenv('MODEL_DEPLOYMENT_NAME', 'Not set')
    
    # Truncate long URLs for display
    if len(project_endpoint) > 45:
        project_display = project_endpoint[:42] + "..."
    else:
        project_display = project_endpoint
        
    if len(function_url) > 45:
        function_display = function_url[:42] + "..."
    else:
        function_display = function_url
    
    print(f"║ 🎯 Project: {project_display:<47} ║")
    print(f"║ 🔧 Function: {function_display:<46} ║")
    print(f"║ 🤖 Model: {model_deployment:<49} ║")
    print("╚" + "═" * 60 + "╝")
    print()

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from agents.ag_web_gen import ag_web_gen





def test_web_gen_agent():
    """Test the web generator agent."""
    
    # Display environment information
    display_environment_info()
    
    # Get agent instance and client (handles everything internally)
    agent = ag_web_gen.instance
    client = ag_web_gen.client
    
    print(f"🤖 Agent ID: {agent.id}")
    print(f"🔧 Tools available: {len(agent.tools)}")
    
    # Get user input with a better prompt
    print("\n" + "="*50)
    print("AG Web Generator Agent Test")
    print("="*50)
    user_prompt = input("Enter your request (or press Enter for default): ").strip()
    if not user_prompt:
        user_prompt = "Generate and publish a random card"
    
    print(f"\n🎯 Processing: {user_prompt}")
    print("-" * 30)
    
    # 🎯 Create conversation and run
    thread = client.threads.create()
    
    client.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_prompt
    )
    
    # Start the agent run
    print("⏳ Running agent...")
    run = client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id
    )
    
    # Check results
    print(f"🏁 Run status: {run.status}")
    
    if run.status == "completed":
        messages = client.messages.list(thread_id=thread.id)
        messages_list = list(messages)  # Convert to list first
        
        print("\n📝 Agent Response:")
        print("-" * 30)
        for msg in reversed(messages_list):  # Now we can reverse
            if msg.role == "assistant":
                # Extract the actual text content from the message
                if hasattr(msg.content, '__iter__') and len(msg.content) > 0:
                    response = msg.content[0].text.value
                else:
                    response = str(msg.content)
                
                print(response)
                break
    else:
        print(f"❌ Run failed with status: {run.status}")
        if hasattr(run, 'last_error') and run.last_error:
            print(f"Error: {run.last_error}")

if __name__ == "__main__":
    test_web_gen_agent()
