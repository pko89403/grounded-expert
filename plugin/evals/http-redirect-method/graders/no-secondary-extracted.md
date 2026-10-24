---
type: regex
target: last_message
match: not_contains
flags: i
weight: 0.5
---
EXTRACTED[^\n]*https?://(?:[\w-]+\.)*(?:wikipedia\.org|stackoverflow\.com|medium\.com|gdpr-info\.eu|w3schools\.com|geeksforgeeks\.org|huggingface\.co|researchgate\.net)
