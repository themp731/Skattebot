# Canonical local artifact contract

`main.py refresh` writes a versioned, JSON-first contract. The refresh worker is the only component that may scrape; the dashboard and recap read these files instead.

| Location | Consumer | Contents |
| --- | --- | --- |
| `outputs/.../raw/*.csv` | refresh/exporter | scraper-compatible raw matchups, team stats, player stats |
| `outputs/.../processed/{metadata,standings,rankings,head_to_head}.json` | canonical backend contract | source, schema/version, records, scoring and derived rankings |
| `outputs/.../site_data/latest.json` | local inspection | one combined site payload |
| `outputs/.../recaps/recap_context_week_N.json` | recap generation | latest-week results plus canonical standings/rankings |
| `public/data/*.json` | static site | copies of the canonical site payload; never secrets |

`metadata.json` contains `schema_version`, `generated_at`, `season`, `latest_completed_week`, `data_source`, and `is_sample_data`. Consumers should reject an incompatible schema version and show a stale/missing-data state. Runtime outputs, credentials, and real recipient lists are ignored and must not be committed.
