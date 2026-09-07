"""Build the SVG assets for the profile README.

    python scripts/build.py

Every SVG embeds its fonts as data URIs because GitHub serves README images
through a proxy that blocks external resources. Fonts are the subsetted
woff2 files in assets/fonts/. Light and dark variants are written for each
asset; README.md picks one with <picture>.
"""

from __future__ import annotations

import base64
import html
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
OUT = ROOT / "assets"
W = 871  # GitHub README content width, minus a little

THEMES = {
    "light": dict(
        paper="#f1f2ed", lift="#fbfbf9", ink="#161a19", muted="#565d5a",
        faint="#8a918d", hair="#c9cdc4", accent="#2036c7", on_accent="#ffffff",
    ),
    "dark": dict(
        paper="#161b22", lift="#1c222b", ink="#e6e8e3", muted="#a3aaa5",
        faint="#6e7571", hair="#30363d", accent="#8b9cff", on_accent="#0d1117",
    ),
}

SITE = "https://moosamemon.me"


# ----------------------------------------------------------------- fonts --

class Face:
    """A subset font: advance widths for layout plus a data URI for embedding."""

    def __init__(self, file: str, family: str, weight: int):
        path = FONTS / file
        self.family, self.weight = family, weight
        font = TTFont(path)
        self.upm = font["head"].unitsPerEm
        self.cmap = font.getBestCmap()
        self.hmtx = font["hmtx"]
        self.b64 = base64.b64encode(path.read_bytes()).decode()

    def width(self, text: str, size: float, tracking: float = 0) -> float:
        units = 0
        for ch in text:
            glyph = self.cmap.get(ord(ch), ".notdef")
            units += self.hmtx[glyph][0]
        return units / self.upm * size + tracking * size * max(len(text) - 1, 0)

    def wrap(self, text: str, size: float, max_w: float) -> list[str]:
        lines, line = [], ""
        for word in text.split():
            trial = f"{line} {word}".strip()
            if line and self.width(trial, size) > max_w:
                lines.append(line)
                line = word
            else:
                line = trial
        if line:
            lines.append(line)
        return lines

    def face_rule(self) -> str:
        return (
            f"@font-face{{font-family:'{self.family}';font-weight:{self.weight};"
            f"src:url(data:font/woff2;base64,{self.b64}) format('woff2')}}"
        )


DISPLAY = Face("bricolage-grotesque-600.woff2", "BG", 600)
MONO = Face("ibm-plex-mono-400.woff2", "PM", 400)
MONO_MED = Face("ibm-plex-mono-500.woff2", "PM", 500)
BODY = Face("hanken-grotesk-400.woff2", "HG", 400)
BODY_BOLD = Face("hanken-grotesk-600.woff2", "HG", 600)


# ------------------------------------------------------------------ svg ----

def esc(s: str) -> str:
    return html.escape(s, quote=False)


def text(x, y, s, cls, anchor="start", extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{extra}>{esc(s)}</text>'


def line(x1, y1, x2, y2, cls="hair"):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}" pathLength="1"/>'


def base_css(t: dict, faces: list[Face]) -> str:
    return "".join(f.face_rule() for f in faces) + f"""
text{{white-space:pre}}
.d{{font-family:'BG','Arial Black',Arial,sans-serif;font-weight:600;fill:{t['ink']}}}
.m{{font-family:'PM',ui-monospace,Consolas,'Liberation Mono',monospace;font-weight:400;fill:{t['ink']}}}
.mm{{font-family:'PM',ui-monospace,Consolas,'Liberation Mono',monospace;font-weight:500;fill:{t['ink']}}}
.b{{font-family:'HG','Segoe UI',system-ui,sans-serif;font-weight:400;fill:{t['ink']}}}
.bb{{font-family:'HG','Segoe UI',system-ui,sans-serif;font-weight:600;fill:{t['ink']}}}
.muted{{fill:{t['muted']}}} .faint{{fill:{t['faint']}}} .accent{{fill:{t['accent']}}}
.label{{font-size:10px;letter-spacing:.1em;text-transform:uppercase;fill:{t['faint']}}}
.hair{{stroke:{t['hair']};stroke-width:1}} .rule{{stroke:{t['ink']};stroke-width:1}}
.onink{{fill:{t['paper']}}}
"""


def anim_css() -> str:
    # Text is visible at rest; only the rules draw in and the underline grows.
    # A renderer that ignores CSS animation still shows the finished sheet.
    return """
.ln{stroke-dasharray:1;animation:draw .9s cubic-bezier(.2,.7,.2,1) both}
.ul{transform-box:fill-box;transform-origin:0 50%;animation:grow .45s cubic-bezier(.2,.7,.2,1) .6s both}
@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@media (prefers-reduced-motion:reduce){.ln,.ul{animation:none}}
"""


def svg(width, height, css, body, label) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{esc(label)}">'
        f"<style>{css}</style>{body}</svg>"
    )


