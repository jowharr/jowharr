#!/usr/bin/env python3
"""Generate the profile's responsive toolkit artwork using only the standard library."""

from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
GROUPS = (
    ("Languages", (("JavaScript", "#f2d76d"), ("TypeScript", "#7fbbff"), ("HTML", "#ffac86"), ("CSS", "#aca4ff"))),
    ("Frontend", (("React", "#79daf3"), ("Next.js", "#e7edf5"), ("Redux", "#bd9fff"), ("Tailwind CSS", "#72e5d6"), ("Bootstrap", "#b9a0ff"))),
    ("Backend", (("Node.js", "#a0d990"), ("Express", "#d3dae6"), ("REST APIs", "#72e5d6"), ("JWT", "#efa1ca"), ("API integrations", "#a8b8ff"))),
    ("Data", (("MongoDB", "#a0d990"), ("PostgreSQL", "#88bde8"), ("MariaDB", "#e7c39c"), ("Redis", "#f3939c"), ("Mongoose", "#d9a0a5"), ("Prisma", "#b9a0ff"), ("Drizzle", "#c6e992"))),
    ("Infrastructure", (("Docker", "#7fbbff"), ("NGINX", "#a0d990"), ("CI/CD", "#72e5d6"), ("DNS", "#b9a0ff"), ("SSL", "#e8cd92"), ("Git", "#ffac86"))),
    ("Workspace", (("Postman", "#ffac86"), ("VS Code", "#7fbbff"), ("Vercel", "#e7edf5"), ("Heroku", "#b9a0ff"), ("GitHub", "#d3dae6"))),
)


def text_width(label, size):
    """Conservative system-sans advance estimates keep labels clear of chip edges."""
    narrow = set("ijlI.,:;!|' ")
    wide = set("MW@%")
    units = sum(0.31 if c in narrow else 0.86 if c in wide else 0.66 if c.isupper() else 0.57 for c in label)
    return round(units * size)


def chip_rows(tools, available, size):
    rows = [[]]
    used = 0
    for label, color in tools:
        width = text_width(label, size) + 38
        gap = 9 if rows[-1] else 0
        if used + gap + width > available:
            rows.append([])
            used, gap = 0, 0
        rows[-1].append((label, color, width))
        used += gap + width
    return rows


def label(x, y, content, size=16, color="#dce6f3", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{escape(content)}</text>'


def render(mobile=False):
    width, padding, columns = (480, 24, 1) if mobile else (960, 36, 2)
    gap, inset = (14, 22) if mobile else (18, 24)
    font_size = 18 if mobile else 17
    chip_height, row_gap = 37, 10
    card_width = (width - padding * 2 - gap * (columns - 1)) // columns
    prepared = [(name, chip_rows(tools, card_width - inset * 2, font_size)) for name, tools in GROUPS]
    heights = [82 + len(rows) * chip_height + (len(rows) - 1) * row_gap + 23 for _, rows in prepared]
    if not mobile:
        for index in range(0, len(heights), 2):
            heights[index] = heights[index + 1] = max(heights[index:index + 2])
    grid_top = 166 if mobile else 176
    height = grid_top + sum(heights[::columns]) + gap * (len(heights) // columns - 1) + padding
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Jowhar — Tools of the trade</title>',
        '<desc id="desc">From the interface to the infrastructure. Languages: JavaScript, TypeScript, HTML, CSS. Frontend: React, Next.js, Redux, Tailwind CSS, Bootstrap. Backend: Node.js, Express, REST APIs, JWT, API integrations. Data: MongoDB, PostgreSQL, MariaDB, Redis, Mongoose, Prisma, Drizzle. Infrastructure: Docker, NGINX, CI/CD, DNS, SSL, Git. Workspace: Postman, VS Code, Vercel, Heroku, GitHub.</desc>',
        '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}.mono{font-family:ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace}@media(prefers-reduced-motion:no-preference){.card{animation:reveal .55s cubic-bezier(.2,.7,.2,1) both}@keyframes reveal{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}}</style>',
        f'<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="20" fill="#0d1117" stroke="#263244"/>',
        f'<circle cx="{padding + 4}" cy="{padding + 8}" r="4" fill="#72e5d6"/>',
        label(padding + 18, padding + 12, "01 / TOOLKIT", 12 if mobile else 13, "#72e5d6", 'class="mono" letter-spacing="2"'),
        label(padding, padding + 58, "Tools of the trade.", 32 if mobile else 38, "#f0f5fb", 'font-weight="650" letter-spacing="-.8"'),
        label(padding, padding + 89, "From the interface to the infrastructure.", 17, "#9baabe"),
        f'<path d="M{padding} {grid_top - 22}H{width - padding}" stroke="#263244"/>',
    ]
    y = grid_top
    for index, (name, rows) in enumerate(prepared):
        x = padding + (index % columns) * (card_width + gap)
        card_height = heights[index]
        accent = "#72e5d6" if index % 2 == 0 else "#b9a0ff"
        parts.extend([
            f'<g class="card" style="animation-delay:{index * 90}ms">',
            f'<rect x="{x}" y="{y}" width="{card_width}" height="{card_height}" rx="13" fill="#141b26" stroke="#263244"/>',
            label(x + inset, y + 36, f"{index + 1:02d}", 12, accent, 'class="mono"'),
            label(x + inset + 31, y + 38, name, 20, "#edf3fb", 'font-weight="600"'),
            f'<path d="M{x + inset} {y + 57}H{x + card_width - inset}" stroke="#263244"/>',
        ])
        chip_y = y + 82
        for row in rows:
            chip_x = x + inset
            for name, color, chip_width in row:
                parts.extend([
                    f'<rect x="{chip_x}" y="{chip_y}" width="{chip_width}" height="{chip_height}" rx="8" fill="#1b2534" stroke="#2b3a4d"/>',
                    f'<circle cx="{chip_x + 14}" cy="{chip_y + chip_height / 2}" r="3" fill="{color}"/>',
                    label(chip_x + 26, chip_y + 24, name, font_size, "#dce6f3"),
                ])
                chip_x += chip_width + 9
            chip_y += chip_height + row_gap
        parts.append('</g>')
        if index % columns == columns - 1:
            y += card_height + gap
    parts.append('</svg>')
    return "\n".join(parts) + "\n", width, height


def main():
    directory = ROOT / "assets"
    directory.mkdir(exist_ok=True)
    for mobile in (False, True):
        artwork, width, height = render(mobile)
        output = directory / ("toolkit-mobile.svg" if mobile else "toolkit.svg")
        output.write_text(artwork, encoding="utf-8")
        print(f"{output.relative_to(ROOT)}: {width} × {height}, {output.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
