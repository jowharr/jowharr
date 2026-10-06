#!/usr/bin/env python3
"""Build self-contained GitHub README artwork with Python's standard library."""

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif"
COLORS = {"text": "#e6edf3", "muted": "#91a3b7", "cyan": "#72e5d6", "violet": "#b9a0ff", "gold": "#e8ba83"}


def text(x, y, value, size=16, color="text", extra="", mono=True):
    return (f'<text x="{x}" y="{y}" fill="{COLORS.get(color, color)}" '
            f'font-family="{MONO if mono else SANS}" font-size="{size}" {extra}>'
            f'{escape(value)}</text>')


def reveal(content, delay):
    return f'<g class="reveal" style="animation-delay:{delay:.2f}s">{content}</g>'


def canvas(width, height, title, description, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(description)}</desc>
  <defs>
    <radialGradient id="cyanGlow"><stop stop-color="#2d898d" stop-opacity=".2"/><stop offset="1" stop-color="#0d1117" stop-opacity="0"/></radialGradient>
    <radialGradient id="violetGlow"><stop stop-color="#7956aa" stop-opacity=".2"/><stop offset="1" stop-color="#0d1117" stop-opacity="0"/></radialGradient>
    <linearGradient id="edge"><stop stop-color="#72e5d6"/><stop offset=".5" stop-color="#b9a0ff"/><stop offset="1" stop-color="#263244"/></linearGradient>
    <clipPath id="card"><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="18"/></clipPath>
  </defs>
  <style>
    .reveal {{ opacity: 1; }}
    @keyframes reveal {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: no-preference) {{
      .reveal {{ animation: reveal .22s ease-out both; }}
    }}
  </style>
  <rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="18" fill="#0d1117" stroke="#263244"/>
  <g clip-path="url(#card)">{body}</g>
