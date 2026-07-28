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

    if termfouten or kaalfouten:
        print('\nLos deze meldingen op of bevestig dat ze terecht zijn voordat je pusht.')
        sys.exit(1)

if __name__ == '__main__':
    main()
