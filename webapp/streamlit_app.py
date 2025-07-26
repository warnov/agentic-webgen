import streamlit as st
import sys
import os
import json
import time
import tempfile
import uuid
import re
from datetime import datetime
import streamlit.components.v1 as components

# Add your agent paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
web_gen_path = os.path.join(parent_dir, 'agent-webmaster-py', 'agents', 'ag_web_gen')

# Add web gen path to sys.path if it exists
if os.path.exists(web_gen_path):
    sys.path.insert(0, web_gen_path)
else:
    st.error(f"Web Gen path does not exist: {web_gen_path}")

# Import ag_web_gen agent
try:
    import ag_web_gen
    web_gen_imported = True
except ImportError as e:
    web_gen_imported = False
    st.error(f"Failed to import ag_web_gen: {e}")

# Show import status in expander for debugging
with st.expander("🔍 Import Status (Click to Debug)", expanded=False):
    st.write("**Agent Import Status:**")
    if web_gen_imported:
        st.success("✅ ag_web_gen imported successfully")
    else:
        st.error("❌ ag_web_gen failed to import")
    
    st.write("**Path Information:**")
    st.code(f"Current Dir: {current_dir}")
    st.code(f"Parent Dir: {parent_dir}")
    st.code(f"Web Gen Path: {web_gen_path}")
    st.code(f"Web Gen Exists: {os.path.exists(web_gen_path)}")
    
    # Show directory contents
    if os.path.exists(web_gen_path):
        st.write("**Web Gen Directory Contents:**")
        try:
            files = os.listdir(web_gen_path)
            for file in files:
                st.text(f"  - {file}")
        except Exception as e:
            st.error(f"Could not list web_gen directory: {e}")
    
    st.write("**sys.path (last 5 entries):**")
    for path in sys.path[-5:]:
        st.code(path)

