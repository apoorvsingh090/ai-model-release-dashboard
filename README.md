# Days Since Latest AI Model Release

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
