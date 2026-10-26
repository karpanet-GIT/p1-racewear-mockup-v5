# V5 = V1 (versione pubblicata) + foto reali dei prodotti + scheda di personalizzazione con selezione colori.
# Si lancia una volta sola sui file della V1: python3 transform.py
import re, pathlib
D = pathlib.Path(__file__).parent
SH = 'https://cdn.shopify.com/s/files/1/0795/7010/8699/files/'
def u(name, w=800): return f'{SH}{name}?width={w}'

PRO_ANT = 'P1Images_0000s_0005_PRO-R_Anthracite.jpg'
PRO_BLK = 'P1Images_0000s_0004_PRO-R_Black.jpg'
PRO_SIL = 'PRO-R_SILVER-min.png'
PRO_BACK = 'PRO-R_BACK_SILVER-min.png'

def img(src, alt, extra=''):
    # foto prodotto dentro un riquadro a altezza fissa: contenuta, con il bianco del fondo fuso nel grigio della card
    return (f'<img src="{src}" alt="{alt}" loading="lazy" style="width: 100%; height: 100%; object-fit: contain; '
            f'padding: 16px; box-sizing: border-box; mix-blend-mode: multiply; display: block{extra}">')

def rep_svg(s, label, new, count=1):
    pat = re.compile(r'<svg\b[^>]*aria-label="' + re.escape(label) + r'"[^>]*>.*?</svg>', re.S)
    s2, n = pat.subn(lambda m: new, s, count=count)
    assert n == count, (label, n)
    return s2

def rm(s, text):
    assert text in s, text[:80]
    return s.replace(text, '', 1)

def sub1(s, old, new):
    assert s.count(old) == 1, (old[:90], s.count(old))
    return s.replace(old, new)

def ph_span(s, inner):
    pat = re.compile(r'<span style="position: absolute; left: \d+px; bottom: \d+px; font-family: \'JetBrains Mono\', monospace; font-size: \d+px; color: #[0-9A-F]{6}">' + re.escape(inner) + '</span>')
    s2, n = pat.subn('', s, count=1)
    assert n == 1, inner
    return s2

def unescape_js(s):
    # niente backslash nei file: le sequenze \uXXXX dei testi diventano caratteri veri
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)

# ---------------- HOMEPAGE ----------------
s = (D / 'index.html').read_text()
s = rep_svg(s, 'Illustrazione tuta PRO-R antracite, grigio e giallo fluo', f'<img src="{u(PRO_ANT, 1000)}" alt="Tuta PRO-R antracite" style="height: 86%; width: auto; max-width: 90%; position: relative; display: block">')
s = ph_span(s, '[FOTO HERO: pilota con tuta PRO-R antracite / giallo fluo]')
s = rep_svg(s, 'Illustrazione tuta da gara antracite e giallo fluo', img(u(PRO_ANT), 'Tuta da gara PRO-R antracite'))
s = rep_svg(s, 'Illustrazione maglia ignifuga giallo fluo e sottocasco bianco', img(u('P1Images_0003s_0022_AIRBalaclava_Yellow.jpg'), 'Sottocasco ignifugo AIR giallo'))
s = rep_svg(s, 'Illustrazione guanto nero e scarpa da gara bianca', img(u('P1Images_0005s_0002_SPEED_Black_Silver.jpg'), 'Guanti SPEED neri e argento'))
s = rep_svg(s, 'Illustrazione tuta kart giallo fluo e tuta meccanico blu', img(u('P1Images_0002s_0004_M3_Black_Orange.jpg'), 'Tuta da meccanico M3 nera e arancio'))
s = rep_svg(s, 'Illustrazione tuta vintage bianca con bande azzurre', '<img src="' + u('parabolica2.jpg', 600) + '" alt="Tuta PRO-PARABOLICA bianca e azzurra" loading="lazy" style="width: 100%; height: 100%; object-fit: cover; display: block">')
s = ph_span(s, '{{d.photo}}')
s = rep_svg(s, '{{p.alt}}', img('{{p.img}}', '{{p.alt}}', '; padding: 28px'))
s = ph_span(s, '[FOTO PRODOTTO]')
s = rep_svg(s, 'Illustrazione tuta femminile argento e fucsia', img(u('LITE-STAR_SILVER_AASTSA_FRONT.png'), 'Tuta LITE-STAR argento da donna'))
s = rep_svg(s, 'Illustrazione tuta da bambino accanto alla sagoma di una tuta adulta', img(u('P1Images_0001s_0000_YOUNGGUN_DarkBlue.jpg'), 'Tuta MID-YOUNG GUN da bambino blu scuro'))
s = rep_svg(s, 'Illustrazione tuta per corporature robuste blu scuro', img(u('LITE-EXTRA_DARK_BLUE_3.png'), 'Tuta LITE-EXTRA blu scuro per corporature robuste'))
s = ph_span(s, '{{f.photo}}')
s = rep_svg(s, 'Illustrazione tuta PRO-PARABOLICA bianca con bande azzurre', '<img src="' + u('parabolica2.jpg', 600) + '" alt="Tuta PRO-PARABOLICA bianca e azzurra" loading="lazy" style="width: 100%; height: 100%; object-fit: cover; display: block">')
s = ph_span(s, '[FOTO: PRO-PARABOLICA su auto storica]')
three = ''.join(f'<img src="{u(n, 500)}" alt="{a}" loading="lazy" style="flex: 1 1 0; min-width: 0; height: 100%; object-fit: contain; mix-blend-mode: multiply">' for n, a in [
    (PRO_ANT, 'Tuta PRO-R'), ('LITE-BEST_ROYAL_BLUE_AABERF_FRONT.png', 'Tuta LITE-BEST'), ('P1Images_0001s_0004_LAP.EVO_Red.jpg', 'Tuta MID-LAP.EVO')])
