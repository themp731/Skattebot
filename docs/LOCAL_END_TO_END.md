# Local end-to-end workflow

No AWS, ESPN credentials, OpenAI key, or SES setup is needed for the default demo.

```powershell
python main.py local-demo --season 2026 --week 4 --teams 12 --seed 10 --output-dir outputs/local --public-dir public
python -m http.server 8000 --directory public
# open http://localhost:8000
python send_weekly_recap_email.py --recap outputs/local/recaps/week_4_recap.md --recipients config/recipients.example.csv --dry-run --preview outputs/local/recaps/week_4_preview.eml
python -m unittest discover -s tests -v
```

The dashboard labels dummy data as `DEMO DATA`. If `public/data/latest.json` is absent, it shows an explicit fallback instead of league results.

`refresh --source dummy` generates deterministic data when `--seed` is supplied. `refresh --source sample --data-dir <directory>` exports existing raw CSVs without scraping. `refresh --source espn --league-id <id>` invokes the existing ESPN scraper and reads `ESPN_S2` and `SWID` only from the environment; it never logs or publishes them. A failed ESPN scrape exits clearly rather than silently publishing stale data.

The generated JSON artifacts are described in [DATA_CONTRACT.md](DATA_CONTRACT.md). `--generate-placeholder-recap` writes an offline markdown recap strictly from `recap_context_week_N.json`; it is not an OpenAI recap.

Still for production: issue #5 owns S3/CloudFront/scheduling/secrets/observability; issue #7 owns OpenAI recap generation; issue #8 owns a real explicit `--send` email integration. The local email command only previews an RFC 822 `.eml` file and rejects `--send`.

The offline test suite creates temporary dummy artifacts, serves the generated
site over localhost, verifies the published payload, and verifies the missing-data
HTTP/fallback path. It does not contact ESPN, OpenAI, AWS, or an email provider.
