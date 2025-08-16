import pandas as pd
import datetime as dt
import networkx as nx
from dateutil import parser

def load_data(base_path):
    ds = pd.read_csv(f"{base_path}/data/datasets.csv", parse_dates=["last_audit_date"])
    cols = pd.read_csv(f"{base_path}/data/columns.csv")
    lin = pd.read_csv(f"{base_path}/data/lineage.csv")
    audits = pd.read_csv(f"{base_path}/data/audits.csv")
    return ds, cols, lin, audits

def pii_columns(cols_df, dataset_name):
    return cols_df[cols_df["dataset"]==dataset_name].query("pii_type != 'none'")

def build_lineage_graph(lin_df):
    g = nx.DiGraph()
    for _, r in lin_df.iterrows():
        g.add_edge(r["source"], r["target"], transformation=r.get("transformation",""))
    return g

def find_lineage_paths(g, target):
    paths = []
    for src in g.nodes:
        if src == target: 
            continue
        if nx.has_path(g, src, target):
            for p in nx.all_simple_paths(g, src, target):
                paths.append(p)
    return paths

def retention_violation(row):
    # Simple rules mirroring internal_policy.md
    if row["domain"] == "marketing" and row["retention_days"] > 90:
        return True, "Marketing data retained > 90 days"
    if row["name"] == "customer_profiles" and row["retention_days"] > 365:
        return True, "Customer profiles retained > 365 days"
    return False, ""

def encryption_required(row):
    return bool(row["has_pii"])

def encrypted(row):
    return str(row["encryption"]).upper() not in ["", "NONE", "NULL", "NA"]

def compliance_checks(datasets, columns, audits):
    results = []
    for _, r in datasets.iterrows():
        req_enc = encryption_required(r)
        is_enc = encrypted(r)
        has_pii = bool(r["has_pii"])
        viol_ret, reason_ret = retention_violation(r)

        audit_row = audits[audits["dataset"]==r["name"]]
        gdpr_ok = bool(audit_row["gdpr_ok"].iloc[0]) if not audit_row.empty else None
        remarks = str(audit_row["remarks"].iloc[0]) if not audit_row.empty else ""

        results.append({
            "dataset": r["name"],
            "domain": r["domain"],
            "has_pii": has_pii,
            "encryption_required": req_enc,
            "encrypted": is_enc,
            "retention_days": int(r["retention_days"]),
            "retention_violation": viol_ret,
            "retention_reason": reason_ret,
            "gdpr_ok": gdpr_ok,
            "audit_remarks": remarks
        })
    return pd.DataFrame(results)