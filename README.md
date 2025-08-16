# 🛡️ AI Data Governance Copilot

An AI-powered copilot that helps **data teams** manage governance with ease using **RAG, LangChain, and AI agents**.  
Built for **conversational compliance checks, lineage tracing, and policy search**.

---

## 🚀 Features
- Conversational Q&A over **GDPR & internal policies**  
- Detect datasets with **PII, missing encryption, or retention violations**  
- **Lineage explorer** to trace dataset dependencies  
- Auto-generate **compliance reports** (CSV/interactive)  
- Extendable with **LangChain agent tools**  

---

## 🛠️ Tech Stack
- **Python, Pandas, NetworkX, Streamlit**  
- **LangChain + OpenAI (optional agent orchestration)**  
- **RAG pipeline** with TF-IDF retriever (pluggable with FAISS/Pinecone)  

---

## ⚡ Quick Start
```bash
git clone https://github.com/am-aslam/atlan-ai-governance-copilot.git
cd atlan-ai-governance-copilot
pip install -r requirements.txt

# Run CLI Copilot
python app/copilot.py

# Or launch Streamlit UI
streamlit run app/streamlit_app.py
