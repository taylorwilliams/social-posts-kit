#!/usr/bin/env python3
"""Draw the images for a social post, in your brand, at each network's exact size.

    python3 render.py SPEC.json

Needs Python 3 and Pillow (`pip install pillow`). Nothing else: it runs on a
laptop, in Claude's code tool and in ChatGPT's.

Your brand comes from ../brand/brand.json (colours, fonts, logo). The spec says
what to draw:

    {
      "slug": "spring-price-update",            names the output folder
      "title": "How to take orders on WhatsApp with AI",
      "accent": "AI",                           optional: one word drawn in your accent colour
      "kicker": "Guide",                        optional: the small line above the title
      "layout": "chat",                         "cover", "chat" or "screenshot"
      "chat": {                                 for "chat": a short phone conversation
        "business": "Your Business",
        "messages": [["in", "Can I book for Friday?"], ["out", "Friday at 10. Is that right?"], ["in", "Yes please"]],
        "card": ["Booking added", "Friday · 10:00"]
      },
      "screenshot": "screen.png",               for "screenshot": a picture of your product (path, or a file in brand/examples)
      "formats": ["linkedin", "instagram"]       optional: leave out for every size
    }

Writes PNGs to output/<slug>/ in the current folder (or the spec's "out" folder) and prints each path.
"""
import json, os, sys

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError:
    sys.exit('This needs Pillow. Install it with: pip install pillow')

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.abspath(os.path.join(HERE, '..'))
BRAND_DIR = os.path.join(SKILL, 'brand')

FORMATS = {
    'linkedin': (1200, 627),            # LinkedIn feed image
    'linkedin-portrait': (1080, 1350),  # LinkedIn portrait, more of the phone screen
    'instagram': (1080, 1350),          # Instagram feed, 4:5, best reach
    'instagram-square': (1080, 1080),   # Instagram feed, square
    'story': (1080, 1920),              # Instagram or Facebook story
}


# ---------- brand ----------

def load_brand():
    path = os.path.join(BRAND_DIR, 'brand.json')
    if not os.path.exists(path):
        sys.exit('No brand/brand.json yet. Run the setup first (see START-HERE.md).')
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def colour(brand, name, fallback):
    return brand.get('colours', {}).get(name) or fallback


def font(brand, role, size):
    """A font from brand.json: {"file": "fonts/Inter.ttf", "variation": "Bold"}."""
    spec = brand.get('fonts', {}).get(role) or {}
    path = os.path.join(BRAND_DIR, spec.get('file', 'fonts/Inter.ttf'))
    try:
        f = ImageFont.truetype(path, size)
    except OSError:
        f = ImageFont.load_default(size)
        return f
    want = spec.get('variation')
    if want:
        try:
            f.set_variation_by_name(want)
        except (OSError, ValueError):
            pass
    return f


# ---------- drawing helpers ----------

def wrap(draw, words, f, width):
    """Split words into lines that fit `width`."""
    lines, line = [], []
    for w in words:
        test = ' '.join(line + [w])
        if line and draw.textlength(test, font=f) > width:
            lines.append(line)
            line = [w]
        else:
            line.append(w)
    if line:
        lines.append(line)
    return lines


def fit_title(draw, text, brand, width, max_lines, start, smallest):
    """The biggest heading size that fits the title in `max_lines`."""
    size = start
    while size > smallest:
        f = font(brand, 'heading', size)
        if len(wrap(draw, text.split(), f, width)) <= max_lines:
            return f, size
        size -= 4
    return font(brand, 'heading', smallest), smallest


def draw_title(draw, xy, text, accent_word, f, size, width, ink, accent):
    """The title, word by word, with the accent word in the accent colour. Returns the bottom y."""
    x0, y = xy
    line_h = int(size * 1.08)
    space = draw.textlength(' ', font=f)
    for line in wrap(draw, text.split(), f, width):
        x = x0
        for w in line:
            bare = w.strip('.,:;!?')
            draw.text((x, y), w, font=f, fill=accent if accent_word and bare == accent_word else ink)
            x += draw.textlength(w, font=f) + space
        y += line_h
    return y


def shadow(base, box, radius, blur, offset=(0, 18), alpha=70):
    layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0 + offset[0], y0 + offset[1], x1 + offset[0], y1 + offset[1]), radius, fill=(15, 23, 42, alpha))
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))


def logo(base, brand, xy, height):
    """The logo from brand.json, or the business name in the heading font."""
    draw = ImageDraw.Draw(base)
    path = brand.get('logo', {}).get('file')
    if path and os.path.exists(os.path.join(BRAND_DIR, path)):
        img = Image.open(os.path.join(BRAND_DIR, path)).convert('RGBA')
        img = img.resize((max(1, int(img.width * height / img.height)), height), Image.LANCZOS)
        base.alpha_composite(img, (int(xy[0]), int(xy[1])))
        return
    f = font(brand, 'heading', int(height * 0.9))
    draw.text(xy, brand.get('name') or 'Your Business', font=f, fill=colour(brand, 'ink', '#111827'))


