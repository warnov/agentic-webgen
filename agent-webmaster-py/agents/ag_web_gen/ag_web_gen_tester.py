#!/usr/bin/env python3
"""
Simple tester for the AG Web Generator agent.
"""

import os
import sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agents.ag_web_gen import ag_web_gen

def test_web_gen_agent():
    """Test the web generator agent."""
    
    # Get agent instance and client (handles everything internally)
    agent = ag_web_gen.instance
    client = ag_web_gen.client
    
    # Get user input
    user_prompt = input("Enter your request (or press Enter for default): ").strip()
    if not user_prompt:
        user_prompt = "Generate and publish a card for a creative professional"
    
    # 🎯 Create conversation and run
    thread = client.threads.create()
    
    client.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_prompt
    )
    
    # Start the agent run
    run = client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id
    )
    
    # Check results
    if run.status == "completed":
        messages = client.messages.list(thread_id=thread.id)
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
    test_web_gen_agent()