s = rep_svg(s, 'Illustrazione: tre tute delle linee PRO, LITE e MID', f'<span style="display: flex; gap: 4px; width: 100%; height: 100%; padding: 14px; box-sizing: border-box">{three}</span>')
for name, f in [('PRO-R', PRO_ANT), ('MID-LAP.EVO', 'P1Images_0001s_0004_LAP.EVO_Red.jpg'), ('LITE-STAR', 'LITE-STAR_SILVER_AASTSA_FRONT.png'), ('LITE-BEST', 'LITE-BEST_ROYAL_BLUE_AABERF_FRONT.png')]:
    s = re.sub(r"(\{ name: '" + re.escape(name) + r"',.*?)alt: 'Illustrazione ([^']*)' \}", lambda m: m.group(1) + f"alt: 'Tuta {m.group(2)}', img: '{u(f)}' }}", s, count=1)
assert s.count("img: '") == 4
for a, b in [("Tuta MID-LAP.EVO antracite", "Tuta MID-LAP.EVO rossa"), ("Tuta LITE-STAR argento e fucsia", "Tuta LITE-STAR argento"), ("Tuta LITE-BEST antracite", "Tuta LITE-BEST blu royal")]:
    s = s.replace("alt: '" + a + "'", "alt: '" + b + "'")
s = unescape_js(s)
(D / 'index.html').write_text(s)

# ---------------- CATEGORIA ----------------
s = (D / 'categoria.html').read_text()
m = re.search(r'<svg viewBox="0 0 200 300" width="160" height="240" role="img" aria-label="\{\{p\.alt\}\}">.*?</svg>', s, re.S)
s = s.replace(m.group(0), '<sc-if value="{{p.img}}">' + img('{{p.img}}', '{{p.alt}}', '; padding: 24px') + '</sc-if><sc-if value="{{p.noImg}}">' + m.group(0))
s = sub1(s, '[FOTO {{p.name}}]</span>', '[FOTO {{p.name}}]</span></sc-if>')
CAT = {'PRO-R': PRO_ANT, 'PRO-SF': 'P1Images_0000s_0000_PRO-SF_Black.jpg', 'PRO-PARABOLICA': 'parabolica2.jpg', 'LITE-BEST': 'LITE-BEST_ROYAL_BLUE_AABERF_FRONT.png',
       'LITE-STAR': 'LITE-STAR_SILVER_AASTSA_FRONT.png', 'LITE-EXTRA': 'LITE-EXTRA_DARK_BLUE_3.png',
       'LITE-PASSION': 'LITE-PASSION_BLACK_AAPABA_THREEQUARTERFRONTRIGHT_4b38ed66-7cae-4e45-a4b9-5233cd83878c.png',
       'MID-LAP.EVO': 'P1Images_0001s_0004_LAP.EVO_Red.jpg', 'MID-CORSA': 'P1Images_0001s_0012_CORSA_Black.jpg',
       'MID-DIVA': 'P1Images_0001s_0011_DIVA_Anthracite.jpg', 'MID-YOUNG GUN': 'P1Images_0001s_0000_YOUNGGUN_DarkBlue.jpg'}
