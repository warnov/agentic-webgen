# Agentic Web Generator - Streamlit App

This is the web interface for the Agentic Web Generator built with Streamlit.

## Features

- 🤖 Interactive chat interface with Azure AI Agents
- 🎴 Personal card generation and publishing
- 📊 Real-time statistics and monitoring
- 🌐 Direct links to generated cards
- 🔧 Debug information and connection status

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```
   PROJECT_ENDPOINT=https://your-azure-ai-project.cognitiveservices.azure.com/
   MODEL_DEPLOYMENT_NAME=your-model-deployment-name
   ```

3. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Deployment

For Azure App Service deployment, use the included `startup.sh` script.

## Usage

1. Open the app in your browser
2. Type requests for personal card creation
3. Include details like name, profession, city, and message
4. Get live URLs to share your generated cards

## Example Prompts

- "Create a card for John Doe, software engineer in Seattle"
- "Make a business card for Maria, marketing director in Madrid"
- "Generate a card for Dr. Smith, cardiologist in Boston with a welcome message"
