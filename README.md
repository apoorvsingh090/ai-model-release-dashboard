# Days Since Latest AI Model Release

[![CI](https://img.shields.io/github/actions/workflow/status/apoorvsingh090/ai-model-release-dashboard/ci.yml?branch=main)](https://github.com/apoorvsingh090/ai-model-release-dashboard/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

🚀 **Live demo:** https://ai-model-release-dashboard-4vupclwmdzprxwdfegdvtw.streamlit.app/

Tracker dashboard for flagship LLM releases — US labs (Meta, Anthropic, Google DeepMind, OpenAI, xAI) plus Chinese labs (DeepSeek, Qwen/Alibaba, Kimi/Moonshot, GLM/Zhipu).

Use the sidebar to filter labs, reorder the leaderboard, or move the reference date and watch every counter recompute. Labs waiting longer than their usual cadence get an ⚠ overdue flag.

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy

Already deployed ☝️. To redeploy elsewhere, import this repo in [Streamlit Community Cloud](https://share.streamlit.io/) — main file is `streamlit_app.py`.

## Updating the data

Model data is **curated by hand, not auto-refreshed** — there is no reliable API for "latest model per lab", so `LABS` in `streamlit_app.py` is the source of truth. To add a release:

1. Edit the lab's `model` / `latest=(month, day)` / `dots` / `avg` in `LABS`, and move `DATA_VINTAGE` to today.
2. Commit + push — Streamlit Cloud redeploys automatically (that part *is* automatic).

The app shows a staleness banner once the vintage is more than 14 days old.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for data-curation rules and the PR
process; [CHANGELOG.md](CHANGELOG.md) tracks changes. By participating you
agree to the [Code of Conduct](CODE_OF_CONDUCT.md). Use the issue templates
for bugs and feature requests.

## Security

Report tooling vulnerabilities privately via
[GitHub Security Advisories](https://github.com/apoorvsingh090/ai-model-release-dashboard/security/advisories);
see [SECURITY.md](SECURITY.md).

## License

MIT — see [LICENSE](LICENSE).
