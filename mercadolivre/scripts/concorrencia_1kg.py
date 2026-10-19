import csv,re,statistics as st,sys
rows=[r for r in csv.reader(open(__import__('pathlib').Path(__file__).parent.parent/'pesquisa'/'concorrencia-1kg-2026-10-08.tsv',encoding='utf8'),delimiter='\t') if len(r)>=9]
def vend(v):
    v=(v or '').replace('.','').strip()
    if not v: return 0
    return int(float(v.replace('mil','').strip())*1000) if 'mil' in v else int(v)
U={}
for r in rows:
    k=(r[2].strip().lower(),r[3])
    if k not in U: U[k]=dict(t=r[2],p=float(r[3] or 0),risc=float(r[4] or 0),out=float(r[5] or 0),v=vend(r[6]),n=r[7],tags=r[8],url=r[9] if len(r)>9 else '',termos={r[0].split(' (')[0]})
    else: U[k]['termos'].add(r[0].split(' (')[0])
L=list(U.values())
for x in L:
    t=x['t'].lower()
    x['kg1']=bool(re.search(r'\b1 ?k(g|ilo)|1000 ?g',t)) and not re.search(r'kit|\b\d+ ?(un|x|pacotes|pct)\b|\d+ ?kg(?<!1kg)|2kg|5kg|com \d',t)
    x['kg2kit']=bool(re.search(r'(kit|2 ?x|2 ?un|2 pac).*500 ?g|500 ?g.*(kit|2 ?x|2 ?un)',t))
    x['grao']=bool(re.search(r'gr[ãa]o',t)); x['moido']=bool(re.search(r'mo[íi]do',t))
    x['esp']=bool(re.search(r'especial|\b8\d ?(\+|pts|pontos)|sca',t)); x['gourmet']='gourmet' in t
    x['robusta']=bool(re.search(r'robusta|conilon|blend',t)); x['espresso']=bool(re.search(r'espresso|expresso',t))
    x['brand_big']=bool(re.search(r'pil[ãa]o|3 cora|melitta|santa m[oô]nica|orfeu|italle|caf[eé] do ponto|baggio|l.or|nescaf|lavazza|illy|tres|segafredo',t))
def stats(name,sel):
    ps=sorted(x['p'] for x in sel)
    if not ps: print(name,'vazio');return
    q=lambda f: ps[min(len(ps)-1,int(f*len(ps)))]
    print(f"\n### {name}: n={len(ps)}  min={ps[0]:.2f} p25={q(.25):.2f} med={st.median(ps):.2f} p75={q(.75):.2f} max={ps[-1]:.2f}")
    for x in sorted(sel,key=lambda x:-x['v'])[:14]:
        print(f"  {x['p']:7.2f} (cart {x['out'] or x['risc']:7.2f}) v={x['v']:>6} n={x['n']:3} {x['tags']:18} {x['t'][:85]}")
graos1=[x for x in L if x['kg1'] and x['grao'] and not x['moido']]
stats('1kg GRÃOS especial (sem robusta)',[x for x in graos1 if x['esp'] and not x['robusta']])
stats('1kg GRÃOS gourmet (não especial)',[x for x in graos1 if x['gourmet'] and not x['esp'] and not x['robusta']])
stats('1kg GRÃOS blend/robusta',[x for x in graos1 if x['robusta']])
stats('1kg GRÃOS espresso (qualquer)',[x for x in graos1 if x['espresso']])
stats('1kg MOÍDO (pacote 1kg)',[x for x in L if x['kg1'] and x['moido'] and not x['grao']])
stats('1kg MOÍDO especial',[x for x in L if x['kg1'] and x['moido'] and not x['grao'] and x['esp']])
stats('KIT 2x500g',[x for x in L if x['kg2kit']])
stats('1kg GRÃOS todos',graos1)
