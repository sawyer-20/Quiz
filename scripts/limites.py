#!/usr/bin/env python3
"""Valida os limites de texto de perguntas em banco/perguntas/ ANTES de irem ao advogado do diabo.

Uso: python3 scripts/limites.py Q-2026-000080 [Q-2026-000083 ...]

Para cada idioma presente: enunciado até 200 caracteres e terminado em «?», explicação com 10 a 300
caracteres e 1 a 2 frases, opções até 60 caracteres. Sai com código 1 se alguma pergunta falhar
(o orquestrador manda então a pergunta ao editor, que encurta sem mudar factos, atribuições ou
opções). Foi o limite de 300 caracteres que reabriu e matou perguntas do lote 4 já no advogado.
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from validar import n_frases  # noqa: E402


def verificar(q):
    erros = []
    for idioma, t in q.get("text", {}).items():
        if len(t["question"]) > 200:
            erros.append(f"{idioma}: enunciado com {len(t['question'])} caracteres (máx. 200)")
        if not t["question"].rstrip().endswith("?"):
            erros.append(f"{idioma}: enunciado sem «?»")
        ex = t["explanation"]
        if not 10 <= len(ex) <= 300:
            erros.append(f"{idioma}: explicação com {len(ex)} caracteres (10 a 300)")
        if n_frases(ex) > 2:
            erros.append(f"{idioma}: explicação com {n_frases(ex)} frases (máx. 2)")
        for o in t["options"]:
            if len(o) > 60:
                erros.append(f"{idioma}: opção com {len(o)} caracteres (máx. 60): {o[:30]}…")
    return erros


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    mau = 0
    for a in sys.argv[1:]:
        f = Path(a) if a.endswith(".json") else RAIZ / "banco" / "perguntas" / f"{a}.json"
        q = json.loads(f.read_text(encoding="utf-8"))
        erros = verificar(q)
        print(("FALHA " if erros else "OK    ") + q["id"])
        for e in erros:
            print("      " + e)
        mau += bool(erros)
    return 1 if mau else 0


if __name__ == "__main__":
    sys.exit(main())
