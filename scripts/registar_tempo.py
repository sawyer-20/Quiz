#!/usr/bin/env python3
"""Acrescenta uma invocação de agente ao registo de tempos de um lote.

Uso: python3 scripts/registar_tempo.py <lote> <agente> <refs> <duracao_ms>

Regista TODAS as invocações, incluindo as de correção (pesquisador a corrigir, segundas
passagens do advogado, verificações repetidas). Cria o ficheiro com o cabeçalho
`agente,refs,duracao_ms` se ainda não existir.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def main() -> int:
    if len(sys.argv) != 5:
        print(__doc__)
        return 2
    lote, agente, refs, ms = sys.argv[1:]
    if not ms.isdigit() or "," in agente + refs:
        print("duracao_ms tem de ser um inteiro; agente e refs sem vírgulas.")
        return 2
    f = RAIZ / "relatorios" / f"{lote}-tempos.csv"
    novo = not f.exists()
    with f.open("a", encoding="utf-8") as fh:
        if novo:
            fh.write("agente,refs,duracao_ms\n")
        fh.write(f"{agente},{refs},{ms}\n")
    print(f"registado: {agente} {refs} {ms} ms em {f.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
