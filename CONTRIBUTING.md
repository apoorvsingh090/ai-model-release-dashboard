# Contributing

Thanks for helping keep the release tracker accurate.

## Updating model data

Data is **curated by hand** in `streamlit_app.py` (`LABS` is the source of
truth). To add or correct a release:

1. Edit the lab's `model` / `latest=(month, day)` / `dots` / `avg`.
2. Move `DATA_VINTAGE` to today (the app shows a staleness banner after 14 days).
3. Open a PR with the source link for the release date.

## Development

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

CI runs a compile check and CodeQL; keep `streamlit_app.py` import-clean.

## Pull requests

- Branch from `main`: `feature/<short-description>` or `fix/<short-description>`.
- Conventional commits (`feat:` / `fix:` / `docs:`), one logical change per commit.
- Data PRs must cite a primary source (official announcement, model card, launch post).

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
