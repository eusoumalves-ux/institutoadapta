"""Gera OG image (1200x630) para /pg13/v1.

Reproduz a essencia do hero: pill MEC no topo, "PÓS-GRADUAÇÃO" grande
em primary blue, subtitulo da pos, headline com destaques verde/azul,
linha de stats e rodape branco com URL.

Saida: og.png ao lado deste script.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630

# Design system
PRIMARY = (0, 84, 202)            # #0054ca
PRIMARY_BRIGHT = (17, 107, 248)   # #116bf8
GREEN = (83, 227, 0)              # #53e300 tertiary-fixed-dim
BG = (248, 249, 250)              # #f8f9fa surface
INK = (25, 28, 29)                # #191c1d on-surface
INK_VARIANT = (66, 70, 85)        # #424655 on-surface-variant
GRID = (0, 84, 202, 18)           # primary @ ~7%
PILL_BG = (218, 226, 255)         # #dae2ff primary-fixed
WHITE = (255, 255, 255)


def font(size, bold=True):
    """Try system fonts in order of preference."""
    candidates = [
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Bold.ttf",
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size, index=1 if bold and p.endswith(".ttc") else 0)
        except Exception:
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def text_size(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1], bbox[0], bbox[1]


def draw_pill(draw, cx, y, text, fnt, fill, text_color, padding=(28, 14)):
    tw, th, ox, oy = text_size(draw, text, fnt)
    px, py = padding
    rect_w = tw + px * 2
    x = cx - rect_w // 2
    rect = [x, y, x + rect_w, y + th + py * 2 + oy]
    radius = (rect[3] - rect[1]) // 2
    draw.rounded_rectangle(rect, radius=radius, fill=fill)
    draw.text((x + px - ox, y + py), text, font=fnt, fill=text_color)
    return rect


def draw_centered(draw, cx, y, text, fnt, fill):
    tw, th, ox, oy = text_size(draw, text, fnt)
    draw.text((cx - tw // 2 - ox, y), text, font=fnt, fill=fill)
    return tw, th


def draw_centered_segments(draw, cx, y, segments, fnt):
    """Draw colored segments centered as one line.
    segments: list of (text, color) tuples.
    """
    widths = []
    total = 0
    for text, _ in segments:
        tw, _, _, _ = text_size(draw, text, fnt)
        widths.append(tw)
        total += tw
    x = cx - total // 2
    for (text, color), w in zip(segments, widths):
        _, _, ox, oy = text_size(draw, text, fnt)
        draw.text((x - ox, y), text, font=fnt, fill=color)
        x += w


def main():
    img = Image.new("RGB", (W, H), BG)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Subtle grid pattern (matches .bg-grid-subtle, 48x48)
    step = 48
    for x in range(0, W, step):
        d.line([(x, 0), (x, H)], fill=GRID, width=1)
    for y in range(0, H, step):
        d.line([(0, y), (W, y)], fill=GRID, width=1)

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")

    cx = W // 2

    # Brand mark top-left
    f_brand = font(22)
    d.text((50, 40), "INSTITUTO ADAPTA", font=f_brand, fill=INK)

    # Pill MEC center-top
    f_pill = font(20)
    draw_pill(
        d, cx, 95,
        "RECONHECIDA PELO MEC  ·  360H  ·  100% ONLINE",
        f_pill, fill=PILL_BG, text_color=PRIMARY,
        padding=(32, 14),
    )

    # PÓS-GRADUAÇÃO big (fits within 1200 with margin)
    f_hero = font(118)
    draw_centered(d, cx, 165, "PÓS-GRADUAÇÃO", f_hero, fill=PRIMARY)

    # Subtitle
    f_sub = font(30)
    draw_centered(
        d, cx, 305,
        "em Fisioterapia em Reabilitação Cardiopulmonar Domiciliar",
        f_sub, fill=INK,
    )

    # Headline with colored highlights (single line)
    f_head = font(40)
    draw_centered_segments(
        d, cx, 380,
        [
            ("Ganhe ", INK),
            ("segurança", GREEN),
            (" e ", INK),
            ("avance para o próximo nível", PRIMARY),
            (".", INK),
        ],
        f_head,
    )

    # Stats line
    f_stats = font(22)
    draw_centered(
        d, cx, 470,
        "360h  ·  100% online  ·  Sem TCC  ·  Diploma MEC · Focus",
        f_stats, fill=INK_VARIANT,
    )

    # Bottom URL bar (primary gradient feel via solid primary)
    bar_h = 70
    d.rectangle([0, H - bar_h, W, H], fill=PRIMARY)
    f_url = font(24)
    draw_centered(
        d, cx, H - bar_h + 22,
        "pos.institutoadapta.com/pg13",
        f_url, fill=WHITE,
    )

    out = "og.png"
    img.save(out, "PNG", optimize=True)
    print(f"saved {out} {img.size}")


if __name__ == "__main__":
    main()
