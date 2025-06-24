import os
import sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agents.ag_card_generator import ag_card_generator

def test_card_generator():
    """Test the card generator agent."""
    
    # Get agent instance and client (handles everything internally)
    agent = ag_card_generator.instance
    agents_client = ag_card_generator.client
    
    # Get user input
    user_prompt = input("Enter your prompt (or press Enter for default): ").strip()
    if not user_prompt:
        user_prompt = "Generate a business card"
    
    # 🎯 Create conversation and run
    thread = agents_client.threads.create()
    
    agents_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_prompt
    )
    
    # Start the agent run
    run = agents_client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id
    )
    
    # Check results
    if run.status == "completed":
        messages = agents_client.messages.list(thread_id=thread.id)
        messages_list = list(messages)  # Convert to list first
        
        for msg in reversed(messages_list):  # Now we can reverse
            if msg.role == "assistant":
                # Extract the actual text content from the message
                if hasattr(msg.content, '__iter__') and len(msg.content) > 0:
                    response = msg.content[0].text.value
                else:
                    response = str(msg.content)
                
                print(response)
                break

if __name__ == "__main__":
    test_card_generator()