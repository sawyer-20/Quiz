#!/usr/bin/env python3
"""Junta o pacote importado: Open Trivia DB traduzido + gerador Wikidata.

Entradas: importacao/opentdb/bruto.json, importacao/opentdb/lotes/saida-*.jsonl (triagem e
tradução), importacao/wikidata/geradas.json e importacao/auditoria/rejeitadas.json (perguntas
que a auditoria tirou, se existir).
Saída: importacao/pacote.json (com licença e origem por pergunta) e app/assets/importadas.json
(formato da app). Não toca em banco/: o pacote importado é separado das 57 verificadas.

Regras mecânicas aplicadas aqui: duplicados (mesmo enunciado), formas do português do Brasil
(lista BR abaixo), limites de texto (enunciado 200, opções 60), opções repetidas, e teto por
modelo do gerador (para um tema não ficar só com perguntas-molde).
Uso: python3 scripts/montar_pacote.py
"""
import json, re, random, hashlib, collections, glob
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
IMP = RAIZ / "importacao"
DIF = {"easy": 2, "medium": 3, "hard": 4}
TETO = {"lua": 110, "grupo": 110, "capital": 120}
BR = re.compile(r"\b(você|vocês|tela|telas|celular|usuário|usuários|arquivo|arquivos|trem|ônibus|"
                r"esporte|esportes|goleiro|gol|gols|copa do mundo|fato|fatos|registro|contato|econômic\w*|"
                r"gênero|gêneros|antônio|câmera|xícara|banheiro|geladeira|sorvete|cardápio|"
                r"fone|caminhão|bonde|aeromoça|ônibus|planejamento|equipe técnica|"
                r"fazendo|jogando|estão \w+ndo|está \w+ndo|moça|garoto|garota|"
                r"\w+ônio|\w+ômico|\w+ômica|\w+ênico|\w+ênica|Antártica|Irã|Moscou|Netuno|Plutão-não|Holanda do Norte)\b", re.I)

BR_TIME = re.compile(r"\b(o|um|do|no|pelo|meu|teu|seu) times?\b")  # «time» = equipa (minúsculas)


def chave(t):
    return re.sub(r"\W+", " ", t.lower()).strip()


def baralhar(qid, pt, en):
    """Opções vêm com a certa em 0; baralha de forma determinística (igual nos dois idiomas)."""
    ordem = list(range(4))
    random.Random(int(hashlib.sha1(qid.encode()).hexdigest()[:8], 16)).shuffle(ordem)
    return [pt[i] for i in ordem], [en[i] for i in ordem], ordem.index(0)


