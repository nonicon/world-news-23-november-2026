#!/usr/bin/env python3
"""One picture of Monday 23 November 2026.

Paints a newspaper front page for the day -- masthead, lead story on
the Gulf, the collapsed climate talks, and the rest of the day's news --
straight onto a pixel canvas and saves it as entry.png.

Pure standard library. No files are read, no network is touched, and
nothing depends on the clock, so every run writes identical bytes.
Run it with MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (246, 241, 227)
INK = (25, 21, 18)
RED = (158, 27, 27)
BLUE = (23, 69, 110)
GOLD = (185, 138, 29)
SEA = (46, 111, 142)
SAND = (217, 197, 143)
GREY = (90, 84, 74)
PALE = (232, 224, 205)

# ------------------------------------------------------------- letterforms --
# Hand-built 5 by 7 dot-matrix capitals and friends.  A '#' cell is ink.
GLYPHS = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
}
GLYPHS.update({
    "N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    "a": (".....", ".....", ".####", "....#", ".####", "#...#", ".###."),
    "b": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "####."),
    "c": (".....", ".....", ".####", "#....", "#....", "#....", ".####"),
    "d": ("....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"),
    "e": (".....", ".....", ".###.", "#...#", "#####", "#....", ".###."),
    "f": ("..##.", ".#...", ".#...", "####.", ".#...", ".#...", ".#..."),
    "g": (".....", ".....", ".####", "#...#", "#...#", ".####", "....#"),
    "h": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"),
    "i": ("..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###."),
    "j": ("...#.", ".....", "..##.", "...#.", "...#.", "...#.", "...#."),
    "k": ("#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."),
    "l": (".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "m": (".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"),
    "n": (".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"),
    "o": (".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."),
    "p": (".....", ".....", "####.", "#...#", "#...#", "####.", "#...."),
    "q": (".....", ".....", ".####", "#...#", "#...#", ".####", "....#"),
    "r": (".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."),
    "s": (".....", ".....", ".####", "#....", ".###.", "....#", "####."),
    "t": (".#...", ".#...", "####.", ".#...", ".#...", ".#...", "..##."),
    "u": (".....", ".....", "#...#", "#...#", "#...#", "#...#", ".###."),
    "v": (".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "w": (".....", ".....", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
    "x": (".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
    "y": (".....", ".....", "#...#", "#...#", "#...#", ".####", "....#"),
    "z": (".....", ".....", "#####", "...#.", "..#..", ".#...", "#####"),
})
GLYPHS.update({
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    "(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "&": (".###.", "#...#", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "%": ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
    "+": (".....", "..#..", "..#..", ".###.", "..#..", "..#..", "....."),
    "=": (".....", ".....", ".###.", ".....", ".###.", ".....", "....."),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "*": (".....", ".#.#.", "..#..", "#####", "..#..", ".#.#.", "....."),
})

BLANK = (".....", ".....", ".....", ".....", ".....", ".....", ".....")


def glyph_of(ch):
    return GLYPHS.get(ch, BLANK)


def text_px(text, scale):
    """Pixel width of text at the given scale (6 cells per character)."""
    return len(text) * 6 * scale


def wrap_words(text, scale, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w pixels."""
    lines = []
    for chunk in text.split("\n"):
        line = ""
        for word in chunk.split(" "):
            trial = word if not line else line + " " + word
            if text_px(trial, scale) <= max_w or not line:
                line = trial
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


