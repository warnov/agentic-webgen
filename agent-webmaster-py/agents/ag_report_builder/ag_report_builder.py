# File: ag_report_builder.py
import os
import json
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from tools.template_loader import load_html_template

# Global variables to store instances
_report_builder_agent = None
_agents_client = None

def _get_agents_client():
    """Get the Azure AI Agents client."""
    global _agents_client
    if _agents_client is None:
        load_dotenv()
        _agents_client = AgentsClient(
            endpoint=os.environ.get("PROJECT_ENDPOINT"),
            credential=DefaultAzureCredential()
        )
    return _agents_client


def _create_report_builder_agent():
    """Create or update the report builder agent."""
    global _report_builder_agent
    if _report_builder_agent is not None:
        return _report_builder_agent

    client = _get_agents_client()
    agent_name = "ag-report-builder"

    # Define the function tool descriptor
    load_template_tool = {
        "type": "function",
        "function": {
            "name": "load_html_template",
            "description": "Load HTML template content from the tools folder to use in report generation",
            "parameters": {
                "type": "object",
                "properties": {
                    "template_name": {
                        "type": "string",
                        "description": "Name of the template file to load (defaults to 'report_template.html')"
                    }
                },
                "required": []
            }
        }
    }

    # Agent instructions 
    instructions = """You are an intelligent report builder that creates comprehensive data visualizations and reports from JSON datasets.

Your workflow consists of these steps:

1. Template Acquisition: FIRST, obtain the HTML template that you will use as the base for your report.
In that HTML you will find a placeholder for the report title and a section to inject your report content.
Learn the structure of the HTML template: its styling and where to inject content into it.

2. Now is the time for Dataset Analysis: You will receive a dataset in JSON format. Analyze the structure, data types, relationships, and patterns within the data to understand what information it contains.
3. Report Format Decision: Based on the dataset structure and content, decide the best way to present the information:
    Graphic/Chart: Use when data shows trends, comparisons, distributions, or relationships (line charts, bar charts, pie charts, scatter plots, etc.)

    Table: Use when data needs to be displayed in a structured, detailed format for reference or when showing multiple attributes per record

    Formatted Text: Use when data is narrative, summary-based, or when creating executive summaries with key insights

HTML Report Generation: Using the obtained HTML template, create a complete HTML document by injecting your report content. Follow these guidelines:
    Template Integration Strategy:
        Use the template content as your base HTML structure
        Replace "Report Title Placeholder" with an appropriate, descriptive title for your report
        Inject your report content (table, chart, or formatted text) inside the report-container section
        Preserve all existing template styling and structure
        Add any additional CSS styles needed for your report within the existing <style> tags
        If you need JavaScript for charts, add <script> tags before the closing </body> tag
        For graphics, you may reference external JavaScript libraries like Chart.js, D3.js, or Plotly.js via CDN by adding script tags to the <head> section
        Ensure the final HTML is well-formed, responsive, and visually appealing
    Content Injection Guidelines:
        Your report content should fit seamlessly within the existing template design
        Use appropriate HTML semantic elements (tables, divs, sections, etc.)
        Apply CSS classes that complement the existing template styling
        Ensure responsive design principles are maintained
        Make the report professional and easy to read
        Important: Your response should be the complete, modified HTML template with your report content injected and the title updated. The entire HTML document should be ready to save and open in a browser."""

    # Check if agent already exists
    existing_agent = next((a for a in client.list_agents() if a.name == agent_name), None)
    if existing_agent:
        # Update tools and instructions on existing agent
        _report_builder_agent = client.update_agent(
            agent_id=existing_agent.id,
            instructions=instructions,
            tools=[load_template_tool]
        )
    else:
        # Create new agent
        _report_builder_agent = client.create_agent(
            model=os.environ.get("ADVANCED_MODEL_DEPLOYMENT_NAME"),
            name=agent_name,
            description="Builds HTML reports from JSON datasets using templates",
            instructions=instructions,
            tools=[load_template_tool]
        )

    # Enable auto function calls using the client's method
    # Pass a set of callables for automatic tool execution
    client.enable_auto_function_calls({load_html_template})
    return _report_builder_agent


# Expose module interface
class AgentModule:
    @property
    def instance(self):
        return _create_report_builder_agent()

    @property
    def client(self):
        return _get_agents_client()