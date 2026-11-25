#!/usr/bin/env python3
"""Pré-filtro mecânico do Open Trivia DB e divisão em ficheiros para triagem/tradução.

Tira: verdadeiro/falso (a app usa 4 opções), categorias fora dos 10 temas (televisão,
celebridades, banda desenhada, anime, desenhos animados, musicais, jogos de tabuleiro,
política), perguntas com palavras que denunciam os EUA ou datas («currently», «as of»…)
e duplicados. O resto vai para importacao/opentdb/lotes/entrada-NN.jsonl (N por ficheiro).
Uso: python3 scripts/preparar_traducao.py [N=200]
"""
import json, re, sys, hashlib, collections
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRUTO = RAIZ / "importacao" / "opentdb" / "bruto.json"
LOTES = RAIZ / "importacao" / "opentdb" / "lotes"
FORA = {13, 14, 16, 24, 26, 29, 31, 32}
EUA = re.compile(r"\b(U\.?S\.?A?\.?|United States|America|American|NFL|NBA|MLB|NHL|NCAA|Super Bowl|"
                 r"Congress|Senate|state of|US state|Uncle Sam|Thanksgiving|Fourth of July)\b", re.I)
DATADA = re.compile(r"\b(currently|current|as of|latest|most recent|newest|this year|nowadays|"
                    r"today|to date|so far|world's (richest|tallest)|reigning)\b", re.I)

def pid(q):
    return "otdb-" + hashlib.sha1((q["pergunta"] + "|" + q["certa"]).encode()).hexdigest()[:10]

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    bruto = json.loads(BRUTO.read_text(encoding="utf-8"))
    motivos, vistos, ficam = collections.Counter(), set(), []
    for q in bruto:
        texto = " ".join([q["pergunta"], q["certa"], *q["erradas"]])
        if q["tipo"] != "multiple":
            motivos["verdadeiro_falso"] += 1; continue
        if q["categoria_id"] in FORA:
            motivos["categoria_fora"] += 1; continue
        if EUA.search(texto):
            motivos["eua_palavra"] += 1; continue
        if DATADA.search(q["pergunta"]):
            motivos["datada_palavra"] += 1; continue
        i = pid(q)
        if i in vistos:
            motivos["duplicada"] += 1; continue
        vistos.add(i)
        ficam.append({"id": i, "cat": q["categoria"], "dif": q["dificuldade"], "q": q["pergunta"].strip(),
                      "certa": q["certa"].strip(), "erradas": [x.strip() for x in q["erradas"]]})
    # Videojogos: 992 candidatas para um só tema; amostra fixa de 450 (semente 2026) para
    # não gastar tradução em excesso. As outras ficam no bruto.json para depois.
    import random
    vg = [q for q in ficam if q["cat"] == "Entertainment: Video Games"]
    fora_vg = set(q["id"] for q in vg) - set(q["id"] for q in random.Random(2026).sample(vg, min(450, len(vg))))
    motivos["videojogos_excedente"] = len(fora_vg)
    ficam = [q for q in ficam if q["id"] not in fora_vg]
    for f in LOTES.glob("entrada-*.jsonl"):
        f.unlink()
    for k in range(0, len(ficam), n):
        with open(LOTES / f"entrada-{k // n + 1:02d}.jsonl", "w", encoding="utf-8") as f:
            for q in ficam[k:k + n]:
                f.write(json.dumps(q, ensure_ascii=False) + "\n")
    resumo = {"total": len(bruto), "fora_pre_filtro": dict(motivos), "para_triagem": len(ficam),
              "por_categoria": dict(collections.Counter(q["cat"] for q in ficam))}
    (RAIZ / "importacao" / "opentdb" / "prefiltro.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(resumo, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
