#!/usr/bin/env python3
"""Draws the four synthetic overhead images of the polygon area search demo (demo_data/area-search/).

Civilian scenes, not military: large buildings, construction and plant equipment, civilian cars.
Drawn with Pillow only, at twice the size and scaled down; the output is deterministic.

    python tools/draw_area_search_images.py
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parent.parent / "demo_data" / "area-search"
SIZE = 800          # output pixels (about 0.3 m per pixel)
S = 2               # drawn at twice the size
W = SIZE * S
SHADOW = (14, 10)   # sun from the south-east: shadows fall north-west... drawn as an offset
CAR_COLOURS = [(236, 236, 232), (238, 238, 236), (200, 202, 206), (176, 178, 182), (40, 42, 46), (28, 30, 34),
               (150, 30, 34), (36, 64, 120), (90, 96, 104), (214, 206, 186), (64, 90, 70), (220, 222, 224)]
YELLOW = (226, 172, 32)


def ground(rng: random.Random, base: tuple[int, int, int]) -> Image.Image:
    """Dry terrain: a base colour broken by noise, field patches and soil streaks."""
    image = Image.new("RGB", (W, W), base)
    for cells, sigma, low in ((W // 160, 60, 165), (W // 40, 55, 180), (W // 8, 55, 190), (W, 50, 200)):
        noise = Image.effect_noise((cells, cells), sigma).resize((W, W), Image.BICUBIC).convert("RGB")
        image = ImageChops.multiply(image, noise.point(lambda v, low=low: min(255, low + v * (255 - low) // 150)))
    draw = ImageDraw.Draw(image)
    for _ in range(14):  # paler soil patches and darker scrub
        x, y, r = rng.randint(0, W), rng.randint(0, W), rng.randint(40, 160) * S
        tone = rng.choice([(14, 12, 8), (-16, -10, -12)])
        patch = Image.new("L", (W, W), 0)
        ImageDraw.Draw(patch).ellipse((x - r, y - r * 0.6, x + r, y + r * 0.6), fill=90)
        patch = patch.filter(ImageFilter.GaussianBlur(30 * S))
        shifted = image.point(lambda v, t=tone[0]: max(0, min(255, v + t)))
        image = Image.composite(shifted, image, patch)
    return image


def trees(draw: ImageDraw.ImageDraw, rng: random.Random, count: int, box: tuple[int, int, int, int]) -> None:
    for _ in range(count):
        x, y = rng.randint(box[0], box[2]), rng.randint(box[1], box[3])
        r = rng.randint(9, 20) * S
        draw.ellipse((x - r + SHADOW[0], y - r + SHADOW[1], x + r + SHADOW[0], y + r + SHADOW[1]), fill=(52, 50, 40))
        shade = rng.randint(0, 22)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(58 + shade, 78 + shade, 44 + shade // 2))
        draw.ellipse((x - r // 2, y - r // 2 - 3, x + r // 3, y + r // 4), fill=(78 + shade, 98 + shade, 56 + shade // 2))


def road(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], width: int, lanes: bool = True) -> None:
    draw.line(points, fill=(184, 176, 160), width=width + 10 * S, joint="curve")
    draw.line(points, fill=(84, 86, 88), width=width, joint="curve")
    if lanes:
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            length = math.hypot(x2 - x1, y2 - y1)
            steps = int(length // (40 * S))
            for i in range(steps):
                a, b = i / steps, (i + 0.45) / steps
                draw.line((x1 + (x2 - x1) * a, y1 + (y2 - y1) * a, x1 + (x2 - x1) * b, y1 + (y2 - y1) * b),
                          fill=(226, 224, 214), width=2 * S)


def shadowed_rect(draw, box, fill, height=1.0):
    x1, y1, x2, y2 = box
    dx, dy = int(SHADOW[0] * height), int(SHADOW[1] * height)
    draw.polygon([(x2, y1), (x2 + dx, y1 + dy), (x2 + dx, y2 + dy), (x1 + dx, y2 + dy), (x1, y2), (x2, y2)], fill=(44, 42, 38))
    draw.rectangle(box, fill=fill)


def building(draw, rng, box, roof, ridges="x", height=3.0, units=True):
    """A large flat or ridged roof with its shadow, ridge lines and rooftop units."""
    shadowed_rect(draw, box, roof, height)
    x1, y1, x2, y2 = box
    darker = tuple(max(0, c - 18) for c in roof)
    if ridges == "x":
        for x in range(x1 + 10 * S, x2, 12 * S):
            draw.line((x, y1 + 2, x, y2 - 2), fill=darker, width=S)
    elif ridges == "y":
        for y in range(y1 + 10 * S, y2, 12 * S):
            draw.line((x1 + 2, y, x2 - 2, y), fill=darker, width=S)
    draw.rectangle(box, outline=tuple(max(0, c - 40) for c in roof), width=2 * S)
    if units:
        for _ in range(max(2, (x2 - x1) * (y2 - y1) // (9000 * S * S))):
            ux, uy = rng.randint(x1 + 12 * S, x2 - 26 * S), rng.randint(y1 + 12 * S, y2 - 22 * S)
            shadowed_rect(draw, (ux, uy, ux + 12 * S, uy + 9 * S), (206, 208, 210), 0.4)


def car(draw, x, y, angle, colour):
    """A civilian car about 4.5 x 1.8 m: body, darker windscreen and rear window, shadow."""
    length, width = 15 * S, 6.5 * S
    ca, sa = math.cos(angle), math.sin(angle)

    def poly(l1, l2, w):
        pts = [(l1, -w), (l2, -w), (l2, w), (l1, w)]
        return [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts]
    draw.polygon([(px + 3 * S, py + 3 * S) for px, py in poly(-length / 2, length / 2, width / 2)], fill=(40, 38, 34))
    draw.polygon(poly(-length / 2, length / 2, width / 2), fill=colour)
    glass = (34, 40, 48) if sum(colour) > 200 else (70, 78, 90)
    draw.polygon(poly(length * 0.12, length * 0.3, width * 0.4), fill=glass)
    draw.polygon(poly(-length * 0.36, -length * 0.24, width * 0.4), fill=glass)


def parking(draw, rng, box, rows, fill_ratio=0.75, vertical=False):
    x1, y1, x2, y2 = box
    draw.rectangle(box, fill=(96, 98, 98))
    stall = 9 * S
    depth = 20 * S
    for r in range(rows):
        ry = y1 + 8 * S + r * (depth * 2 + 14 * S)
        for x in range(x1 + 6 * S, x2 - stall, stall):
            for side, sy in ((0, ry), (1, ry + depth + 14 * S)):
                if sy + depth > y2:
                    continue
                draw.line((x, sy, x, sy + depth), fill=(214, 214, 206), width=S)
                if rng.random() < fill_ratio:
                    car(draw, x + stall / 2, sy + depth / 2, math.pi / 2 + rng.uniform(-0.05, 0.05), rng.choice(CAR_COLOURS))


def excavator(draw, x, y, angle):
    ca, sa = math.cos(angle), math.sin(angle)

    def at(px, py):
        return (x + px * ca - py * sa, y + px * sa + py * ca)
    tracks = [at(-16 * S, -12 * S), at(16 * S, -12 * S), at(16 * S, 12 * S), at(-16 * S, 12 * S)]
    draw.polygon([(px + 6 * S, py + 5 * S) for px, py in tracks], fill=(40, 38, 34))
    draw.polygon(tracks, fill=(52, 52, 50))
    body = [at(-11 * S, -9 * S), at(11 * S, -9 * S), at(11 * S, 9 * S), at(-11 * S, 9 * S)]
    draw.polygon(body, fill=YELLOW)
    draw.polygon([at(-2 * S, -8 * S), at(8 * S, -8 * S), at(8 * S, 0), at(-2 * S, 0)], fill=(48, 56, 64))
    draw.line([at(6 * S, 4 * S), at(32 * S, 6 * S), at(44 * S, 0)], fill=(196, 148, 26), width=5 * S)
    draw.polygon([at(42 * S, -6 * S), at(50 * S, -5 * S), at(50 * S, 6 * S), at(42 * S, 6 * S)], fill=(70, 66, 60))


def dump_truck(draw, x, y, angle, bed=(214, 214, 210)):
    ca, sa = math.cos(angle), math.sin(angle)

    def r(l1, l2, w1, w2):
        return [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in [(l1, w1), (l2, w1), (l2, w2), (l1, w2)]]
    draw.polygon([(px + 5 * S, py + 4 * S) for px, py in r(-24 * S, 22 * S, -9 * S, 9 * S)], fill=(40, 38, 34))
    draw.polygon(r(-24 * S, 10 * S, -9 * S, 9 * S), fill=bed)
    draw.polygon(r(-20 * S, 6 * S, -6 * S, 6 * S), fill=(170, 150, 120))
    draw.polygon(r(12 * S, 22 * S, -8 * S, 8 * S), fill=(196, 60, 40))


def mixer(draw, x, y, angle):
    dump_truck(draw, x, y, angle, bed=(200, 200, 196))
    ca, sa = math.cos(angle), math.sin(angle)
    cx, cy = x - 7 * S * ca, y - 7 * S * sa
    draw.ellipse((cx - 13 * S, cy - 8 * S, cx + 13 * S, cy + 8 * S), fill=(232, 232, 228), outline=(160, 160, 156), width=S)


def crane(draw, x, y, angle, length):
    ca, sa = math.cos(angle), math.sin(angle)
    ex, ey = x + length * ca, y + length * sa
    bx, by = x - length * 0.25 * ca, y - length * 0.25 * sa
    draw.line((bx + 40 * S, by + 30 * S, ex + 40 * S, ey + 30 * S), fill=(46, 44, 40), width=4 * S)  # shadow on the ground
    draw.line((bx, by, ex, ey), fill=(236, 186, 36), width=4 * S)
    for i in range(1, 12):
        t = i / 12
        px, py = bx + (ex - bx) * t, by + (ey - by) * t
        draw.line((px - 3 * S * sa, py + 3 * S * ca, px + 3 * S * sa, py - 3 * S * ca), fill=(180, 140, 30), width=S)
    draw.rectangle((bx - 9 * S, by - 9 * S, bx + 9 * S, by + 9 * S), fill=(150, 150, 146))
    draw.rectangle((x - 7 * S, y - 7 * S, x + 7 * S, y + 7 * S), fill=(236, 186, 36))


def pile(draw, x, y, r, colour):
    draw.ellipse((x - r + 8 * S, y - r * 0.8 + 6 * S, x + r + 8 * S, y + r * 0.8 + 6 * S), fill=(86, 78, 66))
    draw.ellipse((x - r, y - r * 0.8, x + r, y + r * 0.8), fill=colour)
    draw.ellipse((x - r * 0.5, y - r * 0.5, x + r * 0.2, y + r * 0.1), fill=tuple(min(255, c + 22) for c in colour))


def container(draw, x, y, colour, vertical=False):
    box = (x, y, x + (10 if vertical else 24) * S, y + (24 if vertical else 10) * S)
    shadowed_rect(draw, box, colour, 0.6)
    for i in range(1, 6):
        if vertical:
            draw.line((box[0], box[1] + i * 4 * S, box[2], box[1] + i * 4 * S), fill=tuple(c - 20 for c in colour), width=1)
        else:
            draw.line((box[0] + i * 4 * S, box[1], box[0] + i * 4 * S, box[3]), fill=tuple(c - 20 for c in colour), width=1)


def finish(image: Image.Image, name: str, rng: random.Random) -> None:
    image = image.filter(ImageFilter.GaussianBlur(0.8)).resize((SIZE, SIZE), Image.LANCZOS)
    haze = Image.new("RGB", image.size, (196, 194, 186))
    image = ImageChops.blend(image, haze, 0.06)
    ImageDraw.Draw(image).text((8, SIZE - 16), "SYNTHETIC DEMO", fill=(240, 240, 236))
    OUT.mkdir(parents=True, exist_ok=True)
    image.save(OUT / name, optimize=True)


def scene_logistics(rng):
    """A logistics park: two large warehouses, a full staff car park, cars on the access road."""
    image = ground(rng, (178, 160, 124))
    draw = ImageDraw.Draw(image)
    trees(draw, rng, 60, (0, 0, W, 260 * S))
    road(draw, [(0, 640 * S), (520 * S, 600 * S), (W, 560 * S)], 30 * S)
    road(draw, [(420 * S, 610 * S), (430 * S, 470 * S)], 18 * S, lanes=False)
    building(draw, rng, (60 * S, 300 * S, 400 * S, 470 * S), (216, 218, 220), "x", 3.4)
    building(draw, rng, (470 * S, 280 * S, 760 * S, 420 * S), (150, 170, 190), "y", 3.0)
    parking(draw, rng, (470 * S, 440 * S, 760 * S, 545 * S), 1, 0.85)
    for i in range(6):
        car(draw, (60 + i * 120 + rng.randint(-15, 15)) * S, (632 - i * 6) * S, -0.08, rng.choice(CAR_COLOURS))
    trees(draw, rng, 30, (0, 690 * S, W, W))
    return image


def scene_construction(rng):
    """A construction site: a large concrete frame, a tower crane, two excavators, a mixer, material piles."""
    image = ground(rng, (190, 170, 132))
    site = (40 * S, 120 * S, 760 * S, 700 * S)
    image.paste(ground(rng, (176, 156, 122)).crop(site), site[:2])  # graded earth, paler than the land around
    draw = ImageDraw.Draw(image)
    draw.rectangle(site, outline=(150, 136, 108), width=3 * S)
    road(draw, [(0, 740 * S), (W, 730 * S)], 30 * S)
    draw.rectangle((330 * S, 700 * S, 370 * S, 730 * S), fill=(120, 116, 108))
    shadowed_rect(draw, (120 * S, 170 * S, 470 * S, 420 * S), (190, 190, 186), 2.6)
    for x in range(120 * S, 471 * S, 35 * S):
        draw.line((x, 170 * S, x, 420 * S), fill=(150, 150, 146), width=3 * S)
    for y in range(170 * S, 421 * S, 35 * S):
        draw.line((120 * S, y, 470 * S, y), fill=(150, 150, 146), width=3 * S)
    draw.rectangle((330 * S, 240 * S, 470 * S, 420 * S), fill=(212, 210, 204))
    crane(draw, 500 * S, 300 * S, -2.6, 380 * S)
    excavator(draw, 560 * S, 520 * S, 0.6)
    excavator(draw, 230 * S, 540 * S, -0.3)
    dump_truck(draw, 650 * S, 610 * S, 3.0)
    dump_truck(draw, 330 * S, 600 * S, 1.6)
    mixer(draw, 520 * S, 640 * S, 0.1)
    pile(draw, 640 * S, 220 * S, 55 * S, (204, 196, 176))
    pile(draw, 690 * S, 360 * S, 40 * S, (150, 120, 92))
    for i in range(5):
        container(draw, (90 + i * 30) * S, 470 * S, rng.choice([(30, 90, 140), (170, 60, 40), (220, 220, 214)]), vertical=True)
    for i in range(7):
        car(draw, (90 + i * 22) * S, 660 * S, math.pi / 2, rng.choice(CAR_COLOURS))
    trees(draw, rng, 20, (0, 0, W, 100 * S))
    return image


def scene_factory(rng):
    """A factory beside the main road: a long hall, silos, a yard of trucks and cars, traffic on the road."""
    image = ground(rng, (172, 158, 120))
    draw = ImageDraw.Draw(image)
    trees(draw, rng, 45, (0, 560 * S, W, W))
    road(draw, [(0, 470 * S), (W, 520 * S)], 34 * S)
    building(draw, rng, (60 * S, 90 * S, 560 * S, 260 * S), (226, 226, 222), "x", 3.6)
    building(draw, rng, (600 * S, 80 * S, 740 * S, 200 * S), (190, 120, 90), "y", 2.4)
    for i in range(4):
        cx, cy = (620 + (i % 2) * 60) * S, (260 + (i // 2) * 60) * S
        draw.ellipse((cx - 22 * S + 26 * S, cy - 22 * S + 18 * S, cx + 22 * S + 26 * S, cy + 22 * S + 18 * S), fill=(46, 44, 40))
        draw.ellipse((cx - 22 * S, cy - 22 * S, cx + 22 * S, cy + 22 * S), fill=(214, 216, 218), outline=(170, 172, 174), width=2 * S)
    draw.rectangle((60 * S, 290 * S, 560 * S, 420 * S), fill=(132, 130, 124))
    for i in range(4):
        dump_truck(draw, (110 + i * 70) * S, 340 * S, math.pi / 2, bed=(230, 230, 226))
    parking(draw, rng, (380 * S, 300 * S, 560 * S, 410 * S), 1, 0.8)
    for i in range(8):
        lane = 478 if i % 2 else 505
        car(draw, (40 + i * 95 + rng.randint(-20, 20)) * S, (lane + i * 3) * S, 0.06, rng.choice(CAR_COLOURS))
    return image


def scene_depot(rng):
    """A plant-hire depot: a hangar, rows of yellow machines, containers, a customer car park."""
    image = ground(rng, (184, 166, 128))
    draw = ImageDraw.Draw(image)
    trees(draw, rng, 40, (0, 0, 300 * S, W))
    road(draw, [(720 * S, 0), (700 * S, W)], 30 * S)
    yard = (300 * S, 80 * S, 680 * S, 740 * S)
    image.paste(ground(rng, (156, 150, 138)).crop(yard), yard[:2])  # gravel yard
    draw = ImageDraw.Draw(image)
    building(draw, rng, (330 * S, 100 * S, 650 * S, 250 * S), (176, 186, 196), "y", 3.2)
    for i in range(4):
        excavator(draw, (360 + i * 75) * S, 320 * S, math.pi / 2)
    for i in range(3):
        dump_truck(draw, (370 + i * 90) * S, 440 * S, math.pi / 2, bed=YELLOW)
    for i in range(3):
        mixer(draw, (380 + i * 90) * S, 540 * S, math.pi / 2)
    for i in range(6):
        container(draw, (330 + i * 52) * S, 620 * S, [(30, 90, 140), (170, 60, 40), (40, 110, 70)][i % 3])
    parking(draw, rng, (330 * S, 660 * S, 650 * S, 735 * S), 1, 0.7)
    return image


SCENES = [("sat-area-a.png", scene_logistics), ("sat-area-b.png", scene_construction),
          ("sat-area-c.png", scene_factory), ("sat-area-d.png", scene_depot)]


def main() -> int:
    for n, (name, draw_scene) in enumerate(SCENES):
        rng = random.Random(4100 + n)
        finish(draw_scene(rng), name, rng)
        print(f"wrote {OUT / name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