# Page configuration
st.set_page_config(
    page_title="🚀 Agentic Platform",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stAlert {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 Agentic Web Generator</h1>
    <p>Create Beautiful Personal Cards with AI</p>
</div>
""", unsafe_allow_html=True)

# Initialize session states for web generator
def initialize_web_gen_agent():
    """Initialize web generator agent with error handling."""
    if web_gen_imported:
        try:
            st.session_state.web_gen_agent = ag_web_gen.instance
            st.session_state.web_gen_client = ag_web_gen.client
            st.session_state.web_gen_error = None
            return True
        except Exception as e:
            st.session_state.web_gen_error = str(e)
            st.error(f"Web Generator initialization error: {e}")
            return False
    else:
        st.session_state.web_gen_error = "Module import failed"
        return False

if "web_gen_initialized" not in st.session_state:
    st.session_state.web_gen_ready = initialize_web_gen_agent()
    st.session_state.web_gen_initialized = True

# Initialize session states
if "web_gen_messages" not in st.session_state:
    st.session_state.web_gen_messages = []

if "generated_cards" not in st.session_state:
    st.session_state.generated_cards = []

# Sidebar for Web Generator
with st.sidebar:
    st.header("🎴 Web Generator")
    st.markdown("""
    **How to use:**
    1. Type your request for a personal card
    2. Include details like:
       - Name
       - Profession
       - City
       - Personal message
    3. The AI will generate and publish your card
    4. You'll receive a live URL to share!
    
    **Example prompts:**
    - "Create a card for John Doe, software engineer in Seattle"
    - "Make a business card for Maria, marketing director in Madrid"
    """)
    
    # Web Gen Agent status
    st.subheader("🤖 Agent Status")
    if st.session_state.web_gen_ready:
        st.success("✅ Web Generator Ready")
    else:
        st.error("❌ Web Generator Not Ready")
        if hasattr(st.session_state, 'web_gen_error') and st.session_state.web_gen_error:
            st.error(f"Error: {st.session_state.web_gen_error}")
    
    # Generated cards history
    if st.session_state.generated_cards:
        st.subheader("🎴 Generated Cards")
        for i, card in enumerate(st.session_state.generated_cards):
            st.markdown(f"**Card {i+1}:** {card['name']}")
            if st.button(f"🌐 View Card {i+1}", key=f"card_{i}"):
                st.markdown(f"[Open Card]({card['url']})")
            st.markdown("---")

# Main content for Web Generator
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Chat with Web Generator")
    
    # Display chat history
    for message in st.session_state.web_gen_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Tell me about the personal card you want to create..."):
        # Add user message to chat history
        st.session_state.web_gen_messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            if not st.session_state.web_gen_ready:
                st.error("❌ Web Generator is not ready. Please check the agent status in the sidebar.")
            else:
                try:
                    with st.spinner("🤖 Generating your personal card..."):
                        # Create thread and send message
                        thread = st.session_state.web_gen_client.threads.create()
                        st.session_state.web_gen_client.messages.create(
                            thread_id=thread.id,
                            role="user",
                            content=prompt
                        )
                        
                        # Start the run
                        run = st.session_state.web_gen_client.runs.create_and_process(
                            thread_id=thread.id,
                            agent_id=st.session_state.web_gen_agent.id
                        )
                        
                        if run.status == "completed":
                            # Get the assistant's response
                            messages = list(st.session_state.web_gen_client.messages.list(thread_id=thread.id))
                            for msg in reversed(messages):
                                if msg.role == "assistant":
                                    response_content = msg.content[0].text.value if hasattr(msg.content[0], "text") else str(msg.content)
                                    
                                    # Display response
                                    st.markdown(response_content)
                                    
                                    # Add to chat history
                                    st.session_state.web_gen_messages.append({"role": "assistant", "content": response_content})
                                    
                                    # Extract URL if present
                                    url_match = re.search(r'https?://[^\s]+', response_content)
                                    if url_match:
                                        url = url_match.group()
                                        
                                        # Extract name from prompt (simple extraction)
                                        name_match = re.search(r'(?:for|card for|name is)\s+([A-Za-z\s]+)', prompt, re.IGNORECASE)
                                        name = name_match.group(1).strip() if name_match else f"Card {len(st.session_state.generated_cards) + 1}"
                                        
                                        # Store card info
                                        card_info = {
                                            "name": name,
                                            "url": url,
                                            "timestamp": datetime.now(),
                                            "prompt": prompt
                                        }
                                        st.session_state.generated_cards.append(card_info)
                                        
                                        # Show success message
                                        st.success(f"✅ Card created successfully! [Open Card]({url})")
                                    break
                        else:
                            error_msg = f"❌ Generation failed with status: {run.status}"
                            if hasattr(run, 'last_error') and run.last_error:
                                error_msg += f"\nError: {run.last_error}"
                            st.error(error_msg)
                            st.session_state.web_gen_messages.append({"role": "assistant", "content": error_msg})
                            
                except Exception as e:
                    error_msg = f"❌ An error occurred: {str(e)}"
                    st.error(error_msg)
                    st.session_state.web_gen_messages.append({"role": "assistant", "content": error_msg})

with col2:
    st.header("📊 Quick Actions")
    
    # Sample prompts
    st.subheader("💡 Sample Prompts")
    sample_prompts = [
        "Create a card for John Doe, software engineer in Seattle",
        "Make a business card for Maria, marketing director in Madrid",
        "Generate a card for Dr. Sarah Johnson, pediatrician in Boston",
        "Create a card for Mike Chen, graphic designer in San Francisco"
    ]
    
    for i, sample in enumerate(sample_prompts):
        if st.button(f"💬 {sample[:30]}...", key=f"sample_{i}"):
            # Add to chat input by rerunning with the sample prompt
            st.session_state.web_gen_messages.append({"role": "user", "content": sample})
            st.rerun()
    
    # Clear chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.web_gen_messages = []
        st.rerun()
    
    # Cards summary
    st.subheader("📈 Session Summary")
    st.metric("Generated Cards", len(st.session_state.generated_cards))
    st.metric("Chat Messages", len(st.session_state.web_gen_messages))

# Footer
st.markdown("---")
st.markdown("*Powered by Azure AI Agents*")

# Debug information in expander
with st.expander("🔧 Debug Information", expanded=False):
    st.write("**Session State:**")
    debug_info = {
        "Web Gen Ready": st.session_state.web_gen_ready,
        "Web Gen Error": getattr(st.session_state, 'web_gen_error', None),
        "Messages Count": len(st.session_state.web_gen_messages),
        "Generated Cards": len(st.session_state.generated_cards),
        "Current Dir": current_dir,
        "Web Gen Path": web_gen_path,
        "Web Gen Imported": web_gen_imported
    }
    st.json(debug_info)
