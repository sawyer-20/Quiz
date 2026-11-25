#!/usr/bin/env python3
"""Gerador de perguntas a partir do Wikidata (CC0), para temas abaixo de 150 perguntas.

Plano (secção 4): se a importação do Open Trivia DB der menos de 2.000 perguntas limpas,
usa-se o gerador Wikidata. Cada modelo é uma consulta SPARQL + um enunciado fixo nos dois
idiomas; a resposta e as opções vêm só das etiquetas do Wikidata (pt e en). Nenhum facto é
escrito à mão. Exclusões conhecidas (ver EXCLUIR) evitam respostas que o Wikidata dá com
nome anacrónico (ex.: a RFA aparece como «Alemanha»).

Grava importacao/wikidata/geradas.json. Uso: python3 scripts/gerar_wikidata.py
"""
import json, random, re, time, urllib.parse, urllib.request, datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "importacao" / "wikidata" / "geradas.json"
ENDPOINT = "https://query.wikidata.org/sparql"
UA = "quizlux-importer/0.1 (generic client)"
RNG = random.Random(2026)


def sparql(q, tentativas=4):
    url = ENDPOINT + "?format=json&query=" + urllib.parse.quote(q)
    for k in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.load(r)
            time.sleep(2)
            return [{k2: v["value"] for k2, v in b.items()} for b in d["results"]["bindings"]]
        except Exception as e:
            if k == tentativas - 1:
                raise
            print(f"  erro ({e}); nova tentativa", flush=True)
            time.sleep(15 * (k + 1))


def qid(uri):
    return uri.rsplit("/", 1)[-1]


def limpo(s):
    return bool(s) and not re.match(r"^Q\d+$", s) and len(s) <= 60


def distratores(certa_pt, pool, n=3):
    """pool: lista de (pt, en) únicos. Devolve n pares diferentes da certa."""
    cand = [p for p in pool if p[0] != certa_pt]
    RNG.shuffle(cand)
    vistos, r = {certa_pt}, []
    for p in cand:
        if p[0] not in vistos:
            vistos.add(p[0]); r.append(p)
        if len(r) == n:
            break
    return r if len(r) == n else None


def pergunta(modelo, tema, sub, dif, qpt, qen, certa, erradas, entidade):
    return {"id": f"wd-{modelo}-{qid(entidade)}", "modelo": modelo, "topic": tema, "subtopic": sub,
            "difficulty": dif, "pt": {"q": qpt, "o": [certa[0]] + [e[0] for e in erradas]},
            "en": {"q": qen, "o": [certa[1]] + [e[1] for e in erradas]},
            "fonte": f"https://www.wikidata.org/wiki/{qid(entidade)}"}


# ---------------------------------------------------------------- Geografia
CAPITAL_CONTESTADA = {"Q801", "Q865", "Q219060"}  # Israel, Taiwan, Palestina: capital disputada
def capitais():
    rows = sparql("""
SELECT ?c ?cpt ?cen ?k ?kpt ?ken ?cont (COUNT(DISTINCT ?k2) AS ?nk) (COUNT(DISTINCT ?ct2) AS ?nct) WHERE {
 ?c wdt:P31 wd:Q3624078; wdt:P36 ?k; wdt:P36 ?k2; wdt:P30 ?cont; wdt:P30 ?ct2.
 FILTER NOT EXISTS { ?c wdt:P576 ?fim }
 ?c rdfs:label ?cpt FILTER(lang(?cpt)="pt") ?c rdfs:label ?cen FILTER(lang(?cen)="en")
 ?k rdfs:label ?kpt FILTER(lang(?kpt)="pt") ?k rdfs:label ?ken FILTER(lang(?ken)="en")
} GROUP BY ?c ?cpt ?cen ?k ?kpt ?ken ?cont""")
    rows = [r for r in rows if r["nk"] == "1" and r["nct"] == "1" and limpo(r["kpt"]) and limpo(r["cpt"])
            and qid(r["c"]) not in CAPITAL_CONTESTADA]
    por_cont = {}
    for r in rows:
        por_cont.setdefault(r["cont"], []).append((r["kpt"], r["ken"]))
    out = []
    for r in rows:
        er = distratores(r["kpt"], por_cont[r["cont"]])
        if er:
            out.append(pergunta("capital", "Geography", "Capitais", 2,
                                f"Qual é a capital do país {r['cpt']}?", f"What is the capital of {r['cen']}?",
                                (r["kpt"], r["ken"]), er, r["c"]))
    return out


