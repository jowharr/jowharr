#!/usr/bin/env python3
"""Generate responsive, self-contained artwork for the current learning topics."""

from math import ceil
from pathlib import Path
from xml.etree import ElementTree
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
TOPICS = (
    ("AI-Assisted Engineering", "#00e5ff"),
    ("Scalable Frontend Architecture", "#8b5cf6"),
    ("Distributed Systems Visualization", "#3366ff"),
    ("Modern UI Engineering", "#ec4899"),
    ("Real-time Observability", "#a855f7"),
    ("LLM Integrations & Tooling", "#00b4ff"),
)


def text_width(value, font_size):
    """Estimate Arial advances with a little extra room for fallback fonts."""
    widths = {
        " ": .278, "-": .333, "&": .667,
        "i": .222, "l": .222, "t": .278, "f": .278, "r": .333,
        "m": .833, "w": .722, "s": .5, "c": .5,
        "I": .278, "L": .556, "M": .833, "O": .778,
        "S": .667, "T": .611, "U": .722, "V": .667,
    }
    return ceil(sum(widths.get(char, .667 if char.isupper() else .556) for char in value) * font_size * 1.04)


def render(mobile=False):
    width = 480 if mobile else 960
    padding = 28 if mobile else 40
    font_size = 18 if mobile else 16
    chip_height, gap = (46, 16) if mobile else (44, 14)
    available = width - padding * 2
    rows, occupied = [[]], 0
    for title, color in TOPICS:
        chip_width = text_width(title, font_size) + 48
        if rows[-1] and occupied + gap + chip_width > available:
            rows.append([])
            occupied = 0
        rows[-1].append((title, color, chip_width))
        occupied += chip_width + (gap if occupied else 0)
    top = 86 if mobile else 89
    height = top + len(rows) * chip_height + (len(rows) - 1) * gap + (36 if mobile else 55)
    description = "; ".join(title for title, _ in TOPICS) + "."
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Currently exploring</title>',
        f'<desc id="desc">{escape(description)}</desc>',
        '<defs>',
        '<radialGradient id="cyan-glow"><stop stop-color="#00e5ff" stop-opacity=".11"/><stop offset="1" stop-color="#00e5ff" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="violet-glow"><stop stop-color="#8b5cf6" stop-opacity=".13"/><stop offset="1" stop-color="#8b5cf6" stop-opacity="0"/></radialGradient>',
        f'<clipPath id="bounds"><rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="19"/></clipPath>',
        '</defs>',
        '<style>',
        'text{font-family:Arial,Helvetica,sans-serif}',
        '.eyebrow{font-family:ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace}',
        '.topic-trace{opacity:0}',
        '@media(prefers-reduced-motion:no-preference){',
        '.topic{animation:appear .65s ease-out both}',
        '.topic-border{animation:border-glow 6s ease-in-out infinite;animation-delay:var(--phase)}',
        '.topic-trace{opacity:.85;animation:trace 3.2s linear infinite;animation-delay:var(--phase)}',
        '.dot-halo{transform-box:fill-box;transform-origin:center;animation:halo 4.5s ease-in-out infinite;animation-delay:var(--phase)}',
        '.glow{animation:ambient 10s ease-in-out infinite alternate}',
        '.glow.violet{animation-delay:-5s}',
        '@keyframes appear{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}',
        '@keyframes trace{from{stroke-dashoffset:0}to{stroke-dashoffset:-100}}',
        '@keyframes border-glow{0%,100%{stroke-opacity:.28}50%{stroke-opacity:.72}}',
        '@keyframes halo{0%,100%{opacity:.12;transform:scale(.8)}50%{opacity:.32;transform:scale(1.3)}}',
        '@keyframes ambient{from{opacity:.55}to{opacity:1}}',
        '}',
        '</style>',
        f'<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="20" fill="#06060a" stroke="#252536"/>',
        '<g clip-path="url(#bounds)">',
        f'<ellipse class="glow" cx="{width * .08:g}" cy="{height * .9:g}" rx="{width * .48:g}" ry="{height * .95:g}" fill="url(#cyan-glow)"/>',
        f'<ellipse class="glow violet" cx="{width * .91:g}" cy="{height * .12:g}" rx="{width * .45:g}" ry="{height * .95:g}" fill="url(#violet-glow)"/>',
        '</g>',
        f'<text class="eyebrow" x="{padding}" y="47" fill="#aaaabb" font-size="13" letter-spacing="3">CURRENTLY EXPLORING</text>',
    ]
    index = 0
    for row_index, row in enumerate(rows):
        x, y = padding, top + row_index * (chip_height + gap)
        for title, color, chip_width in row:
            parts.extend([
                f'<g class="topic" style="animation-delay:{index * 90 + 100}ms">',
                f'<g style="--phase:{-index * 1.1:g}s">',
                f'<rect class="topic-border" x="{x}" y="{y}" width="{chip_width}" height="{chip_height}" rx="{chip_height / 2:g}" fill="#0d0d17" fill-opacity=".84" stroke="{color}" stroke-opacity=".28"/>',
                f'<rect class="topic-trace" x="{x}" y="{y}" width="{chip_width}" height="{chip_height}" rx="{chip_height / 2:g}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" pathLength="100" stroke-dasharray="18 82"/>',
                f'<circle class="dot-halo" cx="{x + 18}" cy="{y + chip_height / 2:g}" r="6.5" fill="{color}" opacity=".16"/>',
                f'<circle cx="{x + 18}" cy="{y + chip_height / 2:g}" r="3.5" fill="{color}"/>',
                f'<text x="{x + 31}" y="{y + chip_height / 2 + font_size * .35:g}" fill="#d6d6e1" font-size="{font_size}">{escape(title)}</text>',
                '</g>',
                '</g>',
            ])
            x += chip_width + gap
            index += 1
    parts.append('</svg>')
    artwork = "\n".join(parts) + "\n"
    ElementTree.fromstring(artwork)
    return artwork, width, height


def main():
    directory = ROOT / "assets"
    directory.mkdir(exist_ok=True)
    for mobile in (False, True):
        artwork, width, height = render(mobile)
        output = directory / ("focus-mobile.svg" if mobile else "focus.svg")
        output.write_text(artwork, encoding="utf-8")
        print(f"{output.relative_to(ROOT)}: {width} × {height}, {output.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
