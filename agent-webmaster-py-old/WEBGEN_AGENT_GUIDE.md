# Webgen Agent - Transparent Instantiation Guide

## Overview

The `ag_webgen.py` module provides a transparent agent instantiation pattern that ensures the webgen agent maintains uniqueness in Azure AI Foundry while being easily accessible from other files.

## Key Features

✅ **Singleton Pattern**: Only one agent instance exists in AI Foundry  
✅ **Transparent Access**: Simple function calls from any file  
✅ **Automatic Creation**: Agent is created/fetched automatically on first use  
✅ **Session Caching**: Agent reference is cached locally for performance  
✅ **Error Handling**: Comprehensive error handling and status reporting  

## Public Interface Functions

### Core Agent Access

```python
from ag_webgen import get_webgen_agent, get_agents_client

# Get the webgen agent (creates/fetches automatically)
agent = get_webgen_agent()

# Get the Azure AI agents client
client = get_agents_client()
```

### High-Level Conversation

```python
from ag_webgen import create_conversation_with_webgen_agent

# Have a conversation with the agent
response = create_conversation_with_webgen_agent("Generate a professional card")
print(response)
```

### Specialized Card Generation

```python
from ag_webgen import generate_card_from_data, generate_card_with_random_data

# Generate card with specific data
card_data = {
    "title": "Professional Card",
    "name": "John Doe", 
    "city": "New York",
    "profession": "Software Engineer",
    "message": "Passionate about AI and cloud technologies",
    "date": "2025-06-24"
}
url = generate_card_from_data(card_data)

# Generate card with random data
url = generate_card_with_random_data()
```

### Agent Management

```python
from ag_webgen import (
    get_agent_info,
    is_webgen_agent_initialized,
    reset_webgen_agent,
    list_all_agents
)

# Check agent status
info = get_agent_info()
is_initialized = is_webgen_agent_initialized()

# Reset local cache (agent remains in AI Foundry)
reset_webgen_agent()

# List all agents in the project
agents = list_all_agents()
```

## Usage Examples

### Example 1: Simple Card Generation from Another File

```python
# my_app.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "agents", "ag_webgen"))

from ag_webgen import generate_card_from_data

def create_employee_card(employee_data):
    card_data = {
        "title": f"{employee_data['department']} Team Member",
        "name": employee_data['name'],
        "city": employee_data['location'],
        "profession": employee_data['role'],
        "message": f"Member of {employee_data['department']} since {employee_data['start_date']}",
        "date": "2025-06-24"
    }
    return generate_card_from_data(card_data)

# Usage
employee = {
    "name": "Alice Smith",
    "department": "Engineering", 
    "location": "San Francisco",
    "role": "Senior Developer",
    "start_date": "2023"
}
card_url = create_employee_card(employee)
print(f"Employee card: {card_url}")
```

### Example 2: Custom Workflow Integration

```python
# workflow.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "agents", "ag_webgen"))

from ag_webgen import get_webgen_agent, get_agents_client, create_conversation_with_webgen_agent

class CardWorkflow:
    def __init__(self):
        # Agent is automatically created/fetched when needed
        self.agent = None
        self.client = None
    
    def initialize(self):
        """Initialize the workflow with agent access."""
        self.agent = get_webgen_agent()
        self.client = get_agents_client()
        print(f"✅ Workflow initialized with agent: {self.agent.id}")
    
    def process_batch_requests(self, requests):
        """Process multiple card requests."""
        if not self.agent:
            self.initialize()
        
        results = []
        for request in requests:
            response = create_conversation_with_webgen_agent(request)
            results.append(response)
        
        return results

# Usage
workflow = CardWorkflow()
requests = [
    "Create a card for a marketing manager in Tokyo",
    "Generate a random creative professional card",
    "Make a card for a data scientist in London"
]
results = workflow.process_batch_requests(requests)
```

### Example 3: Direct Agent Operations

```python
# advanced_usage.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "agents", "ag_webgen"))

from ag_webgen import get_webgen_agent, get_agents_client

def advanced_agent_operations():
    # Get direct access to agent and client for advanced operations
    agent = get_webgen_agent()
    client = get_agents_client()
    
    # Create a persistent conversation thread
    thread = client.threads.create()
    
    # Send multiple messages in the same conversation
    messages = [
        "Create a professional card for a software architect",
        "Now modify it to emphasize cloud expertise",
        "Add a modern design theme"
    ]
    
    for msg in messages:
        client.messages.create(
            thread_id=thread.id,
            role="user", 
            content=msg
        )
        
        run = client.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id
        )
        
        if run.status == "completed":
            messages_list = list(client.messages.list(thread_id=thread.id))
            latest_response = messages_list[0]  # Most recent message
            print(f"🤖 Response: {latest_response.content}")
```

## Environment Setup

Make sure these environment variables are set:

```bash
PROJECT_ENDPOINT=your_ai_foundry_endpoint
MODEL_DEPLOYMENT_NAME=your_model_deployment
AZURE_FUNCTION_URL=your_azure_function_url
```

## Agent Lifecycle

1. **First Call**: Agent is created in AI Foundry or existing agent is fetched
2. **Subsequent Calls**: Cached agent reference is used for performance
3. **Session Reset**: `reset_webgen_agent()` clears local cache but keeps agent in AI Foundry
4. **Deletion**: `delete_webgen_agent()` removes agent from AI Foundry entirely

## Benefits

- **🎯 Simplicity**: Just import and call functions
- **⚡ Performance**: Agent instance is cached locally
- **🔒 Uniqueness**: Only one agent exists in AI Foundry
- **🛡️ Error Handling**: Comprehensive error handling built-in
- **🔧 Flexibility**: Both high-level and low-level access available
- **📦 Modularity**: Easy to integrate into any project structure

## Error Handling

All functions include proper error handling:

```python
try:
    url = generate_card_from_data(card_data)
    print(f"Success: {url}")
except EnvironmentError as e:
    print(f"Environment setup issue: {e}")
except RuntimeError as e:
    print(f"Agent creation failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

This transparent instantiation pattern makes the webgen agent easy to use from anywhere in your application while maintaining clean separation of concerns and optimal resource usage.