cat_js = 'const P1IMG = {' + ', '.join(f"'{k}': '{u(v, 600 if v == 'parabolica2.jpg' else 800)}'" for k, v in CAT.items()) + '};\n'
s = sub1(s, 'const products = raw.map((p) => ({', cat_js + 'const products = raw.map((p) => ({')
s = sub1(s, "alt: 'Illustrazione tuta ' + p.name,", "alt: 'Tuta ' + p.name, img: P1IMG[p.name] || '', noImg: !P1IMG[p.name],")
s = unescape_js(s)
(D / 'categoria.html').write_text(s)

# ---------------- STORIA ----------------
s = (D / 'storia.html').read_text()
pano = ''.join(f'<span style="flex: 1 1 0; min-width: 0; height: 100%; background: #FFFFFF; display: flex; align-items: center; justify-content: center"><img src="{u(n, 600)}" alt="{a}" loading="lazy" style="width: 100%; height: 100%; object-fit: contain; padding: 12px; box-sizing: border-box"></span>' for n, a in [
    (PRO_ANT, 'Tuta PRO-R antracite'), ('LITE-STAR_SILVER_AASTSA_FRONT.png', 'Tuta LITE-STAR argento'), ('P1Images_0001s_0004_LAP.EVO_Red.jpg', 'Tuta MID-LAP.EVO rossa'),
    ('LITE-BEST_ROYAL_BLUE_AABERF_FRONT.png', 'Tuta LITE-BEST blu royal'), ('P1Images_0001s_0000_YOUNGGUN_DarkBlue.jpg', 'Tuta MID-YOUNG GUN blu scuro')])
s = rep_svg(s, 'Illustrazione: tute da gara P1 appese in atelier', f'<span style="display: flex; gap: 12px; width: 100%; height: 100%; padding: 40px; box-sizing: border-box">{pano}</span>')
s = rep_svg(s, 'Illustrazione: tuta PRO-R su gruccia con iniziali ricamate', img(u(PRO_ANT), 'Tuta PRO-R antracite'))
trio = ''.join(f'<img src="{u(n, 600)}" alt="{a}" loading="lazy" style="flex: 1 1 0; min-width: 0; height: 100%; object-fit: contain; mix-blend-mode: multiply">' for n, a in [
    (PRO_BLK, 'Tuta PRO-R nera'), ('P1Images_0001s_0011_DIVA_Anthracite.jpg', 'Tuta MID-DIVA antracite'), ('P1Images_0001s_0012_CORSA_Black.jpg', 'Tuta MID-CORSA nera')])
s = rep_svg(s, 'Illustrazione: tre tute P1 appese', f'<span style="display: flex; gap: 12px; width: 100%; height: 100%; padding: 32px; box-sizing: border-box">{trio}</span>')
s = unescape_js(s)
(D / 'storia.html').write_text(s)

# ---------------- PRODOTTO ----------------
s = (D / 'prodotto.html').read_text()

