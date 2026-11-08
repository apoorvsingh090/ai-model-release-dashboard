"""Days since latest AI model release — US + China extended (Streamlit).

Run locally:  streamlit run streamlit_app.py
Needs: streamlit, matplotlib, pandas (see requirements.txt).
All logic lives in logic.py so it can be tested without a Streamlit runtime.
"""
from datetime import date

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st

from logic import (
    DATA_VINTAGE,
    LABS,
    REF_DEFAULT,
    REPO_URL,
    lab_view,
    sort_labs,
    timeline_points,
    x_ticks,
)

st.set_page_config(page_title="Days since latest AI model release", layout="wide")

st.markdown(
    "<h1 style='font-size:clamp(30px,4.5vw,54px);font-weight:800;letter-spacing:-.02em;"
    "background:linear-gradient(90deg,#f0a07a,#b678e0,#5b8def,#2dd4bf);"
    "-webkit-background-clip:text;background-clip:text;color:transparent'>"
    "Days since latest AI model release.</h1>",
    unsafe_allow_html=True,
)
st.caption("US labs (Meta · Anthropic · Google DeepMind · OpenAI · xAI) plus Chinese labs 🇨🇳 "
           "(DeepSeek · Qwen/Alibaba · Kimi/Moonshot · GLM/Zhipu). Language models only.")
_vintage_age = (date.today() - DATA_VINTAGE).days
if _vintage_age > 14:
    st.warning(
        f"📅 Data vintage: {DATA_VINTAGE.strftime('%b %d, %Y')} "
        f"({_vintage_age} days ago) — newer model releases may exist. "
        "Data here is curated by hand; see README 'Updating the data'."
    )

# ---- controls live in the sidebar so the dashboard stays uncluttered ----
with st.sidebar:
    st.header("⚙️ Controls")
    filt = st.radio("Show", ["All labs (9)", "US only (5)", "China only (4)"])
    sort = st.radio("Card order", ["Lab order", "Longest wait first", "Freshest first"],
                    help="Reorder the leaderboard cards below.")
    ref = st.date_input("Reference date", value=REF_DEFAULT,
                        min_value=date(2026, 1, 1), max_value=date(2026, 12, 31),
                        help="Every 'days since' count is computed from this date. "
                             "Move it forward to watch the counters tick up.")
    st.divider()
    st.caption(f"📅 Data vintage: {DATA_VINTAGE.strftime('%b %d, %Y')}. US dots are illustrative; "
               "CN dots are dated public releases (see Sources).")
    st.link_button("⭐ GitHub repo", REPO_URL)

region = {"All labs (9)": None, "US only (5)": "US", "China only (4)": "CN"}[filt]
labs = sort_labs([lab for lab in LABS if region is None or lab["region"] == region], sort, ref)
year = ref.year
jan1 = date(year, 1, 1)
xmax = (ref - jan1).days + 1
views = [lab_view(lab, ref) for lab in labs]

# ---- leaderboard cards (same look as static HTML) ----
st.subheader("Leaderboard")
st.markdown(
    """<style>
.cards{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));border-radius:22px;overflow:hidden}
@media(max-width:1100px){.cards{grid-template-columns:repeat(5,minmax(0,1fr))}}
@media(max-width:640px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}}
.card{min-width:0;padding:20px 18px 0;display:flex;flex-direction:column;justify-content:space-between;color:#fff}
.card .brand{font-weight:700;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card .num{font-size:clamp(40px,4vw,68px);font-weight:800;line-height:1;margin:12px 0 2px}
.card .bar{height:4px;background:rgba(255,255,255,.28);border-radius:99px;overflow:hidden}
.card .bar>div{height:100%;background:#fff;border-radius:99px}
.card .avg{font-size:12.5px;opacity:.92;margin:8px 0 16px}
.card .foot{margin:0 -18px;padding:10px 18px;background:rgba(0,0,0,.28);font-size:12.5px}
</style>""",
    unsafe_allow_html=True,
)
cards_html = ["<div class='cards'>"]
for v in views:
    lab = v["lab"]
    cards_html.append(
        f"<div class='card' style='background:{lab['bg']}'>"
        f"<div><div class='brand'>{lab['icon']} {lab['name']}</div>"
        f"<div class='num'>{v['display']}</div>"
        f"<div>{'day' if v['display'] == '1' else 'days'}</div>"
        f"<div class='bar' title='Days elapsed vs average release cadence'>"
        f"<div style='width:{v['fill']:.1f}%'></div></div>"
        f"<div class='avg'>Avg. every {lab['avg']} days"
        f"{' · ⚠ overdue' if v['overdue'] else ''}</div></div>"
        f"<div class='foot'><b>{lab['model']}</b><span>{v['date_label']}</span></div></div>"
    )
