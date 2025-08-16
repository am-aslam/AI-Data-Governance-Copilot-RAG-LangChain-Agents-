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