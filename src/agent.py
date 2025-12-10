import os
import json
import time
from typing import TypedDict, List, Any
import google.generativeai as genai
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import pandas as pd

# --- 1. CONFIGURATION ---
load_dotenv()
API_KEY = os.environ.get("GOOGLE_API_KEY")

# ✅ UPDATED: Using the correct Flash model version
MODEL_NAME = "gemini-2.5-flash"

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("⚠️ No API Key found. Running in MOCK MODE.")

# --- 2. STATE DEFINITION ---
class DistribIQState(TypedDict):
    question_id: str
    question: str
    context_files: List[Any]    # Handles for PDFs
    context_text: str           # Text content for Excel
    final_answer: dict

# --- 3. THE FILE LOADER ---
# In src/agent.py

def prepare_knowledge_base():
    """
    Reads Excel locally (converting to markdown) and uploads PDFs to Gemini.
    """
    
    # ✅ NEW PATH LOGIC: 
    # Get the folder where THIS script (agent.py) lives
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level (..), then down into data/docs
    base_folder = os.path.join(current_dir, "..", "data", "docs")
    
    # Files to look for
    excel_file = "DM_Report_MASTER_Generic.xlsx"
    pdf_files = [
        "Shipping_Tariffs_EMEA_Generic.pdf",
        "Regulatory_Compliance_Guide_Generic.pdf"
    ]
    
    knowledge_context = {
        "pdf_handles": [],
        "excel_text": ""
    }
    
    print(f"📂 Preparing Knowledge Base from: {base_folder}")
    
    # Verify folder exists
    if not os.path.exists(base_folder):
        print(f"❌ ERROR: Folder '{base_folder}' not found.")
        return knowledge_context

    # ... (The rest of the logic remains the same) ...
    # (Just make sure the loop below uses 'base_folder' which we just defined)
    
    # --- PART A: PROCESS EXCEL ---
    excel_path = os.path.join(base_folder, excel_file)
    if os.path.exists(excel_path):
        # ... (keep existing code) ...
        try:
            # Add this import if missing at top: import pandas as pd
            xls = pd.ExcelFile(excel_path)
            full_text = f"--- SOURCE FILE: {excel_file} ---\n"
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                markdown_table = df.to_markdown(index=False)
                full_text += f"\n### SHEET: {sheet_name}\n{markdown_table}\n"
            knowledge_context["excel_text"] = full_text
            print(f"   ✅ Excel processed")
        except Exception as e:
            print(f"   ❌ Excel Error: {e}")

    # --- PART B: UPLOAD PDFS ---
    for filename in pdf_files:
        full_path = os.path.join(base_folder, filename)
        if os.path.exists(full_path):
            # ... (keep existing code) ...
            try:
                f = genai.upload_file(full_path)
                while f.state.name == "PROCESSING":
                    time.sleep(1)
                    f = genai.get_file(f.name)
                knowledge_context["pdf_handles"].append(f)
                print(f"   ✅ PDF Ready: {filename}")
            except Exception as e:
                 print(f"   ❌ PDF Error: {e}")

    return knowledge_context
    
    # --- PART A: PROCESS EXCEL (Convert to Text) ---
    excel_path = os.path.join(base_folder, excel_file)
    if os.path.exists(excel_path):
        print(f"   -> Reading {excel_file}...")
        try:
            xls = pd.ExcelFile(excel_path)
            full_text = f"--- SOURCE FILE: {excel_file} ---\n"
            
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                # Convert to clean markdown table for the LLM
                markdown_table = df.to_markdown(index=False)
                full_text += f"\n### SHEET: {sheet_name}\n{markdown_table}\n"
            
            knowledge_context["excel_text"] = full_text
            print(f"   ✅ Excel processed successfully ({len(full_text)} chars)")
        except Exception as e:
            print(f"   ❌ Error reading Excel: {e}")
    else:
        print(f"   ⚠️ Excel file not found at: {excel_path}")

    # --- PART B: UPLOAD PDFs (Native Gemini Support) ---
    for filename in pdf_files:
        full_path = os.path.join(base_folder, filename)
        if os.path.exists(full_path):
            print(f"   -> Uploading PDF {filename}...")
            try:
                f = genai.upload_file(full_path)
                # Wait for file to be ready
                while f.state.name == "PROCESSING":
                    time.sleep(1)
                    f = genai.get_file(f.name)
                knowledge_context["pdf_handles"].append(f)
                print(f"   ✅ Ready: {filename}")
            except Exception as e:
                print(f"   ❌ PDF Upload failed: {e}")
        else:
            print(f"   ⚠️ PDF not found at: {full_path}")
            
    return knowledge_context

# --- 4. THE AGENT (Updated with Reasoning) ---
def solver_agent(state: DistribIQState):
    print(f"\n⚙️ [DistribIQ] Thinking about: {state['question']}...")
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        
        prompt_parts = [
            f"""
            You are an expert assistant for Barentz. 
            Answer the question using the provided context.
            
            CONTEXT 1 (Excel Data converted to Text):
            {state['context_text']}
            
            CONTEXT 2 (Attached PDF Documents):
            (See attached files)
            
            Question: {state['question']}
            
            Output format (JSON):
            {{
                "answer": "The direct answer to the user's question.",
                "explanation": "A concise, step-by-step explanation of how you derived the answer. Mention specific data points used (e.g. 'Found Tier 3 price of €2.38, added €0.15 freight').",
                "citations": ["Sheet Name", "PDF Page X"],
                "confidence": 0.95
            }}
            """
        ]
        
        if state['context_files']:
            prompt_parts.extend(state['context_files'])
        
        response = model.generate_content(
            prompt_parts,
            generation_config={"response_mime_type": "application/json"}
        )
        state["final_answer"] = json.loads(response.text)
        
    except Exception as e:
        print(f"   ❌ AI Error: {e}")
        state["final_answer"] = {"error": str(e)}
        
    return state

# --- 5. RUNNER ---
if __name__ == "__main__":
    # 1. Prepare Data
    kb_data = prepare_knowledge_base()
    
    # 2. Build Graph
    workflow = StateGraph(DistribIQState)
    workflow.add_node("solver", solver_agent)
    workflow.set_entry_point("solver")
    workflow.add_edge("solver", END)
    app = workflow.compile()
    
    # 3. Ask Question (S001)
    # Check if we have ANY data (Excel text OR PDF handles)
    if kb_data["excel_text"] or kb_data["pdf_handles"]:
        print("🚀 Running DistribIQ Stage 2...")
        result = app.invoke({
            "question_id": "S001",
            "question": "What is the lead time for Citric Acid from Jungbunzlauer?",
            "context_files": kb_data["pdf_handles"],
            "context_text": kb_data["excel_text"]
        })
        
        print("\n📢 REAL ANSWER:")
        print(json.dumps(result["final_answer"], indent=2))
    else:
        print("\n🛑 STOPPING: No data found. Please check the folder path 'docs/dataset_prototype/'.")