# galleria: foto vere per fronte, retro e dettagli; l'etichetta FIA resta disegnata (non c'è una foto)
MAINIMG = '<img src="{{mainImg}}" alt="{{mainAlt}}" style="{{mainImgStyle}}">'
s = re.sub(r'<sc-if value="\{\{mv\.front\}\}"><svg\b.*?</svg></sc-if>', '<sc-if value="{{mv.front}}">' + MAINIMG + '</sc-if>', s, count=1, flags=re.S)
s = re.sub(r'<sc-if value="\{\{mv\.back\}\}"><svg\b.*?</svg></sc-if>', '<sc-if value="{{mv.back}}">' + MAINIMG + '</sc-if>', s, count=1, flags=re.S)
TIMG = '<span style="width: 72px; height: 74px; overflow: hidden; display: block; background: #FFFFFF"><img src="{{t.img}}" alt="" style="{{t.imgStyle}}"></span>'
s = re.sub(r'<sc-if value="\{\{t\.front\}\}"><svg\b.*?</svg></sc-if>', '<sc-if value="{{t.front}}">' + TIMG + '</sc-if>', s, count=1, flags=re.S)
s = re.sub(r'<sc-if value="\{\{t\.back\}\}"><svg\b.*?</svg></sc-if>', '<sc-if value="{{t.back}}">' + TIMG + '</sc-if>', s, count=1, flags=re.S)
s = ph_span(s, '{{mainPhoto}}')
s = sub1(s, 'style="flex: 1; min-width: 0; height: 760px; background: #FFFFFF; position: relative; display: flex; align-items: center; justify-content: center"',
         'style="flex: 1; min-width: 0; height: 760px; background: #FFFFFF; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden"')
s = sub1(s, '<span style="position: absolute; top: 18px; left: 18px; display: flex; gap: 6px; flex-wrap: wrap">',
         '<span style="position: absolute; top: 18px; left: 18px; display: flex; gap: 6px; flex-wrap: wrap; z-index: 2">')

# "Completa il kit": foto vere
s = rep_svg(s, 'Illustrazione: maglia X-FLOW giallo fluo e nera', img(u('X-FLOW_COMFORTTOP_1.png'), 'Maglia ignifuga X-FLOW nera'))
s = rep_svg(s, 'Illustrazione: sottocasco AIR bianco', img(u('P1Images_0003s_0027_AIRBalaclavaLarge_White.jpg'), 'Sottocasco AIR bianco'))
s = rep_svg(s, 'Illustrazione: guanto SPEED nero', img(u('P1Images_0005s_0002_SPEED_Black_Silver.jpg'), 'Guanti SPEED neri e argento'))
s = rep_svg(s, 'Illustrazione: scarpa SUPERLIGHT', img(u('P1Images_0004s_0000_SUPERLIGHT_White.jpg'), 'Scarpe da gara SUPERLIGHT bianche'))
s = ph_span(s, '{{p.photo}}')

# carrello laterale: miniature fotografiche
CIMG = '<img src="{{i.img}}" alt="" style="width: 100%; height: 100%; object-fit: contain; padding: 4px; box-sizing: border-box; mix-blend-mode: multiply">'
for k in ['isSuit', 'isTop', 'isGlove']:
    s = re.sub(r'<sc-if value="\{\{i\.' + k + r'\}\}"><svg\b.*?</svg></sc-if>', '<sc-if value="{{i.' + k + '}}">' + CIMG + '</sc-if>', s, count=1, flags=re.S)

# ---- scheda di personalizzazione: selezione colori con anteprima ----
SUIT_F = ('<svg viewBox="0 0 200 300" role="img" aria-label="Anteprima della tuta, fronte" style="width: 46%; max-width: 170px; height: auto">'
 '<path data-fill="c1" style="fill: {{cfgC1}}" d="M80 22 L120 22 L145 38 L172 150 L156 154 L136 80 L138 150 L140 285 L104 285 L100 165 L96 285 L60 285 L62 150 L64 80 L44 154 L28 150 L55 38 Z"></path>'
 '<path data-fill="c2" style="fill: {{cfgC2}}" d="M80 22 L120 22 L145 38 L141 54 L59 54 L55 38 Z"></path>'
 '<path data-fill="c3" style="fill: {{cfgC3}}" d="M86 22 L114 22 L112 30 L88 30 Z M28 150 L44 154 L46 144 L31 140 Z M172 150 L156 154 L154 144 L169 140 Z M61 190 L67 190 L65 285 L60 285 Z M139 190 L133 190 L135 285 L140 285 Z"></path>'
 '<path data-fill="c2" style="fill: {{cfgC2}}" d="M64 112 L136 112 L136 120 L64 120 Z M64 205 L96 205 L96 222 L64 222 Z M104 205 L136 205 L136 222 L104 222 Z"></path>'
 '<path data-stroke="c3" style="fill: none; stroke: {{cfgC3}}" stroke-width="2.5" d="M62 44 L68 72 M70 42 L75 70 M138 44 L132 72 M130 42 L125 70"></path></svg>')
