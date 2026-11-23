#!/usr/bin/env python3
"""Gera a capa PNG sem copiar imagens de jogos comerciais."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist" / "Jorge_Truck_Driver.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

S = 320
im = Image.new("RGB", (S, S), "#65c8e8")
d = ImageDraw.Draw(im)

def font(size):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()

# Pixel art original, criado por formas geometricas.
d.rectangle((0, 0, 319, 108), fill="#143b62")
d.rectangle((0, 107, 319, 166), fill="#71cde4")
d.ellipse((236, 115, 289, 167), fill="#ffcf53")
for x, y in [(21, 128), (91, 145), (175, 118)]:
    d.rectangle((x, y, x+42, y+11), fill="#f0f6ff")
    d.rectangle((x+10, y-7, x+30, y+16), fill="#f0f6ff")

# Predios ao fundo.
for x, h, w in [(0, 40, 26), (32, 55, 28), (70, 72, 30),
                (114, 47, 32), (153, 61, 31), (205, 45, 25),
                (249, 75, 31), (289, 62, 32)]:
    d.rectangle((x, 169-h, x+w, 169), fill="#406882")
    for iy in range(169-h+9, 165, 12):
        for ix in range(x+6, x+w-3, 10):
            d.rectangle((ix, iy, ix+3, iy+4), fill="#f9d776")

d.rectangle((0, 169, 319, 202), fill="#3fae75")
d.rectangle((0, 202, 319, 290), fill="#303846")
for y in [226, 257, 280]:
    for x in range(0, 320, 36):
        d.rectangle((x, y, x+17, y+3), fill="#fff3a2")

# Caminhao de lado com carga.
d.rectangle((45, 196, 199, 245), fill="#f0a735")
d.rectangle((48, 201, 194, 225), fill="#d8862f")
d.rectangle((201, 203, 263, 248), fill="#f06641")
d.polygon([(207, 205), (242, 205), (257, 223), (257, 232), (207, 232)], fill="#f57d5a")
d.rectangle((218, 209, 241, 226), fill="#c8edfd")
d.rectangle((39, 242, 263, 252), fill="#22252a")
for x in [79, 221]:
    d.ellipse((x-21, 228, x+21, 270), fill="#121c28")
    d.ellipse((x-10, 239, x+10, 260), fill="#d9e1e5")
d.rectangle((270, 210, 292, 234), fill="#f3c257")
d.line([(274, 213), (288, 229)], fill="#9b5b30", width=3)
d.line([(288, 213), (274, 229)], fill="#9b5b30", width=3)

# Titulo legivel em miniatura.
title_font = font(30)
sub_font = font(18)
small = font(16)
for t, y, f in [("JORGE", 14, title_font), ("TRUCK DRIVER", 49, sub_font),
                ("MEGA DRIVE EDITION", 83, small)]:
    bbox = d.textbbox((0,0), t, font=f)
    x = (S - (bbox[2] - bbox[0])) // 2
    d.text((x+2, y+2), t, font=f, fill="#051421")
    d.text((x, y), t, font=f, fill="#fff1a6")

d.rectangle((0, 293, 319, 319), fill="#18354e")
footer = "16 BIT  |  ENTREGA DE CAIXAS"
w = d.textbbox((0, 0), footer, font=small)[2]
d.text(((S-w)//2, 298), footer, font=small, fill="white")

im.save(OUT, "PNG")
print(f"Capa criada: {OUT} ({OUT.stat().st_size} bytes)")