cards_html.append("</div>")
st.markdown("".join(cards_html), unsafe_allow_html=True)
st.caption("Progress bar = days elapsed ÷ average release cadence. "
           "⚠ overdue = waiting longer than usual for this lab.")

scored = [v for v in views if v["days_since"] is not None and v["days_since"] >= 0]
if scored:
    freshest = min(scored, key=lambda v: v["days_since"])
    stalest = max(scored, key=lambda v: v["days_since"])
    f_lab, f_ds = freshest["lab"], freshest["days_since"]
    s_lab, s_ds = stalest["lab"], stalest["days_since"]
    st.info(f"🏆 Freshest: **{f_lab['name']}** — {f_lab['model']} "
            f"({f_ds} day{'s' if f_ds != 1 else ''} ago) · "
            f"⌛ Stalest: **{s_lab['name']}** — {s_lab['model']} ({s_ds} days ago)")

# ---- timeline ----
st.subheader(f"{year} releases")
st.caption("Each dot is a new model. US dots illustrative from original artifact (counts preserved). "
           "CN dots: public release dates. Dashed line = reference date.")
plt.rcParams["figure.max_open_warning"] = 0
fig_h = max(3.2, 0.62 * len(labs) + 1.2)
with plt.style.context("dark_background"):
    fig, ax = plt.subplots(figsize=(11, fig_h))
fig.patch.set_alpha(0.0)
ax.set_facecolor("none")
ys = list(range(len(labs)))[::-1]  # first lab on top
for y, lab in zip(ys, labs):
    pts = timeline_points(lab, ref, xmax)
    ax.hlines(y, 1, xmax, colors="#2a2a35", linewidth=2, zorder=1)
    if pts:
        ax.scatter(pts[:-1], [y] * max(len(pts) - 1, 0), s=28, color=lab["color"], zorder=3)
        ax.scatter([pts[-1]], [y], s=120, color=lab["color"],
                   edgecolors="white", linewidths=1.2, zorder=4)
    ax.text(xmax, y, f"  {len(pts)} releases", va="center", ha="left",
            fontsize=9, color="#9aa0ae", clip_on=False)
ax.axvline(xmax, color="#6b7280", linestyle="--", linewidth=1.2)
ax.set_yticks(ys)
ax.set_yticklabels([f"{lab['icon']} {lab['name']}" for lab in labs], fontsize=10)
ax.set_xlim(1, xmax)
ax.margins(x=0)
ax.set_ylim(min(ys) - 0.7, max(ys) + 0.7)
tick_x, tick_labels = x_ticks(year, ref)
ax.set_xticks(tick_x)
ax.set_xticklabels(tick_labels, fontsize=9)
ax.tick_params(colors="#9aa0ae")
for s in ax.spines.values():
    s.set_visible(False)
ax.grid(axis="x", color="#22212b", linewidth=0.6, linestyle=":")
fig.subplots_adjust(left=0.18, right=0.80, top=0.94, bottom=0.12)
try:
    st.pyplot(fig, use_container_width=True)
finally:
    # Close every rerun: unclosed figures accumulate per session.
    plt.close(fig)

# ---- table + sources ----
st.subheader("All releases")
rows = []
for v in views:
    lab = v["lab"]
    rows.append({"Lab": f"{lab['icon']} {lab['name']}", "Region": lab["region"],
                 "Latest model": lab["model"], "Date": v["date_label"],
                 "Days since": v["days_since"], "Status": v["status"],
                 "Avg (days)": lab["avg"], f"{year} releases": v["releases"]})
st.dataframe(rows, use_container_width=True, hide_index=True)

with st.expander("Sources & methodology"):
    st.markdown(
        "- **DeepSeek** — V4.1-Flash Sep 10, 2026 (api-docs.deepseek.com).\n"
        "- **Qwen** — Qwen3.8 Max Prime Sep 23, 2026; 13 language-model releases tracked "
        "(lmmarketcap + OpenCode Data; Sep 24 decision-preview excluded as unclassified). QwenCloud changelog + qwen.ai blog.\n"
        "- **Kimi** — K2.8 Preview Sep 11, 2026 (kimi.com/code/docs + Moonshot blog).\n"
        "- **GLM** — GLM-5.3 Prime Sep 23, 2026 (z.ai blog + NIST CAISI Sep 17 assessment; Prime date via LMMarketCap).\n"
        "- Averages = releases ÷ 285 days elapsed (Jan 1 → Oct 13, 2026), rounded. "
        "US avgs kept from the original artifact screenshots."
    )

st.divider()
st.caption(f"Language models only · Data vintage {DATA_VINTAGE.strftime('%b %d, %Y')} · "
           f"[⭐ Star on GitHub]({REPO_URL})")
