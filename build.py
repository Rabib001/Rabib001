"""Generates the SVG assets for the GitHub profile README.

Run:  python build.py   (writes into ./assets)
Every asset carries its own dark background, so it reads the same in
GitHub's light and dark themes.
"""
from pathlib import Path
from html import escape
import textwrap

OUT = Path(__file__).parent / "assets"
(OUT / "cards").mkdir(parents=True, exist_ok=True)

MONO = "'SF Mono','Cascadia Code',Consolas,'Liberation Mono',Menlo,monospace"
SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"

BG0, BG1 = "#0a0e17", "#111827"
LINE = "#1f2937"
TXT, DIM, MUTED = "#e5e7eb", "#9ca3af", "#6b7280"
VIOLET, CYAN, GREEN, AMBER, PINK = "#a78bfa", "#22d3ee", "#4ade80", "#fbbf24", "#f472b6"


def frame(w, h, body, defs="", style=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" stroke="#ffffff" stroke-opacity=".035"/></pattern>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
  {defs}
</defs>
<style>
  .fade{{opacity:0;animation:fade .5s ease-out forwards}}
  .up{{opacity:0;animation:up .6s cubic-bezier(.2,.8,.2,1) forwards}}
  .blink{{animation:blink 1s steps(1) infinite}}
  .pulse{{animation:pulse 6s ease-in-out infinite}}
  .twinkle{{opacity:0;animation:twinkle 3.2s ease-in-out infinite}}
  @keyframes fade{{to{{opacity:1}}}}
  @keyframes up{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
  @keyframes blink{{50%{{opacity:0}}}}
  @keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:.6}}}}
  @keyframes twinkle{{0%,70%,100%{{opacity:0;transform:scale(.4)}}80%{{opacity:1;transform:scale(1)}}}}
  {style}
</style>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="url(#bg)" stroke="{LINE}"/>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="url(#grid)"/>
{body}
</svg>
"""


def write(name, svg):
    (OUT / name).write_text(svg, encoding="utf-8")


# ---------------------------------------------------------------- header
def header():
    W, H = 900, 400
    rows = [
        ("education", "UT Arlington · Honors B.S. Computer Science '26"),
        ("role[0]", "Founding Engineer @ Spaceodd"),
        ("role[1]", "ML/LLM Intern @ University Lands / UT System"),
        ("focus", "LLM agents · multi-agent systems · backend infra"),
        ("trophies", "7 hackathon wins, incl. Cal Hacks"),
        ("location", "Austin, TX"),
    ]
    y0, step, t0, dt = 104, 25, 1.9, 0.35
    lines = []
    for i, (k, v) in enumerate(rows):
        y, d = y0 + i * step, t0 + i * dt
        lines.append(
            f'<g class="fade" style="animation-delay:{d:.2f}s" font-family="{MONO}" font-size="14.5">'
            f'<text x="34" y="{y}" fill="{CYAN}">→</text>'
            f'<text x="56" y="{y}" fill="{MUTED}">{escape(k)}</text>'
            f'<text x="170" y="{y}" fill="{TXT}">{escape(v)}</text>'
            f'<text x="866" y="{y}" fill="{GREEN}" text-anchor="end">ok</text></g>'
        )
    t_name = t0 + len(rows) * dt + 0.35
    cmd = 'orchestrator run --task "introduce rabib"'
    body = f"""
<circle cx="140" cy="60" r="140" fill="{VIOLET}" filter="url(#blur)" class="pulse"/>
<circle cx="800" cy="360" r="150" fill="{CYAN}" filter="url(#blur)" class="pulse" style="animation-delay:-3s"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{BG0}" fill-opacity=".55"/>
<line x1="0" y1="44" x2="{W}" y2="44" stroke="{LINE}"/>
<circle cx="26" cy="22" r="6" fill="#ff5f57"/><circle cx="46" cy="22" r="6" fill="#febc2e"/><circle cx="66" cy="22" r="6" fill="#28c840"/>
<text x="{W/2}" y="27" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{MUTED}">rabib@austin: ~/agents</text>
<g font-family="{MONO}" font-size="15">
  <text x="34" y="74" fill="{GREEN}">$</text>
  <text x="52" y="74" fill="{TXT}" clip-path="url(#type)">{escape(cmd)}</text>
</g>
<g class="fade" style="animation-delay:{t_name:.2f}s">
  <line x1="34" y1="268" x2="866" y2="268" stroke="{LINE}" stroke-dasharray="4 6"/>
</g>
<g class="up" style="animation-delay:{t_name:.2f}s">
  <text x="32" y="330" font-family="{SANS}" font-size="54" font-weight="800" letter-spacing="-1.5" fill="url(#name)">Rabib Husain</text>
</g>
<g class="up" style="animation-delay:{t_name+0.3:.2f}s" font-family="{MONO}" font-size="15">
  <text x="34" y="368" fill="{DIM}">I build LLM agents, and the backends they run on.</text>
