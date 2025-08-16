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