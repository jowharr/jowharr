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
    width, padding = (480, 26) if mobile else (960, 52)
    font_size, chip_height = (18, 42) if mobile else (16, 42)
    # Float the same verified toolkit as compact chips, matching the reference.
    tools = [tool for _, group in GROUPS for tool in group]
    rows = chip_rows(tools, width - 2*padding, font_size)
    top, gap = 88, 12
    height = top + len(rows)*(chip_height+gap) - gap + 42
    description = "Jowhar's toolkit: " + ", ".join(name for name, _ in tools) + "."
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Jowhar — Tech stack</title>',
        f'<desc id="desc">{escape(description)}</desc>',
        '<defs><radialGradient id="violet"><stop stop-color="#8b5cf6" stop-opacity=".21"/><stop offset="1" stop-color="#8b5cf6" stop-opacity="0"/></radialGradient><radialGradient id="cyan"><stop stop-color="#00e5ff" stop-opacity=".14"/><stop offset="1" stop-color="#00e5ff" stop-opacity="0"/></radialGradient><clipPath id="bounds"><rect x="1" y="1" width="'+str(width-2)+'" height="'+str(height-2)+'" rx="20"/></clipPath></defs>',
        '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}.chip{opacity:1}@media(prefers-reduced-motion:no-preference){.chip{animation:reveal .35s ease-out both}.ambient{animation:drift 11s ease-in-out infinite alternate}@keyframes reveal{from{opacity:0}to{opacity:1}}@keyframes drift{from{transform:translate(0,0)}to{transform:translate(15px,-10px)}}}</style>',
        f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="20" fill="#06060a" stroke="#202036"/>',
        '<g clip-path="url(#bounds)">',
        f'<ellipse class="ambient" cx="130" cy="{height-40}" rx="320" ry="250" fill="url(#violet)"/><ellipse class="ambient" cx="{width-100}" cy="55" rx="300" ry="220" fill="url(#cyan)"/>',
        label(width/2, 48, "TECH STACK", 12, "#b1a0d4", 'text-anchor="middle" letter-spacing="5"'),
    ]
    index = 0
    for row_index, row in enumerate(rows):
        row_width = sum(item[2] for item in row) + 9*(len(row)-1)
        x, y = (width-row_width)/2, top+row_index*(chip_height+gap)
        for name, color, chip_width in row:
            parts.extend([
                f'<g class="chip" style="animation-delay:{index*22}ms">',
                f'<rect x="{x}" y="{y}" width="{chip_width}" height="{chip_height}" rx="11" fill="{color}" fill-opacity=".055" stroke="{color}" stroke-opacity=".22"/>',
                f'<circle cx="{x+14}" cy="{y+chip_height/2}" r="7" fill="{color}" opacity=".08"/>',
                f'<circle cx="{x+14}" cy="{y+chip_height/2}" r="3.5" fill="{color}"/>',
                label(x+26, y+27, name, font_size, "#d5d7e6"),
                '</g>',
            ])
            index += 1
            x += chip_width+9
    parts.extend(['</g>', '</svg>'])
    return "\n".join(parts)+"\n", width, height


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
