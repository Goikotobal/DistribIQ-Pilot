# DistribIQ: AI-Powered Ingredient Distribution System
## Using Gemini File Search + Agentic Framework

---

## PROJECT OVERVIEW

I'm building **DistribIQ**, an AI decision support system for Barentz (pharmaceutical/food ingredient distributor). This is a **parallel implementation** to compare:

- **ProvAI** (Custom RAG: LangChain + ChromaDB + Claude Sonnet 4)
- **DistribIQ** (Managed Service: Gemini File Search + Agentic AI)

**Goal:** Same functionality, different approach, then compare costs/accuracy/speed.

---

## WHAT I NEED YOU TO BUILD

A complete system that:

1. **Ingests 3 files** (Excel + 2 PDFs) using Gemini File Search API
2. **Answers 20 test questions** from the golden dataset
3. **Orchestrates multi-step queries** using an agentic framework
4. **Generates answers with citations** and confidence scores
5. **Rejects out-of-scope queries** (not about Barentz)
6. **Measures accuracy** against expected answers

---

## DATA FILES (I'll upload these)

### 1. **DM_Report_MASTER_Complete.xlsx** (7 sheets)
- Sheet 1: Product Master Data (20 products: Citric Acid, Sodium Benzoate, etc.)
- Sheet 2: Quality Requirements (certifications, testing specs)
- Sheet 3: Compliance Matrix (EU/USA regulations)
- Sheet 4: Logistics Matrix (shipping routes, transit times)
- Sheet 5: Pricing Tiers (spot/volume/contract pricing)
- Sheet 6: Decision Scenarios (20 test questions) ← **Golden Dataset**
- Sheet 7: Business Rules (validation logic)

### 2. **Shipping_Tariffs_EMEA_2024.pdf**
- Road transport rates (intra-EU)
- Air freight rates (inter-continental)
- Sea freight rates (FCL)
- Additional surcharges (temp control, hazmat, etc.)

### 3. **Regulatory_Compliance_Guide_EU_USA.pdf**
- EU regulations (Food Additives EC 1333/2008, REACH, Pharma)
- USA regulations (FDA CFR, GRAS status, DMF requirements)
- Compliance comparison tables

---

## GOLDEN DATASET (20 Test Questions)

Located in Excel Sheet 6. Examples:

**Simple (should be 100% accurate):**
- S001: "What is the lead time for Citric Acid?"
- S002: "What certifications does Sodium Benzoate have?"
- S003: "What is the shipping rate from Netherlands to Germany?"

**Medium (should be 80-90% accurate):**
- S005: "Calculate total cost for 5000kg Citric Acid delivered to Netherlands"
- S008: "What are EU compliance requirements for pharma-grade ingredients?"
- S011: "Compare lead times for Xanthan Gum vs MCC"

**Complex (should be 70-80% accurate):**
- S015: "Find pharma-grade preservative with Kosher cert, available in 3 weeks, shippable to Germany"
- S018: "Fastest delivery for 1500kg Xanthan Gum to Netherlands with total cost?"
- S020: "Which products require temperature-controlled shipping and what's the cost impact?"

---

## ARCHITECTURE REQUIREMENTS

### **Option A: Gemini File Search Only (Simplest)**
```python
# 1. Upload files to Gemini
# 2. Use File Search API for each question
# 3. Parse answers and calculate confidence
# 4. Compare against golden dataset
```

**Pros:** Simplest implementation, fastest time-to-market
**Cons:** Less control over retrieval/ranking

### **Option B: Gemini + LangGraph (Agentic) - RECOMMENDED**
```python
# Multi-agent workflow:
# 1. Query Analysis Agent (categorize question)
# 2. Retrieval Agent (Gemini File Search)
# 3. Synthesis Agent (multi-doc reasoning)
# 4. Validation Agent (confidence scoring)
# 5. Citation Agent (source attribution)
```

**Pros:** Better for complex queries, explainable reasoning
**Cons:** More implementation complexity

### **Option C: Gemini + LangChain Agent (Alternative)**
```python
# Use LangChain's Agent framework:
# - Tools: Gemini File Search, Calculator, etc.
# - Agent: ReAct pattern for reasoning
# - Memory: Conversation history
```

**Pros:** Proven framework, good documentation
**Cons:** May be overkill for this use case

---

## SYSTEM REQUIREMENTS

### **1. Out-of-Scope Detection**
Reject queries NOT about:
- Barentz products/pricing
- Compliance/regulations
- Logistics/shipping
- Suppliers/quality

**Example rejections:**
- "What's the weather?" → Reject
- "How do I cook pasta?" → Reject
- "Tell me a joke" → Reject

### **2. Confidence Scoring**
Return confidence 0.0-1.0 based on:
- Retrieval quality (how relevant were the documents?)
- Answer completeness (did we find all needed info?)
- Source diversity (multiple sources agree?)

### **3. Source Citations**
Always cite which file/sheet/section the answer came from:
- "According to Sheet 1 (Product Master), lead time is 2-3 weeks"
- "Based on Shipping Tariffs PDF page 1, rate is €0.12/kg"

### **4. Multi-Step Reasoning**
For complex queries, break down into steps:
1. Find product specs
2. Get pricing
3. Get shipping cost
4. Calculate total
5. Format answer

---

## EXPECTED OUTPUT