def cidades():
    rows = sparql("""
SELECT ?x ?xpt ?xen ?c ?cpt ?cen ?cont (COUNT(DISTINCT ?c2) AS ?nc) WHERE {
 ?x wdt:P31/wdt:P279* wd:Q515; wdt:P1082 ?pop; wdt:P17 ?c; wdt:P17 ?c2; wikibase:sitelinks ?sl.
 FILTER(?pop > 1500000 && ?sl >= 80)
 ?c wdt:P31 wd:Q3624078; wdt:P30 ?cont. FILTER NOT EXISTS { ?c wdt:P36 ?x }
 ?x rdfs:label ?xpt FILTER(lang(?xpt)="pt") ?x rdfs:label ?xen FILTER(lang(?xen)="en")
 ?c rdfs:label ?cpt FILTER(lang(?cpt)="pt") ?c rdfs:label ?cen FILTER(lang(?cen)="en")
} GROUP BY ?x ?xpt ?xen ?c ?cpt ?cen ?cont""")
    rows = [r for r in rows if r["nc"] == "1" and limpo(r["xpt"])]
    vistos, uni = set(), []
    for r in rows:
        if r["x"] not in vistos:
            vistos.add(r["x"]); uni.append(r)
    paises = {}
    for r in uni:
        paises.setdefault(r["cont"], set()).add((r["cpt"], r["cen"]))
    out = []
    for r in uni:
        er = distratores(r["cpt"], sorted(paises[r["cont"]]))
        if er:
            out.append(pergunta("cidade", "Geography", "Cidades", 3,
                                f"Em que país fica a cidade de {r['xpt']}?", f"In which country is the city of {r['xen']}?",
                                (r["cpt"], r["cen"]), er, r["x"]))
    return out


# ---------------------------------------------------------------- Espaço
PLANETAS = "wd:Q111 wd:Q319 wd:Q193 wd:Q324 wd:Q332"  # Marte, Júpiter, Saturno, Urano, Neptuno


def luas():
    rows = sparql(f"""
SELECT ?m ?mpt ?men ?ppt ?pen (COUNT(DISTINCT ?p2) AS ?np) WHERE {{
 VALUES ?p {{{PLANETAS}}}
 ?m wdt:P397 ?p; wdt:P397 ?p2; wikibase:sitelinks ?sl. FILTER(?sl >= 48)
 ?m wdt:P31/wdt:P279* wd:Q2537.
 FILTER NOT EXISTS {{ ?m wdt:P31/wdt:P279* wd:Q1137272 }}
 ?m rdfs:label ?mpt FILTER(lang(?mpt)="pt") ?m rdfs:label ?men FILTER(lang(?men)="en")
 ?p rdfs:label ?ppt FILTER(lang(?ppt)="pt") ?p rdfs:label ?pen FILTER(lang(?pen)="en")
}} GROUP BY ?m ?mpt ?men ?ppt ?pen""")
    # Sem designações provisórias («S/2003 J 5»: o «J» denuncia Júpiter) e sem anéis/sondas.
    rows = [r for r in rows if r["np"] == "1" and limpo(r["mpt"]) and not re.search(r"[\d/]", r["men"] + r["mpt"])
            and not re.search(r"anel|anéis|ring", r["mpt"] + r["men"], re.I)]
    pool = sorted({(r["ppt"], r["pen"]) for r in rows})
    out = []
    for r in rows:
        er = distratores(r["ppt"], pool)
        if er:
            out.append(pergunta("lua", "Space", "Luas", 3,
                                f"{r['mpt']} é uma lua de que planeta?", f"{r['men']} is a moon of which planet?",
                                (r["ppt"], r["pen"]), er, r["m"]))
    return out