SUIT_B = ('<svg viewBox="0 0 200 300" role="img" aria-label="Anteprima della tuta, retro" style="width: 46%; max-width: 170px; height: auto">'
 '<path data-fill="c1" style="fill: {{cfgC1}}" d="M80 22 L120 22 L145 38 L172 150 L156 154 L136 80 L138 150 L140 285 L104 285 L100 165 L96 285 L60 285 L62 150 L64 80 L44 154 L28 150 L55 38 Z"></path>'
 '<path data-fill="c2" style="fill: {{cfgC2}}" d="M80 22 L120 22 L145 38 L141 54 L59 54 L55 38 Z M76 66 L124 66 L124 106 L76 106 Z M64 112 L136 112 L136 120 L64 120 Z"></path>'
 '<path data-fill="c3" style="fill: {{cfgC3}}" d="M28 150 L44 154 L46 144 L31 140 Z M172 150 L156 154 L154 144 L169 140 Z M61 190 L67 190 L65 285 L60 285 Z M139 190 L133 190 L135 285 L140 285 Z"></path>'
 '<text data-fill="c3" x="100" y="96" text-anchor="middle" font-family="Barlow Condensed, sans-serif" font-weight="800" font-size="28" style="fill: {{cfgC3}}">P1</text></svg>')
CFG = ('<div class="cfgbox">'
 '<div class="cfg-prev"><div class="cfg-views">' + SUIT_F + SUIT_B + '</div>'
 '<span class="cfg-name" data-cfg-name="">{{cfgName}}</span>'
 '<span class="cfg-hint">Anteprima indicativa: la bozza definitiva te la manda l’atelier.</span></div>'
 '<div class="cfg-rows"><sc-for list="{{cfgRows}}" as="r">'
 '<div class="cfg-row"><div class="cfg-head"><label for="sel-{{r.key}}" style="font-size: 14px; font-weight: 500">{{r.label}}</label>'
 '<select id="sel-{{r.key}}" class="fld cfg-sel" data-sel="{{r.key}}" onChange="{{r.change}}"><sc-for list="{{r.sw}}" as="w"><option value="{{w.hex}}" selected="{{w.on}}">{{w.name}}</option></sc-for></select></div>'
 '<div class="sw-grid" role="radiogroup" aria-label="{{r.label}}"><sc-for list="{{r.sw}}" as="w">'
 '<button type="button" role="radio" class="sw" aria-checked="{{w.onTxt}}" aria-label="{{w.label}}" title="{{w.name}}" data-row="{{r.key}}" data-hex="{{w.hex}}" style="{{w.style}}" onClick="{{w.pick}}"></button>'
 '</sc-for></div><input type="hidden" name="{{r.key}}" data-hid="{{r.key}}" value="{{r.hid}}"></div>'
 '</sc-for></div></div>')
old_sel = re.search(r'<div style="display: grid; grid-template-columns: repeat\(auto-fit, minmax\(180px, 1fr\)\); gap: 14px">\s*<div class="z0"><label for="c1".*?</select></div>\s*</div>', s, re.S)
s = s.replace(old_sel.group(0), CFG)
s = sub1(s, '<div class="z0"><label for="loghi" style="font-size: 14px; font-weight: 500">Nome, scritte, loghi e posizioni</label>',
 '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px">'
 '<div class="z0"><label for="ricamo" style="font-size: 14px; font-weight: 500">Nome da ricamare</label><input id="ricamo" class="fld" placeholder="es. M. Rossi"></div>'
 '<div class="z0"><label for="bandiera" style="font-size: 14px; font-weight: 500">Bandiera</label><input id="bandiera" class="fld" placeholder="es. Italia"></div>'
 '<div class="z0"><label for="gruppo" style="font-size: 14px; font-weight: 500">Gruppo sanguigno (facoltativo)</label><select id="gruppo" class="fld"><option>Non ricamare</option><option>0+</option><option>0−</option><option>A+</option><option>A−</option><option>B+</option><option>B−</option><option>AB+</option><option>AB−</option></select></div>'
 '</div>\n<div class="z0"><label for="loghi" style="font-size: 14px; font-weight: 500">Sponsor, scritte e posizioni</label>')
