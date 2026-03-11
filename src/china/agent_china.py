import os
import json
import time
from datetime import datetime
import pytz  # [OK] NEW: For timezone support
from typing import TypedDict, List, Any
from openai import OpenAI  # [OK] CHANGED: Using OpenAI SDK for Qwen
import PyPDF2  # [OK] NEW: For PDF text extraction
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import pandas as pd

# --- 1. CONFIGURATION ---
# Load environment variables from .env.china file using absolute path
# Get the directory where this script lives
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up two levels to project root, then find .env.china
env_path = os.path.join(current_script_dir, "..", "..", ".env.china")
env_path = os.path.abspath(env_path)

print(f"[DEBUG] Looking for .env.china at: {env_path}")
print(f"[DEBUG] File exists: {os.path.exists(env_path)}")

load_dotenv(env_path)

# [OK] CHANGED: Using Qwen API configuration
QWEN_API_KEY = os.environ.get("QWEN_API_KEY")
QWEN_BASE_URL = os.environ.get("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
QWEN_MODEL = os.environ.get("QWEN_MODEL", "qwen-plus")  # Changed to qwen-plus for faster responses

# Debug: Print first 8 chars of API key to verify it's loaded
if QWEN_API_KEY:
    print(f"[DEBUG] QWEN_API_KEY loaded: {QWEN_API_KEY[:8]}...")
else:
    print("[DEBUG] QWEN_API_KEY: None")

# [OK] NEW: Timezone configuration (change to your preferred timezone)
TIMEZONE = os.environ.get("TIMEZONE", "Asia/Shanghai")  # Default to China timezone

if QWEN_API_KEY:
    # Add 120 second timeout for API calls to handle large contexts
    client = OpenAI(api_key=QWEN_API_KEY, base_url=QWEN_BASE_URL, timeout=120.0)
else:
    client = None
    print("[WARNING] No API Key found. Running in MOCK MODE.")

# --- 2. STATE DEFINITION ---
class DistribIQState(TypedDict):
    question_id: str
    question: str
    context_text: str           # Combined text content for Excel and PDFs
    final_answer: dict

# --- 3. DATE/TIME HELPER FUNCTIONS --- [OK] SAME AS ORIGINAL
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

    # Determine business hours (assuming 8:00-18:00 local time)
    hour = int(datetime.now(pytz.timezone(TIMEZONE)).strftime("%H"))
    is_business_hours = 8 <= hour < 18 and not dt["is_weekend"]

    return {
        **dt,
        "is_business_hours": is_business_hours,
        "business_status": "Open" if is_business_hours else "Closed",
        "note": "Consider next business day for responses if outside business hours"
    }

# --- 4. PDF TEXT EXTRACTION --- [OK] NEW FUNCTION
def extract_pdf_text(pdf_path):
    """
    Extracts text from a PDF file using PyPDF2.
    """
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages):
                text += f"\n--- PAGE {page_num + 1} ---\n"
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"   [ERROR] Error extracting PDF text: {e}")
        return ""

# --- 5. THE FILE LOADER --- [OK] MODIFIED FOR PDF TEXT EXTRACTION
def prepare_knowledge_base():
    """
    Reads Excel locally (converting to markdown) and extracts text from PDFs.
    """

    # [OK] PATH LOGIC:
    # Get the folder where THIS script (agent_china.py) lives
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two levels (.., ..), then down into data/docs
    base_folder = os.path.join(current_dir, "..", "..", "data", "docs")

    # Files to look for
    excel_file = "DM_Report_MASTER_Generic.xlsx"
    pdf_files = [
        "Shipping_Tariffs_EMEA_Generic.pdf",
        "Regulatory_Compliance_Guide_Generic.pdf"
    ]

    knowledge_context = {
        "pdf_text": "",
        "excel_text": ""
    }

    print(f"[INFO] Preparing Knowledge Base from: {base_folder}")

    # Verify folder exists
    if not os.path.exists(base_folder):
        print(f"[ERROR] ERROR: Folder '{base_folder}' not found.")
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
            print(f"   [OK] Excel processed")
        except Exception as e:
            print(f"   [ERROR] Excel Error: {e}")

    # --- PART B: EXTRACT PDF TEXT --- [OK] CHANGED FROM UPLOAD TO EXTRACTION
    pdf_text_combined = ""
    for filename in pdf_files:
        full_path = os.path.join(base_folder, filename)
        if os.path.exists(full_path):
            print(f"   [INFO] Extracting text from: {filename}")
            pdf_text = extract_pdf_text(full_path)
            if pdf_text:
                pdf_text_combined += f"\n\n=== PDF SOURCE: {filename} ===\n{pdf_text}\n"
                print(f"   [OK] PDF processed: {filename}")

    knowledge_context["pdf_text"] = pdf_text_combined

    return knowledge_context

# --- 6. THE AGENT (Updated for Qwen-Max) --- [OK] MODIFIED FOR OPENAI API
def solver_agent(state: DistribIQState):
    print(f"\n[PROCESSING] [DistribIQ-China] Thinking about: {state['question']}...")

    # [OK] SAME: Get current date/time context
    time_context = get_business_context()

    try:
        if not client:
            raise Exception("No Qwen API client configured")

        # Truncate context to prevent timeout (max 8000 characters)
        context_text = state['context_text']
        if len(context_text) > 8000:
            context_text = context_text[:8000] + "\n\n[... context truncated for size ...]"
            print(f"   [INFO] Context truncated from {len(state['context_text'])} to 8000 chars")

        # [OK] SAME PROMPT STRUCTURE, just combined into single string
        prompt = f"""
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
{context_text}

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

        # [OK] CHANGED: Using OpenAI chat completions API with streaming
        stream = client.chat.completions.create(
            model=QWEN_MODEL,
            messages=[
                {"role": "system", "content": "You are DistribIQ, an expert supply chain AI assistant. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            stream=True
        )

        # Collect the streamed response
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content

        # [OK] CHANGED: Parse OpenAI response format
        state["final_answer"] = json.loads(full_response)

    except Exception as e:
        print(f"   [ERROR] AI Error: {e}")
        state["final_answer"] = {"error": str(e)}

    return state

# --- 7. RUNNER ---
if __name__ == "__main__":
    # Show current time context
    print("\n[INFO] Current Time Context:")
    ctx = get_business_context()
    for key, value in ctx.items():
        print(f"   {key}: {value}")

    # 1. Prepare Data
    kb_data = prepare_knowledge_base()

    # 2. Build Graph ([OK] SAME AS ORIGINAL - LangGraph unchanged)
    workflow = StateGraph(DistribIQState)
    workflow.add_node("solver", solver_agent)
    workflow.set_entry_point("solver")
    workflow.add_edge("solver", END)
    app = workflow.compile()

    # 3. Ask Question (S001)
    if kb_data["excel_text"] or kb_data["pdf_text"]:
        print("\n[INFO] Running DistribIQ-China with Qwen-Plus...")
        # [OK] CHANGED: Combine excel_text and pdf_text into context_text
        combined_context = kb_data["excel_text"] + "\n\n" + kb_data["pdf_text"]

        result = app.invoke({
            "question_id": "S001",
            "question": "What is the lead time for Citric Acid from Jungbunzlauer? When would it arrive if I order today?",
            "context_text": combined_context
        })

        print("\n[ANSWER]:")
        print(json.dumps(result["final_answer"], indent=2))
    else:
        print("\n[STOPPING] No data found.")