</g>
<rect x="{34+50*9.1+6:.0f}" y="355" width="9" height="17" fill="{GREEN}" class="blink"/>
{''.join(lines)}
"""
    defs = f"""
  <clipPath id="type"><rect x="52" y="56" width="0" height="26">
    <animate attributeName="width" from="0" to="{len(cmd)*9.4:.0f}" begin="0.3s" dur="1.3s" fill="freeze" calcMode="discrete"
      values="{';'.join(str(round(i*9.4)) for i in range(len(cmd)+1))}"/>
  </rect></clipPath>
  <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{VIOLET}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{GREEN}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-0.3 0;0.3 0;-0.3 0" dur="8s" repeatCount="indefinite"/>
  </linearGradient>"""
    write("header.svg", frame(W, H, body, defs))


# ---------------------------------------------------------------- stats
def stats():
    W, H = 900, 116
    tiles = [
        ("7×", "hackathon wins", "incl. Cal Hacks", AMBER),
        ("70+", "beta users at the", "Spaceodd launch", VIOLET),
        ("8", "developers run the agent", "orchestrator I built", CYAN),
        ("3.5 yrs", "teaching CS as a", "PLTL peer leader", GREEN),
    ]
    tw, gap, pad = 204, 12, 18
    out = []
    for i, (num, a, b, c) in enumerate(tiles):
        x = pad + i * (tw + gap)
        out.append(f"""<g class="up" style="animation-delay:{0.15*i:.2f}s">
  <rect x="{x}" y="16" width="{tw}" height="84" rx="12" fill="#ffffff" fill-opacity=".03" stroke="{LINE}"/>
  <rect x="{x}" y="30" width="3" height="56" rx="1.5" fill="{c}"/>
  <text x="{x+20}" y="60" font-family="{SANS}" font-size="30" font-weight="800" fill="{c}">{escape(num)}</text>
  <text x="{x+20}" y="78" font-family="{MONO}" font-size="11.5" fill="{DIM}">{escape(a)}</text>
  <text x="{x+20}" y="92" font-family="{MONO}" font-size="11.5" fill="{DIM}">{escape(b)}</text>