s = sub1(s, '<div class="z0"><label for="m5" style="font-size: 14px; font-weight: 500">Fianchi (cm)</label><input id="m5" class="fld" inputmode="numeric"></div>',
 '<div class="z0"><label for="m5" style="font-size: 14px; font-weight: 500">Fianchi (cm)</label><input id="m5" class="fld" inputmode="numeric"></div>'
 '<div class="z0"><label for="m6" style="font-size: 14px; font-weight: 500">Taglia abituale</label><select id="m6" class="fld"><option>Non so</option><option>46</option><option>48</option><option>50</option><option>52</option><option>54</option><option>56</option><option>58</option><option>60</option><option>62</option><option>64</option></select></div>')

CSS = ('.cfgbox{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start}'
 '.cfg-prev{flex:1 1 240px;min-width:0;background:#F7F7F4;padding:20px 12px 16px;display:flex;flex-direction:column;align-items:center;gap:10px;position:sticky;top:12px}'
 '.cfg-views{display:flex;gap:8px;justify-content:center;width:100%}'
 '.cfg-views path,.cfg-views text{transition:fill .3s ease,stroke .3s ease}'
 '.cfg-name{font-weight:600;font-size:15px;text-align:center}'
 '.cfg-hint{font-size:13px;color:#5A5B5E;text-align:center;max-width:260px}'
 '.cfg-rows{flex:2 1 320px;min-width:0;display:flex;flex-direction:column;gap:20px}'
 '.cfg-head{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;justify-content:space-between;margin-bottom:10px}'
 '.cfg-sel{width:auto;min-width:180px;flex:0 1 220px}'
 '.sw-grid{display:grid;grid-template-columns:repeat(13,minmax(0,1fr));gap:5px}'
 '.sw:focus-visible{outline:3px solid #0E0E0E;outline-offset:2px}'
 '@media (max-width:600px){.sw-grid{grid-template-columns:repeat(9,minmax(0,1fr))}.cfg-prev{position:static}.cfg-sel{flex:1 1 100%}}\n')
s = sub1(s, '<style>\nbody{margin:0}', '<style>\n' + CSS + 'body{margin:0}')

# ---- logica ----
PAL = [['Bianco','#FFFFFF'],['Argento','#D3D4D6'],['Grigio medio','#868686'],['Antracite','#3F3F3F'],['Nero','#111111'],
['Blu navy','#1A2131'],['Blu scuro','#22375E'],['Blu royal','#1D4C89'],['Azzurro cielo','#8DADD2'],['Azzurro neon','#00E1FD'],['Azzurro player','#538DBC'],['Verde Petronas','#42A29D'],
['Giallo neon','#EFFF01'],['Giallo','#FEED02'],['Giallo DHL','#F0C643'],['Oro','#BE9F55'],
['Verde neon','#51FE00'],['Verde prato','#5C975D'],['Verde British','#335B49'],
['Arancio neon','#F2632A'],['Arancio','#C4391D'],['Rosso','#C10E18'],['Viola','#41306F'],['Fucsia','#C4017A'],['Rosa','#CB92BC']]
HELP = ("// I 25 colori della linea PRO, dalla cartella colori ufficiale P1\n"
 "const P1PAL = [" + ', '.join(f"['{n}', '{h}']" for n, h in PAL) + "];\n"
 "const p1Name = (h) => { const p = P1PAL.find((x) => x[1] === String(h).toUpperCase()); return p ? p[0] : h; };\n"
 "const p1Sw = (hex, on) => 'aspect-ratio: 1; min-width: 0; min-height: 22px; padding: 0; border: 0; cursor: pointer; background: ' + hex + '; box-shadow: inset 0 0 0 1px rgba(0,0,0,0.18)' + (on ? '; outline: 2px solid #0E0E0E; outline-offset: 2px' : '');\n"
 "const p1Hex = (v) => (v && /^#[0-9a-f]{6}$/i.test(v)) ? v.toUpperCase() : null;\n"
 "class Component extends DCLogic {")
