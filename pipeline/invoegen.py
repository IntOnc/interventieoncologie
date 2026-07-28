#!/usr/bin/env python3
# Voegt geverifieerde literatuurvoorstellen toe aan content.json.
# Gebruik: python3 pipeline/invoegen.py <voorstellen.json>
# Het voorstellenbestand is {kaart-id: [ {lijst,titel,tijdschrift,jaar,url,sk,auteur,score,nl,en}, ... ]}
import json, re, sys

def norm_url(u):
    u = re.sub(r'^https?://', '', (u or '').lower())
    u = re.sub(r'^(www\.|dx\.)', '', u)
    u = re.sub(r'/(full|abstract|fulltext|pdf|html)$', '', u.rstrip('/'))
    u = re.sub(r'^doi\.org/', 'doi:', u)
    u = re.sub(r'^link\.springer\.com/article/', 'doi:', u)
    return u

def norm_titel(t):
    return re.sub(r'[^a-z0-9]', '', (t or '').lower())

def main(pad):
    d = json.load(open('content.json'))
    voors = json.load(open(pad))
    toegevoegd, overgeslagen = 0, []
    for cid, lijst in voors.items():
        if cid not in d['cards']:
            print('ONBEKENDE KAART:', cid); continue
        c = d['cards'][cid]
        # index van bestaande urls en titels over alle lijsten
        bestaand_u, bestaand_t = set(), set()
        for k in ('guides', 'core', 'latest', 'ongoing'):
            for it in c['nl'][k]:
                bestaand_u.add(norm_url(it[2])); bestaand_t.add(norm_titel(it[0]))
        for v in lijst:
            nu = norm_url(v['url']); nt = norm_titel(v['titel'])
            if nu in bestaand_u or nt in bestaand_t:
                overgeslagen.append((cid, v['titel'][:55], 'dubbel')); continue
            k = v['lijst']
            if k not in ('core', 'latest'):
                overgeslagen.append((cid, v['titel'][:55], 'ongeldige lijst')); continue
            venue = f"{v['tijdschrift']} · {v['jaar']}"
            rij_nl = [v['titel'], venue, v['url'], v['nl'], int(v['sk']), v.get('auteur', ''), v['score']]
            rij_en = [v['titel'], venue, v['url'], v['en'], int(v['sk']), v.get('auteur', ''), v['score']]
            c['nl'][k].append(rij_nl); c['en'][k].append(rij_en)
            bestaand_u.add(nu); bestaand_t.add(nt); toegevoegd += 1
    json.dump(d, open('content.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    print('toegevoegd:', toegevoegd)
    if overgeslagen:
        print('overgeslagen:', len(overgeslagen))
        for cid, t, r in overgeslagen: print(f'  {cid}: {t} ({r})')

if __name__ == '__main__':
    main(sys.argv[1])
