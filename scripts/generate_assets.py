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
    <radialGradient id="cyanGlow"><stop stop-color="#00b8d4" stop-opacity=".23"/><stop offset="1" stop-color="#06060a" stop-opacity="0"/></radialGradient>
    <radialGradient id="violetGlow"><stop stop-color="#8b5cf6" stop-opacity=".24"/><stop offset="1" stop-color="#06060a" stop-opacity="0"/></radialGradient>
    <linearGradient id="edge"><stop stop-color="#72e5d6"/><stop offset=".5" stop-color="#b9a0ff"/><stop offset="1" stop-color="#263244"/></linearGradient>
    <clipPath id="card"><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="18"/></clipPath>
  </defs>
  <style>
    .reveal {{ opacity: 1; }}
    @keyframes reveal {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: no-preference) {{
      .reveal {{ animation: reveal .22s ease-out both; }}
      .ambient {{ animation: drift 10s ease-in-out infinite alternate; }}
      .ambient-alt {{ animation: drift 12s ease-in-out infinite alternate-reverse; }}
      @keyframes drift {{ from {{ transform: translate(0, 0); }} to {{ transform: translate(15px, -10px); }} }}
    }}
  </style>
  <rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="18" fill="#06060a" stroke="#202036"/>
  <g clip-path="url(#card)">{body}</g>