s = sub1(s, 'class Component extends DCLogic {', HELP)
s = sub1(s, "this.state = { cw: 0, size: '52', tab: 'desc', req: 'grafica', thumb: 0, cart: [], cartOpen: false, justAdded: '' };",
 "const q = typeof location !== 'undefined' ? new URLSearchParams(location.search) : null;\n"
 "this.state = { cw: 0, size: '52', tab: 'desc', req: 'grafica', thumb: 0, cart: [], cartOpen: false, justAdded: '',\n"
 "cfg: { c1: p1Hex(q && q.get('c1')) || '#3F3F3F', c2: p1Hex(q && q.get('c2')) || '#868686', c3: p1Hex(q && q.get('c3')) || '#EFFF01' } };\n"
 "}\n"
 "// cambio colore senza ridisegnare la pagina: i campi gia compilati restano\n"
 "pickColor(k, hex) {\n"
 "this.state.cfg[k] = hex;\n"
 "if (typeof document === 'undefined') return;\n"
 "const D = document, cfg = this.state.cfg;\n"
 "D.querySelectorAll('[data-fill=\"' + k + '\"]').forEach((el) => { el.style.fill = hex; });\n"
 "D.querySelectorAll('[data-stroke=\"' + k + '\"]').forEach((el) => { el.style.stroke = hex; });\n"
 "D.querySelectorAll('.sw[data-row=\"' + k + '\"]').forEach((b) => { const on = b.getAttribute('data-hex') === hex; b.setAttribute('aria-checked', on ? 'true' : 'false'); b.setAttribute('style', p1Sw(b.getAttribute('data-hex'), on)); });\n"
 "D.querySelectorAll('[data-sel=\"' + k + '\"]').forEach((el) => { el.value = hex; });\n"
 "D.querySelectorAll('[data-hid=\"' + k + '\"]').forEach((el) => { el.value = p1Name(hex) + ' ' + hex; });\n"
 "D.querySelectorAll('[data-cfg-name]').forEach((el) => { el.textContent = p1Name(cfg.c1) + ' / ' + p1Name(cfg.c2) + ' / ' + p1Name(cfg.c3); });")

# colorway con foto
s = sub1(s, "{ name: 'Antracite / Grigio medio / Giallo fluo', c1: '#3A3B3E', c2: '#8A8C90', c3: '#DBFB00' },",
 f"{{ name: 'Antracite / Grigio medio / Giallo fluo', c1: '#3A3B3E', c2: '#8A8C90', c3: '#DBFB00', img: '{PRO_ANT}' }},")
s = sub1(s, "{ name: 'Nero / Argento / Azzurro fluo', c1: '#111111', c2: '#C3C5C8', c3: '#3FD8FF' },",
 f"{{ name: 'Nero / Argento / Azzurro fluo', c1: '#111111', c2: '#C3C5C8', c3: '#3FD8FF', img: '{PRO_BLK}' }},")
s = sub1(s, "{ name: 'Argento / Grigio medio / Blu scuro', c1: '#C3C5C8', c2: '#8A8C90', c3: '#1C2A55' }",
 f"{{ name: 'Argento / Grigio medio / Blu scuro', c1: '#C3C5C8', c2: '#8A8C90', c3: '#1C2A55', img: '{PRO_SIL}' }}")
