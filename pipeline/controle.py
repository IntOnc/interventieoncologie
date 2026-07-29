#!/usr/bin/env python3
# Controle op terminologie en kale statements, te draaien voor het pushen.
# Gebruik: python3 pipeline/controle.py
#
# 1. Terminologie: bewaakt dat afkortingen aan de juiste term gekoppeld zijn.
#    RFA hoort bij radiofrequente ablatie, MWA bij microwave/microgolf,
#    TARE/SIRT bij radio-embolisatie (niet chemo), cTACE bij conventioneel en
#    DEB-TACE bij drug-eluting. Een afkorting die in een uitleg tussen haakjes
#    aan de verkeerde term wordt gekoppeld, wordt gemeld. Een gewone opsomming
#    als "RFA of microwave" is geen fout en wordt niet gemeld.
# 2. Kale statements: een kaart met cijfermatige uitkomsten in de tekst maar
#    zonder kernpublicatie, of een kaart zonder enige referentie, wordt gemeld.
import json, re, sys

# afkorting -> (juiste term-fragmenten, foute term-fragmenten)
DEF = {
    'RFA':      (['radiofrequen'], ['microwave', 'microgolf', 'cryo', 'irreversibele elektro']),
    'MWA':      (['microwave', 'microgolf'], ['radiofrequen', 'cryo']),
    'TARE':     (['radio-embol', 'radioembol', 'radio embol', 'yttrium', 'y-90', 'y90', 'sirt', 'internal radiation'],
                 ['chemo-embol', 'chemoembol', 'chemo embol']),
    'SIRT':     (['radio', 'yttrium', 'y-90', 'y90', 'internal radiation'],
                 ['chemo-embol', 'chemoembol', 'chemo embol']),
    'cTACE':    (['conventional', 'conventionele', 'conventionel'], ['drug-eluting', 'drug eluting', 'deb-tace', 'deb ']),
    'DEB-TACE': (['drug-eluting', 'drug eluting'], ['conventional', 'conventionele', 'conventionel']),
}

def kaal(x):
    if x is None: return ''
    if isinstance(x, list):
        return ' '.join(kaal(y) for y in x)
    if isinstance(x, dict):
        return ' '.join(kaal(y) for y in x.values())
    return re.sub(r'<[^>]+>', ' ', str(x))

def check_term(tekst):
    meldingen = []
    for afk, (goed, fout) in DEF.items():
        e = re.escape(afk)
        # patroon "AFK (uitleg)"
        for m in re.finditer(rf'\b{e}\b\s*\(([^)]{{0,60}})\)', tekst, re.I):
            uit = m.group(1).lower()
            if any(f in uit for f in fout) and not any(g in uit for g in goed):
                meldingen.append(f'{afk} gekoppeld aan "{m.group(1).strip()}"')
        # patroon "uitleg (AFK)"
        for m in re.finditer(rf'([A-Za-zÀ-ÿ\-/ ]{{3,45}})\(\s*{e}\s*\)', tekst, re.I):
            voor = m.group(1).lower()
            if any(f in voor for f in fout) and not any(g in voor for g in goed):
                meldingen.append(f'{afk} omschreven als "{m.group(1).strip()}"')
    return meldingen

CIJFER = re.compile(r'\d+\s?%|\d+[\.,]?\d*\s*(maand|month|jaar|year|week|dag|day)|HR\s*[0-9]|\bp\s*[<=]\s*0|'
                    r'\d+\s*(patiënt|patient|pt\b)|\b\d{2,}\b')

# --- Stijl: harde en zachte checks ------------------------------------------
# Harde checks (falen): em-dash of en-dash, dubbele spatie, en een p-waarde die
# niet de compacte kleine-letter-vorm heeft (dus "P<0,001" of "p = 0,05").
# Zachte checks (waarschuwing, falen niet): een kwalitatief uitkomstwoord zonder
# getal in de buurt, en een te lange zin in de kernboodschap.
EMDASH, ENDASH = '—', '–'
P_HOOFD = re.compile(r'\bP\s*[<>=]\s*0[.,]\d')          # hoofdletter-P p-waarde
P_SPATIE = re.compile(r'\bp\s+[<>=]\s*0[.,]\d|\bp[<>=]\s+0[.,]\d')  # spatie rond de operator
VAAG_UITKOMST = re.compile(r'\b(hoge|hoog|lage|laag|hoogste|laagste|snelle|snel|gunstige|gunstig)\b', re.I)

def strings_van(o):
    if isinstance(o, str): return [o]
    if isinstance(o, dict): return [s for v in o.values() for s in strings_van(v)]
    if isinstance(o, list): return [s for v in o for s in strings_van(v)]
    return []

def redactie_velden(d, cid, lang):
    """De redactionele velden van een kaart (geen literatuursamenvattingen)."""
    cc = d['cards'][cid][lang]
    uit = []
    for k in ('bl', 'crit', 'results', 'lim', 'alts'):
        v = cc.get(k)
        if isinstance(v, str): uit.append((k, v))
        elif isinstance(v, list):
            uit += [(f'{k}{i}', x) for i, x in enumerate(v) if isinstance(x, str)]
    pos = d.get('pos', {}).get(cid, {}).get(lang, {})
    uit += [(f'pos.{k}', pos[k]) for k in ('g', 'l', 'v') if pos.get(k)]
    return uit

