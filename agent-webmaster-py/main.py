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
# Enable automatic function calling for the toolset
# This is necessary to allow the agent to call the function automatically
agents_client.enable_auto_function_calls(toolset)

# 🤖 Create the agent
agent = agents_client.create_agent(
    model=MODEL_DEPLOYMENT_NAME,
    name="html-template-agent",
    instructions =
        "You are an agent that receives requests for publishing personal cards. These cards contain name, city and profession. For this publishing, it is required that an html template be filled with a json representing the person info to publish. When the user describes a person in natural language, extract exactly three fields—\"name\", \"city\" and \"profession\"—and build a JSON object like:\n" +
        "{\n" +
        "  \"name\": \"<Full Name>\",\n" +
        "  \"city\": \"<City Name>\",\n" +
        "  \"profession\": \"<Profession Title>\"\n" +
        "}\n" +
        "Return only the file URL to the user.",
    toolset=toolset,
)


user_input = f"Publica una tarjeta personal para Walter Novoa, que vive en New York y trabaja como Solutions Architect."

# 🎯 Create conversation and run
thread = agents_client.threads.create()

agents_client.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_input
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
            url_match = re.search(r'https://[^\s]+', str(msg.content))
            if url_match:
                print(url_match.group())
                break
    else:
        print("❌ No URL was generated")
else:
    print(f"❌ Agent run failed with status: {run.status}")