def descobridores():
    rows = sparql(f"""
SELECT ?m ?mpt ?men ?dpt ?den (COUNT(DISTINCT ?d2) AS ?nd) WHERE {{
 VALUES ?p {{{PLANETAS}}}
 ?m wdt:P397 ?p; wdt:P61 ?d; wdt:P61 ?d2; wikibase:sitelinks ?sl. FILTER(?sl >= 45)
 ?d wdt:P31 wd:Q5; wikibase:sitelinks ?dsl. FILTER(?dsl >= 40)
 ?m rdfs:label ?mpt FILTER(lang(?mpt)="pt") ?m rdfs:label ?men FILTER(lang(?men)="en")
 ?d rdfs:label ?dpt FILTER(lang(?dpt)="pt") ?d rdfs:label ?den FILTER(lang(?den)="en")
}} GROUP BY ?m ?mpt ?men ?dpt ?den""")
    rows = [r for r in rows if r["nd"] == "1" and limpo(r["mpt"])]
    pool = sorted({(r["dpt"], r["den"]) for r in rows})
    out = []
    for r in rows:
        er = distratores(r["dpt"], pool)
        if er:
            out.append(pergunta("descobridor", "Space", "Luas", 4,
                                f"Quem descobriu {r['mpt']}, lua de um planeta do Sistema Solar?",
                                f"Who discovered {r['men']}, a moon of a Solar System planet?",
                                (r["dpt"], r["den"]), er, r["m"]))
    return out


# ---------------------------------------------------------------- Natureza
GRUPOS = {"Q7377": ("Mamíferos", "Mammals"), "Q5113": ("Aves", "Birds"), "Q10811": ("Répteis", "Reptiles"),
          "Q10908": ("Anfíbios", "Amphibians")}


def animais():
    ids = [qid(r["s"]) for r in sparql(
        "SELECT DISTINCT ?s ?sl WHERE { ?s wdt:P141 ?st; wikibase:sitelinks ?sl. FILTER(?sl >= 80) }")]
    rows = []
    for k in range(0, len(ids), 150):
        v = " ".join("wd:" + i for i in ids[k:k + 150])
        rows += sparql(f"""SELECT ?s ?pt ?en ?tax ?cl WHERE {{ VALUES ?s {{{v}}}
 ?s wdt:P225 ?tax; wdt:P105 wd:Q7432.
 ?s rdfs:label ?pt FILTER(lang(?pt)="pt") ?s rdfs:label ?en FILTER(lang(?en)="en")
 ?s wdt:P171+ ?cl. VALUES ?cl {{wd:Q7377 wd:Q5113 wd:Q10811 wd:Q10908}} }}""")
    esp = {}
    for r in rows:
        e = esp.setdefault(r["s"], {"pt": r["pt"], "en": r["en"], "tax": set(), "cl": set()})
        e["tax"].add(r["tax"]); e["cl"].add(qid(r["cl"]))
    bons = {}
    for s_, e in esp.items():
        cl = e["cl"] - {"Q10811"} if "Q5113" in e["cl"] else e["cl"]  # aves também caem em répteis
        nome = e["pt"]
        if len(cl) != 1 or len(e["tax"]) != 1 or nome.lower() in {t.lower() for t in e["tax"]} \
                or nome.lower() == e["en"].lower() or not limpo(nome) or " " in nome.strip():
            continue  # sem nome comum em português, ou classificação duvidosa
        bons[s_] = {"pt": nome[0].lower() + nome[1:], "en": e["en"][0].lower() + e["en"][1:],
                    "tax": next(iter(e["tax"])), "cl": next(iter(cl))}
    out = []
    for k, (s_, e) in enumerate(sorted(bons.items())):
        if False:  # modelo «nome científico» retirado na auditoria 1 (pista em en-US, nomes pt pouco fiáveis)
            pool = sorted({(x["pt"], x["en"]) for x in bons.values() if x["cl"] == e["cl"]})
            er = distratores(e["pt"], pool)
            if er:
                out.append(pergunta("nomecientifico", "Nature & Animals", "Nomes científicos", 3,
                                    f"Que animal tem o nome científico {e['tax']}?",
                                    f"Which animal has the scientific name {e['tax']}?",
                                    (e["pt"], e["en"]), er, s_))
        if True:
            certa = GRUPOS[e["cl"]]
            er = [g for c, g in GRUPOS.items() if c != e["cl"]]
            out.append(pergunta("grupo", "Nature & Animals", "Classificação", 2,
                                f"A que grupo de animais pertence a espécie {e['pt']}?",
                                f"Which group of animals does the {e['en']} belong to?",
                                certa, er, s_))
    return out