</g>""")
    write("stats.svg", frame(W, H, "\n".join(out)))


# ---------------------------------------------------------------- trophies
def trophies():
    W, H = 900, 270
    wins = [
        ("CAL HACKS", "Relay · '25"),
        ("HACKUTD", "AutoBoard · '25"),
        ("HACKTX", "FleetPulse · '24"),
        ("HACKUTA", "Waste.0 · '24"),
        ("HACKSMU", "LegalAI"),
        ("+2 MORE", "and counting"),
    ]
    shelf = 182
    cup = (
        '<path d="M-28,-70 H28 V-52 C28,-26 15,-13 0,-11 C-15,-13 -28,-26 -28,-52 Z" fill="url(#gold)"/>'
        '<path d="M-28,-62 C-48,-62 -48,-32 -22,-30 M28,-62 C48,-62 48,-32 22,-30" stroke="url(#gold)" stroke-width="5" fill="none"/>'
        '<path d="M-16,-64 V-50 C-16,-36 -10,-26 -4,-22" stroke="#fff" stroke-opacity=".45" stroke-width="4" stroke-linecap="round" fill="none"/>'
        '<rect x="-5" y="-12" width="10" height="20" fill="url(#gold)"/>'
        '<rect x="-20" y="6" width="40" height="9" rx="2" fill="url(#gold)"/>'
        '<rect x="-30" y="15" width="60" height="17" rx="3" fill="#1c1917" stroke="#44403c"/>'
    )
    ghost = (
        '<path d="M-28,-70 H28 V-52 C28,-26 15,-13 0,-11 C-15,-13 -28,-26 -28,-52 Z" stroke="#57534e" stroke-width="2" stroke-dasharray="5 5"/>'
        '<rect x="-30" y="15" width="60" height="17" rx="3" stroke="#57534e" stroke-width="2" stroke-dasharray="5 5"/>'
    )
    star = '<path d="M0,-9 L2.2,-2.2 L9,0 L2.2,2.2 L0,9 L-2.2,2.2 L-9,0 L-2.2,-2.2 Z" fill="#fff"/>'
    out = [
        f'<ellipse cx="450" cy="{shelf-40}" rx="380" ry="70" fill="{AMBER}" fill-opacity=".10" filter="url(#blur)"/>',
        f'<rect x="40" y="{shelf}" width="820" height="12" rx="3" fill="#292524"/>',
        f'<rect x="40" y="{shelf}" width="820" height="2" fill="#78716c"/>',
        f'<rect x="56" y="{shelf+12}" width="788" height="8" fill="#000" fill-opacity=".35"/>',
    ]
    for i, (name, sub) in enumerate(wins):
        cx = 100 + i * 140
        last = i == len(wins) - 1
        out.append(f'<g class="up" style="animation-delay:{0.12*i:.2f}s">'
                   f'<g transform="translate({cx},{shelf-32})">{ghost if last else cup}</g>'
                   f'<text x="{cx}" y="{shelf+46}" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="1" fill="{MUTED if last else AMBER}">{escape(name)}</text>'
                   f'<text x="{cx}" y="{shelf+64}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{DIM}">{escape(sub)}</text></g>')
        if not last:
            sx, sy = cx + (18 if i % 2 else -16), shelf - 32 - 64 + (i % 3) * 8
            out.append(f'<g transform="translate({sx},{sy})"><g class="twinkle" style="animation-delay:{0.55*i:.2f}s;transform-box:fill-box;transform-origin:center">{star}</g></g>')
    out.append(f'<text x="450" y="34" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{MUTED}">THE TROPHY SHELF</text>')
    defs = f'<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fde68a"/><stop offset=".45" stop-color="{AMBER}"/><stop offset="1" stop-color="#b45309"/></linearGradient>'
    write("trophies.svg", frame(W, H, "\n".join(out), defs))


# ---------------------------------------------------------------- project cards
PROJECTS = [
    ("relay", "Relay", "CAL HACKS WINNER", AMBER,
     "Bridges PMs and engineers by wiring Slack, GitHub and Snowflake together, with real-time WebSocket sync and automated PR creation.",
     ["Python", "Node.js", "Postman Flows", "Snowflake"]),
    ("autoboard", "AutoBoard", "HACKUTD WINNER", AMBER,
     "Vendor onboarding for Goldman Sachs, months down to weeks. Textract OCR pulls fields from vendor docs; Lambda turns them into a credibility score.",
     ["React", "AWS Lambda", "Textract", "SQL"]),
    ("sam", "Fine-tuned SAM", "IoU 0.09 → 0.76", CYAN,
     "Fine-tuned Meta's Segment Anything (ViT-H) to segment mitochondria in electron microscopy, trained with DiceCE loss on CUDA.",
     ["PyTorch", "ViT-H", "CUDA"]),
    ("fleetpulse", "FleetPulse", "HACKTX WINNER", AMBER,
     "Cuts vehicle emissions with eco-friendly routing and maintenance prediction. Deploys and model updates ship through GitHub Actions + Cloudflare.",
     ["Next.js", "Python", "Databricks", "Cloudflare"]),
    ("waste0", "Waste.0", "HACKUTA WINNER", AMBER,
     "Predicts food spoilage and routes surplus to local charities, with a dashboard for order recommendations and daily surplus estimates.",
     ["Next.js", "Python", "MongoDB", "Databricks"]),
    ("legalai", "LegalAI", "HACKSMU WINNER", AMBER,
     "Reviews contracts and legal documents with AI, flagging risks, ambiguities and inconsistencies in seconds.",
     ["TypeScript", "LLMs"]),
]
TAG_COLORS = [VIOLET, CYAN, GREEN, PINK]


def card(slug, title, badge, bc, desc, tags):
    W, H = 440, 190
    bw = len(badge) * 7.2 + 22
    body = [
        f'<circle cx="{W-30}" cy="20" r="70" fill="{bc}" fill-opacity=".22" filter="url(#blur)"/>',
        f'<rect x="20" y="20" width="{bw:.0f}" height="22" rx="11" fill="{bc}" fill-opacity=".12" stroke="{bc}" stroke-opacity=".5"/>',
        f'<text x="{20+bw/2:.0f}" y="35" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing=".5" fill="{bc}">{escape(badge)}</text>',
        f'<text x="{W-22}" y="38" text-anchor="end" font-family="{SANS}" font-size="18" fill="{MUTED}">↗</text>',
        f'<text x="20" y="74" font-family="{SANS}" font-size="22" font-weight="800" fill="{TXT}">{escape(title)}</text>',
    ]
    for i, ln in enumerate(textwrap.wrap(desc, 58)[:3]):
        body.append(f'<text x="20" y="{100+i*19}" font-family="{SANS}" font-size="13" fill="{DIM}">{escape(ln)}</text>')
    x = 20
    for i, t in enumerate(tags):
        w = len(t) * 6.7 + 18
        c = TAG_COLORS[i % len(TAG_COLORS)]
        body.append(f'<rect x="{x:.0f}" y="155" width="{w:.0f}" height="20" rx="5" fill="{c}" fill-opacity=".10"/>'
                    f'<text x="{x+w/2:.0f}" y="169" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{c}">{escape(t)}</text>')
        x += w + 7
    write(f"cards/{slug}.svg", frame(W, H, "\n".join(body)))


# ---------------------------------------------------------------- footer
def footer():
    W, H = 900, 64
    body = f"""<g font-family="{MONO}" font-size="14">
  <text x="28" y="38" fill="{GREEN}">$</text>
  <text x="46" y="38" fill="{TXT}">echo "thanks for scrolling. say hi anytime"</text>
  <rect x="{46+43*8.5+6:.0f}" y="25" width="9" height="17" fill="{GREEN}" class="blink"/>
  <text x="872" y="38" text-anchor="end" fill="{MUTED}">exit 0</text>
</g>"""
    write("footer.svg", frame(W, H, body))


if __name__ == "__main__":
    header(); stats(); trophies(); footer()
    for p in PROJECTS:
        card(*p)
    print("wrote", sorted(str(p.relative_to(OUT)) for p in OUT.rglob("*.svg")))
