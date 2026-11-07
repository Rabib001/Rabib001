"""Generates the SVG assets for the GitHub profile README.

Run:  python build.py   (rewrites ./assets)
Each asset comes in a -dark and -light version that match GitHub's own
colors; the README picks one with <picture> based on the viewer's theme.
"""
from pathlib import Path
from html import escape
import shutil
import textwrap

OUT = Path(__file__).parent / "assets"
shutil.rmtree(OUT, ignore_errors=True)
(OUT / "cards").mkdir(parents=True)

MONO = "'SF Mono','Cascadia Code',Consolas,'Liberation Mono',Menlo,monospace"
SANS = "-apple-system,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"

# GitHub's own palette (Primer), so the graphics sit in the page instead of on top of it.
THEMES = {
    "dark":  dict(bg="#0d1117", border="#30363d", fg="#e6edf3", dim="#8b949e", accent="#3fb950", link="#4493f8"),
    "light": dict(bg="#ffffff", border="#d0d7de", fg="#1f2328", dim="#59636e", accent="#1a7f37", link="#0969da"),
}
LANG = {"Python": "#3572A5", "TypeScript": "#3178c6", "JavaScript": "#f1e05a"}


def frame(w, h, t, body, defs=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
<defs>{defs}</defs>
<style>
  .fade{{opacity:0;animation:fade .4s ease-out forwards}}
  .blink{{animation:blink 1.1s steps(1) infinite}}
  @keyframes fade{{to{{opacity:1}}}}
  @keyframes blink{{50%{{opacity:0}}}}
</style>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="6" fill="{t['bg']}" stroke="{t['border']}"/>
{body}
</svg>
"""


def write(name, svg):
    (OUT / name).write_text(svg, encoding="utf-8")


def header(mode, t):
    W, H = 900, 210
    cmd = "whoami"
    cw = 9.0  # approx monospace advance at 15px
    body = f"""
<g fill="{t['border']}"><circle cx="22" cy="20" r="5"/><circle cx="38" cy="20" r="5"/><circle cx="54" cy="20" r="5"/></g>
<line x1="0" y1="40" x2="{W}" y2="40" stroke="{t['border']}"/>
<g font-family="{MONO}" font-size="15">
  <text x="28" y="74" fill="{t['accent']}">$</text>
  <text x="46" y="74" fill="{t['fg']}" clip-path="url(#type)">{cmd}</text>
</g>
<g class="fade" style="animation-delay:1.1s">
  <text x="28" y="122" font-family="{SANS}" font-size="34" font-weight="600" fill="{t['fg']}">Rabib Husain</text>
  <text x="28" y="150" font-family="{MONO}" font-size="14.5" fill="{t['dim']}">software engineer · austin, tx</text>
</g>
<g class="fade" style="animation-delay:1.5s" font-family="{MONO}" font-size="15">
  <text x="28" y="186" fill="{t['accent']}">$</text>
  <rect x="46" y="173" width="9" height="17" fill="{t['dim']}" class="blink"/>
</g>"""
    steps = ";".join(str(round(i * cw)) for i in range(len(cmd) + 1))
    defs = f"""<clipPath id="type"><rect x="46" y="56" width="0" height="26">
  <animate attributeName="width" begin="0.3s" dur="0.6s" fill="freeze" calcMode="discrete" values="{steps}"/>
</rect></clipPath>"""
    write(f"header-{mode}.svg", frame(W, H, t, body, defs))


PROJECTS = [
    ("relay", "relay", "Cal Hacks '25",
     "Keeps PMs and engineers in sync across Slack, GitHub and Snowflake, with live WebSocket updates.",
     ["Python", "TypeScript"]),
    ("autoboard", "AutoBoard", "HackUTD '25",
     "Vendor onboarding prototype. Textract reads vendor documents and a Lambda function scores them.",
     ["Python", "JavaScript"]),
    ("waste0", "waste.0", "HackUTA '24",
     "Estimates food spoilage for restaurants and suggests surplus to donate to local charities, with a Next.js dashboard.",
     ["TypeScript", "Python"]),
]


def card(mode, t, slug, title, event, desc, langs):
    W, H = 290, 146
    body = [
        f'<path d="M20 22.5h9.5a1.5 1.5 0 0 1 1.5 1.5v11h-9.5A1.5 1.5 0 0 0 20 36.5zm0 0V36.5M23 26h5M23 29h5" stroke="{t["dim"]}" stroke-width="1.3" stroke-linecap="round"/>',
        f'<text x="40" y="34" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["link"]}">{escape(title)}</text>',
        f'<rect x="{W-20-len(event)*6.6-14:.0f}" y="21" width="{len(event)*6.6+14:.0f}" height="18" rx="9" stroke="{t["border"]}"/>',
        f'<text x="{W-20-(len(event)*6.6+14)/2:.0f}" y="34" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{t["dim"]}">{escape(event)}</text>',
    ]
    for i, ln in enumerate(textwrap.wrap(desc, 40)[:3]):
        body.append(f'<text x="20" y="{62+i*18}" font-family="{SANS}" font-size="12.5" fill="{t["dim"]}">{escape(ln)}</text>')
    x = 20
    for lang in langs:
        body.append(f'<circle cx="{x+5}" cy="{H-20}" r="5" fill="{LANG[lang]}"/>'
                    f'<text x="{x+15}" y="{H-16}" font-family="{SANS}" font-size="11.5" fill="{t["dim"]}">{lang}</text>')
        x += 15 + len(lang) * 6.6 + 14
    write(f"cards/{slug}-{mode}.svg", frame(W, H, t, "\n".join(body)))


if __name__ == "__main__":
    for mode, t in THEMES.items():
        header(mode, t)
        for p in PROJECTS:
            card(mode, t, *p)
    print("wrote", sorted(str(p.relative_to(OUT)) for p in OUT.rglob("*.svg")))