# ---------------------------------------------------------------- Futebol
# Anos em que o Wikidata dá o vencedor/anfitrião com nome atual e não com o da época
# (RFA = «Alemanha»; Inglaterra = «Reino Unido»), e edições demasiado recentes.
EXCLUIR = {"mundial": {"1954", "1966", "1974", "1990", "2026"}, "euro": {"1972", "1980", "1988", "2021", "2024"}}  # 2021 = Euro 2020


def torneio(serie, chave, nome_pt, nome_en):
    eds = sparql(f"""SELECT ?e ?d WHERE {{ ?e wdt:P3450 wd:{serie}; wdt:P31 ?tipo; wdt:P585 ?d. VALUES ?tipo {{wd:Q27020041 wd:Q107540719}} }}""")
    anos = {r["e"]: r["d"][:4] for r in eds}
    v = " ".join("wd:" + qid(e) for e in anos)
    vw = sparql(f"""SELECT ?e ?wpt ?wen WHERE {{ VALUES ?e {{{v}}} ?e wdt:P1346 ?w. ?w wdt:P17 ?wc.
 ?wc rdfs:label ?wpt FILTER(lang(?wpt)="pt") ?wc rdfs:label ?wen FILTER(lang(?wen)="en") }}""")
    hs = sparql(f"""SELECT ?e ?hpt ?hen WHERE {{ VALUES ?e {{{v}}} ?e wdt:P17 ?h.
 ?h rdfs:label ?hpt FILTER(lang(?hpt)="pt") ?h rdfs:label ?hen FILTER(lang(?hen)="en") }}""")
    venc, anf = {}, {}
    for r in vw:
        venc.setdefault(r["e"], set()).add((r["wpt"], r["wen"]))
    for r in hs:
        anf.setdefault(r["e"], set()).add((r["hpt"], r["hen"]))
    validos = [e for e, y in anos.items() if y not in EXCLUIR[chave]]
    pool_w = sorted(set().union(*[venc.get(e, set()) for e in validos]))
    pool_h = sorted(set().union(*[anf.get(e, set()) for e in validos]))
    out = []
    for e, y in sorted(anos.items(), key=lambda x: x[1]):
        if y in EXCLUIR[chave]:
            continue
        if len(venc.get(e, ())) == 1:
            c = next(iter(venc[e])); er = distratores(c[0], pool_w)
            if er:
                q = pergunta(f"{chave}-vencedor", "Football", nome_pt, 2,
                             f"Que seleção venceu o {nome_pt} de {y}?", f"Which national team won the {y} {nome_en}?", c, er, e)
                q["id"] = f"wd-{chave}-vencedor-{qid(e)}"; out.append(q)
        if len(anf.get(e, ())) == 1:
            c = next(iter(anf[e])); er = distratores(c[0], pool_h)
            if er:
                q = pergunta(f"{chave}-anfitriao", "Football", nome_pt, 3,
                             f"Que país organizou o {nome_pt} de {y}?", f"Which country hosted the {y} {nome_en}?", c, er, e)
                q["id"] = f"wd-{chave}-anfitriao-{qid(e)}"; out.append(q)
    return out


