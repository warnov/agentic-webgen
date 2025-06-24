import sys
try:
    from azure.ai.projects import AIProjectClient
    print("✅ azure.ai.projects.AIProjectClient available")
    print("Available:", dir(AIProjectClient))
except ImportError as e:
    print("❌ azure.ai.projects.AIProjectClient not available:", e)

try:
    from azure.ai.agents import AgentsClient  
    print("✅ azure.ai.agents.AgentsClient available")
except ImportError as e:
    print("❌ azure.ai.agents.AgentsClient not available:", e)

try:
    import azure.ai.agents
    print("✅ azure.ai.agents module available")
    print("Content:", dir(azure.ai.agents))
except ImportError as e:
    print("❌ azure.ai.agents module not available:", e)
