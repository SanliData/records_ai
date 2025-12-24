# UPAP Architecture — Binding Specification

## Definition
UPAP is the canonical pipeline for Records_AI V2.

Stages:
1. Upload
2. Archive
3. Process (OCR / AI / Analysis)
4. Publish

No stage may be skipped, reordered, or bypassed.

## Binding Rules
- UPAP overrides all legacy designs
- Any conflicting documentation is invalid
- New development MUST attach to UPAP

## Legacy Systems
- records_ai
- records_ai_v2 (pre-UPAP)

Status:
- Read-only
- Historical context only
- No new features
- No architectural authority

## Conflict Resolution
If:
- Legacy behavior conflicts with UPAP → UPAP wins
- Documentation conflicts with code → Active UPAP code wins
- User request conflicts with governance → Request is refused

## Determinism
- No auto-fix
- No hidden retries
- No speculative recovery
- Errors must surface explicitly

## GPT Enforcement
The GPT must:
- Enforce UPAP order
- Reject shortcuts
- Reject invented endpoints
- Reject non-UPAP workflows
