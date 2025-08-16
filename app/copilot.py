import os, sys, re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils import load_data, pii_columns, build_lineage_graph, find_lineage_paths, compliance_checks

BASE = os.path.dirname(os.path.dirname(__file__))

def load_corpus():
    docs = []
    paths = [
        f"{BASE}/data/policies/gdpr.md",
        f"{BASE}/data/policies/internal_policy.md",
        f"{BASE}/data/raw_docs/data_dictionary.md",
    ]
    for p in paths:
        with open(p, "r", encoding="utf-8") as f:
            docs.append(f.read())
    return docs, paths

def retrieve_snippets(query, docs, top_k=2):
    vect = TfidfVectorizer(stop_words="english")
    X = vect.fit_transform(docs + [query])
    sims = cosine_similarity(X[-1], X[:-1]).flatten()
    idxs = sims.argsort()[::-1][:top_k]
    return [(i, sims[i]) for i in idxs]

def handle_pii_not_encrypted(datasets):
    df = datasets.query("has_pii == True")
    df = df[df["encryption"].str.upper().isin(["NONE", "NULL", "NA"])]
    return df

def handle_lineage(graph, dataset):
    if dataset not in graph.nodes:
        return f"No lineage info for {dataset}."
    paths = find_lineage_paths(graph, dataset)
    if not paths:
        return f"No upstream lineage paths found for {dataset}."
    return "\n".join(" -> ".join(p) for p in paths)

def handle_report(datasets, columns, audits):
    comp = compliance_checks(datasets, columns, audits)
    return comp

def main():
    datasets, columns, lineage, audits = load_data(BASE)
    graph = build_lineage_graph(lineage)
    docs, paths = load_corpus()

    print("AI Data Governance Copilot (CLI)")
    print("Type a question, or 'exit' to quit.")
    print("Examples:")
    print("- Which datasets contain PII and are not encrypted?")
    print("- Trace the lineage of customer_profiles")
    print("- Generate a GDPR compliance report")
    print("- What does GDPR say about retention?")
    print()

    while True:
        q = input("You: ").strip()
        if q.lower() in ["exit", "quit"]:
            break

        q_low = q.lower()

        if "pii" in q_low and ("not encrypted" in q_low or "without encryption" in q_low):
            df = handle_pii_not_encrypted(datasets)
            if df.empty:
                print("Bot: All PII datasets have encryption configured.")
            else:
                print("Bot: Datasets with PII and no encryption:")
                print(df[["name","system","owner","domain","encryption"]].to_string(index=False))
            continue

        m = re.search(r"lineage of ([a-zA-Z0-9_]+)", q_low)
        if m:
            ds = m.group(1)
            print("Bot: Upstream lineage paths:")
            print(handle_lineage(graph, ds))
            continue

        if "generate" in q_low and "report" in q_low:
            comp = handle_report(datasets, columns, audits)
            out_path = os.path.join(BASE, "data", "compliance_report.csv")
            comp.to_csv(out_path, index=False)
            print(f"Bot: Generated compliance report at {out_path}")
            print(comp.to_string(index=False))
            continue

        # Default: retrieve relevant policy/document snippets
        hits = retrieve_snippets(q, docs, top_k=2)
        answer = []
        for (i, score) in hits:
            answer.append(f"[{os.path.basename(paths[i])}] (score={score:.2f})\n" + docs[i].splitlines()[0:15][0])
        print("Bot: Here are relevant snippets to answer your question:")
        print("\n---\n".join(answer))

if __name__ == "__main__":
    main()