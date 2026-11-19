#!/usr/bin/env python3
"""Exporta as perguntas `aprovada` do banco para app/assets/perguntas.json.

Só entram perguntas aprovadas e publicadas-ou-aprovadas com os dois idiomas; as suspensas,
rejeitadas e em verificação ficam de fora. Não escreve texto factual: copia o que está no banco.
Uso: python3 scripts/exportar_app.py            (teste fechado: inclui as com `confirmacao_pendente`)
     python3 scripts/exportar_app.py --publico   (versão pública: exclui as com `confirmacao_pendente`)
"""
import sys
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ESTADOS = {"aprovada", "publicada"}

def main():
    publico = "--publico" in sys.argv
    saida = []
    for f in sorted((RAIZ / "banco" / "perguntas").glob("Q-*.json")):
        q = json.loads(f.read_text(encoding="utf-8"))
        if q.get("estado") not in ESTADOS:
            continue
        t = q["text"]
        if "pt-PT" not in t or "en-US" not in t:
            continue
        if publico and q.get("confirmacao_pendente") is True:
            continue
        saida.append({
            "id": f.stem,
            "topic": q["topic"],
            "difficulty": q["difficulty"],
            "daily": bool(q.get("daily_eligible")),
            "pendente": bool(q.get("confirmacao_pendente")),
            "correct": q["correct"],
            "text": {l: {"q": t[l]["question"], "o": t[l]["options"], "e": t[l]["explanation"]} for l in ("pt-PT", "en-US")},
        })
    destino = RAIZ / "app" / "assets" / "perguntas.json"
    destino.write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(saida)} perguntas exportadas para {destino.relative_to(RAIZ)}")

if __name__ == "__main__":
    main()