def campeoes_europeus():
    rows = sparql("""
SELECT ?e ?ept ?een ?w ?wpt ?wen ?curto WHERE {
 ?e wdt:P3450 wd:Q18756; wdt:P1346 ?w.
 ?e rdfs:label ?ept FILTER(lang(?ept)="pt") ?e rdfs:label ?een FILTER(lang(?een)="en")
 ?w rdfs:label ?wpt FILTER(lang(?wpt)="pt") ?w rdfs:label ?wen FILTER(lang(?wen)="en")
}""")
    por_ed = {}
    for r in rows:
        m = re.search(r"(\d{4})\D(\d{2,4})", r["ept"])
        if not m:
            continue
        fim = int(m.group(2)) if len(m.group(2)) == 4 else int(m.group(1)[:2] + m.group(2))
        if fim > 2025:
            continue
        nome = r["wen"]  # o nome curto (P1813) às vezes é sigla («NFO»)
        por_ed.setdefault(r["e"], {})[r["w"]] = (r["ept"], r["een"], nome)
    linhas = [(e, next(iter(d.values()))) for e, d in por_ed.items() if len(d) == 1]
    pool = sorted({(x[2], x[2]) for _, x in linhas if limpo(x[2])})
    out = []
    for e, (ept, een, nome) in linhas:
        if not limpo(nome):
            continue
        er = distratores(nome, pool)
        if er:
            m2 = re.match(r"^(.*?)\s+(?:de\s+)?(\d{4}[-–]\d{2,4})$", ept)
            if not m2 or qid(e) in {"Q330674"}:  # 1985-86: título disputado (Steaua/FCSB)
                continue
            out.append(pergunta("ligacampeoes", "Football", "Liga dos Campeões", 3,
                                f"Que clube venceu a {m2.group(1)} de {m2.group(2)}?", f"Which club won the {een}?",
                                (nome, nome), er, e))
    return out


def bola_de_ouro():
    rows = sparql("""
SELECT ?p ?ppt ?pen ?y WHERE {
 ?p wdt:P21 wd:Q6581097; p:P166 ?st. ?st ps:P166 wd:Q166177; pq:P585 ?d. BIND(STR(YEAR(?d)) AS ?y) FILTER(YEAR(?d) <= 2025)
 ?p rdfs:label ?ppt FILTER(lang(?ppt)="pt") ?p rdfs:label ?pen FILTER(lang(?pen)="en")
}""")
    por_ano = {}
    for r in rows:
        por_ano.setdefault(r["y"], set()).add((r["ppt"], r["pen"], r["p"]))
    pool = sorted({(r["ppt"], r["pen"]) for r in rows})
    out = []
    for y, s in sorted(por_ano.items()):
        if len(s) != 1:
            continue
        ppt, pen, p = next(iter(s))
        er = distratores(ppt, pool)
        if er:
            q = pergunta("boladeouro", "Football", "Bola de Ouro", 3,
                         f"Quem ganhou a Bola de Ouro de {y}?", f"Who won the {y} Ballon d'Or?",
                         (ppt, pen), er, p)
            q["id"] = f"wd-boladeouro-{y}"
            out.append(q)
    return out


MODELOS = [capitais, luas, descobridores, animais,
           lambda: torneio("Q19317", "mundial", "Campeonato do Mundo", "FIFA World Cup"),
           lambda: torneio("Q260858", "euro", "Campeonato da Europa", "UEFA European Championship"),
           campeoes_europeus, bola_de_ouro]


def main():
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    todas = []
    for m in MODELOS:
        r = m()
        print(f"{getattr(m, '__name__', 'torneio')}: {len(r)}", flush=True)
        todas += r
    hoje = datetime.date.today().isoformat()
    for q in todas:
        q.update({"licenca": "CC0 1.0", "origem": "Wikidata (https://www.wikidata.org)", "gerada_em": hoje})
    vistos, uni = set(), []
    for q in todas:
        if q["id"] not in vistos:
            vistos.add(q["id"]); uni.append(q)
    SAIDA.write_text(json.dumps(uni, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Total: {len(uni)}")


if __name__ == "__main__":
    main()
