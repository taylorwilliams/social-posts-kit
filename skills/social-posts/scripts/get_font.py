#!/usr/bin/env python3
"""Download a Google Font into brand/fonts, for the images.

    python3 get_font.py "Font Name"

Prints the file it saved, and the weights it has (such as Bold), for brand.json.
Only works for fonts on fonts.google.com, and needs internet access. For any
other font, put the .ttf or .otf file you are licensed to use in brand/fonts.
"""
import json, os, sys, urllib.parse, urllib.request

FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'brand', 'fonts')


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'social-posts-kit'}), timeout=60) as r:
        return r.read()


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    name = sys.argv[1]
    folder = ''.join(name.lower().split())
    for licence in ('ofl', 'apache', 'ufl'):
        try:
            files = json.loads(get(f'https://api.github.com/repos/google/fonts/contents/{licence}/{folder}'))
        except Exception:
            continue
        ttfs = [f for f in files if f['name'].endswith('.ttf')]
        # Prefer the upright variable font, which holds every weight.
        ttfs.sort(key=lambda f: ('Italic' in f['name'], '[' not in f['name'], f['name']))
        if not ttfs:
            continue
        os.makedirs(FONTS, exist_ok=True)
        target = os.path.join(FONTS, ''.join(name.split()) + '.ttf')
        with open(target, 'wb') as out:
            out.write(get(ttfs[0]['download_url']))
        for f in files:
            if f['name'].upper().startswith(('OFL', 'LICENSE')):
                with open(os.path.join(FONTS, f'{"".join(name.split())}-{f["name"]}'), 'wb') as out:
                    out.write(get(f['download_url']))
        print(f'Saved fonts/{os.path.basename(target)}')
        try:
            from PIL import ImageFont
            weights = [v.decode() for v in ImageFont.truetype(target, 20).get_variation_names()]
            print('Weights: ' + ', '.join(weights))
        except Exception:
            print('One weight only (not a variable font): leave "variation" out in brand.json.')
        return
    sys.exit(f'"{name}" is not on Google Fonts. Ask for the font file, or pick a similar Google Font.')


if __name__ == '__main__':
    main()
