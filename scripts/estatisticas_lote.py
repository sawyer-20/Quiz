#!/usr/bin/env python3
"""Números do relatório de um lote.

Uso:
    python3 scripts/estatisticas_lote.py lote-2026-11-04-historia

Lê as perguntas do lote em banco/perguntas/ e, se existir, o registo de tempos
relatorios/<lote>-tempos.csv (colunas: agente,refs,duracao_ms — uma linha por invocação
de agente, com a duração que a notificação do agente indica).

Tempo por pergunta aprovada = soma das durações dos agentes / perguntas aprovadas. É
tempo de trabalho dos agentes: não conta pausas por limite de utilização, esperas por
respostas do Andre nem o tempo do orquestrador. Agentes em paralelo somam-se, por isso
mede o custo, não o tempo de relógio.
"""

import csv
import json
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    lote = sys.argv[1]
    perguntas = []
    for f in sorted((RAIZ / "banco" / "perguntas").glob("*.json")):
        q = json.loads(f.read_text(encoding="utf-8"))
        if q.get("lote") == lote:
            perguntas.append(q)
    if not perguntas:
        print(f"Nenhuma pergunta do lote {lote}.")
        return 1

    estados = Counter(q["estado"] for q in perguntas)
    aprovadas = [q for q in perguntas if q["estado"] in ("aprovada", "publicada")]
    rejeitadas = [q for q in perguntas if q["estado"] == "rejeitada"]

    def n1_pesquisador(q):
        return any(f.get("papel") == "pesquisador" and f.get("nivel") == 1 for f in q["fontes"])

    print(f"Lote: {lote}")
    print(f"Perguntas criadas: {len(perguntas)}")
    print("Por estado: " + ", ".join(f"{k} {v}" for k, v in sorted(estados.items())))
    n1 = sum(n1_pesquisador(q) for q in perguntas)
    print(f"Com fonte de nível 1 do pesquisador: {n1} de {len(perguntas)} ({n1 / len(perguntas):.0%})")
    if aprovadas:
        n1a = sum(n1_pesquisador(q) for q in aprovadas)
        print(f"  … entre as aprovadas: {n1a} de {len(aprovadas)} ({n1a / len(aprovadas):.0%})")
    classicos = sum("classico" in (q.get("etiquetas") or []) for q in perguntas if q["estado"] != "rejeitada")
    ativas = sum(q["estado"] != "rejeitada" for q in perguntas)
    print(f"Clássicos: {classicos} de {ativas} não rejeitadas" + (f" ({classicos / ativas:.0%})" if ativas else ""))
    if rejeitadas:
        print("Rejeitadas por agente:")
        por_agente = Counter()
        for q in rejeitadas:
            ev = [e for e in q["historico"] if e.get("evento") == "rejeitada"]
            por_agente[ev[-1]["agente"] if ev else "?"] += 1
        for a, n in por_agente.most_common():
            print(f"  {a}: {n}")

    tempos = RAIZ / "relatorios" / f"{lote}-tempos.csv"
    if tempos.exists():
        with tempos.open(encoding="utf-8") as fh:
            linhas = list(csv.DictReader(fh))
        total_ms = sum(int(l["duracao_ms"]) for l in linhas)
        por_agente = Counter()
        for l in linhas:
            por_agente[l["agente"]] += int(l["duracao_ms"])
        print(f"Tempo de agentes (sem pausas): {total_ms / 60000:.1f} min em {len(linhas)} invocações")
        for a, ms in por_agente.most_common():
            print(f"  {a}: {ms / 60000:.1f} min")
        if aprovadas:
            print(f"Tempo de agentes por pergunta aprovada: {total_ms / 60000 / len(aprovadas):.1f} min")
    else:
        print(f"Sem registo de tempos ({tempos.relative_to(RAIZ)}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
