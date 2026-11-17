#!/usr/bin/env python3
"""Monta banco/perguntas/<id>.json (esquema v2) a partir de uma pergunta do pesquisador.

Uso: python3 scripts/montar_pergunta.py <pesquisador.json> <indice> <id> <lote>

O pesquisador devolve a ficha de facto com o texto de trabalho em pt-PT: `topic` (um dos 10
tópicos), `subtopic`, `markets` (opcional), `enunciado`, `resposta`, `distratores`,
`explicacao`, `dificuldade_estimada`, `valid_until` (ou null), `fontes`, `riscos`.
Baralha as opções (SystemRandom) e imprime a entrada às cegas para o verificador:
enunciado, opções baralhadas de novo e domínios das fontes do pesquisador a evitar.
"""

import json
import random
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from validar import TOPICS, dominio_registavel  # noqa: E402


def urls_para_jogador(fontes):
    """Até 3 URLs de domínios diferentes, nível 1 primeiro, sem Wikipédia."""
    ordem = sorted((f for f in fontes if dominio_registavel(f["url"]) != "wikipedia.org"),
                   key=lambda f: f["nivel"])
    urls, vistos = [], set()
    for f in ordem:
        d = dominio_registavel(f["url"])
        if d not in vistos:
            vistos.add(d)
            urls.append(f["url"])
        if len(urls) == 3:
            break
    return urls


def main():
    if len(sys.argv) != 5:
        print(__doc__)
        return 2
    ficheiro, idx, pid, lote = sys.argv[1:]
    dados = json.loads(Path(ficheiro).read_text(encoding="utf-8"))
    p = dados["perguntas"][int(idx)] if "perguntas" in dados else dados
    if p["topic"] not in TOPICS:
        print(f"ERRO: topic desconhecido: {p['topic']}")
        return 1
    hoje = date.today().isoformat()
    r = random.SystemRandom()
    opcoes = [p["resposta"]] + list(p["distratores"])
    r.shuffle(opcoes)
    fontes = [{"url": f["url"], "dominio": dominio_registavel(f["url"]), "titulo": f["titulo"],
               "nivel": f["nivel"], "excerto": f["excerto"][:300], "consultada_em": hoje,
               "papel": "pesquisador"} for f in p["fontes"]]
    q = {"id": pid, "topic": p["topic"]}
    if p.get("subtopic"):
        q["subtopic"] = p["subtopic"][:60]
    if p.get("markets"):
        q["markets"] = p["markets"]
    q["text"] = {"pt-PT": {"question": p["enunciado"], "options": opcoes, "explanation": p["explicacao"]}}
    q["correct"] = opcoes.index(p["resposta"])
    q["difficulty"] = p["dificuldade_estimada"]
    q["valid_until"] = p.get("valid_until")
    q["daily_eligible"] = q["valid_until"] is None
    q["sources"] = urls_para_jogador(fontes)
    q["fontes"] = fontes
    q["verificacao"] = {"verificador": None, "advogado": None, "editor": None}
    q["estado"] = "em_verificacao"
    q["motivo_rejeicao"] = None
    q["lote"] = lote
    q["criada_em"] = hoje
    q["historico"] = [{"data": hoje, "evento": "criada", "agente": "pesquisador", "nota": p.get("riscos", "")}]
    q["etiquetas"] = []
    out = RAIZ / "banco" / "perguntas" / f"{pid}.json"
    if out.exists():
        print(f"ERRO: {out} já existe")
        return 1
    out.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cego = opcoes[:]
    r.shuffle(cego)
    print(json.dumps({"id": pid, "enunciado": p["enunciado"], "opcoes": opcoes, "opcoes_cego": cego,
                      "proibidos": sorted({f["dominio"] for f in fontes}),
                      "titulos_a_evitar": [f["titulo"] for f in fontes]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
