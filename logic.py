"""Pure data + logic for the AI model release dashboard (no Streamlit imports).

Keeping this module UI-free makes the date math, sorting and data invariants
testable without launching a Streamlit runtime.
"""
from datetime import date

REF_DEFAULT = date(2026, 10, 13)
DATA_VINTAGE = REF_DEFAULT  # alias: one constant, two names for readability
REPO_URL = "https://github.com/apoorvsingh090/ai-model-release-dashboard"

# Days elapsed in the tracked window (Jan 1 -> REF_DEFAULT, exclusive of REF).
ELAPSED_DAYS = (REF_DEFAULT - date(REF_DEFAULT.year, 1, 1)).days

MON = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# (month, day) tuples; US early dots illustrative, CN dots public release dates.
# `latest` is NOT stored: it is derived as dots[-1] so the two can never drift.
LABS = [
    dict(id="meta", name="Meta", icon="∞", region="US",
         color="#7c5cff", bg="linear-gradient(180deg,#9a72ff,#6d3df5)",
         avg=47, model="Muse Wonder",
         dots=[(4, 8), (7, 12), (8, 5), (9, 8), (10, 12)]),
    dict(id="anth", name="Anthropic", icon="⋀", region="US",
         color="#d97a56", bg="linear-gradient(180deg,#d3764f,#a34a2c)",
         avg=24, model="Claude Haiku 5.5",
         dots=[(2, 2), (2, 20), (4, 15), (5, 22), (6, 5), (6, 28), (7, 20), (9, 2), (9, 25), (9, 28), (10, 7)]),
    dict(id="goog", name="Google DeepMind", icon="◍", region="US",
         color="#4f8cff", bg="linear-gradient(180deg,#3b78ff,#1e40d8)",
         avg=32, model="Gemini 4 Argon",
         dots=[(2, 18), (3, 5), (4, 10), (5, 20), (7, 15), (8, 10), (9, 5), (9, 30)]),
    dict(id="openai", name="OpenAI", icon="❖", region="US",
         color="#22c55e", bg="linear-gradient(180deg,#1db584,#0b7a55)",
         avg=29, model="GPT-6.1 Sol",
         dots=[(1, 15), (2, 10), (3, 8), (3, 12), (3, 25), (4, 28), (7, 10), (9, 8), (9, 24), (9, 29)]),
    dict(id="xai", name="SpaceXSI", icon="𝕏", region="US",
         color="#9aa0ae", bg="linear-gradient(180deg,#3a4150,#171b24)",
         avg=39, model="Grok 4.7",
         dots=[(3, 12), (5, 5), (5, 28), (7, 14), (8, 12), (9, 21)]),
    dict(id="deepseek", name="DeepSeek", icon="🐋", region="CN",
         color="#38bdf8", bg="linear-gradient(180deg,#1291d4,#0a4d7a)",
         avg=48, model="DeepSeek V4.1-Flash",
         dots=[(2, 19), (4, 24), (7, 31), (8, 13), (8, 21), (9, 10)]),
    dict(id="qwen", name="Qwen · Alibaba", icon="☁️", region="CN",
         color="#fb923c", bg="linear-gradient(180deg,#f97316,#7c2d12)",
         avg=22, model="Qwen3.8 Max Prime",
         dots=[(1, 25), (2, 20), (3, 15), (4, 20), (5, 18), (6, 22), (7, 19), (8, 12), (8, 26), (9, 14), (9, 18), (9, 21), (9, 23)]),
    dict(id="kimi", name="Kimi · Moonshot", icon="🌙", region="CN",
         color="#e8e8e8", bg="linear-gradient(180deg,#2b2f38,#0d0e12)",
         avg=57, model="Kimi K2.8 Preview",
         dots=[(1, 28), (4, 20), (6, 12), (7, 16), (9, 11)]),
    dict(id="glm", name="GLM · Zhipu", icon="⚡", region="CN",
         color="#2dd4bf", bg="linear-gradient(180deg,#0d9488,#123f3a)",
         avg=36, model="GLM-5.3 Prime",
         dots=[(2, 11), (4, 7), (6, 16), (8, 14), (8, 26), (8, 29), (9, 18), (9, 23)]),
]

