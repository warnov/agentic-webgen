# main.py

import os
import json
import re
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FunctionTool, ToolSet
from tools.html_tools import fill_template_from_json
from dotenv import load_dotenv


load_dotenv()

# 🔧 Environment setup
PROJECT_ENDPOINT = os.environ.get("PROJECT_ENDPOINT")
MODEL_DEPLOYMENT_NAME = os.environ.get("MODEL_DEPLOYMENT_NAME")

if not PROJECT_ENDPOINT or not MODEL_DEPLOYMENT_NAME:
    raise EnvironmentError("Please set PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME as environment variables.")

# 🧠 Initialize the agents client directly
agents_client = AgentsClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

# 🛠️ Register the tool following the exact pattern from documentation
functions = FunctionTool([fill_template_from_json])

toolset = ToolSet()
toolset.add(functions)

# 🔑 THIS IS THE KEY STEP WE WERE MISSING!
agents_client.enable_auto_function_calls(toolset)

# 🤖 Create the agent
agent = agents_client.create_agent(
    model=MODEL_DEPLOYMENT_NAME,
    name="html-template-agent",
    instructions="You are an agent that receives JSON data and uses the fill_template_from_json function to fill an HTML template. Return only the file URL to the user.",
    toolset=toolset,
)

# 📤 Sample message
json_data = {
    "name": "Walter Novoa",
    "city": "Medellín", 
    "profession": "Systems Engineer"
}

user_input = f"Please fill the HTML template with this data: {json.dumps(json_data)}"

# 🎯 Create conversation and run
thread = agents_client.threads.create()

agents_client.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_input
)

# Now automatic function calling should work!
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
            url_match = re.search(r'https://[^\s]+', str(msg.content))
            if url_match:
                print(url_match.group())
                break
    else:
        print("❌ No URL was generated")
else:
    print(f"❌ Agent run failed with status: {run.status}")