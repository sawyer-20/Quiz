#!/usr/bin/env python3
"""Gera respostas fictícias para testar o calibrador antes de haver jogadores.

Uso:
    python3 scripts/simular_respostas.py [--saida banco/respostas/simulado.csv]
    python3 scripts/calibrar.py banco/respostas/simulado.csv

Simula 300 jogadores e 40 perguntas (SIM-001 a SIM-040), com 4 opções e acerto ao
acaso de 25%. Duas perguntas têm problemas de propósito:
- SIM-013 tem a chave errada: os melhores jogadores escolhem a resposta verdadeira, que
  está marcada como errada, por isso acertam MENOS do que os piores;
- SIM-027 é demasiado fácil.
O calibrador deve assinalar ambas.
"""

import argparse
import csv
import math
import random
from pathlib import Path


def sigmoide(x):
    return 1 / (1 + math.exp(-x))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", type=Path, default=Path("banco/respostas/simulado.csv"))
    args = ap.parse_args()

    rng = random.Random(42)
    jogadores = {f"J{i:04d}": rng.gauss(0, 1) for i in range(1, 301)}
    perguntas = {f"SIM-{i:03d}": rng.uniform(-2, 2) for i in range(1, 41)}
    perguntas["SIM-027"] = -6.0

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    with args.saida.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(["jogador_id", "pergunta_id", "correta", "tempo_ms"])
        for jogador, capacidade in jogadores.items():
            for pergunta in rng.sample(sorted(perguntas), 25):
                if pergunta == "SIM-013":
                    p = 0.15 + 0.6 * (1 - sigmoide(1.5 * capacidade))
                else:
                    p = 0.25 + 0.75 * sigmoide(capacidade - perguntas[pergunta])
                escritor.writerow([jogador, pergunta, int(rng.random() < p), rng.randint(2500, 14000)])
    print(f"Respostas simuladas gravadas em {args.saida}")


if __name__ == "__main__":
    main()
