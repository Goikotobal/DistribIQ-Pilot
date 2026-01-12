import os
import json
import time
from datetime import datetime
import pytz  # ✅ NEW: For timezone support
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

# ✅ NEW: Timezone configuration (change to your preferred timezone)
TIMEZONE = "Europe/Amsterdam"  # Options: "Europe/Berlin", "America/New_York", etc.

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

# --- 3. DATE/TIME HELPER FUNCTIONS --- ✅ NEW SECTION
def get_current_datetime():
    """
    Returns current date and time in the configured timezone.
    Used to provide real-time context to the AI agent.
    """
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    return {
        "full_datetime": now.strftime("%A, %B %d, %Y at %H:%M %Z"),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "day_of_week": now.strftime("%A"),
        "week_number": now.strftime("%W"),
        "quarter": f"Q{(now.month - 1) // 3 + 1}",
        "year": now.year,
        "month": now.strftime("%B"),
        "is_weekend": now.weekday() >= 5
    }

def get_business_context():
    """
    Returns business-relevant time context for supply chain operations.
    """
    dt = get_current_datetime()
    
    # Determine business hours (assuming 8:00-18:00 CET)
    hour = int(datetime.now(pytz.timezone(TIMEZONE)).strftime("%H"))
    is_business_hours = 8 <= hour < 18 and not dt["is_weekend"]
    
    return {
        **dt,
        "is_business_hours": is_business_hours,
        "business_status": "Open" if is_business_hours else "Closed",
        "note": "Consider next business day for responses if outside business hours"
    }

# --- 4. THE FILE LOADER ---
def prepare_knowledge_base():
    """
    Reads Excel locally (converting to markdown) and uploads PDFs to Gemini.
    """
    
    # ✅ PATH LOGIC: 
    # Get the folder where THIS script (agent.py) lives
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level (..), then down into data/docs
    base_folder = os.path.join(current_dir, "..", "data", "docs")
    
    # Files to look for
    excel_file = "DM_Report_MASTER_Complete.xlsx"
    pdf_files = [
        "Shipping_Tariffs_EMEA_2024.pdf",
        "Regulatory_Compliance_Guide_EU_USA.pdf"
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
    
    # --- PART A: PROCESS EXCEL ---
    excel_path = os.path.join(base_folder, excel_file)
    if os.path.exists(excel_path):
        try:
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

# --- 5. THE AGENT (Updated with Date/Time Awareness) --- ✅ UPDATED
def solver_agent(state: DistribIQState):
    print(f"\n⚙️ [DistribIQ] Thinking about: {state['question']}...")
    
    # ✅ NEW: Get current date/time context
    time_context = get_business_context()
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        
        # ✅ UPDATED PROMPT: Now includes real-time awareness
        prompt_parts = [
            f"""
            You are DistribIQ, an expert AI assistant for Barentz specializing in supply chain, 
            product information, logistics, and regulatory compliance.
            
            ═══════════════════════════════════════════════════════════════
            📅 CURRENT DATE & TIME CONTEXT
            ═══════════════════════════════════════════════════════════════
            Today is: {time_context['full_datetime']}
            Day: {time_context['day_of_week']}
            Week: {time_context['week_number']} of {time_context['year']}
            Quarter: {time_context['quarter']}
            Business Hours: {time_context['business_status']}
            
            USE THIS DATE FOR:
            - Calculating lead times and delivery dates
            - Determining shipping schedules (exclude weekends if needed)
            - Checking if tariffs/regulations are current
            - Estimating arrival dates based on transit times
            - Any date-related calculations
            
            ═══════════════════════════════════════════════════════════════
            📊 CONTEXT 1: PRODUCT & PRICING DATA (Excel)
            ═══════════════════════════════════════════════════════════════
            {state['context_text']}
            
            ═══════════════════════════════════════════════════════════════
            📄 CONTEXT 2: ATTACHED PDF DOCUMENTS
            ═══════════════════════════════════════════════════════════════
            (See attached files for Shipping Tariffs and Compliance Guide)
            
            ═══════════════════════════════════════════════════════════════
            ❓ USER QUESTION
            ═══════════════════════════════════════════════════════════════
            {state['question']}
            
            ═══════════════════════════════════════════════════════════════
            📋 RESPONSE INSTRUCTIONS
            ═══════════════════════════════════════════════════════════════
            1. Answer precisely using the provided data
            2. For lead times: Calculate actual delivery dates from TODAY ({time_context['date']})
            3. For shipping: Consider business days only (Mon-Fri)
            4. Show your calculations step-by-step
            5. Cite specific sources (sheet names, PDF sections)
            
            Output format (JSON):
            {{
                "answer": "The direct answer to the user's question. If calculating dates, show the actual calendar date.",
                "explanation": "Step-by-step explanation. For date calculations, show: Today ({time_context['date']}) + X days = [calculated date]",
                "citations": ["Sheet Name or PDF Section"],
                "confidence": 0.95,
                "timestamp": "{time_context['full_datetime']}"
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

# --- 6. RUNNER ---
if __name__ == "__main__":
    # Show current time context
    print("\n🕐 Current Time Context:")
    ctx = get_business_context()
    for key, value in ctx.items():
        print(f"   {key}: {value}")
    
    # 1. Prepare Data
    kb_data = prepare_knowledge_base()
    
    # 2. Build Graph
    workflow = StateGraph(DistribIQState)
    workflow.add_node("solver", solver_agent)
    workflow.set_entry_point("solver")
    workflow.add_edge("solver", END)
    app = workflow.compile()
    
    # 3. Ask Question (S001)
    if kb_data["excel_text"] or kb_data["pdf_handles"]:
        print("\n🚀 Running DistribIQ with Time Awareness...")
        result = app.invoke({
            "question_id": "S001",
            "question": "What is the lead time for Citric Acid from Jungbunzlauer? When would it arrive if I order today?",
            "context_files": kb_data["pdf_handles"],
            "context_text": kb_data["excel_text"]
        })
        
        print("\n📢 ANSWER:")
        print(json.dumps(result["final_answer"], indent=2))
    else:
        print("\n🛑 STOPPING: No data found.")