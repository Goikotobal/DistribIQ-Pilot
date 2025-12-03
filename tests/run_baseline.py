import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
import sys

# ✅ NEW IMPORT LOGIC
# Add the parent directory to the path so we can see 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agent import prepare_knowledge_base, solver_agent

# --- SETUP ---
load_dotenv()
OUTPUT_FILE = "distribiq_baseline_accuracy.json"

def run_tests():
    print("🚀 STARTING BASELINE TEST RUN (20 QUESTIONS)...")
    
    # 1. Load the Knowledge Base ONCE (Efficiency!)
    print("\n📦 Pre-loading Knowledge Base (PDFs + Excel)...")
    kb_data = prepare_knowledge_base()
    
    if not kb_data["excel_text"] and not kb_data["pdf_handles"]:
        print("❌ CRITICAL: No data found. Stopping test.")
        return

    # 2. Load the Questions (Golden Dataset)
    # We read the same Excel file, but specifically the "Decision Scenarios" sheet
    # ... inside run_tests() ...

    # ✅ ROBUST PATH FIX:
    # 1. Get the folder where THIS script (run_baseline.py) lives
    test_dir = os.path.dirname(os.path.abspath(__file__))
    # 2. Go UP one level to project root, then DOWN into data/docs
    project_root = os.path.abspath(os.path.join(test_dir, ".."))
    dataset_path = os.path.join(project_root, "data", "docs", "DM_Report_MASTER_Complete.xlsx")
    
    print(f"📋 Loading questions from: {dataset_path}...")
    
    try:
        df = pd.read_excel(dataset_path, sheet_name="Decision Scenarios")
        # Filter for the first 20 scenarios just in case
        questions = df.head(20).to_dict('records')
    except Exception as e:
        print(f"❌ Error loading questions: {e}")
        return

    results = []
    total_start_time = time.time()

    # 3. The Loop
    for i, row in enumerate(questions):
        q_id = row.get("Scenario ID", f"Q{i}")
        q_text = row.get("Question / Request", "Unknown Question")
        
        print(f"\n[{i+1}/20] Testing {q_id}: {q_text[:50]}...")
        
        start_time = time.time()
        
        # --- RUN THE AGENT ---
        # We manually invoke the solver_agent logic here
        state = {
            "question_id": q_id,
            "question": q_text,
            "context_files": kb_data["pdf_handles"],
            "context_text": kb_data["excel_text"],
            "final_answer": {}
        }
        
        try:
            # Invoke the agent function directly
            result_state = solver_agent(state)
            final = result_state["final_answer"]
        except Exception as e:
            final = {"answer": "Error", "error": str(e)}
            
        duration = round(time.time() - start_time, 2)
        print(f"   ✅ Done in {duration}s")
        
        # 4. Capture Result
        result_entry = {
            "question_id": q_id,
            "question": q_text,
            "generated_answer": final.get("answer", "No answer generated"),
            "confidence": final.get("confidence", 0.0),
            "citations": final.get("citations", []),
            "response_time_sec": duration,
            "status": "PASS" if final.get("confidence", 0) > 0.7 else "REVIEW"
        }
        results.append(result_entry)

    # 4. Generate Report
    total_time = round(time.time() - total_start_time, 2)
    avg_time = round(total_time / len(results), 2)
    
    report = {
        "meta": {
            "total_questions": len(results),
            "total_time_sec": total_time,
            "avg_time_per_query": avg_time,
            "model": "gemini-2.5-flash"
        },
        "results": results
    }
    
    # 5. Save to JSON
    with open(OUTPUT_FILE, "w") as f:
        json.dump(report, f, indent=2)
        
    print(f"\n🎉 TESTS COMPLETED!")
    print(f"📄 Report saved to: {OUTPUT_FILE}")
    print(f"⏱️  Average Speed: {avg_time}s per query")

if __name__ == "__main__":
    run_tests()