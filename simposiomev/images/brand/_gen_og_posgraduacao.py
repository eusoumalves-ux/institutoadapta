"""Gera OG image para a página de Pós-Graduação em MEV.

Saída: og-posgraduacao.png (1200x630), focada na palavra "Pós-Graduação"
e na chancela CBMEV. Mantém a linguagem visual da og-image.png existente
(gradiente azul → azul claro, título em verde, pill verde, faixa branca
inferior com URL).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630

# Cores do design system
PRIMARY_DARK = (0, 84, 202)      # #0054ca
PRIMARY_LIGHT = (17, 107, 248)   # #116bf8
GREEN = (125, 255, 70)           # #7dff46 tertiary-fixed
WHITE = (255, 255, 255)
WHITE_70 = (255, 255, 255, 180)
DARK_TEXT = (25, 28, 29)         # #191c1d on-surface


def gradient_bg(w, h, c1, c2):
    img = Image.new("RGB", (w, h), c1)
    px = img.load()
    for y in range(h):
        t = y / h
        for x in range(w):
            tx = (x / w + t) / 2
            r = int(c1[0] * (1 - tx) + c2[0] * tx)
            g = int(c1[1] * (1 - tx) + c2[1] * tx)
            b = int(c1[2] * (1 - tx) + c2[2] * tx)
            px[x, y] = (r, g, b)
    return img


def font(size, weight="Bold"):
    candidates = [
        f"/System/Library/Fonts/HelveticaNeue.ttc",
        f"/System/Library/Fonts/Helvetica.ttc",
        f"/Library/Fonts/Arial Bold.ttf",
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_pill(draw, xy, text, fnt, fill, text_color, padding=(28, 14)):
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    px, py = padding
    rect = [x, y, x + tw + px * 2, y + th + py * 2]
    radius = (rect[3] - rect[1]) // 2
    draw.rounded_rectangle(rect, radius=radius, fill=fill)
    draw.text((x + px - bbox[0], y + py - bbox[1]), text, font=fnt, fill=text_color)
    return rect


def main():
    img = gradient_bg(W, H, PRIMARY_DARK, PRIMARY_LIGHT)
    d = ImageDraw.Draw(img, "RGBA")

    # Top: brand
    f_brand = font(26)
    d.text((60, 50), "INSTITUTO ADAPTA", font=f_brand, fill=WHITE)

    # PÓS-GRADUAÇÃO — protagonista
    f_title = font(160)
    d.text((60, 130), "PÓS-", font=f_title, fill=GREEN)
    d.text((60, 265), "GRADUAÇÃO", font=f_title, fill=GREEN)

    # Subtitle (white, bold)
    f_sub = font(32)
    d.text((60, 460), "em Medicina do Estilo de Vida e Mudança de Comportamento",
           font=f_sub, fill=WHITE)

    # Stats row
    f_stats = font(22)
    d.text((60, 510),
           "360h  ·  Diploma MEC  ·  100% Online  ·  Acesso vitalício  ·  Harvard · Yale · Einstein",
           font=f_stats, fill=(255, 255, 255, 220))

    # White footer with URL
    footer_h = 60
    d.rectangle([0, H - footer_h, W, H], fill=WHITE)
    f_url = font(22)
    d.text((60, H - footer_h + 18),
           "eventos.institutoadapta.com/simposiomev/posgraduacao",
           font=f_url, fill=DARK_TEXT)

    out = "/Users/malves/Documents/GitHub/institutoadapta/.claude/worktrees/dazzling-colden/simposiomev/images/brand/og-posgraduacao.png"
    img.save(out, "PNG", optimize=True)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