</svg>
'''


def hero(mobile=False):
    width, height = (480, 300) if mobile else (960, 290)
    x = 28 if mobile else 48
    body = f'<ellipse cx="{width*.85}" cy="70" rx="310" ry="220" fill="url(#violetGlow)"/>'
    body += f'<ellipse cx="60" cy="{height}" rx="380" ry="230" fill="url(#cyanGlow)"/>'
    body += f'<path d="M{x} 1 H{width-x}" stroke="url(#edge)" stroke-width="2"/>'
    body += reveal(text(x, 49, "FULL-STACK DEVELOPER", 12, "cyan", 'letter-spacing="3"'), .08)
    body += reveal(text(x-3, 129, "Jowhar", 72 if mobile else 82, extra='font-weight="700" letter-spacing="-4"', mono=False), .25)
    body += reveal(text(x, 171, "From idea to working software.", 21 if mobile else 24, mono=False), .48)
    body += reveal(text(x, 204, "Web apps / Backend systems / APIs", 13 if mobile else 16, "muted"), .70)
    body += reveal(text(x, 262 if mobile else 256, "KERALA, INDIA", 11, "muted", 'letter-spacing="2"'), .86)
    if not mobile:
        body += reveal(text(735, 256, "@jowharr", 13, "cyan"), .95)
        body += '<g stroke="#72e5d6" fill="none" stroke-width="1" opacity=".14"><path d="M748 65 H862 V162 Q862 206 811 206 Q760 206 760 163"/><path d="M736 53 H850 V150 Q850 194 799 194 Q748 194 748 151"/><path d="M724 41 H838 V138 Q838 182 787 182 Q736 182 736 139"/></g>'
    return canvas(width, height, "Jowhar | Full-Stack Developer", "Web applications, backend systems, and APIs. Based in Kerala, India.", body)


def portrait(x, y, width=232, row_height=5.1, start_delay=.45):
    """Render the supplied photo as native SVG text rows."""
    rows = (OUT / "portrait.txt").read_text(encoding="utf-8").splitlines()
    parts = []
    for index, line in enumerate(rows):
        baseline = y + index * row_height
        extra = f'xml:space="preserve" textLength="{width}" lengthAdjust="spacingAndGlyphs"'
        parts.append(reveal(
            text(x, baseline, line, 6.2, "cyan", extra),
            start_delay + index * .036,
        ))
    return "".join(parts)


def terminal(mobile=False):
    width, height = (480, 1142) if mobile else (960, 634)
    body = f'<path d="M1 18 Q1 1 18 1 H{width-18} Q{width-1} 1 {width-1} 18 V54 H1Z" fill="#141b26"/>'
    for x, color in [(25, "#f07883"), (44, "#e8ba83"), (63, "#72e5d6")]:
        body += f'<circle cx="{x}" cy="28" r="4.5" fill="{color}"/>'
    body += text(width/2, 33, "jowhar — profile.sh", 12, "muted", 'text-anchor="middle"')
    body += f'<path d="M1 54 H{width-1}" stroke="#263244"/>'
    body += reveal(text(28, 93, "~", 16, "violet") + text(47, 93, "$", 16, "cyan") + text(68, 93, "whoami --full", 16), .1)
    body += f'<path d="M28 115 H{width-28}" stroke="#263244" stroke-dasharray="2 5"/>'
    if mobile:
        body += portrait(124, 146, start_delay=.35)
        body += reveal(text(240, 482, "J O W H A R", 12, "muted", 'text-anchor="middle"'), 2.7)
        rows = [
            (154, "jowhar@github", "cyan", 21),
            (186, "Senior Full-Stack Developer", "text", 20),
            (215, "Kerala, India / working remotely", "muted", 18),
            (264, "01 / STACK", "gold", 13),
            (298, "React · Next.js · TypeScript", "text", 18),
            (328, "Node.js · Express · REST APIs", "text", 18),
            (358, "MongoDB · PostgreSQL · Redis", "text", 18),
            (388, "Docker · NGINX · CI/CD", "text", 18),
            (439, "02 / BUILDING", "gold", 13),
            (473, "Web apps & backend systems", "text", 18),
            (503, "ERP platforms & dashboards", "text", 18),
            (533, "Mobile backends & integrations", "text", 18),
            (584, "03 / CONTACT", "gold", 13),
            (618, "mohdalijowhar@gmail.com", "text", 18),
            (648, "github.com/jowharr", "muted", 18),
            (678, "linkedin.com/in/jowharr", "muted", 18),
        ]
        for index, (y, value, color, size) in enumerate(rows):
            body += reveal(text(28, y + 360, value, size, color), 2.9 + index * .07)
        footer_y, end_delay = 1106, 4.1
    else:
        body += portrait(36, 169, start_delay=.6)
        body += reveal(text(139, 518, "J O W H A R", 12, "muted", 'text-anchor="middle"'), 2.9)
        body += '<path d="M290 146 V546" stroke="#263244"/>'
        x = 325
        rows = [
            (155, None, "jowhar@github", "cyan"),
            (190, "Role", "Senior Full-Stack Developer", "text"),
            (219, "Based in", "Kerala, India / remote", "text"),
            (265, None, "01 / STACK", "gold"),
            (297, "Frontend", "React · Next.js · TypeScript", "text"),
            (326, "Backend", "Node.js · Express · REST APIs", "text"),
            (355, "Data", "MongoDB · PostgreSQL · Redis", "text"),
            (384, "Infra", "Docker · NGINX · CI/CD", "text"),
            (430, None, "02 / BUILDING", "gold"),
            (462, "Systems", "Web apps · ERP · Dashboards", "text"),
            (491, "APIs", "Mobile backends · Integrations", "text"),
            (537, "Contact", "mohdalijowhar@gmail.com", "cyan"),
        ]
        for index, (y, label, value, color) in enumerate(rows):
            if label:
                content = text(x, y, label, 15, "muted") + text(x+108, y, ":", 15, "muted") + text(x+131, y, value, 15, color)
            else:
                content = text(x, y, value, 20 if index == 0 else 13, color, 'letter-spacing="1"')
            body += reveal(content, .45 + (y - 145)*.0065)
        footer_y, end_delay = 599, 3.35
    body += f'<path d="M28 {footer_y-28} H{width-28}" stroke="#263244"/>'
    body += reveal(text(28, footer_y, "$", 16, "cyan") + text(49, footer_y, "let’s build something.", 15, "muted") + f'<rect x="262" y="{footer_y-13}" width="8" height="17" rx="1" fill="#72e5d6"/>', end_delay)
    return canvas(width, height, "Jowhar's terminal profile", "An animated terminal with an ASCII portrait of Jowhar derived from his photo and a top-to-bottom introduction, toolkit, work, and contact details. The complete profile stays visible after the reveal.", body)


def main():
    OUT.mkdir(exist_ok=True)
    for name, content in {
        "hero.svg": hero(), "hero-mobile.svg": hero(True),
        "terminal.svg": terminal(), "terminal-mobile.svg": terminal(True),
    }.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"Generated assets/{name}")
    from generate_stack import main as generate_stack
    generate_stack()


if __name__ == "__main__":
    main()
