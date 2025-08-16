# AI Data Governance Copilot (RAG + LangChain + Agents)

This project provides a portfolio-ready **AI copilot** for data governance use-cases:
- Conversational search over **policies, metadata, and lineage**
- **Compliance checks** for PII (encryption, retention, consent)
- **Lineage tracing** between datasets
- **Report generation** (text/CSV)

## Project Structure
```
atlan_ai_governance_copilot/
├── app/
│   ├── copilot.py               # CLI copilot (no API keys needed)
│   ├── streamlit_app.py         # UI (optional)
│   ├── langchain_agent_stub.py  # Agent wiring example (needs OpenAI key)
│   └── utils.py                 # Shared utils
├── data/
│   ├── datasets.csv
│   ├── columns.csv
│   ├── lineage.csv
│   ├── audits.csv
│   └── policies/
│       ├── gdpr.md
│       └── internal_policy.md
├── notebooks/
│   └── exploration.ipynb        # EDA + examples
└── README.md
```

## Quick Start (CLI)
```bash
pip install pandas networkx scikit-learn python-dateutil
python app/copilot.py
```
Then try questions like:
- "Which datasets contain PII and are not encrypted?"
- "Generate a GDPR compliance report for marketing and customer domains."
- "Trace the lineage of customer_profiles."
- "Show datasets violating internal retention policy."
- "What does GDPR say about retention?"

## Streamlit UI
```bash
pip install streamlit pandas networkx scikit-learn python-dateutil
streamlit run app/streamlit_app.py
```

## LangChain Agent (Optional)
See **app/langchain_agent_stub.py** for a reference agent with tools:
- `search_policies`
- `check_compliance`
- `trace_lineage`
- `summarize_report`

> Requires: `pip install langchain openai` and an `OPENAI_API_KEY`.

## Notes
- The sample data is synthetic but realistic.
- Extend by connecting to real metadata catalogs (AWS Glue, Snowflake), vector DBs, and auth.