def main():
    bruto = {}
    for q in json.loads((IMP / "opentdb" / "bruto.json").read_text(encoding="utf-8")):
        k = "otdb-" + hashlib.sha1((q["pergunta"] + "|" + q["certa"]).encode()).hexdigest()[:10]
        bruto[k] = q
    tirar = set()
    rej = IMP / "auditoria" / "rejeitadas.json"
    if rej.exists():
        tirar = set(json.loads(rej.read_text(encoding="utf-8")))
    motivos = collections.Counter()
    pacote, vistos, br = [], set(), []

    # Revisão (2.ª passagem): opções na mesma ordem já baralhada; nunca muda a certa.
    revisao = {}
    for f in sorted(glob.glob(str(IMP / "revisao" / "saida-*.jsonl"))):
        for linha in open(f, encoding="utf-8"):
            r = json.loads(linha); revisao[r["id"]] = r

    def juntar(q):
        if q["id"] in tirar:
            motivos["auditoria"] += 1; return
        r = revisao.get(q["id"])
        if r and r["acao"] == "tirar":
            motivos["revisao_" + r.get("motivo", "outro")] += 1; return
        if r and r["acao"] == "corrigir":
            if len(r["pt"]["o"]) != 4 or len(r["en"]["o"]) != 4:
                motivos["revisao_invalida"] += 1; return
            for l, k in (("pt-PT", "pt"), ("en-US", "en")):
                q["text"][l]["q"], q["text"][l]["o"] = r[k]["q"], r[k]["o"]
            q["revista"] = r.get("nota", "")
            motivos["revisao_corrigida"] += 1
        pt, en = q["text"]["pt-PT"], q["text"]["en-US"]
        for t in (pt, en):  # espaços a mais (defeito frequente no Open Trivia DB)
            t["q"] = re.sub(r"\s+", " ", t["q"]).strip()
            t["o"] = [re.sub(r"\s+", " ", o).strip() for o in t["o"]]
        k = chave(en["q"])
        if k in vistos or chave(pt["q"]) in vistos:
            motivos["duplicada"] += 1; return
        if len(pt["q"]) > 200 or len(en["q"]) > 200 or any(len(o) > 60 for o in pt["o"] + en["o"]):
            motivos["limite_texto"] += 1; return
        if len({chave(o) for o in pt["o"]}) < 4 or len({chave(o) for o in en["o"]}) < 4:
            motivos["opcoes_repetidas"] += 1; return
        m = BR.search(" ".join([pt["q"], *pt["o"]])) or BR_TIME.search(" ".join([pt["q"], *pt["o"]]))
        if m:
            motivos["forma_brasil"] += 1; br.append((q["id"], m.group(0), pt["q"])); return
        vistos.add(k); vistos.add(chave(pt["q"]))
        pacote.append(q)

    for f in sorted(glob.glob(str(IMP / "opentdb" / "lotes" / "saida-*.jsonl"))):
        for linha in open(f, encoding="utf-8"):
            d = json.loads(linha)
            if not d["keep"]:
                continue
            b = bruto[d["id"]]
            en = [b["certa"], *b["erradas"]]
            ptq, enq, c = baralhar(d["id"], d["pt"]["o"], en)
            juntar({"id": d["id"], "topic": d["topic"], "difficulty": DIF[b["dificuldade"]],
                    "correct": c, "sources": ["https://opentdb.com/"],
                    "licenca": "CC BY-SA 4.0", "origem": "Open Trivia DB (https://opentdb.com), traduzida por máquina para pt-PT",
                    "categoria_origem": b["categoria"],
                    "text": {"pt-PT": {"q": d["pt"]["q"], "o": ptq, "e": ""},
                             "en-US": {"q": b["pergunta"], "o": enq, "e": ""}}})
    gerados = json.loads((IMP / "wikidata" / "geradas.json").read_text(encoding="utf-8"))
    por_modelo = collections.defaultdict(list)
    for g in gerados:
        por_modelo[g["modelo"]].append(g)
    for m, lista in sorted(por_modelo.items()):
        if m in TETO and len(lista) > TETO[m]:
            motivos[f"teto_{m}"] += len(lista) - TETO[m]
            lista = random.Random(2026).sample(lista, TETO[m])
        for g in sorted(lista, key=lambda x: x["id"]):
            ptq, enq, c = baralhar(g["id"], g["pt"]["o"], g["en"]["o"])
            juntar({"id": g["id"], "topic": g["topic"], "difficulty": g["difficulty"], "correct": c,
                    "sources": [g["fonte"]], "licenca": g["licenca"], "origem": g["origem"],
                    "modelo": g["modelo"],
                    "text": {"pt-PT": {"q": g["pt"]["q"], "o": ptq, "e": ""},
                             "en-US": {"q": g["en"]["q"], "o": enq, "e": ""}}})
    (IMP / "pacote.json").write_text(json.dumps(pacote, ensure_ascii=False, indent=1), encoding="utf-8")
    app = [{"id": q["id"], "topic": q["topic"], "difficulty": q["difficulty"], "daily": False, "pendente": False,
            "importada": True, "correct": q["correct"], "sources": q["sources"], "text": q["text"]} for q in pacote]
    (RAIZ / "app" / "assets" / "importadas.json").write_text(json.dumps(app, ensure_ascii=False, indent=0), encoding="utf-8")
    (IMP / "formas-brasil.json").write_text(json.dumps(br, ensure_ascii=False, indent=1), encoding="utf-8")
    temas = collections.Counter(q["topic"] for q in pacote)
    origem = collections.Counter(("wikidata" if q["id"].startswith("wd-") else "opentdb", q["topic"]) for q in pacote)
    print(json.dumps({"total": len(pacote), "por_tema": dict(temas.most_common()),
                      "por_origem": {f"{a}/{b}": n for (a, b), n in sorted(origem.items())},
                      "fora": dict(motivos)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
