#!/usr/bin/env python3
"""Sample a decoded photo into text for the terminal's native SVG portrait.

Decode HEIC with macOS sips first:
    sips -s format bmp input.HEIC --out /tmp/portrait.bmp
Then:
    python3 scripts/photo_to_ascii.py /tmp/portrait.bmp
Only the ASCII output is saved in this repository.
"""

import argparse
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAMP = " .,:;irsXA253hMHGS#9B&@"


def convert(path, crop, columns=64, rows=62):
    data = path.read_bytes()
    offset = struct.unpack_from("<I", data, 10)[0]
    width, signed_height = struct.unpack_from("<ii", data, 18)
    depth = struct.unpack_from("<H", data, 28)[0]
    compression = struct.unpack_from("<I", data, 30)[0]
    if data[:2] != b"BM" or depth != 24 or compression != 0:
        raise ValueError("Use an uncompressed 24-bit BMP, as produced by sips.")
    height = abs(signed_height)
    stride = (width * 3 + 3) // 4 * 4
    left, top, crop_width, crop_height = crop
    if not (0 <= left < left + crop_width <= width and
            0 <= top < top + crop_height <= height):
        raise ValueError("Crop lies outside the source photo.")

    def luminance(x, y):
        y = y if signed_height < 0 else height - 1 - y
        index = offset + y * stride + x * 3
        b, g, r = data[index:index + 3]
        # The supplied portrait has a green backdrop. Suppress those cells
        # so foliage does not compete with the facial features in ASCII.
        if g > r * .98:
            return 0
        return .2126 * r + .7152 * g + .0722 * b

    output = []
    for row in range(rows):
        line = []
        for col in range(columns):
            # Average a small regular grid inside each character cell.
            samples = [
                luminance(
                    int(left + (col + (sx + .5)/4) * crop_width / columns),
                    int(top + (row + (sy + .5)/4) * crop_height / rows),
                )
                for sy in range(4) for sx in range(4)
            ]
            value = sum(samples) / len(samples)
            contrast = max(0, min(1, (value - 26) / 184)) ** .9
            line.append(RAMP[round(contrast * (len(RAMP) - 1))])
        output.append("".join(line))
    # Discard isolated backdrop specks, retaining the connected portrait detail.
    grid = [list(line) for line in output]
    seen = set()
    for y in range(rows):
        for x in range(columns):
            if grid[y][x] == " " or (x, y) in seen:
                continue
            pending, component = [(x, y)], []
            seen.add((x, y))
            while pending:
                px, py = pending.pop()
                component.append((px, py))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        nx, ny = px + dx, py + dy
                        if (0 <= nx < columns and 0 <= ny < rows and
                                (nx, ny) not in seen and grid[ny][nx] != " "):
                            seen.add((nx, ny))
                            pending.append((nx, ny))
            if len(component) < 48:
                for px, py in component:
                    grid[py][px] = " "
    return "\n".join("".join(line) for line in grid) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("photo", type=Path)
    parser.add_argument("--crop", type=int, nargs=4, default=(450, 285, 1370, 1860),
                        metavar=("LEFT", "TOP", "WIDTH", "HEIGHT"))
    args = parser.parse_args()
    output = ROOT / "assets" / "portrait.txt"
    output.write_text(convert(args.photo, args.crop), encoding="utf-8")
    print(f"Generated {output.relative_to(ROOT)} (64 columns × 62 rows)")


if __name__ == "__main__":
    main()
