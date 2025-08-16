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