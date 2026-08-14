"""Build the animated ASCII portrait + ARTA wordmark identity panel.

The generated ``identity.svg`` is used above the original neofetch information
card. Run this after regenerating ``avi-ascii.svg`` so the portrait stays in
sync with the source photo.

    python scripts/make_identity.py
    STATIC=1 python scripts/make_identity.py  # completed frame for screenshots
"""

import os
import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent

WORDMARK = "ARTA"
USER = "arta"
HOST = "jenesyx"

BG = "#0d1117"
BAR = "#161b22"
PANEL = "#0a171c"
STROKE = "#1f3946"
GREEN = "#39d353"
MINT = "#69f0a0"
BLUE = "#58a6ff"
TEXT = "#c9d1d9"
DIM = "#8b949e"

GLYPHS = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
}


def split_svg(path: Path) -> tuple[float, float, str]:
    source = path.read_text(encoding="utf-8")
    root = re.match(r"<svg\b[^>]*>", source)
    if not root:
        raise SystemExit(f"{path.name}: missing root SVG element")
    view_box = re.search(r'viewBox="([^"]+)"', root.group(0))
    if not view_box:
        raise SystemExit(f"{path.name}: missing viewBox")
    _, _, width, height = (float(value) for value in view_box.group(1).split())
    inner = source[root.end():]
    return width, height, inner[:inner.rfind("</svg>")]


def wordmark_lines(alphabet: str) -> list[str]:
    lines: list[str] = []
    for row in range(7):
        characters = []
        for letter_index, letter in enumerate(WORDMARK):
            glyph = GLYPHS[letter][row]
            characters.append("".join(
                alphabet[(row + letter_index + pixel_index) % len(alphabet)] * 4
                if pixel == "1" else " " * 4
                for pixel_index, pixel in enumerate(glyph)
            ))
        lines.append("    ".join(characters))
    return lines


def wordmark_group(lines: list[str], class_name: str) -> str:
    rows = "".join(
        f'<text x="0" y="{26 + index * 31}" textLength="424" '
        f'lengthAdjust="spacingAndGlyphs" xml:space="preserve">{escape(line)}</text>'
        for index, line in enumerate(lines)
    )
    return f'<g class="{class_name}">{rows}</g>'


def build() -> str:
    portrait_path = ROOT / "avi-ascii.svg"
    if not portrait_path.exists():
        raise SystemExit("avi-ascii.svg missing; generate the portrait first")

    portrait_width, portrait_height, portrait = split_svg(portrait_path)
    first = wordmark_group(wordmark_lines("$s+"), "phase-a")
    second = wordmark_group(wordmark_lines("#*="), "phase-b")
    static = os.environ.get("STATIC") == "1"

    if static:
        motion = ".phase-b{display:none}"
        type_clip = '<rect width="424" height="238"/>'
        cursor = ""
    else:
        motion = (
            "@keyframes phaseA{0%,40%{opacity:1}55%,91%{opacity:0}100%{opacity:1}}"
            "@keyframes phaseB{0%,40%{opacity:0}55%,91%{opacity:1}100%{opacity:0}}"
            ".phase-a{animation:phaseA 3.8s cubic-bezier(.32,.72,0,1) infinite}"
            ".phase-b{animation:phaseB 3.8s cubic-bezier(.32,.72,0,1) infinite}"
            "@media(prefers-reduced-motion:reduce){.phase-a,.phase-b{animation:none}.phase-b{display:none}}"
        )
        type_clip = (
            '<rect width="424" height="238"><animate attributeName="width" '
            'from="0" to="424" dur="2.25s" calcMode="spline" '
            'keySplines=".32 .72 0 1" fill="freeze"/></rect>'
        )
        cursor = (
            f'<rect x="397" y="111" width="6" height="22" fill="{MINT}">'
            '<animate attributeName="x" from="397" to="821" dur="2.25s" '
            'calcMode="spline" keySplines=".32 .72 0 1" fill="freeze"/>'
            '<set attributeName="opacity" to="0" begin="2.25s" fill="freeze"/></rect>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="432" viewBox="0 0 860 432" role="img" aria-label="Animated ASCII portrait and ARTA wordmark">
<defs>
  <linearGradient id="frame" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{GREEN}"/><stop offset=".52" stop-color="#167847"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>
  <linearGradient id="word" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{MINT}"/><stop offset=".58" stop-color="{GREEN}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>
  <radialGradient id="glow"><stop stop-color="{GREEN}" stop-opacity=".16"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>
  <clipPath id="type">{type_clip}</clipPath><style>{motion}</style>
</defs>
<rect width="860" height="432" rx="14" fill="{BG}"/><rect x="1" y="1" width="858" height="430" rx="13" fill="none" stroke="url(#frame)"/>
<path d="M1 14A13 13 0 0 1 14 1h832a13 13 0 0 1 13 13v37H1z" fill="{BAR}"/><line x1="1" y1="51" x2="859" y2="51" stroke="{STROKE}"/>
<circle cx="24" cy="26" r="6" fill="#ff5f56"/><circle cx="46" cy="26" r="6" fill="#ffbd2e"/><circle cx="68" cy="26" r="6" fill="#27c93f"/>
<text x="430" y="31" text-anchor="middle" font-family="ui-monospace,Consolas,monospace" font-size="12" fill="{DIM}">{USER}@{HOST}: ~$ whoami --ascii</text>
<rect x="12" y="63" width="354" height="357" rx="11" fill="{PANEL}" stroke="{STROKE}"/><text x="28" y="86" font-family="ui-monospace,Consolas,monospace" font-size="10" font-weight="700" letter-spacing="1.3" fill="{GREEN}">PORTRAIT.ASCII / @{HOST.upper()}</text>
<svg x="20" y="95" width="338" height="318" viewBox="0 0 {portrait_width:g} {portrait_height:g}" preserveAspectRatio="xMidYMid meet">{portrait}</svg>
<rect x="378" y="63" width="470" height="357" rx="11" fill="{PANEL}" stroke="{STROKE}"/><circle cx="621" cy="218" r="220" fill="url(#glow)"/>
<text x="396" y="87" font-family="ui-monospace,Consolas,monospace" font-size="10" font-weight="700" letter-spacing="1.3" fill="{BLUE}">WORDMARK.SH / --NAME {WORDMARK}</text>
<g transform="translate(397 108)" clip-path="url(#type)" font-family="ui-monospace,Consolas,monospace" font-size="19" font-weight="700" fill="url(#word)">{first}{second}</g>{cursor}
<text x="397" y="368" font-family="ui-monospace,Consolas,monospace" font-size="13" font-weight="700" fill="{TEXT}">ARTA BIDKHORI</text>
<text x="397" y="391" font-family="ui-monospace,Consolas,monospace" font-size="11" fill="{DIM}">FULL-STACK · AI AUTOMATION · UI/UX</text><circle cx="823" cy="386" r="4" fill="{GREEN}"/><text x="813" y="390" text-anchor="end" font-family="ui-monospace,Consolas,monospace" font-size="9" fill="{GREEN}">ONLINE</text>
</svg>'''


def main() -> int:
    destination = ROOT / "identity.svg"
    destination.write_text(build(), encoding="utf-8")
    print(f"wrote {destination} (860x432)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
