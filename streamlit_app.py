"""Days since latest AI model release — US + China extended (Streamlit).

Run locally:  streamlit run streamlit_app.py
Needs: streamlit, matplotlib (see requirements.txt).
"""
from datetime import date

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Days since latest AI model release", layout="wide")

REF_DEFAULT = date(2026, 10, 13)
REPO_URL = "https://github.com/apoorvsingh090/ai-model-release-dashboard"

# (month, day) tuples; US early dots illustrative, CN dots public release dates.
LABS = [
    dict(id="meta", name="Meta", icon="∞", region="US",
         color="#7c5cff", bg="linear-gradient(180deg,#9a72ff,#6d3df5)",
         avg=47, model="Muse Wonder", latest=(10, 12),
         dots=[(4, 8), (7, 12), (8, 5), (9, 8), (10, 12)]),
    dict(id="anth", name="Anthropic", icon="⋀", region="US",
         color="#d97a56", bg="linear-gradient(180deg,#d3764f,#a34a2c)",
         avg=24, model="Claude Haiku 5.5", latest=(10, 7),
         dots=[(2, 2), (2, 20), (4, 15), (5, 22), (6, 5), (6, 28), (7, 20), (9, 2), (9, 25), (9, 28), (10, 7)]),
    dict(id="goog", name="Google DeepMind", icon="◍", region="US",
         color="#4f8cff", bg="linear-gradient(180deg,#3b78ff,#1e40d8)",
         avg=32, model="Gemini 4 Argon", latest=(9, 30),
         dots=[(2, 18), (3, 5), (4, 10), (5, 20), (7, 15), (8, 10), (9, 5), (9, 30)]),
    dict(id="openai", name="OpenAI", icon="❖", region="US",
         color="#22c55e", bg="linear-gradient(180deg,#1db584,#0b7a55)",
         avg=29, model="GPT-6.1 Sol", latest=(9, 29),
         dots=[(1, 15), (2, 10), (3, 8), (3, 12), (3, 25), (4, 28), (7, 10), (9, 8), (9, 24), (9, 29)]),
    dict(id="xai", name="SpaceXSI", icon="𝕏", region="US",
         color="#9aa0ae", bg="linear-gradient(180deg,#3a4150,#171b24)",
         avg=39, model="Grok 4.7", latest=(9, 21),
         dots=[(3, 12), (5, 5), (5, 28), (7, 14), (8, 12), (9, 21)]),
    dict(id="deepseek", name="DeepSeek", icon="🐋", region="CN",
         color="#38bdf8", bg="linear-gradient(180deg,#1291d4,#0a4d7a)",
         avg=48, model="DeepSeek V4.1-Flash", latest=(9, 10),
         dots=[(2, 19), (4, 24), (7, 31), (8, 13), (8, 21), (9, 10)]),
    dict(id="qwen", name="Qwen · Alibaba", icon="☁️", region="CN",
         color="#fb923c", bg="linear-gradient(180deg,#f97316,#7c2d12)",
         avg=24, model="Qwen3.8-Omni-Flash", latest=(9, 18),
         dots=[(1, 25), (2, 20), (3, 15), (4, 20), (5, 18), (6, 22), (7, 19), (8, 12), (8, 26), (9, 14), (9, 18), (9, 21)]),
    dict(id="kimi", name="Kimi · Moonshot", icon="🌙", region="CN",
         color="#e8e8e8", bg="linear-gradient(180deg,#2b2f38,#0d0e12)",
         avg=57, model="Kimi K2.8 Preview", latest=(9, 11),
         dots=[(1, 28), (4, 20), (6, 12), (7, 16), (9, 11)]),
    dict(id="glm", name="GLM · Zhipu", icon="⚡", region="CN",
         color="#2dd4bf", bg="linear-gradient(180deg,#0d9488,#123f3a)",
         avg=36, model="GLM-5.3 Prime", latest=(9, 23),
         dots=[(2, 11), (4, 7), (6, 16), (8, 14), (8, 26), (8, 29), (9, 18), (9, 23)]),
]