def tick(draw, centre, r, fill, line):
    cx, cy = centre
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)
    draw.line([(cx - r * .45, cy + r * .02), (cx - r * .1, cy + r * .38), (cx + r * .5, cy - r * .35)], fill=line, width=max(3, int(r * .2)), joint='curve')


# ---------- the three visuals ----------

def chat_phone(base, brand, box, spec):
    """A phone with a short conversation, and an optional result card over its lower half."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    draw = ImageDraw.Draw(base)
    ink = colour(brand, 'ink', '#111827')
    r = int(w * 0.14)
    shadow(base, box, r, 30)
    draw.rounded_rectangle(box, r, fill=ink)
    pad = int(w * 0.035)
    sx0, sy0, sx1, sy1 = x0 + pad, y0 + pad, x1 - pad, y1 - pad
    draw.rounded_rectangle((sx0, sy0, sx1, sy1), r - pad, fill=colour(brand, 'chatBackground', '#EFE7DD'))
    head_h = int(w * 0.24)
    draw.rounded_rectangle((sx0, sy0, sx1, sy0 + head_h), r - pad, fill=colour(brand, 'chatHeader', '#075E54'))
    draw.rectangle((sx0, sy0 + head_h // 2, sx1, sy0 + head_h), fill=colour(brand, 'chatHeader', '#075E54'))
    av = int(w * 0.1)
    ay = sy0 + head_h - av - int(w * 0.04)
    draw.ellipse((sx0 + pad * 2, ay, sx0 + pad * 2 + av, ay + av), fill='#CFD8DC')
    hf = font(brand, 'bodyBold', int(w * 0.06))
    chat = spec.get('chat', {})
    draw.text((sx0 + pad * 2 + av + pad * 1.5, ay + av / 2), chat.get('business') or brand.get('name') or 'Your Business', font=hf, fill='#FFFFFF', anchor='lm')
    bf = font(brand, 'body', int(w * 0.058))
    y = sy0 + head_h + pad * 2
    max_bw = (sx1 - sx0) * 0.78
    for side, text in chat.get('messages', []):
        lines = [' '.join(l) for l in wrap(draw, text.split(), bf, max_bw - pad * 3)]
        lh = int(bf.size * 1.3)
        bw = max(draw.textlength(l, font=bf) for l in lines) + pad * 3
        bh = lh * len(lines) + pad * 2
        bx = sx0 + pad * 1.5 if side == 'in' else sx1 - pad * 1.5 - bw
        draw.rounded_rectangle((bx, y, bx + bw, y + bh), int(pad * 1.2), fill='#FFFFFF' if side == 'in' else colour(brand, 'chatOut', '#D9FDD3'))
        for i, l in enumerate(lines):
            draw.text((bx + pad * 1.5, y + pad + i * lh), l, font=bf, fill='#111B21')
        y += bh + pad * 1.4
    card = chat.get('card')
    if card:
        cw = int(w * 1.25)
        cx0 = x0 - int(w * 0.38)
        cy0 = int(y + pad * 2)
        tf = font(brand, 'heading', int(w * 0.062))
        df = font(brand, 'body', int(w * 0.055))
        ch = int(tf.size * 1.3 + df.size * 1.3 + pad * 5)
        shadow(base, (cx0, cy0, cx0 + cw, cy0 + ch), int(pad * 2.4), 18, (0, 10), 60)
        draw.rounded_rectangle((cx0, cy0, cx0 + cw, cy0 + ch), int(pad * 2.4), fill='#FFFFFF')
        tr = int(ch * 0.24)
        tick(draw, (cx0 + pad * 2.5 + tr, cy0 + ch / 2), tr, colour(brand, 'accent', '#4F46E5'), '#FFFFFF')
        tx = cx0 + pad * 5 + tr * 2
        draw.text((tx, cy0 + pad * 2.5), card[0], font=tf, fill=ink)
        draw.text((tx, cy0 + pad * 2.5 + tf.size * 1.3), card[1] if len(card) > 1 else '', font=df, fill=colour(brand, 'muted', '#4B5563'))


def screenshot(base, brand, box, spec):
    """A picture of your product, in a light browser frame."""
    path = spec.get('screenshot') or ''
    full = next((p for p in (path, os.path.join(BRAND_DIR, 'examples', path)) if p and os.path.exists(p)), path)
    if not path or not os.path.exists(full):
        sys.exit(f'No screenshot at {path}')
    x0, y0, x1, y1 = box
    img = Image.open(full).convert('RGBA')
    bar = int((x1 - x0) * 0.035)
    w = x1 - x0
    h = min(int(img.height * w / img.width), y1 - y0 - bar)
    img = img.resize((w, int(img.height * w / img.width)), Image.LANCZOS).crop((0, 0, w, h))
    frame = (x0, y0, x1, y0 + bar + h)
    shadow(base, frame, 18, 26)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(frame, 18, fill=colour(brand, 'ink', '#111827'))
    for i in range(3):
        cx = x0 + bar * (0.9 + i * 0.7)
        d.ellipse((cx - bar * .18, y0 + bar * .32, cx + bar * .18, y0 + bar * .68), fill='#6B7280')
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, -20, w, h), 18, fill=255)
    base.paste(img, (x0, y0 + bar), mask)


def cover(base, brand, box, spec):
    """A plain brand panel: overlapping circles in the brand colours."""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, 28, fill=colour(brand, 'soft', '#E0E7FF'))
    w, h = x1 - x0, y1 - y0
    r = int(min(w, h) * 0.3)
    cx, cy = x0 + w // 2, y0 + h // 2
    d.ellipse((cx - r - r // 2, cy - r, cx + r - r // 2, cy + r), fill=colour(brand, 'accent', '#4F46E5'))
    d.ellipse((cx - r + r // 2, cy - r, cx + r + r // 2, cy + r), outline=colour(brand, 'ink', '#111827'), width=max(4, r // 18))


VISUALS = {'chat': chat_phone, 'screenshot': screenshot, 'cover': cover}


# ---------- page layouts ----------

def render(brand, spec, w, h):
    base = Image.new('RGBA', (w, h), colour(brand, 'background', '#F7F7F5'))
    draw = ImageDraw.Draw(base)
    ink = colour(brand, 'ink', '#111827')
    accent = colour(brand, 'accent', '#4F46E5')
    kicker = (spec.get('kicker') or '').upper()
    visual = VISUALS[spec.get('layout', 'cover')]
    wide = w > h * 1.3
    m = int(min(w, h) * 0.075)

    if wide:
        col = int(w * 0.47)
        f, size = fit_title(draw, spec['title'], brand, col, 3, int(h * 0.11), 46)
        if len(wrap(draw, spec['title'].split(), f, col)) > 3:
            f, size = fit_title(draw, spec['title'], brand, col, 4, 46, 30)
        kf = font(brand, 'bodyBold', int(h * 0.03))
        lines = len(wrap(draw, spec['title'].split(), f, col))
        block = (kf.size * 2 if kicker else 0) + int(size * 1.08) * lines + int(h * 0.12)
        y = (h - block) // 2
        if kicker:
            draw.text((m, y), kicker, font=kf, fill=accent)
            y += kf.size * 2
        y = draw_title(draw, (m, y), spec['title'], spec.get('accent'), f, size, col, ink, accent)
        logo(base, brand, (m, y + int(h * 0.04)), int(h * 0.06))
        vx0 = m + col + int(w * 0.05)
        if spec.get('layout') == 'chat':
            pw = int(w * 0.25)
            chat_phone(base, brand, (w - m - pw, int(h * 0.07), w - m, int(h * 0.07) + int(pw * 2.1)), spec)
        else:
            visual(base, brand, (vx0, m, w - m, h - m), spec)
    else:
        col = w - 2 * m
        top = int(h * (0.08 if h < 1500 else 0.12))
        kf = font(brand, 'bodyBold', int(w * 0.03))
        y = top
        if kicker:
            draw.text((m, y), kicker, font=kf, fill=accent)
            y += int(kf.size * 1.9)
        f, size = fit_title(draw, spec['title'], brand, col, 3, int(w * 0.09), 40)
        y = draw_title(draw, (m, y), spec['title'], spec.get('accent'), f, size, col, ink, accent)
        logo(base, brand, (m, y + int(w * 0.02)), int(w * 0.05))
        vy0 = y + int(w * 0.13)
        if spec.get('layout') == 'chat':
            pw = int(w * 0.42)
            px0 = (w - pw) // 2 + int(w * 0.08)
            chat_phone(base, brand, (px0, vy0, px0 + pw, vy0 + int(pw * 2.1)), spec)
        else:
            visual(base, brand, (m, vy0, w - m, h - m), spec)
    return base.convert('RGB')


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding='utf-8') as f:
        spec = json.load(f)
    brand = load_brand()
    out = os.path.join(spec.get('out') or os.path.join(os.getcwd(), 'output'), spec['slug'])
    os.makedirs(out, exist_ok=True)
    for name in spec.get('formats') or list(FORMATS):
        w, h = FORMATS[name]
        path = os.path.join(out, f'{name}-{w}x{h}.png')
        render(brand, spec, w, h).save(path)
        print(path)


if __name__ == '__main__':
    main()