# ---------------------------------------------------------------- canvas --
class Sheet:
    """A plain RGB pixel sheet with a few drawing helpers."""

    def __init__(self, w, h, base):
        self.w = w
        self.h = h
        self.pix = bytearray(base * (w * h))

    def dot(self, x, y, colour):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.pix[i:i + 3] = bytes(colour)

    def block(self, x, y, w, h, colour):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.pix[i:i + 3] = bytes(colour)

    def frame(self, x, y, w, h, colour, thick=2):
        self.block(x, y, w, thick, colour)
        self.block(x, y + h - thick, w, thick, colour)
        self.block(x, y, thick, h, colour)
        self.block(x + w - thick, y, thick, h, colour)

    def stroke(self, x0, y0, x1, y1, colour, thick=1):
        """Bresenham line, thickened by stamping small squares."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            self.block(x - thick // 2, y - thick // 2, thick, thick, colour)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def disc(self, cx, cy, r, colour, filled=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) ** 2 + (yy - cy) ** 2
                if filled:
                    if d2 <= r * r:
                        self.dot(xx, yy, colour)
                else:
                    if abs(d2 - r * r) <= r * 2:
                        self.dot(xx, yy, colour)

    def put_text(self, x, y, text, scale, colour, bold=False):
        """Draw text with the bitmap font; returns the pixel width used."""
        cx = x
        for ch in text:
            rows = glyph_of(ch)
            for ry, row in enumerate(rows):
                for rx, cell in enumerate(row):
                    if cell == "#":
                        self.block(cx + rx * scale, y + ry * scale,
                                   scale, scale, colour)
                        if bold:
                            self.block(cx + rx * scale + 1, y + ry * scale,
                                       scale, scale, colour)
            cx += 6 * scale
        return cx - x

    def centred(self, y, text, scale, colour, bold=False):
        w = text_px(text, scale)
        return self.put_text((self.w - w) // 2, y, text, scale, colour, bold)

    def para(self, x, y, text, scale, colour, max_w, leading=None):
        """Wrapped paragraph; returns the y just below the last line."""
        gap = leading if leading is not None else 10 * scale
        for line in wrap_words(text, scale, max_w):
            self.put_text(x, y, line, scale, colour)
            y += gap
        return y


def png_bytes(sheet):
    """Encode the sheet as a PNG (filter byte 0 on every scanline)."""
    raw = bytearray()
    stride = sheet.w * 3
    for y in range(sheet.h):
        raw.append(0)
        raw += sheet.pix[y * stride:(y + 1) * stride]

    def chunk(kind, payload):
        out = struct.pack(">I", len(payload)) + kind + payload
        out += struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", sheet.w, sheet.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


# ----------------------------------------------------------------- drawing --
def rule(sheet, y, colour=INK, thick=2, x0=30, x1=994):
    sheet.block(x0, y, x1 - x0, thick, colour)


def gulf_scene(sheet, x, y, w, h):
    """A stylised Gulf: sea, land on both shores, Bahrain, the strait."""
    sheet.block(x, y, w, h, SEA)
    # Iran, left shore; Arabia, right shore.
    sheet.block(x, y, 150, h, SAND)
    sheet.block(x + 430, y, w - 430, h, SAND)
    sheet.stroke(x + 150, y, x + 190, y + h, SAND, 14)
    sheet.stroke(x + 430, y, x + 400, y + h, SAND, 14)
    # The strait: a narrow blue gap at the bottom right.
    sheet.block(x + 400, y + h - 26, 60, 26, SEA)
    sheet.put_text(x + 12, y + 8, "IRAN", 2, INK)
    sheet.put_text(x + 470, y + 8, "ARABIA", 2, INK)
    sheet.put_text(x + 190, y + h - 22, "THE GULF", 2, PAPER)
    # Bahrain: a gold dot with a ring, and the incoming strikes.
    bx, by = x + 330, y + 52
    sheet.disc(bx, by, 10, GOLD)
    sheet.disc(bx, by, 16, GOLD, filled=False)
    sheet.put_text(bx + 22, by - 8, "BAHRAIN", 2, PAPER, bold=True)
    sheet.stroke(x + 40, y + 14, bx - 8, by - 6, RED, 3)
    sheet.stroke(x + 90, y + 96, bx - 8, by + 8, RED, 3)
    sheet.put_text(x + w - 150, y + h - 20, "HORMUZ", 2, PAPER, bold=True)
    # Tankers queuing in the strait.
    for i, ty in enumerate((y + h - 22, y + h - 12)):
        sheet.block(x + 405 + i * 8, ty, 34, 8, INK)
        sheet.block(x + 405 + i * 8, ty, 34, 3, PAPER)


def cracked_globe(sheet, cx, cy, r):
    sheet.disc(cx, cy, r, BLUE, filled=False)
    sheet.disc(cx, cy, r - 3, BLUE, filled=False)
    sheet.stroke(cx - r + 8, cy - 6, cx - 6, cy + 4, BLUE, 3)
    sheet.stroke(cx - 6, cy + 4, cx + 8, cy - 8, BLUE, 3)
    sheet.stroke(cx + 8, cy - 8, cx + r - 6, cy + 10, BLUE, 3)
    sheet.stroke(cx - r + 12, cy + 18, cx, cy + 26, RED, 3)
    sheet.stroke(cx, cy + 26, cx + r - 14, cy + 16, RED, 3)
    sheet.stroke(cx - 14, cy - r + 10, cx + 4, cy - r + 26, RED, 3)


def cuffs_icon(sheet, x, y):
    sheet.disc(x + 14, y + 14, 11, INK, filled=False)
    sheet.disc(x + 48, y + 14, 11, INK, filled=False)
    sheet.stroke(x + 24, y + 8, x + 38, y + 8, INK, 3)


def cap_icon(sheet, x, y):
    sheet.stroke(x + 6, y + 12, x + 31, y + 2, INK, 3)
    sheet.stroke(x + 31, y + 2, x + 56, y + 12, INK, 3)
    sheet.stroke(x + 6, y + 12, x + 56, y + 12, INK, 3)
    sheet.block(x + 20, y + 16, 22, 6, INK)
    sheet.stroke(x + 56, y + 12, x + 56, y + 26, INK, 2)


def robot_icon(sheet, x, y):
    sheet.stroke(x + 31, y, x + 31, y + 8, INK, 2)
    sheet.disc(x + 31, y, 3, RED)
    sheet.frame(x + 12, y + 8, 38, 28, INK, 3)
    sheet.disc(x + 24, y + 20, 4, BLUE)
    sheet.disc(x + 38, y + 20, 4, BLUE)
    sheet.block(x + 22, y + 28, 18, 3, INK)


def story(sheet, x, y, w, icon, kicker, headline, body):
    """One column story: icon, red kicker, headline, body text."""
    icon(sheet, x, y)
    sheet.put_text(x, y + 44, kicker, 2, RED, bold=True)
    hy = y + 66
    for line in wrap_words(headline, 3, w):
        sheet.put_text(x, hy, line, 3, INK, bold=True)
        hy += 30
    sheet.para(x, hy + 6, body, 2, INK, w, leading=17)


def build_page():
    s = Sheet(W, H, PAPER)
    # Masthead.
    s.block(30, 14, 964, 8, RED)
    s.centred(30, "THE WORLD TODAY", 7, INK, bold=True)
    s.centred(88, "MONDAY 23 NOVEMBER 2026", 4, RED, bold=True)
    s.centred(120, "ONE DAY IN ONE PICTURE", 2, GREY)
    rule(s, 142, INK, 3)
    rule(s, 148, INK, 1)

    # Lead story: the Gulf.
    s.put_text(30, 160, "THE GULF - LEAD STORY", 2, RED, bold=True)
    s.put_text(30, 184, "IRAN HITS US BASES", 4, INK, bold=True)
    s.put_text(30, 212, "IN BAHRAIN AGAIN", 4, INK, bold=True)
    s.para(30, 248, "Iran fired drones and missiles at US sites in "
         "Bahrain, the latest Gulf strike. Bahrain said its defences "
         "stopped it, but a civilian site caught fire. Tankers wait "
         "to test the US blockade of Hormuz.",
         2, INK, 630, leading=19)
    gulf_scene(s, 30, 344, 630, 92)

    # Climate, right column.
    s.frame(690, 156, 304, 280, INK, 2)
    s.put_text(706, 170, "CLIMATE", 2, RED, bold=True)
    s.put_text(706, 194, "CLIMATE TALKS", 3, INK, bold=True)
    s.put_text(706, 222, "COLLAPSE", 3, INK, bold=True)
    cracked_globe(s, 842, 288, 30)
    s.para(706, 322, "COP31 in Antalya ended on Sunday with no deal. "
         "The EU rejected a pact that never mentioned fossil fuels - "
         "the first such collapse since 2009.", 2, INK, 272, leading=16)

    rule(s, 452, INK, 2)

    # Three stories across the middle.
    story(s, 30, 468, 304, cuffs_icon, "MEXICO",
          "CAPTURE OF 'EL CHAPO ISIDRO'",
          "Mexican forces captured the FBI's most-wanted cartel boss "
          "'El Chapo Isidro' after firefights in Sinaloa left 11 dead.")
    story(s, 360, 468, 304, cap_icon, "SEOUL",
          "MINISTER QUITS OVER AI CHEATING",
          "South Korea's education minister resigned amid a scandal "
          "over AI-driven cheating in school exams.")
    story(s, 690, 468, 304, robot_icon, "UNITED NATIONS",
          "TALKS GO ON OVER KILLER ROBOTS",
          "Countries at the UN agreed to keep negotiating rules for "
          "lethal autonomous weapons.")

    rule(s, 700, INK, 2)

    # The rest of the day, in brief.
    s.put_text(30, 714, "ALSO TODAY", 3, RED, bold=True)
    briefs = [
        ("UKRAINE - ", "Russian cargo ship ablaze off Finland after a "
         "drone attack; 14 missing near Kyiv."),
        ("INDONESIA - ", "Dozens missing after a factory fire; bodies "
         "recovered as the search goes on."),
        ("PORTUGAL - ", "Thousands marched in Lisbon over living costs."),
        ("INDIA - ", "Nepal PM Shah held talks with PM Modi; India hit "
         "a record 720 for 9 in Wellington."),
        ("WASHINGTON - ", "The FBI's crime database was hacked, Trump "
         "confirmed."),
        ("WEST BANK - ", "An Israeli minister called settler violence "
         "'Jewish terrorism'."),
    ]
    by = 748
    for tag, text in briefs:
        end = s.para(48, by, tag + text, 2, INK, 964 - 48, leading=17)
        s.block(30, by + 3, 10, 10, RED)
        s.put_text(48, by, tag, 2, INK, bold=True)
        by = end + 5

    rule(s, 980, INK, 2)
    s.centred(992, "All stories as reported on Monday 23 November 2026.",
              2, GREY)
    return s


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    data = png_bytes(build_page())
    with open(path, "wb") as fh:
        fh.write(data)
    print("wrote %s (%d bytes, %dx%d)" % (path, len(data), W, H))


if __name__ == "__main__":
    main()