def zinnen(t):
    return re.split(r'(?<=[.]) (?=[A-Z0-9])', kaal(t))

def check_stijl(d):
    """Retourneert (harde_fouten, waarschuwingen)."""
    hard, zacht = [], []
    # harde checks over alle tekst
    for s in strings_van(d):
        if EMDASH in s or ENDASH in s:
            hard.append(f'em/en-dash in tekst :: ...{s[max(0,s.find(EMDASH)-15) if EMDASH in s else max(0,s.find(ENDASH)-15):][:40]}...')
        if P_HOOFD.search(s) or P_SPATIE.search(s):
            m = (P_HOOFD.search(s) or P_SPATIE.search(s))
            hard.append(f'p-notatie niet compact :: ...{s[max(0,m.start()-12):m.start()+12]}...')
    # per kaart, redactionele velden
    for cid in d['cards']:
        for lang in ('nl', 'en'):
            for f, t in redactie_velden(d, cid, lang):
                plat = kaal(t)
                if '  ' in t:  # ruwe tekst; kaal() zou tag-spaties als dubbel tellen
                    hard.append(f'{cid} [{lang}] {f} :: dubbele spatie')
                # zacht: vaag uitkomstwoord zonder getal in de buurt
                for m in VAAG_UITKOMST.finditer(plat):
                    seg = plat[max(0, m.start()-45):m.start()+45]
                    if not re.search(r'\d', seg):
                        zacht.append(f'{cid} [{lang}] {f} :: "{m.group()}" zonder getal :: ...{plat[max(0,m.start()-20):m.start()+30]}...')
            # zacht: te lange zin in de kernboodschap
            for z in zinnen(d['cards'][cid][lang].get('bl', '')):
                w = len(z.split())
                if w > 45:
                    zacht.append(f'{cid} [{lang}] bl :: zin van {w} woorden (>45)')
    return list(dict.fromkeys(hard)), list(dict.fromkeys(zacht))

def main():
    d = json.load(open('content.json'))
    termfouten, kaalfouten = [], []
    for rij in d['index']:
        cid = rij['id']
        c = d['cards'].get(cid)
        if not c: continue
        for lang in ('nl', 'en'):
            cc = c[lang]
            velden = ' '.join(kaal(cc.get(k)) for k in ('bl', 'crit', 'results', 'lim', 'alts'))
            pos = d.get('pos', {}).get(cid, {}).get(lang, {})
            velden += ' ' + kaal(pos)
            for lijst in ('guides', 'core', 'latest', 'ongoing'):
                for it in cc.get(lijst, []):
                    velden += ' ' + kaal(it[0]) + ' ' + kaal(it[3] if len(it) > 3 else '')
            for m in check_term(velden):
                termfouten.append(f'{cid} [{lang}] :: {m}')
        # kale statements: cijfers in resultaten zonder kernpublicatie
        nl = c['nl']
        res = kaal(nl.get('results'))
        kern = len(nl.get('core', [])) + len(nl.get('latest', []))
        refs = kern + len(nl.get('guides', []))
        if CIJFER.search(res) and kern == 0:
            kaalfouten.append(f'{cid} :: resultaten bevat cijfers maar geen kern- of recente publicatie')
        if refs == 0:
            kaalfouten.append(f'{cid} :: kaart zonder enige referentie')

    stijlfouten, waarschuwingen = check_stijl(d)

    # ontdubbelen met behoud van volgorde
    termfouten = list(dict.fromkeys(termfouten))
    kaalfouten = list(dict.fromkeys(kaalfouten))

    if termfouten:
        print(f'TERMINOLOGIE, {len(termfouten)} mogelijke verwarring(en):')
        for x in termfouten: print('  - ' + x)
    else:
        print('Terminologie: geen verwarring gevonden.')
    if kaalfouten:
        print(f'\nKALE STATEMENTS, {len(kaalfouten)} melding(en):')
        for x in kaalfouten: print('  - ' + x)
    else:
        print('Kale statements: geen kaart met een onbewezen claim gevonden.')
    if stijlfouten:
        print(f'\nSTIJL (hard), {len(stijlfouten)} fout(en):')
        for x in stijlfouten: print('  - ' + x)
    else:
        print('Stijl: geen dash-, spatie- of p-notatiefouten gevonden.')

    if waarschuwingen:
        print(f'\nLET OP (zacht, faalt niet), {len(waarschuwingen)} punt(en) om na te lopen:')
        for x in waarschuwingen: print('  - ' + x)

    if termfouten or kaalfouten or stijlfouten:
        print('\nLos deze meldingen op of bevestig dat ze terecht zijn voordat je pusht.')
        sys.exit(1)

if __name__ == '__main__':
    main()