</svg>
'''


def hero(mobile=False):
    width, height = (480, 360) if mobile else (960, 340)
    cx = width / 2
    body = f'<ellipse class="ambient" cx="{width*.18}" cy="{height*.85}" rx="320" ry="220" fill="url(#cyanGlow)"/>'
    body += f'<ellipse class="ambient-alt" cx="{width*.80}" cy="55" rx="340" ry="230" fill="url(#violetGlow)"/>'
    for radius in (68, 115, 174, 226):
        body += f'<circle cx="{cx}" cy="{height/2}" r="{radius}" stroke="#00e5ff" stroke-opacity=".035" fill="none"/>'
    center = 'text-anchor="middle"'
    body += reveal(text(cx, 56 if mobile else 78, "FULL STACK ENGINEER", 11 if mobile else 12, "#8ba9be", center + ' letter-spacing="5"'), .08)
    body += reveal(text(cx, 126 if mobile else 153, "Jowhar", 64 if mobile else 76, "#ffffff", center + ' font-weight="800" letter-spacing="-2"', mono=False), .25)
    if mobile:
        body += reveal(text(cx, 166, "> Web apps · Backend systems", 16, "#b8c0dd", center), .45)
        badges = [("Full-Stack Development", 206), ("Backend Systems", 184), ("API Integrations", 184), ("Product Engineering", 206)]
        positions = [(39, 205), (257, 205), (39, 249), (235, 249)]
    else:
        body += reveal(text(cx, 198, "> Web applications · Backend systems · Product engineering _", 16, "#b8c0dd", center), .45)
        badges = [("Full-Stack Development", 210), ("Backend Systems", 176), ("API Integrations", 168), ("Product Engineering", 192)]
        positions = [(91, 236), (311, 236), (497, 236), (675, 236)]
    for index, ((label, badge_width), (x, y)) in enumerate(zip(badges, positions)):
        chip = f'<rect x="{x}" y="{y}" width="{badge_width}" height="31" rx="15.5" fill="#00e5ff" fill-opacity=".035" stroke="#00e5ff" stroke-opacity=".16"/>'
        chip += text(x+badge_width/2, y+20, label, 12, "#9ac2ce", center, mono=False)
        body += reveal(chip, .6 + index*.1)
    body += reveal(text(cx, 328 if mobile else 310, "KERALA, INDIA  /  @JOWHARR", 10, "#8c93ad", center + ' letter-spacing="2"'), 1)
    return canvas(width, height, "Jowhar | Full Stack Engineer", "Full-stack development, backend systems, API integrations and product engineering. Based in Kerala, India.", body)


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
    body += f'<path d="M1 54 H{width-1}" stroke="#202036"/>'
    body += reveal(text(28, 93, "~", 16, "violet") + text(47, 93, "$", 16, "cyan") + text(68, 93, "whoami --full", 16), .1)
    body += f'<path d="M28 115 H{width-28}" stroke="#202036" stroke-dasharray="2 5"/>'
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
            (618, "jowhar.dev@gmail.com", "text", 18),
            (648, "github.com/jowharr", "muted", 18),
            (678, "linkedin.com/in/jowharr", "muted", 18),
        ]
        for index, (y, value, color, size) in enumerate(rows):
            body += reveal(text(28, y + 360, value, size, color), 2.9 + index * .07)
        footer_y, end_delay = 1106, 4.1
    else:
        body += portrait(36, 169, start_delay=.6)
        body += reveal(text(139, 518, "J O W H A R", 12, "muted", 'text-anchor="middle"'), 2.9)
        body += '<path d="M290 146 V546" stroke="#202036"/>'
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
            (537, "Contact", "jowhar.dev@gmail.com", "cyan"),
        ]
        for index, (y, label, value, color) in enumerate(rows):
            if label:
                content = text(x, y, label, 15, "muted") + text(x+108, y, ":", 15, "muted") + text(x+131, y, value, 15, color)
            else:
                content = text(x, y, value, 20 if index == 0 else 13, color, 'letter-spacing="1"')
            body += reveal(content, .45 + (y - 145)*.0065)
        footer_y, end_delay = 599, 3.35
    body += f'<path d="M28 {footer_y-28} H{width-28}" stroke="#202036"/>'
    body += reveal(text(28, footer_y, "$", 16, "cyan") + text(49, footer_y, "let’s build something.", 15, "muted") + f'<rect x="262" y="{footer_y-13}" width="8" height="17" rx="1" fill="#72e5d6"/>', end_delay)
    return canvas(width, height, "Jowhar's terminal profile", "An animated terminal with an ASCII portrait of Jowhar derived from his photo and a top-to-bottom introduction, toolkit, work, and contact details. The complete profile stays visible after the reveal.", body)


def social_button(name, glyph, color):
    width, height = 140, 44
    body = f'<rect x=".5" y=".5" width="139" height="43" rx="11" fill="#0a0a12" stroke="{color}" stroke-opacity=".5"/>'
    if name == "GitHub":
        body += f'<g transform="translate(12 13) scale(.75)" fill="{color}"><path d="M12 .5C5.86.5.5 5.86.5 12c0 5.25 3.4 9.7 8.12 11.28.6.11.82-.26.82-.58 0-.28-.02-1.23-.02-2.23-3.02.56-3.83-.74-4.08-1.4-.14-.35-.73-1.41-1.25-1.69-.43-.23-1.04-.8-.01-.81.96-.02 1.65.88 1.88 1.26 1.1 1.85 2.85 1.33 3.54 1.01.11-.79.42-1.34.76-1.64-2.66-.31-5.45-1.33-5.45-5.92 0-1.31.47-2.38 1.24-3.22-.12-.31-.54-1.54.12-3.2 0 0 1.01-.32 3.3 1.23.96-.27 1.99-.4 3.01-.4s2.05.14 3.02.4c2.28-1.55 3.29-1.23 3.29-1.23.66 1.66.24 2.89.12 3.2.77.84 1.23 1.91 1.23 3.22 0 4.61-2.8 5.62-5.48 5.92.43.37.81 1.1.81 2.22 0 1.6-.02 2.89-.02 3.29 0 .32.22.69.83.57A11.5 11.5 0 0 0 23.5 12C23.5 5.86 18.14.5 12 .5Z"/></g>'
    else:
        body += text(21, 28, glyph, 17, color, 'text-anchor="middle" font-weight="600"')
    body += text(43, 28, name, 14, "#c9d0e7", mono=False)
    return canvas(width, height, name, f"Connect with Jowhar on {name}.", body)


def footer(mobile=False):
    width = 480 if mobile else 960
    cx = width/2
    body = f'<ellipse class="ambient" cx="{cx}" cy="60" rx="340" ry="110" fill="url(#violetGlow)"/>'
    for x, color in ((cx-13, "#00e5ff"), (cx, "#8b5cf6"), (cx+13, "#ec4899")):
        body += f'<circle cx="{x}" cy="33" r="2.5" fill="{color}"/>'
    body += text(cx, 68, "JOWHAR · BUILT WITH CURIOSITY", 11, "#9197af", 'text-anchor="middle" letter-spacing="2"')
    return canvas(width, 100, "Built with curiosity", "Jowhar — full stack engineer.", body)


def main():
    OUT.mkdir(exist_ok=True)
    for name, content in {
        "hero.svg": hero(), "hero-mobile.svg": hero(True),
        "terminal.svg": terminal(), "terminal-mobile.svg": terminal(True),
        "link-github.svg": social_button("GitHub", "⌘", "#00e5ff"),
        "link-linkedin.svg": social_button("LinkedIn", "in", "#7ab8f1"),
        "link-portfolio.svg": social_button("Portfolio", "↗", "#ad8df5"),
        "link-email.svg": social_button("Email", "@", "#ef91b3"),
        "footer.svg": footer(), "footer-mobile.svg": footer(True),
    }.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"Generated assets/{name}")
    from generate_stack import main as generate_stack
    generate_stack()
    from generate_focus import main as generate_focus
    generate_focus()


if __name__ == "__main__":
    main()