### **For Each Question:**
```python
{
  "question_id": "S001",
  "question": "What is the lead time for Citric Acid?",
  "answer": "The lead time for Citric Acid is 2-3 weeks from order confirmation.",
  "confidence": 0.92,
  "sources": [
    {
      "file": "DM_Report_MASTER_Complete.xlsx",
      "sheet": "Product Master Data",
      "relevance": 0.95
    }
  ],
  "response_time": 2.3,
  "reasoning_steps": [
    "1. Identified product: Citric Acid",
    "2. Located in Product Master sheet",
    "3. Extracted lead time field"
  ]
}
```

### **Accuracy Report:**
```python
{
  "total_questions": 20,
  "passed": 18,
  "failed": 2,
  "accuracy": 90.0,
  "avg_confidence": 0.85,
  "avg_response_time": 3.2,
  "by_complexity": {
    "simple": {"accuracy": 100, "count": 7},
    "medium": {"accuracy": 87.5, "count": 8},
    "complex": {"accuracy": 80.0, "count": 5}
  }
}
```

---

## COST TRACKING

Track and report:
- **File upload cost** (one-time)
- **Per-query cost** (Gemini API calls)
- **Total cost** for 20 questions
- **Projected cost** for 1000 users × 20 queries/day

Compare with ProvAI:
- ProvAI: ~$0.0135/query (Claude Sonnet 4)
- DistribIQ: ~$? (Gemini File Search)

---

## DELIVERABLES

### **Code:**
1. `distribiq_system.py` - Main system
2. `test_distribiq.py` - Testing script
3. `requirements.txt` - Dependencies
4. `README.md` - Setup instructions

### **Reports:**
1. `distribiq_baseline_accuracy.json` - Test results
2. `distribiq_baseline_accuracy.csv` - Summary table
3. `distribiq_cost_analysis.json` - Cost breakdown
4. `comparison_report.md` - ProvAI vs DistribIQ

---

## COMPARISON METRICS

Generate comparison:

| Metric | ProvAI (Custom) | DistribIQ (Managed) |
|--------|----------------|---------------------|
| **Setup Time** | 2 days | ? hours |
| **Accuracy** | 90% | ?% |
| **Avg Response Time** | 3.5s | ?s |
| **Cost per Query** | $0.0135 | $? |
| **Cost (20 queries)** | $0.27 | $? |
| **Annual Cost (7.3M queries)** | $98,600 | $? |
| **Customization** | High | Low |
| **Control** | Full | Limited |

---

## TECHNICAL APPROACH

### **Recommended: Gemini + LangGraph**
```python
from langgraph.graph import StateGraph, END
from google import generativeai as genai

class DistribIQState(TypedDict):
    question: str
    question_category: str
    search_results: List[Dict]
    synthesized_answer: str
    confidence: float
    sources: List[Dict]

class DistribIQWorkflow:
    def __init__(self):
        self.workflow = self._create_workflow()
        # Upload files to Gemini
        self.file_ids = self._upload_files()
    
    def _create_workflow(self):
        workflow = StateGraph(DistribIQState)
        
        # Add nodes
        workflow.add_node("analyze_question", self.analyze_question)
        workflow.add_node("search_files", self.search_with_gemini)
        workflow.add_node("synthesize", self.synthesize_answer)
        workflow.add_node("validate", self.calculate_confidence)
        
        # Define flow
        workflow.set_entry_point("analyze_question")
        workflow.add_edge("analyze_question", "search_files")
        workflow.add_edge("search_files", "synthesize")
        workflow.add_edge("synthesize", "validate")
        workflow.add_edge("validate", END)
        
        return workflow.compile()
    
    def _upload_files(self):
        # Upload to Gemini File API
        excel_file = genai.upload_file("DM_Report_MASTER_Complete.xlsx")
        pdf1_file = genai.upload_file("Shipping_Tariffs_EMEA_2024.pdf")
        pdf2_file = genai.upload_file("Regulatory_Compliance_Guide_EU_USA.pdf")
        return [excel_file, pdf1_file, pdf2_file]
    
    def search_with_gemini(self, state):
        # Use Gemini File Search
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        Question: {state['question']}
        
        Search the uploaded files and provide:
        1. Direct answer to the question
        2. Which file(s) and sections you used
        3. Confidence in the answer (0-1)
        """
        response = model.generate_content([
            prompt,
            *self.file_ids
        ])
        return state
```

---

## QUESTIONS FOR YOU (Gemini)

1. **Framework choice:** Should I use LangGraph, LangChain Agent, or pure Gemini API?
2. **File handling:** What's the best way to upload Excel + PDFs to Gemini File Search?
3. **Structured output:** Can Gemini return JSON for programmatic parsing?
4. **Cost optimization:** How to minimize API calls while maintaining accuracy?
5. **Multi-step reasoning:** How to implement chain-of-thought for complex queries?

---

## SUCCESS CRITERIA

- [ ] All 3 files uploaded successfully
- [ ] 20 test questions answered
- [ ] Accuracy ≥ 85% overall
- [ ] Response time < 5 seconds average
- [ ] Out-of-scope queries rejected correctly
- [ ] Source citations provided for all answers
- [ ] Cost tracking implemented
- [ ] Comparison report generated

---

## NEXT STEPS

1. **You build** the DistribIQ system
2. **I upload** the 3 data files
3. **We run** the 20 test questions
4. **We compare** ProvAI vs DistribIQ
5. **We present** both options to client (Barentz)

---

Let's build DistribIQ and see how it compares to ProvAI! 🚀