st.markdown(
    "<h1 style='font-size:clamp(30px,4.5vw,54px);font-weight:800;letter-spacing:-.02em;"
    "background:linear-gradient(90deg,#f0a07a,#b678e0,#5b8def,#2dd4bf);"
    "-webkit-background-clip:text;background-clip:text;color:transparent'>"
    "Days since latest AI model release.</h1>",
    unsafe_allow_html=True,
)
st.caption("US labs (Meta · Anthropic · Google DeepMind · OpenAI · xAI) plus Chinese labs 🇨🇳 "
           "(DeepSeek · Qwen/Alibaba · Kimi/Moonshot · GLM/Zhipu). Language models only.")

# ---- controls live in the sidebar so the dashboard stays uncluttered ----
with st.sidebar:
    st.header("⚙️ Controls")
    filt = st.radio("Show", ["All labs (9)", "US only (5)", "China only (4)"])
    sort = st.radio("Card order", ["Lab order", "Longest wait first", "Freshest first"],
                    help="Reorder the leaderboard cards below.")
    ref = st.date_input("Reference date", value=REF_DEFAULT,
                        min_value=date(2026, 1, 1), max_value=date(2027, 6, 30),
                        help="Every 'days since' count is computed from this date. "
                             "Move it forward to watch the counters tick up.")
    st.divider()
    st.caption("📅 Data vintage: Oct 13, 2026. US dots are illustrative; "
               "CN dots are dated public releases (see Sources).")
    st.link_button("⭐ GitHub repo", REPO_URL)

region = {"All labs (9)": None, "US only (5)": "US", "China only (4)": "CN"}[filt]
labs = [l for l in LABS if region is None or l["region"] == region]
year = ref.year
jan1 = date(year, 1, 1)
MON = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def days_since(lab):
    m, d = lab["latest"]
    try:
        return (ref - date(year, m, d)).days
    except ValueError:
        return None


def _ds_or_zero(lab):
    ds = days_since(lab)
    return ds if ds is not None else 0


if sort == "Longest wait first":
    labs.sort(key=lambda l: (days_since(l) is None, -_ds_or_zero(l)))
elif sort == "Freshest first":
    labs.sort(key=lambda l: (days_since(l) is None, _ds_or_zero(l)))

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
for l in labs:
    ds = days_since(l)
    ds_txt = str(max(ds, 0)) if ds is not None and ds >= 0 else "–"
    fill = min(100, max(ds or 0, 0) / l["avg"] * 100)
    overdue = ds is not None and ds > l["avg"]
    lm, ld = l["latest"]
    cards_html.append(
        f"<div class='card' style='background:{l['bg']}'>"
        f"<div><div class='brand'>{l['icon']} {l['name']}</div>"
        f"<div class='num'>{ds_txt}</div><div>{'day' if ds_txt == '1' else 'days'}</div>"
        f"<div class='bar' title='Days elapsed vs average release cadence'>"
        f"<div style='width:{fill:.1f}%'></div></div>"
        f"<div class='avg'>Avg. every {l['avg']} days"
        f"{' · ⚠ overdue' if overdue else ''}</div></div>"
        f"<div class='foot'><b>{l['model']}</b><span>{MON[lm]} {ld}, {year}</span></div></div>"
    )
cards_html.append("</div>")
st.markdown("".join(cards_html), unsafe_allow_html=True)
st.caption("Progress bar = days elapsed ÷ average release cadence. "
           "⚠ overdue = waiting longer than usual for this lab.")

scored = [(l, ds) for l in labs if (ds := days_since(l)) is not None and ds >= 0]
if scored:
    f_lab, f_ds = min(scored, key=lambda t: t[1])
    s_lab, s_ds = max(scored, key=lambda t: t[1])
    st.info(f"🏆 Freshest: **{f_lab['name']}** — {f_lab['model']} "
            f"({f_ds} day{'s' if f_ds != 1 else ''} ago) · "
            f"⌛ Stalest: **{s_lab['name']}** — {s_lab['model']} ({s_ds} days ago)")

# ---- timeline ----
st.subheader("2026 releases")
st.caption("Each dot is a new model. US dots illustrative from original artifact (counts preserved). "
           "CN dots: public release dates. Dashed line = reference date.")
