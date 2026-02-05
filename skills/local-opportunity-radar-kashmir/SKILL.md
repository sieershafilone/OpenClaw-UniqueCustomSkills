---
name: local-opportunity-radar-kashmir
description: Kashmir-specific opportunity intelligence engine. Aggregates local government, NGO, and informal postings (WhatsApp/Telegram/PDFs) and filters them by real user eligibility. Use when the user needs to find income-generating opportunities, jobs, or tenders in Kashmir that they are actually eligible for.
---

# Local Opportunity Radar (Kashmir)

LOR-K is a high-precision filter for income-generating opportunities in Jammu & Kashmir. It bypasses the noise of general job portals by scanning local, often informal, sources and matching them against a strictly defined user profile.

## Core Workflow

1. **Source Aggregation**: Scan DC office PDFs, JKSSB notices, and curated WhatsApp/Telegram signals.
2. **OCR & Extraction**: Convert images and PDF notices into structured data (Pay, Location, Deadline, Criteria).
3. **Eligibility Filtering**: Compare the opportunity against the user's `profile.yaml`.
4. **Digest Generation**: Present a prioritized list of eligible opportunities via `lor.today`.

## User Commands

- `lor.today`: Generate today's prioritized opportunity report.
- `lor.profile`: View or update your local eligibility criteria (District, Education, Age).
- `lor.sources`: Check the status of the scanned sources (JKSSB, Telegram, etc.).

## References

- See [specification.md](references/specification.md) for the product blueprint, revenue strategy, and the **District-wise Sourcing Consolidation**.

## Implementation Notes

The magic of LOR-K is the **negative space**—it purposefully hides opportunities for which the user is over-age, under-qualified, or geographically excluded. This maintains high trust and daily utility.