s = sub1(s, "{ label: 'Fronte', short: 'FRONTE', vb: '0 0 200 300', front: true },", "{ label: 'Fronte', short: 'FRONTE', vb: '0 0 200 300', front: true, z: '' },")
s = sub1(s, "{ label: 'Retro', short: 'RETRO', vb: '0 0 200 300', back: true },", "{ label: 'Retro', short: 'RETRO', vb: '0 0 200 300', back: true, z: '' },")
s = sub1(s, "{ label: 'Dettaglio spalle R-FLEXI', short: 'SPALLE', vb: '30 12 140 104', front: true },", "{ label: 'Dettaglio spalle R-FLEXI', short: 'SPALLE', vb: '30 12 140 104', front: true, z: '50% 22%' },")
s = sub1(s, "{ label: 'Dettaglio gamba e ginocchio', short: 'GAMBA', vb: '40 150 120 140', front: true },", "{ label: 'Dettaglio gamba e ginocchio', short: 'GAMBA', vb: '40 150 120 140', front: true, z: '50% 74%' },")
s = sub1(s, "const thumbs = views.map((v, i) => Object.assign({}, v, {",
 "const cwI = cwDefs[st.cw];\n"
 "const SH = '" + SH + "';\n"
 "const photoOf = (v, w) => SH + (v.back ? '" + PRO_BACK + "' : cwI.img) + '?width=' + w;\n"
 "const imgStyle = (v, pad) => 'width: 100%; height: 100%; object-fit: contain; display: block; padding: ' + (v.z ? '0' : pad) + '; box-sizing: border-box' + (v.z ? '; transform: scale(2.4); transform-origin: ' + v.z : '');\n"
 "const thumbs = views.map((v, i) => Object.assign({}, v, {\n"
 "img: photoOf(v, 200), imgStyle: imgStyle(v, '2px'),")
s = sub1(s, "'width: 88px; height: 104px; padding: 4px; cursor: pointer; background: #FFFFFF;", "'width: 88px; height: 104px; padding: 4px; overflow: hidden; cursor: pointer; background: #FFFFFF;")
s = sub1(s, "mainAlt: 'Illustrazione tuta PRO-R, ' + cw.name,",
 "mainAlt: 'Tuta PRO-R, ' + (views[st.thumb].back ? 'argento' : cw.name.toLowerCase()) + ', ' + views[st.thumb].label.toLowerCase(),\n"
 "mainImg: photoOf(views[st.thumb], 1400), mainImgStyle: imgStyle(views[st.thumb], '28px'),")
s = re.sub(r"mainPhoto: '[^\n]*\n", '', s, count=1)
# carrello e upsell con foto
s = sub1(s, "name: x.name, sub: x.sub, qty: x.qty,", "name: x.name, sub: x.sub, qty: x.qty, img: x.img,")
s = sub1(s, "unit: 181.78, kind: 'top' }", "unit: 181.78, kind: 'top', img: '" + u('X-FLOW_COMFORTTOP_1.png', 200) + "' }")
s = sub1(s, "unit: 142.74, kind: 'glove' }", "unit: 142.74, kind: 'glove', img: '" + u('P1Images_0005s_0002_SPEED_Black_Silver.jpg', 200) + "' }")
s = sub1(s, "kind: 'suit', c1: cw.c1, c2: cw.c2, c3: cw.c3 }, q);", "kind: 'suit', c1: cw.c1, c2: cw.c2, c3: cw.c3, img: SH + cw.img + '?width=200' }, q);")
# righe della scheda colori
s = sub1(s, "showGraphic: showGraphic, showMeasures: showMeasures,",
 "showGraphic: showGraphic, showMeasures: showMeasures,\n"
 "cfgC1: st.cfg.c1, cfgC2: st.cfg.c2, cfgC3: st.cfg.c3,\n"
 "cfgName: p1Name(st.cfg.c1) + ' / ' + p1Name(st.cfg.c2) + ' / ' + p1Name(st.cfg.c3),\n"
 "cfgRows: [['c1', 'Colore principale'], ['c2', 'Spalle e fasce'], ['c3', 'Dettagli e profili']].map(([k, label]) => ({\n"
 "key: k, label: label, hid: p1Name(st.cfg[k]) + ' ' + st.cfg[k],\n"
 "change: (e) => this.pickColor(k, e.target.value),\n"
 "sw: P1PAL.map(([nm, hex]) => ({ name: nm, hex: hex, on: st.cfg[k] === hex, onTxt: st.cfg[k] === hex ? 'true' : 'false', label: label + ': ' + nm, style: p1Sw(hex, st.cfg[k] === hex), pick: () => this.pickColor(k, hex) }))\n"
 "})),")
s = unescape_js(s)
(D / 'prodotto.html').write_text(s)
print('ok')