# Derived once, at import: latest = last dot.
for _lab in LABS:
    _lab["latest"] = _lab["dots"][-1]


def days_since(lab: dict, ref: date = REF_DEFAULT) -> int | None:
    """Days from this lab's latest release to ref; None if the date is invalid."""
    m, d = lab["latest"]
    try:
        return (ref - date(ref.year, m, d)).days
    except ValueError:
        return None


def sort_labs(labs: list[dict], mode: str, ref: date = REF_DEFAULT) -> list[dict]:
    if mode == "Longest wait first":
        return sorted(labs, key=lambda lab: (days_since(lab, ref) is None, -(days_since(lab, ref) or 0)))
    if mode == "Freshest first":
        return sorted(labs, key=lambda lab: (days_since(lab, ref) is None, days_since(lab, ref) or 0))
    return list(labs)


def lab_view(lab: dict, ref: date = REF_DEFAULT) -> dict:
    """Everything a card/table row needs, computed once per lab per rerun."""
    ds = days_since(lab, ref)
    avg = lab["avg"]
    fill = min(100.0, max(ds or 0, 0) / avg * 100)
    if ds is None or ds < 0:
        status = "—"
    elif ds <= avg:
        status = "✅ on pace"
    else:
        status = "⚠ overdue"
    m, d = lab["latest"]
    return {
        "lab": lab,
        "days_since": ds,
        "display": str(max(ds, 0)) if ds is not None and ds >= 0 else "–",
        "fill": fill,
        "overdue": ds is not None and ds > avg,
        "status": status,
        "date_label": f"{MON[m]} {d}, {ref.year}",
        "releases": len(lab["dots"]),
    }


def month_starts(year: int) -> list[tuple[str, int]]:
    """('Jan', 1) ... ('Dec', n) as day-of-year offsets (1-based)."""
    jan1 = date(year, 1, 1)
    return [(MON[m], (date(year, m, 1) - jan1).days + 1) for m in range(1, 13)]


def timeline_points(lab: dict, ref: date = REF_DEFAULT, xmax: int | None = None) -> list[int]:
    """X offsets (1-based) of this lab's dots that fall inside (1, xmax]."""
    year = ref.year
    jan1 = date(year, 1, 1)
    if xmax is None:
        xmax = (ref - jan1).days + 1
    pts = []
    for m, d in lab["dots"]:
        try:
            x = (date(year, m, d) - jan1).days + 1
        except ValueError:
            continue
        if 1 <= x <= xmax:
            pts.append(x)
    return pts


def x_ticks(year: int, ref: date = REF_DEFAULT) -> tuple[list[int], list[str]]:
    """Month ticks up to the reference date, plus a de-duplicated 'Today' tick."""
    jan1 = date(year, 1, 1)
    xmax = (ref - jan1).days + 1
    positions = [(x, name) for name, x in month_starts(year) if x <= xmax]
    if not positions or positions[-1][0] != xmax:
        positions.append((xmax, "Today"))
    else:
        positions[-1] = (xmax, "Today")
    return [x for x, _ in positions], [n for _, n in positions]


def validate_labs(labs: list[dict] = LABS) -> list[str]:
    """Invariant checks; returns a list of problems (empty == healthy)."""
    problems = []
    ids = [lab["id"] for lab in labs]
    if len(ids) != len(set(ids)):
        problems.append("duplicate lab ids")
    for lab in labs:
        dots = lab["dots"]
        if not dots:
            problems.append(f"{lab['id']}: no dots")
            continue
        if dots != sorted(dots):
            problems.append(f"{lab['id']}: dots not chronological")
        if lab["latest"] != dots[-1]:
            problems.append(f"{lab['id']}: latest != dots[-1]")
        for m, d in dots:
            try:
                date(REF_DEFAULT.year, m, d)
            except ValueError:
                problems.append(f"{lab['id']}: invalid date ({m}, {d})")
        if lab["avg"] <= 0:
            problems.append(f"{lab['id']}: non-positive average")
    return problems
