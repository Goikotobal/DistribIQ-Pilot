import streamlit as st
import time
import json
import uuid

# ✅ FIX 1: This MUST be the very first Streamlit command (Line 6)
st.set_page_config(
    page_title="DistribIQ | Barentz AI",
    page_icon="src/logo.png", # Use your new logo as the browser tab icon too!
    layout="wide"
)

# ✅ NEW IMPORT LOGIC
try:
    from agent import prepare_knowledge_base, solver_agent
except ImportError:
    from src.agent import prepare_knowledge_base, solver_agent

# --- CUSTOM CSS (Branding) ---
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #0056b3; font-weight: 700;}
    .sub-header {font-size: 1.2rem; color: #6c757d;}
    .chat-container {background-color: #f8f9fa; padding: 20px; border-radius: 10px;}
    .stChatMessage {border-radius: 10px; padding: 10px;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Settings & Status) ---
with st.sidebar:
    # 1. THE LOGO (Robust Path)
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, "logo.png")

    try:
        # Check if file exists first to avoid ugly errors
        if os.path.exists(logo_path):
            # Pass the path variable you created on line 34
            st.image(logo_path, use_column_width=True)
        else:
            st.warning(f"⚠️ Logo not found at: {logo_path}")
            # Fallback title if logo is missing
            st.markdown("## DistribIQ") 
    except Exception as e:
        st.error(f"Logo Error: {e}")

    # 2. TITLE & INFO
    st.title("Control Panel")
    st.caption("🚀 Engine: Gemini 2.5 Flash")
    st.divider()
    
    # 3. KNOWLEDGE BASE LOADER
    if "kb_loaded" not in st.session_state:
        st.session_state.kb_loaded = False
        st.session_state.kb_data = None

    if not st.session_state.kb_loaded:
        if st.button("🔄 Load Knowledge Base", type="primary"):
            with st.spinner("Ingesting Excel & PDFs..."):
                try:
                    data = prepare_knowledge_base()
                    
                    if data["excel_text"] or data["pdf_handles"]:
                        st.session_state.kb_data = data
                        st.session_state.kb_loaded = True
                        st.success("✅ System Ready")
                        time.sleep(1) # Small pause to let user see the success
                        st.rerun()    # Refresh to unlock the chat
                    else:
                        st.error("❌ No data found in data/docs/")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.success("✅ Knowledge Base Active")
        st.info("Files Loaded:\n- Product Master (Excel)\n- Shipping Tariffs (PDF)\n- Compliance Guide (PDF)")
        if st.button("Reload Data"):
            st.session_state.kb_loaded = False
            st.rerun()

# --- MAIN CHAT INTERFACE ---
st.markdown('<div class="main-header">🧬 DistribIQ</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI Decision Support for Ingredient Distribution</div>', unsafe_allow_html=True)
st.divider()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am DistribIQ. I have access to the Product Master, Pricing Tiers, and Logistics data. How can I help?"}
    ]

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        try:
            if isinstance(msg["content"], str) and msg["content"].strip().startswith("{"):
                data = json.loads(msg["content"])
                st.markdown(data.get("answer", "No answer"))
                
                # Show Explanation (if available)
                if data.get("explanation"):
                    with st.expander("🕵️ How I calculated this"):
                        st.markdown(data["explanation"])
                        
                if data.get("citations"):
                    st.caption(f"📚 Source: {', '.join(data['citations'])}")
            else:
                st.markdown(msg["content"])
        except:
            st.markdown(msg["content"])

# --- USER INPUT HANDLER ---
if prompt := st.chat_input("Ask about products, shipping, or regulations..."):
    if not st.session_state.kb_loaded:
        st.error("⚠️ Please load the Knowledge Base in the sidebar first!")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Analyzing Decision Matrices..."):
            start_time = time.time()
            
            state = {
                "question_id": str(uuid.uuid4())[:8],
                "question": prompt,
                "context_files": st.session_state.kb_data["pdf_handles"],
                "context_text": st.session_state.kb_data["excel_text"],
                "final_answer": {}
            }
            
            try:
                result_state = solver_agent(state)
                final = result_state["final_answer"]
                
                # 1. Answer
                st.markdown(final.get("answer", "I could not generate an answer."))
                
                # 2. Reasoning
                if final.get("explanation"):
                    with st.expander("🕵️ How I calculated this"):
                        st.markdown(final["explanation"])

                # 3. Sources
                if final.get("citations"):
                    st.caption(f"📚 Sources: {', '.join(final['citations'])}")
                
                # 4. Debug Metadata
                with st.expander("⚙️ Technical Metadata"):
                    st.write(f"**Confidence:** {final.get('confidence', 0.0)}")
                    st.write(f"**Latency:** {round(time.time() - start_time, 2)}s")
                    st.json(final)
                
                st.session_state.messages.append({"role": "assistant", "content": json.dumps(final)})
                
            except Exception as e:
                st.error(f"System Error: {e}")