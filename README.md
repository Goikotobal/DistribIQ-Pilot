# 🧬 DistribIQ: AI Decision Support System

**DistribIQ** is an agentic AI pilot designed to assist Barentz teams with complex supply chain, regulatory, and pricing decisions. 

It leverages a **Hybrid Retrieval Architecture**:
* **Excel Logic:** Parses structured Master Data (Pricing, Lead Times).
* **PDF Analysis:** Interprets unstructured Regulatory Guides & Shipping Tariffs.
* **Reasoning Engine:** Uses Chain-of-Thought (CoT) to explain calculations.

---

## 🏗 Architecture

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Brain** | Google Gemini 2.5 Flash | Long-context reasoning & synthesis. |
| **Orchestrator** | LangGraph | Managing state & agent workflow. |
| **Interface** | Streamlit | Interactive chat UI for end-users. |
| **Data Layer** | Pandas + Native File API | Hybrid structured/unstructured ingestion. |

## 🚀 Quick Start

### Prerequisites
* Python 3.10+
* Google AI Studio API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/DistribIQ-Pilot.git](https://github.com/YourUsername/DistribIQ-Pilot.git)
    cd DistribIQ-Pilot
    ```

2.  **Set up the environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configure Credentials:**
    Create a `.env` file in the root directory:
    ```text
    GOOGLE_API_KEY=your_api_key_here
    ```

4.  **Run the Application:**
    ```bash
    streamlit run src/app.py
    ```

---

## 🔒 Security & Deployment

### Cloud Pilot (Current)
* **Hosting:** Streamlit Community Cloud (Secure Enclave).
* **Data Processing:** Google Vertex AI / Gemini API.
* **Access:** Password-protected via Streamlit Secrets.

### On-Premises Production (Roadmap)
For air-gapped requirements, this architecture supports swapping the **Gemini** model for local open-source models (e.g., **Llama 3** running on Ollama) to ensure zero data egress.

---

## 📂 Project Structure

```text
DistribIQ/
├── src/                # Source Code
│   ├── agent.py        # Logic Core (The "Brain")
│   └── app.py          # User Interface
├── tests/              # Validation Scripts
├── data/               # Knowledge Base (Excel/PDFs)
└── .streamlit/         # UI Configuration