def write(name: str, theme: str, content: str):
    path = OUT / f"{name}-{theme}.svg"
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"{path.relative_to(ROOT)}  {len(content.encode()) // 1024} KB")


# ------------------------------------------------------------------ hero ---

def hero(theme: str) -> str:
    t = THEMES[theme]
    H = 300
    css = base_css(t, [DISPLAY, MONO, MONO_MED, BODY_BOLD]) + anim_css() + f"""
.name{{font-size:15px}} .head{{font-size:46px;letter-spacing:-.01em}}
.cell{{font-size:13px}} .cell2{{font-size:12.5px}}
"""
    lines, texts = [], []

    # sheet
    body = f'<rect x="0" y="0" width="{W}" height="{H}" fill="{t["paper"]}"/>'
    lines.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" class="rule ln" pathLength="1"/>')

    # masthead
    texts.append(text(28, 38, "Moosa Memon", "bb name"))
    texts.append(text(W - 28, 38, "PROFILE  ·  REV 2026.09", "mm label", anchor="end"))
    lines.append(line(0, 56, W, 56, "hair ln"))

    # headline with the drafting-blue underline under "survive production"
    hs = 46
    texts.append(text(28, 128, "I build AI systems that", "d head"))
    texts.append(text(28, 182, "survive production.", "d head"))
    uw = DISPLAY.width("survive production", hs, -0.01)
    body_extra = f'<rect x="28" y="187" width="{uw:.1f}" height="6" fill="{t["accent"]}" class="ul"/>'

    # mini title block, right
    mx, my, mw = 606, 78, W - 28 - 606
    rows = [("Sheet", "1 of 1"), ("Drawn", "M. Memon"), ("Checked", "in production"), ("Scale", "right-sized")]
    rh = 27
    lines.append(f'<rect x="{mx+0.5}" y="{my+0.5}" width="{mw-1}" height="{rh*len(rows)-1}" fill="none" class="hair ln" pathLength="1"/>')
    lines.append(line(mx + 92, my, mx + 92, my + rh * len(rows), "hair ln"))
    for i, (k, v) in enumerate(rows):
        y = my + rh * i
        if i:
            lines.append(line(mx, y, mx + mw, y, "hair ln"))
        texts.append(text(mx + 12, y + 18, k, "mm label"))
        texts.append(text(mx + 104, y + 18, v, "m cell2"))

    # bottom strip: the title block proper
    sy = H - 74
    lines.append(line(0, sy, W, sy, "rule ln"))
    cells = [
        ("Title", "AI Automation Engineer"),
        ("Location", "Karachi, Pakistan"),
        ("Hours", "US Eastern to Pacific"),
        ("Scope", "RAG · Agents · Automation"),
        ("Shipping", "since 2025"),
    ]
    pad = 14
    widths = [max(MONO.width(v, 13), MONO_MED.width(k.upper(), 10, 0.1)) + 2 * pad for k, v in cells]
    scale = W / sum(widths)
    widths = [w * scale for w in widths]
    x = 0
    for i, ((k, v), cw) in enumerate(zip(cells, widths)):
        if i:
            lines.append(line(x, sy, x, H, "hair ln"))
            lines.append(line(x, 0, x, 8, "hair ln"))  # zone tick on the top edge
        texts.append(text(x + pad, sy + 24, k, "mm label"))
        texts.append(text(x + pad, sy + 50, v, "m cell"))
        x += cw

    label = "Moosa Memon, AI automation engineer. I build AI systems that survive production. Karachi, Pakistan, working US hours. RAG, agents, automation."
    return svg(W, H, css, body + "".join(lines) + body_extra + "".join(texts), label)


# ------------------------------------------------------------ buttons ------

def button(theme: str, label: str, primary=False) -> str:
    t = THEMES[theme]
    size, tr, h = 11.5, 0.08, 34
    tw = MONO_MED.width(label.upper(), size, tr)
    w = round(tw + 32)
    css = base_css(t, [MONO_MED]) + f".l{{font-size:{size}px;letter-spacing:{tr}em;text-transform:uppercase}}"
    if primary:
        body = f'<rect x="0" y="0" width="{w}" height="{h}" fill="{t["ink"]}"/>'
        body += text(w / 2, 22, label.upper(), "mm l onink", anchor="middle")
    else:
        body = f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="none" stroke="{t["ink"]}" stroke-width="1"/>'
        body += text(w / 2, 22, label.upper(), "mm l", anchor="middle")
    return svg(w, h, css, body, label)


# --------------------------------------------------------------- rows ------

