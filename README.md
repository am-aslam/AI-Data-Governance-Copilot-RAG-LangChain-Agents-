# Create project structure and files for "AI Data Governance Copilot (RAG + LangChain + Agents)"
import os, json, textwrap, zipfile, pandas as pd, datetime as dt, networkx as nx

base = "/mnt/data/atlan_ai_governance_copilot"
dirs = [
    f"{base}/data/policies",
    f"{base}/data/raw_docs",
    f"{base}/app",
    f"{base}/notebooks",
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

# -----------------------
# 1) Create sample datasets
# -----------------------

datasets_csv = pd.DataFrame([
    # name, system, owner, domain, has_pii, encryption, retention_days, last_audit_date, classification
    ["customer_profiles", "postgres_prod", "data.stewards@acme.com", "customer", True, "AES256", 365, "2025-07-10", "confidential"],
    ["customer_events", "s3_lake", "analytics@acme.com", "customer", True, "NONE", 180, "2025-06-28", "restricted"],
    ["orders", "snowflake_wh", "finance@acme.com", "finance", False, "AES256", 730, "2025-05-18", "internal"],
    ["payments", "snowflake_wh", "finance@acme.com", "finance", True, "AES256", 1095, "2025-05-18", "confidential"],
    ["marketing_leads", "bigquery_mkt", "growth@acme.com", "marketing", True, "KMS_MANAGED", 90, "2025-04-30", "restricted"],
    ["product_catalog", "postgres_prod", "catalog@acme.com", "product", False, "AES256", 1825, "2025-03-11", "public"],
    ["support_tickets", "s3_lake", "support@acme.com", "support", True, "AES256", 365, "2025-07-01", "confidential"],
    ["web_analytics", "bigquery_mkt", "growth@acme.com", "marketing", False, "KMS_MANAGED", 365, "2025-06-01", "internal"],
], columns=["name","system","owner","domain","has_pii","encryption","retention_days","last_audit_date","classification"])

columns_csv = pd.DataFrame([
    # dataset, column, data_type, pii_type
    ["customer_profiles","customer_id","uuid","none"],
    ["customer_profiles","full_name","string","name"],
    ["customer_profiles","email","string","email"],
    ["customer_profiles","phone","string","phone"],
    ["customer_profiles","dob","date","dob"],
    ["customer_profiles","address","string","address"],
    ["customer_events","event_id","string","none"],
    ["customer_events","customer_id","uuid","none"],
    ["customer_events","event_type","string","none"],
    ["customer_events","ip_address","string","ip"],
    ["orders","order_id","string","none"],
    ["orders","customer_id","uuid","none"],
    ["orders","amount","decimal","none"],
    ["payments","payment_id","string","none"],
    ["payments","card_last4","string","financial"],
    ["payments","billing_email","string","email"],
    ["marketing_leads","lead_id","string","none"],
    ["marketing_leads","email","string","email"],
    ["marketing_leads","phone","string","phone"],
    ["product_catalog","sku","string","none"],
    ["product_catalog","title","string","none"],
    ["support_tickets","ticket_id","string","none"],
    ["support_tickets","customer_email","string","email"],
    ["support_tickets","transcript","text","sensitive_text"],
    ["web_analytics","session_id","string","none"],
    ["web_analytics","country","string","none"],
], columns=["dataset","column","data_type","pii_type"])

lineage_csv = pd.DataFrame([
    # source, target, transformation
    ["customer_profiles", "customer_events", "left_join_on(customer_id)"],
    ["customer_profiles", "support_tickets", "lookup(email)"],
    ["orders", "payments", "join(order_id)"],
    ["customer_events", "web_analytics", "aggregate_by_session"],
    ["marketing_leads", "customer_profiles", "match(email, phone)"],
    ["product_catalog", "orders", "lookup(sku)"],
], columns=["source","target","transformation"])

audits_csv = pd.DataFrame([
    # dataset, gdpr_ok, remarks
    ["customer_profiles", False, "Missing consent tracking for legacy rows; DPIA pending."],
    ["customer_events", False, "Contains IP without documented retention controls."],
    ["orders", True, "No PII and encryption in place."],
    ["payments", True, "PII masked at source; PCI scope controlled."],
    ["marketing_leads", True, "Consent captured via webform; 90-day retention."],
    ["product_catalog", True, "No PII."],
    ["support_tickets", False, "Transcripts may include sensitive personal data; redaction incomplete."],
    ["web_analytics", True, "Aggregated; no direct identifiers."],
], columns=["dataset","gdpr_ok","remarks"])

datasets_path = f"{base}/data/datasets.csv"
columns_path  = f"{base}/data/columns.csv"
lineage_path  = f"{base}/data/lineage.csv"
audits_path   = f"{base}/data/audits.csv"

datasets_csv.to_csv(datasets_path, index=False)
columns_csv.to_csv(columns_path, index=False)
lineage_csv.to_csv(lineage_path, index=False)
audits_csv.to_csv(audits_path, index=False)

# -----------------------
# 2) Create policy & raw docs
# -----------------------

gdpr_md = """
# GDPR Quick Reference (Simplified)

- **PII (Personal Data)** requires:
  - Lawful basis (consent, contract, legal obligation, vital interests, public task, legitimate interests)
  - **Encryption at rest** and in transit where feasible
  - **Data minimization** and **purpose limitation**
  - **Retention limits**: Keep only as long as necessary
  - **Data Subject Rights**: Access, rectification, deletion (erasure)
- **Special Category Data** (health, biometrics, etc.) requires extra protection.
- **Records of Processing Activities** and **DPIA** (impact assessment) when high risk.

**Common checks for datasets with PII:**
- Encryption configured (KMS/AES)
- Retention period documented and reasonable
- Consent/Legal basis available
- Ability to delete on request
"""

internal_policy_md = """
# Internal Data Governance Policy (Simplified)

1. **Classification**: public, internal, confidential, restricted.
2. **PII Handling**:
   - Datasets with PII **must** use encryption at rest.
   - Retention:
     - Marketing leads: <= 90 days unless consent renewed.
     - Customer profiles: <= 365 days for inactive users.
   - Access must be role-based with least privilege.
3. **Lineage & Documentation**:
   - All datasets must have declared upstream sources.
   - Transformations should be reviewed quarterly.
4. **Audit & Alerts**:
   - Non-compliance triggers Slack/email alerts to data stewards.
"""

open_data_dict_md = """
# Data Dictionary (Excerpt)

- customer_profiles:
  - full_name (string, PII:name)
  - email (string, PII:email)
  - phone (string, PII:phone)
  - dob (date, PII:dob)
  - address (string, PII:address)

- marketing_leads:
  - email (string, PII:email)
  - phone (string, PII:phone)

- support_tickets:
  - transcript (text, may contain personal or sensitive data)
"""

with open(f"{base}/data/policies/gdpr.md","w") as f: f.write(gdpr_md.strip())
with open(f"{base}/data/policies/internal_policy.md","w") as f: f.write(internal_policy_md.strip())
with open(f"{base}/data/raw_docs/data_dictionary.md","w") as f: f.write(open_data_dict_md.strip())

# -----------------------
# 3) Create core app files
# -----------------------

readme = f"""
# AI Data Governance Copilot (RAG + LangChain + Agents)

This project provides a portfolio-ready **AI copilot** for data governance use-cases:
- Conversational search over **policies, metadata, and lineage**
- **Compliance checks** for PII (encryption, retention, consent)
- **Lineage tracing** between datasets
- **Report generation** (text/CSV)

## Project Structure
