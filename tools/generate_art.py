#!/usr/bin/env python3
"""Arte pixelada original, otimizada em tiles 8x8 para Mega Drive.
Gera src/graphics.h, dist/preview-pixelart.png e dist/sprites-pixelart.png.
Nao utiliza personagens, sprites ou materiais do Mario/Nintendo.
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
(ROOT/"src").mkdir(exist_ok=True)
(ROOT/"dist").mkdir(exist_ok=True)

# 16 cores compartilhadas (1 palette 4bpp do Mega Drive).
PALETTE=[
  (0,0,0), (16,30,49), (40,70,109), (248,245,219),
  (101,204,241), (35,114,199), (40,162,87), (111,215,115),
  (254,214,84), (239,150,44), (142,86,53), (227,75,65),
  (64,72,92), (113,125,145), (183,227,241), (18,104,62)
]
HEX=[0x000,0x222,0x446,0xEEE,0xAEC,0x46C,0x284,0x6C6,0xEC4,0xC82,0x864,0xC44,0x444,0x888,0xCEC,0x264]
# Mega Drive usa 0x0BGR, 3 bits por componente (valores pares).
def cr16(c):
    r,g,b=c
    return ((b//36)*2<<8)|((g//36)*2<<4)|((r//36)*2)
HEX=[cr16(c) for c in PALETTE]

def blank(w,h,color=0):
    im=Image.new("P",(w,h),color)
    im.putpalette(sum(([r,g,b] for r,g,b in PALETTE),[])+[0]*(768-48))
    return im

bg=blank(320,224,4)
d=ImageDraw.Draw(bg)
# Horizonte do Rio, mar, montanhas e predios.
d.rectangle((0,0,319,37),fill=1)
d.rectangle((0,38,319,81),fill=4)
d.ellipse((248,45,279,76),fill=8)
for x,y,w in [(10,45,36),(60,57,24),(161,47,45)]:
    d.ellipse((x,y,x+w,y+11),fill=14)
    d.rectangle((x+8,y-4,x+w-11,y+12),fill=14)
d.polygon([(0,83),(44,46),(91,80),(118,62),(152,86)],fill=5)
d.polygon([(123,85),(185,45),(235,89),(273,64),(319,91)],fill=6)
d.polygon([(182,74),(203,59),(226,87)],fill=7)
# Panorama e arvores pixeladas, sem elementos licenciados.
for x,h,w in [(1,16,11),(16,28,13),(34,21,13),(54,33,12),(78,17,15),
              (102,27,14),(142,20,12),(240,28,12),(260,34,12),
              (282,19,14),(303,30,15)]:
    d.rectangle((x,83-h,x+w,85),fill=2)
    for ix in range(x+3,x+w,6):
        for iy in range(89-h,83,9): d.rectangle((ix,iy,ix+2,iy+3),fill=8)
for x in [18,91,161,292]:
    d.rectangle((x+8,78,x+12,94),fill=10)
    d.ellipse((x,64,x+25,86),fill=15)
    d.ellipse((x+5,60,x+22,78),fill=7)
d.rectangle((0,88,319,101),fill=7)
d.rectangle((0,100,319,223),fill=12)
# 3 faixas largas, tracado de asfalto.
for y in (100,140,180,221):
    d.rectangle((0,y,319,y+2),fill=13)
for y in (138,178):
    for x in range(0,320,38): d.rectangle((x,y,x+21,y+2),fill=8)
for y in range(111,223,36):
    for x in range(8,320,50):
        d.point((x,y),fill=13);d.point((x+12,y+6),fill=1)

# Caminhao do Jorge: sprite de 48x24, desenhado em pixels.
truck=blank(48,24)
t=ImageDraw.Draw(truck)
t.rectangle((0,5,30,18),fill=1)
t.rectangle((2,3,29,16),fill=8)
t.rectangle((4,5,27,14),fill=9)
t.rectangle((5,7,27,10),fill=8)
t.rectangle((6,11,27,13),fill=6)
t.rectangle((29,9,45,18),fill=1)
t.rectangle((31,7,43,16),fill=5)
t.polygon([(32,7),(40,7),(43,11),(43,15),(32,15)],fill=5)
t.polygon([(35,9),(39,9),(41,12),(35,12)],fill=14)
t.rectangle((31,18,47,20),fill=1)
t.rectangle((1,17,47,19),fill=2)
for x in [10,37]:
    t.rectangle((x-5,16,x+5,22),fill=1)
    t.ellipse((x-5,16,x+5,23),fill=1)
    t.ellipse((x-2,18,x+2,22),fill=13)
t.rectangle((44,13,47,16),fill=8)

crate=blank(16,16);c=ImageDraw.Draw(crate)
c.rectangle((1,2,14,14),fill=1)
c.rectangle((2,2,13,13),fill=9)
c.rectangle((4,4,11,11),fill=10)
c.line((4,4,11,11),fill=8,width=2)
c.line((11,4,4,11),fill=8,width=2)
c.rectangle((1,2,14,3),fill=8)
c.rectangle((2,12,14,14),fill=1)

rock=blank(16,16);r=ImageDraw.Draw(rock)
r.polygon([(1,12),(4,7),(8,4),(12,6),(15,11),(13,14),(3,14)],fill=1)
r.polygon([(3,11),(6,6),(10,5),(13,9),(12,12)],fill=13)
r.polygon([(4,9),(7,6),(9,6),(7,9)],fill=14)
r.line((6,10,10,13),fill=2,width=2)

cone=blank(16,16);o=ImageDraw.Draw(cone)
o.polygon([(2,13),(6,2),(10,2),(14,13)],fill=1)
o.polygon([(4,12),(7,4),(9,4),(12,12)],fill=9)
o.rectangle((5,9,11,10),fill=3)
o.rectangle((1,13,15,15),fill=1)
o.rectangle((3,13,13,13),fill=8)

tile_bytes=[]
ids={}
def tile_id(raw):
    v=bytes(raw)
    if v not in ids:
        ids[v]=len(ids)
        for y in range(8):
            row=0
            for x in range(8):row=(row<<4)|(v[y*8+x]&15)
            tile_bytes.append(row)
    return ids[v]

def tilemap(im):
    w,h=im.size
    result=[]
    for y in range(0,h,8):
        for x in range(0,w,8):
            raw=im.crop((x,y,x+8,y+8)).tobytes()
            result.append(tile_id(raw))
    return result

# Tile 0 precisa ser totalmente transparente para a camada BG_A.
tile_id([0]*64)
bgmap=tilemap(bg)
truckmap=tilemap(truck)
cratemap=tilemap(crate)
rockmap=tilemap(rock)
conemap=tilemap(cone)

def arr(name,ctype,items,perline=12,hexformat=False):
    parts=[]
    for i in range(0,len(items),perline):
        vals=items[i:i+perline]
        parts.append("    "+", ".join((f"0x{v:08X}" if hexformat else str(v)) for v in vals)+",")
    return f"static const {ctype} {name}[{len(items)}] = {{\n"+"\n".join(parts)+"\n};\n"

header=("/* Arquivo GERADO automaticamente por tools/generate_art.py. Nao editar. */\n"
        "#ifndef JORGE_GRAPHICS_H\n#define JORGE_GRAPHICS_H\n"
        f"#define GFX_TILE_COUNT {len(ids)}\n"
        "#define GFX_BG_WIDTH 40\n#define GFX_BG_HEIGHT 28\n"
        +arr("gfxPalette","u16",HEX,8)
        +arr("gfxTiles","u32",tile_bytes,8,True)
        +arr("gfxBgMap","u16",bgmap,20)
        +arr("gfxTruck","u16",truckmap,12)
        +arr("gfxCrate","u16",cratemap,8)
        +arr("gfxRock","u16",rockmap,8)
        +arr("gfxCone","u16",conemap,8)
        +"#endif\n")
(ROOT/"src"/"graphics.h").write_text(header,encoding="utf-8")

# Preview com os mesmos sprites e cenarios que serao compilados na ROM.
preview=bg.convert("RGB")
mask=truck.convert('L').point(lambda v:255 if v else 0)
preview.paste(truck.convert("RGB"),(40,115),mask)
for im,x,y in [(crate,244,113),(rock,170,155),(cone,263,190),(crate,294,190)]:
    mask=im.convert('L').point(lambda v:255 if v else 0)
    preview.paste(im.convert("RGB"),(x,y),mask)
preview.resize((960,672),Image.Resampling.NEAREST).save(ROOT/"dist"/"preview-pixelart.png")
atlas=blank(112,32)
for im,x in [(truck,0),(crate,48),(rock,64),(cone,80)]:
    atlas.paste(im,(x,0))
atlas.resize((896,256),Image.Resampling.NEAREST).save(ROOT/"dist"/"sprites-pixelart.png")
print(f"Gerados {len(ids)} tiles, {len(header)} caracteres em graphics.h")