SYSTEMS = [
    dict(slug="customer-ops-agent", type="Agents",
         title="A support agent that asks before it acts",
         stack="LangGraph / MCP / FastAPI / Qdrant / Langfuse",
         figure="0%", hook="false-action rate on a 44-case golden set, enforced as a CI gate"),
    dict(slug="fintex", type="Agents",
         title="A financial research agent for the PSX that shows its sources",
         stack="FastAPI / Gemini / Qdrant / Supabase / React",
         figure="20 / 20", hook="router accuracy with 0% wrong routes, from 13.6 and 32% before the rewrite"),
    dict(slug="beachhead", type="Environmental",
         title="Flagging invasive species a year before official detection",
         stack="Python / FastAPI / GBIF API / WorldClim",
         figure="5 of 7", hook="real invasions flagged 12 to 36 months before official first detection"),
    dict(slug="autopricer", type="ML Systems",
         title="A price prediction API that explains every rupee",
         stack="FastAPI / scikit-learn / SHAP / Redis / Grafana",
         figure="730 → 380 ms", hook="median latency after the cache, 0 failures at 20 users, R² 0.94"),
    dict(slug="verify-bridge", type="Agents",
         title="A support agent that can't touch an account it hasn't verified",
         stack="Dify / n8n / FastAPI / Qdrant / Langfuse",
         figure="403", hook="on every bypass, prompt or webhook, with a denial in the audit log"),
    dict(slug="ops-relay", type="Agents",
         title="An ops hub where the AI can't certify its own claims",
         stack="LangGraph / Claude API / n8n / Supabase / Slack",
         figure="117 tests", hook="on the real pipeline; a fact is verified only if the platform sent it"),
    dict(slug="converse-iq", type="Agents",
         title="A WhatsApp booking agent that cannot double-book",
         stack="FastAPI / Gemini / Qdrant / WhatsApp Cloud API",
         figure="145 tests", hook="offline; any wrong-date booking fails the eval run outright"),
    dict(slug="doclens", type="RAG",
         title="Answers from your PDFs, with the source highlighted on the page",
         stack="FastAPI / LangChain / ChromaDB / React / Groq",
         figure="page-level", hook="citations on every answer; declines instead of guessing"),
]


def row(theme: str, i: int, s: dict) -> str:
    t = THEMES[theme]
    H = 114
    css = base_css(t, [DISPLAY, MONO, MONO_MED]) + """
.title{font-size:21px;letter-spacing:-.01em} .fig{font-size:28px;letter-spacing:-.01em}
.small{font-size:11.5px} .num{font-size:12px}
"""
    tx, fx, rx = 56, 548, W - 8
    parts = [text(8, 36, f"{i:02d}", "mm num faint")]
    tl = DISPLAY.wrap(s["title"], 21, fx - - 24)
    for j, ln in enumerate(tl[:2]):
        parts.append(text(tx, 36 + j * 25, ln, "d title"))
    parts.append(text(tx, 92, s["stack"], "m small faint"))
    parts.append(text(fx, 38, s["figure"], "d fig accent"))
    hl = MONO.wrap(s["hook"], 11.5, rx - fx - 8)
    for j, ln in enumerate(hl[:3]):
        parts.append(text(fx, 62 + j * 16, ln, "m small muted"))
    parts.append(text(rx, 36, s["type"], "mm label", anchor="end"))
    parts.append(text(rx, 92, "case study →", "mm label accent", anchor="end"))
    parts.append(line(0, H - 0.5, W, H - 0.5, "hair"))
    label = f"{i:02d}. {s['title']}. {s['figure']} {s['hook']}. {s['stack']}."
    return svg(W, H, css, "".join(parts), label)


# ---------------------------------------------------------------- cta ------

def cta(theme: str) -> str:
    t = THEMES[theme]
    H = 128
    css = base_css(t, [DISPLAY, MONO, MONO_MED]) + anim_css() + """
.h{font-size:26px;letter-spacing:-.01em} .sub{font-size:12.5px}
.l{font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
"""
    body = f'<rect x="0" y="0" width="{W}" height="{H}" fill="{t["paper"]}"/>'
    body += f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" class="rule ln" pathLength="1"/>'
    body += text(28, 56, "Bring me the problem, leave with how I'd build it.", "d h")
    body += text(28, 86, "20 minutes, no pitch. Replies within 12 hours.", "m sub muted")
    lbl = "Book a call  →"
    bw = MONO_MED.width(lbl.upper(), 11.5, 0.08) + 36
    bx = W - 28 - bw
    body += f'<rect x="{bx:.1f}" y="{(H-38)/2:.1f}" width="{bw:.1f}" height="38" fill="{t["ink"]}"/>'
    body += text(bx + bw / 2, H / 2 + 4, lbl.upper(), "mm l onink", anchor="middle")
    return svg(W, H, css, body, "Bring me the problem, leave with how I'd build it. 20 minutes, no pitch. Book a call.")


# --------------------------------------------------------------- main ------

BUTTONS = [
    ("website", "moosamemon.me", False),
    ("linkedin", "LinkedIn", False),
    ("x", "X / @moosamemonn", False),
    ("email", "Email", False),
    ("call", "Book a call", True),
]

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for theme in THEMES:
        write("hero", theme, hero(theme))
        for key, label, primary in BUTTONS:
            write(f"btn-{key}", theme, button(theme, label, primary))
        for i, s in enumerate(SYSTEMS, 1):
            write(f"row-{s['slug']}", theme, row(theme, i, s))
        write("cta", theme, cta(theme))
