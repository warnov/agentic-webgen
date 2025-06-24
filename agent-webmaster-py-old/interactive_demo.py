# interactive_demo.py
"""
Interactive demo of the integrated card generation and publishing system.
Simplified using transparent agent instantiation.
"""

import os
import sys
from datetime import datetime

# Add path for direct imports
sys.path.append(os.path.join(os.path.dirname(__file__), "agents", "ag_webgen"))

# Try to import the ag_webgen module with proper error handling
try:
    from ag_webgen import (
        generate_card_from_data, 
        generate_card_with_random_data,
        create_conversation_with_webgen_agent,
        get_agent_info
    )
    AGENT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Error importing ag_webgen: {e}")
    print("🔧 This is likely due to missing Azure AI dependencies")
    print("📦 Please install required packages: pip install azure-ai-agents azure-identity python-dotenv")
    print("🌐 Or set up your Azure environment variables if packages are installed")
    AGENT_AVAILABLE = False

def handle_agent_call(func, *args, **kwargs):
    """Handle agent function calls with proper error handling."""
    if not AGENT_AVAILABLE:
        return "Demo unavailable: Azure AI dependencies not properly configured"
    
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_msg = str(e)
        if "PROJECT_ENDPOINT" in error_msg:
            return "Error: PROJECT_ENDPOINT environment variable not set. Please configure your Azure AI Foundry endpoint."
        elif "MODEL_DEPLOYMENT_NAME" in error_msg:
            return "Error: MODEL_DEPLOYMENT_NAME environment variable not set. Please configure your model deployment."
        elif "AZURE_FUNCTION_URL" in error_msg:
            return "Error: AZURE_FUNCTION_URL environment variable not set. Please configure your Azure Function URL."
        elif "authentication" in error_msg.lower() or "credential" in error_msg.lower():
            return "Error: Azure authentication failed. Please ensure you're logged into Azure CLI or have proper credentials configured."
        else:
            return f"Error: {error_msg}"

def main():
    """Main interactive demo function."""
    print("🎯 Professional Card Generator & Publisher")
    print("=" * 50)
    print("🤖 Powered by Azure AI Foundry Agent Integration")
    
    # Get agent info to display
    try:
        if AGENT_AVAILABLE:
            agent_info = get_agent_info()
            print(f"📊 Agent: {agent_info.get('agent_name', 'webgen-fx-tool')}")
            print(f"🆔 Agent ID: {agent_info.get('agent_id', 'Loading...')}")
        else:
            print("📊 Agent: Demo mode (Azure dependencies not available)")
            print("🆔 Agent ID: N/A")
    except Exception as e:
        print(f"⚠️  Agent info: {e}")
    
    print("=" * 50)
    
    while True:
        print("\n📋 Options:")
        print("1. Generate random professional card")
        print("2. Create card with specific details")
        print("3. Generate from custom prompt")
        print("4. Exit")
        
        choice = input("\n🔮 Choose an option (1-4): ").strip()
        
        if choice == "1":
            print("\n🎲 Generating random professional card...")
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Enhanced prompt to ensure date is included
            prompt = f"Generate a creative random professional card and publish it. Make sure to include today's date: {current_date} in the card data."
            url = handle_agent_call(create_conversation_with_webgen_agent, prompt)
            
            if url and "https://" in url:
                print(f"✅ Random card generated: {url}")
            else:
                print(f"❌ Failed to generate random card. Response: {url}")
                print("💡 This might be due to:")
                print("   - Missing environment variables")
                print("   - Azure Function not accessible")
                print("   - Agent configuration issues")
                
        elif choice == "2":
            print("\n📝 Enter the details for your professional card:")
            name = input("Name: ").strip()
            if not name:
                print("❌ Name is required!")
                continue
                
            city = input("City: ").strip() or "Unknown City"
            profession = input("Profession: ").strip() or "Professional"
            title = input("Card Title (optional): ").strip() or "Professional Card"
            message = input("Personal Message (optional): ").strip() or f"Professional {profession} based in {city}"
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            card_data = {
                "title": title,
                "name": name,
                "city": city,
                "profession": profession,
                "message": message,
                "date": current_date
            }
            
            print(f"\n🔄 Creating card for {name}...")
            url = handle_agent_call(generate_card_from_data, card_data)
            
            if url and "https://" in url:
                print(f"✅ Custom card created: {url}")
            else:
                print(f"❌ Failed to create custom card. Response: {url}")
                
        elif choice == "3":
            print("\n💬 Enter your custom prompt for card generation:")
            print("   (The system will automatically include today's date)")
            user_prompt = input("Prompt: ").strip()
            
            if user_prompt:
                current_date = datetime.now().strftime("%Y-%m-%d")
                enhanced_prompt = f"{user_prompt}. Make sure to include today's date: {current_date} in the card data."
                
                print(f"\n🔄 Processing custom prompt...")
                url = handle_agent_call(create_conversation_with_webgen_agent, enhanced_prompt)
                
                if url and "https://" in url:
                    print(f"✅ Card generated from prompt: {url}")
                else:
                    print(f"❌ Failed to generate card from prompt. Response: {url}")
            else:
                print("❌ No prompt provided")
                
        elif choice == "4":
            print("\n👋 Thanks for using the Professional Card Generator!")
            break
            
        else:
            print("❌ Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
