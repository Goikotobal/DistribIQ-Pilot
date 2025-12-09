import streamlit as st
import time
import json
import uuid
import pandas as pd
import ast
import re

# 1. PAGE CONFIG
st.set_page_config(
    page_title="DistribIQ | Barentz AI",
    page_icon="src/logo.png",
    layout="wide"
)

# 2. IMPORTS
try:
    from agent import prepare_knowledge_base, solver_agent
except ImportError:
    from src.agent import prepare_knowledge_base, solver_agent

# 3. CSS STYLING (Improved Readability)
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #0056b3; font-weight: 700;}
    .sub-header {font-size: 1.2rem; color: #6c757d;}
    .chat-container {background-color: #f8f9fa; padding: 20px; border-radius: 10px;}
    .stChatMessage {border-radius: 10px; padding: 10px;}
    .stAlert {padding: 10px !important;}
    /* Make lists in markdown breathe more */
    li {margin-bottom: 5px !important;}
</style>
""", unsafe_allow_html=True)

# --- 🛠️ HELPER 1: UNIVERSAL TABLE PARSER ---
def extract_and_display_table(input_data):
    """
    Handles both raw Lists and text Strings to generate a table.
    """
    data_list = []

    # CASE 1: It is ALREADY a list
    if isinstance(input_data, list):
        data_list = input_data

    # CASE 2: It is a String (needs scanning)
    elif isinstance(input_data, str):
        clean_text = input_data.replace("```json", "").replace("```python", "").replace("```", "").strip()
        buffer = ""
        depth = 0
        recording = False
        
        for char in clean_text:
            if char == '{':
                if depth == 0:
                    recording = True
                    buffer = ""
                depth += 1
            if recording:
                buffer += char
            if char == '}':
                depth -= 1
                if depth == 0:
                    recording = False
                    try:
                        obj = ast.literal_eval(buffer)
                        if isinstance(obj, dict):
                            data_list.append(obj)
                    except:
                        pass
                    buffer = ""
    
    # --- RENDER TABLE ---
    if data_list and len(data_list) > 0:
        df = pd.DataFrame(data_list)
        
        # Smart Column Sorting
        cols = list(df.columns)
        priority = ['Barentz SKU', 'Product Name', 'EU Compliance', 'EU Compliance Status']
        sorted_cols = [c for c in priority if c in cols] + [c for c in cols if c not in priority]
        
        df = df[sorted_cols]
        df = df.rename(columns={'Barentz SKU': 'SKU', 'Product Name': 'Product'})

        st.success(f"✅ Found {len(df)} products:")
        st.dataframe(df, use_container_width=True, hide_index=True)
        return True 

    return False

# --- 🛠️ HELPER 2: EXPLANATION BEAUTIFIER ---
def display_pretty_explanation(text):
    """
    Formats the explanation text to be easier to read using Markdown spacing.
    """
    if text:
        with st.expander("🕵️ How I calculated this", expanded=False):
            # 1. Add double newlines before numbers (e.g., "1." -> "\n\n**1.**")
            # This forces Streamlit to render them as a proper list
            formatted_text = re.sub(r'(\d+\.)', r'\n\n\1', text)
            
            # 2. Render inside a clean info box
            st.info(formatted_text)

# --- SIDEBAR ---
with st.sidebar:
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, "logo.png")

    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("## DistribIQ") 

    st.title("Control Panel")
    st.divider()
    
    # KNOWLEDGE BASE STATE
    if "kb_loaded" not in st.session_state:
        st.session_state.kb_loaded = False
        st.session_state.kb_data = None

    if not st.session_state.kb_loaded:
        st.warning("⚠️ Data not loaded")
        if st.button("🔄 Load Knowledge Base", type="primary"):
            with st.spinner("Ingesting Excel & PDFs..."):
                try:
                    data = prepare_knowledge_base()
                    if data["excel_text"] or data["pdf_handles"]:
                        st.session_state.kb_data = data
                        st.session_state.kb_loaded = True
                        st.rerun()
                    else:
                        st.error("❌ No data found")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.success("✅ Knowledge Base Active")
        st.info("""
        **Files Loaded:**
        * 📄 Product Master (Excel)
        * 🚛 Shipping Tariffs (PDF)
        * ⚖️ Compliance Guide (PDF)
        """)
        if st.button("Reload Data"):
            st.session_state.kb_loaded = False
            st.rerun()

# --- MAIN CHAT ---
st.markdown('<div class="main-header">🧬 DistribIQ</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI Decision Support for Ingredient Distribution</div>', unsafe_allow_html=True)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am DistribIQ. I have access to the Product Master, Pricing Tiers, and Logistics data. How can I help?"}
    ]

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], str) and msg["content"].strip().startswith("{") and '"answer":' in msg["content"]:
            try:
                data = json.loads(msg["content"])
                
                # 1. Table
                if not extract_and_display_table(data.get("answer", "")):
                    st.markdown(str(data.get("answer", "")))
                
                # 2. Pretty Explanation
                display_pretty_explanation(data.get("explanation"))
                
                # 3. Citations
                if data.get("citations"):
                    st.caption(f"📚 Sources: {', '.join(data['citations'])}")
            except:
                st.markdown(msg["content"])
        else:
            st.markdown(msg["content"])

# --- USER INPUT ---
if prompt := st.chat_input("Ask about products, shipping, or regulations..."):
    if not st.session_state.kb_loaded:
        st.error("⚠️ Please click 'Load Knowledge Base' in the sidebar first!")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Analyzing Decision Matrices..."):
            
            # API Key Check
            if "GOOGLE_API_KEY" not in os.environ:
                 st.warning("⚠️ No API Key found. Results might be empty (Mock Mode).")

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
                
                # 1. RENDER TABLE
                if not extract_and_display_table(final.get("answer", "")):
                    st.markdown(str(final.get("answer", "")))

                # 2. RENDER PRETTY EXPLANATION
                display_pretty_explanation(final.get("explanation"))
                
                # 3. SAVE HISTORY
                st.session_state.messages.append({"role": "assistant", "content": json.dumps(final)})
                
            except Exception as e:
                st.error(f"System Error: {e}")