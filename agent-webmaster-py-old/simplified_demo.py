# simplified_demo.py
"""
Simplified demo showing the improved structure without Azure dependencies.
This demonstrates the transparent instantiation pattern.
"""

import os
from datetime import datetime

print("🎯 Professional Card Generator & Publisher")
print("=" * 50)
print("🤖 Powered by Azure AI Foundry Agent Integration")
print("📊 Using Transparent Agent Instantiation Pattern")
print("=" * 50)

# Simulate the improved interface
class MockAgent:
    def __init__(self):
        self.id = "mock-agent-123"
        self.name = "webgen-fx-tool"
    
    def generate_card_from_data(self, card_data):
        """Simulate card generation with improved error handling."""
        date_str = card_data.get('date', datetime.now().strftime("%Y-%m-%d"))
        name = card_data.get('name', 'Unknown')
        
        # Simulate the enhanced prompt with date
        print(f"🔄 Generating card for {name} with date: {date_str}")
        
        # Simulate different scenarios
        import random
        scenarios = [
            ("success", f"https://example-cards.com/card-{name.lower().replace(' ', '-')}-{date_str}"),
            ("failed", f"Agent run failed with status: RunStatus.FAILED - Azure Function timeout"),
            ("no_url", "Card generation completed but no URL was returned")
        ]
        
        scenario, result = random.choice(scenarios)
        
        if scenario == "success":
            print(f"✅ Card generated successfully")
            return result
        elif scenario == "failed":
            print(f"❌ {result}")
            print("💡 Enhanced error handling now provides:")
            print("   - Detailed status information")
            print("   - Azure Function connectivity check")
            print("   - Environment variable validation")
            return result
        else:
            print(f"⚠️  {result}")
            return result

def main():
    """Demonstrate the improved interface."""
    agent = MockAgent()
    
    while True:
        print("\n📋 Options:")
        print("1. Generate random professional card")
        print("2. Create card with specific details") 
        print("3. Generate from custom prompt")
        print("4. Show improvements")
        print("5. Exit")
        
        choice = input("\n🔮 Choose an option (1-5): ").strip()
        
        if choice == "1":
            print("\n🎲 Using: create_conversation_with_webgen_agent()")
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Demonstrate enhanced prompt
            prompt = f"Generate a creative random professional card. Include today's date: {current_date}"
            print(f"📝 Enhanced prompt: {prompt}")
            
            # Simulate result
            result = agent.generate_card_from_data({"name": "Random User", "date": current_date})
            print(f"🔗 Result: {result}")
            
        elif choice == "2":
            print("\n📝 Using: generate_card_from_data()")
            name = input("Name: ").strip() or "Test User"
            city = input("City: ").strip() or "Demo City"
            profession = input("Profession: ").strip() or "Developer"
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            card_data = {
                "title": "Professional Card",
                "name": name,
                "city": city,
                "profession": profession,
                "message": f"Professional {profession} based in {city}",
                "date": current_date
            }
            
            print(f"📊 Card data with date field: {card_data}")
            result = agent.generate_card_from_data(card_data)
            print(f"🔗 Result: {result}")
            
        elif choice == "3":
            print("\n💬 Using: create_conversation_with_webgen_agent()")
            user_prompt = input("Custom prompt: ").strip()
            if user_prompt:
                current_date = datetime.now().strftime("%Y-%m-%d")
                enhanced_prompt = f"{user_prompt}. Include today's date: {current_date}"
                print(f"🔧 Enhanced with date: {enhanced_prompt}")
                
                result = agent.generate_card_from_data({"name": "Custom User", "date": current_date})
                print(f"🔗 Result: {result}")
            else:
                print("❌ No prompt provided")
                
        elif choice == "4":
            print("\n🚀 Improvements Made:")
            print("✅ Transparent Agent Instantiation:")
            print("   - get_webgen_agent() - Auto-create/fetch agent")
            print("   - Singleton pattern ensures uniqueness in AI Foundry")
            print("   - Session caching for performance")
            print()
            print("✅ Simplified Interactive Demo:")
            print("   - 116 lines vs 172 lines (33% reduction)")
            print("   - 4 imports vs 9 imports (56% reduction)")
            print("   - No manual setup code needed")
            print()
            print("✅ Enhanced Error Handling:")
            print("   - Detailed run status information")
            print("   - Azure Function connectivity diagnostics")
            print("   - Environment variable validation")
            print()
            print("✅ Date Field Handling:")
            print("   - Explicit date parameter in card_data")
            print("   - Enhanced prompts with date instructions")
            print("   - Better JSON payload structure")
            print()
            print("✅ Public Interface Functions:")
            print("   - create_conversation_with_webgen_agent()")
            print("   - generate_card_from_data()")
            print("   - generate_card_with_random_data()")
            print("   - get_agent_info(), is_webgen_agent_initialized()")
            
        elif choice == "5":
            print("\n👋 Demo completed!")
            print("📋 Key files created:")
            print("   - agents/ag_webgen/ag_webgen.py (transparent instantiation)")
            print("   - example_agent_usage.py (usage examples)")
            print("   - WEBGEN_AGENT_GUIDE.md (documentation)")
            print("   - interactive_demo.py (simplified 116 lines)")
            break
            
        else:
            print("❌ Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
