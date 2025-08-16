import streamlit as st
import pandas as pd
from utils import load_data, build_lineage_graph, find_lineage_paths, compliance_checks

BASE = "."

st.set_page_config(page_title="AI Data Governance Copilot", layout="wide")

datasets, columns, lineage, audits = load_data(BASE)
graph = build_lineage_graph(lineage)

st.title("🛡️ AI Data Governance Copilot")

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Compliance", "Lineage", "Search"])

with tab1:
    st.subheader("Datasets")
    st.dataframe(datasets)

with tab2:
    st.subheader("Compliance Report")
    comp = compliance_checks(datasets, columns, audits)
    st.dataframe(comp)
    viol = comp[(comp['encryption_required'] & ~comp['encrypted']) | (comp['retention_violation']) | (~comp['gdpr_ok'])]
    st.markdown("**Violations:**")
    st.dataframe(viol)

with tab3:
    st.subheader("Lineage Explorer")
    ds = st.selectbox("Select target dataset", datasets['name'].tolist())
    paths = find_lineage_paths(graph, ds)
    if not paths:
        st.info("No upstream paths found.")
    else:
        for p in paths:
            st.write(" ➜ ".join(p))

with tab4:
    st.subheader("Policy & Doc Search (keyword-based demo)")
    query = st.text_input("Ask about GDPR/internal policy (e.g., 'What does GDPR say about retention?')")
    if st.button("Search") and query:
        st.write("See CLI version for snippet retrieval demo (TF-IDF).")
        st.caption("For production, plug in vector DB + embeddings.")