xmax = (ref - jan1).days + 1
plt.style.use("dark_background")
fig_h = max(3.2, 0.62 * len(labs) + 1.2)
fig, ax = plt.subplots(figsize=(11, fig_h))
fig.patch.set_alpha(0.0)
ax.set_facecolor("none")
ys = list(range(len(labs)))[::-1]  # first lab on top
month_starts = [("Jan", 1), ("Feb", 32), ("Mar", 60), ("Apr", 91), ("May", 121),
                ("Jun", 152), ("Jul", 182), ("Aug", 213), ("Sep", 244), ("Oct", 274)]
for y, l in zip(ys, labs):
    pts = []
    for m, d in l["dots"]:
        try:
            x = (date(year, m, d) - jan1).days + 1
        except ValueError:
            continue
        if 1 <= x <= xmax:
            pts.append(x)
    ax.hlines(y, 1, xmax, colors="#2a2a35", linewidth=2, zorder=1)
    if pts:
        ax.scatter(pts[:-1], [y] * max(len(pts) - 1, 0), s=28, color=l["color"], zorder=3)
        ax.scatter([pts[-1]], [y], s=120, color=l["color"],
                   edgecolors="white", linewidths=1.2, zorder=4)
    ax.text(xmax, y, f"  {len(pts)} releases", va="center", ha="left",
            fontsize=9, color="#9aa0ae", clip_on=False)
ax.axvline(xmax, color="#6b7280", linestyle="--", linewidth=1.2)
ax.set_yticks(ys)
ax.set_yticklabels([f"{l['icon']} {l['name']}" for l in labs], fontsize=10)
ax.set_xlim(1, xmax)
ax.margins(x=0)
ax.set_ylim(min(ys) - 0.7, max(ys) + 0.7)
ax.set_xticks([x for _, x in month_starts if x <= xmax] + [xmax])
ax.set_xticklabels([n for n, x in month_starts if x <= xmax] + ["Today"], fontsize=9)
ax.tick_params(colors="#9aa0ae")
for s in ax.spines.values():
    s.set_visible(False)
ax.grid(axis="x", color="#22212b", linewidth=0.6, linestyle=":")
fig.subplots_adjust(left=0.18, right=0.80, top=0.94, bottom=0.12)
st.pyplot(fig, use_container_width=True)

# ---- table + sources ----
st.subheader("All releases")
rows = []
for l in labs:
    ds = days_since(l)
    lm, ld = l["latest"]
    if ds is None or ds < 0:
        status = "—"
    elif ds <= l["avg"]:
        status = "✅ on pace"
    else:
        status = "⚠ overdue"
    rows.append({"Lab": f"{l['icon']} {l['name']}", "Region": l["region"],
                 "Latest model": l["model"], "Date": f"{MON[lm]} {ld}, {year}",
                 "Days since": ds, "Status": status,
                 "Avg (days)": l["avg"], "2026 releases": len(l["dots"])})
st.dataframe(rows, use_container_width=True, hide_index=True)

with st.expander("Sources & methodology"):
    st.markdown(
        "- **DeepSeek** — V4.1-Flash Sep 10, 2026 (api-docs.deepseek.com).\n"
        "- **Qwen** — Qwen3.8-Omni-Flash Sep 18, 2026; 12 language-model releases tracked "
        "(Sep 21 Omni-Realtime voice + Sep 24 decision-preview excluded). QwenCloud changelog + qwen.ai blog.\n"
        "- **Kimi** — K2.8 Preview Sep 11, 2026 (kimi.com/code/docs + Moonshot blog).\n"
        "- **GLM** — GLM-5.3 Prime Sep 23, 2026 (z.ai blog + NIST CAISI Sep 17 assessment; Prime date via LMMarketCap).\n"
        "- Averages = releases ÷ 285 days elapsed (Jan 1 → Oct 13, 2026), rounded. "
        "US avgs kept from the original artifact screenshots."
    )

st.divider()
st.caption(f"Language models only · Data vintage Oct 13, 2026 · "
           f"[⭐ Star on GitHub]({REPO_URL})")
