# API Reference — Read Only (Documentation)

## IMPORTANT
This GPT does NOT execute APIs.
This reference exists to prevent hallucination.

## Known Endpoint Categories

### Upload
- Accepts raw input (file + metadata)
- Produces a record_id
- Does NOT publish

### Archive
- Persists uploaded content
- Assigns canonical storage identity

### Process
- OCR
- AI analysis
- Evidence extraction
- Classification

### Publish
- Makes record externally visible
- Final stage only

## Non-Rules
- No undocumented endpoints exist
- No auto-publish
- No direct archive-to-publish jump

## GPT Constraint
If an endpoint is not explicitly documented:
→ GPT must state: "This endpoint is not documented."

No guessing is allowed.
