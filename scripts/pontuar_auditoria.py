#!/usr/bin/env python3
"""Compara a auditoria cega com a chave e calcula o erro por lote (tema).

Erro = a resposta às cegas difere da chave, ou o auditor assinalou nenhuma_certa, ambigua,
datada, traducao, brasil, pista, eua ou texto em pt-PT. As gralhas só no en-US (problema
`texto` com nota a começar por «en-US»; na ronda 1 nem eram pedidas) contam à parte em
`so_en`, como defeito de texto. Lote com erro > 5% (mais de 2 em 50) é devolvido.
Uso: python3 scripts/pontuar_auditoria.py <chave.json> <ronda>   (ronda: 1, 2, ...)
"""
import json, sys, glob, collections
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
AUD = RAIZ / "importacao" / "auditoria"

def main():
    chave = json.load(open(sys.argv[1], encoding="utf-8"))
    ronda = sys.argv[2] if len(sys.argv) > 2 else "1"
    sufixo = "" if ronda == "1" else f"-r{ronda}"
    res, erradas = {}, []
    for f in sorted(glob.glob(str(AUD / f"resultado-*{sufixo}.json"))):
        nome = Path(f).stem.replace("resultado-", "")
        if ronda == "1" and "-r" in nome:
            continue
        lote = nome.replace(sufixo, "") if sufixo else nome
        n = err = 0
        tipos = collections.Counter()
        for r in json.load(open(f, encoding="utf-8")):
            n += 1
            k = chave[r["id"]]
            probs = list(r.get("problemas") or [])
            if r.get("resposta") is not None and r["resposta"] != k["certa"]:
                probs.append("resposta_diferente")
            if r.get("resposta") is None:
                probs.append("sem_resposta")
            so_en = probs == ["texto"] and r.get("nota", "").lower().startswith("en-us") \
                and "pt" not in r.get("nota", "")[:20].lower()
            if so_en:
                tipos["so_en"] += 1
                erradas.append({"lote": lote, "id": r["id"], "problemas": ["texto_en"], "nota": r.get("nota", "")})
            elif probs:
                err += 1
                tipos.update(probs)
                erradas.append({"lote": lote, "id": r["id"], "problemas": probs, "nota": r.get("nota", "")})
        res[lote] = {"n": n, "erros": err, "taxa": round(100 * err / n, 1),
                     "decisao": "devolvido" if err / n > 0.05 else "aceite", "tipos": dict(tipos)}
    print(json.dumps(res, ensure_ascii=False, indent=1))
    (AUD / f"pontuacao-r{ronda}.json").write_text(json.dumps({"lotes": res, "assinaladas": erradas}, ensure_ascii=False, indent=1), encoding="utf-8")

if __name__ == "__main__":
    main()
