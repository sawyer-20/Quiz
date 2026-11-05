#!/usr/bin/env python3
"""Aprova perguntas: a única forma de uma pergunta passar a "aprovada".

Uso:
    python3 scripts/aprovar.py Q-2026-000005 [Q-2026-000006 ...]
    python3 scripts/aprovar.py banco/perguntas/Q-2026-000005.json

Para cada pergunta em "em_verificacao":
  1. prepara a versão aprovada (estado "aprovada" e o evento "aprovada por aprovar.py"
     no histórico);
  2. corre o scripts/validar.py sobre essa versão e, se for um clássico, verifica a quota
     de clássicos do lote;
  3. só se tudo passar grava o ficheiro. Se falhar, o ficheiro fica como estava.

Sai com código 1 se alguma pergunta não for aprovada.
"""

import json
import subprocess
import sys
import tempfile
from copy import deepcopy
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BANCO = RAIZ / "banco" / "perguntas"
sys.path.insert(0, str(RAIZ / "scripts"))
from validar import EVENTO_APROVACAO, erros_de_lote  # noqa: E402


def caminho(arg: str) -> Path:
    p = Path(arg)
    return p if p.suffix == ".json" else BANCO / f"{arg}.json"


def validar_candidata(candidata: dict) -> list[str]:
    """Corre o validar.py sobre a versão candidata e devolve as linhas de erro."""
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / f"{candidata['id']}.json"
        f.write_text(json.dumps(candidata, ensure_ascii=False, indent=2), encoding="utf-8")
        r = subprocess.run([sys.executable, str(RAIZ / "scripts" / "validar.py"), str(f)],
                           capture_output=True, text=True)
    erros = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("ERRO:")]
    if r.returncode != 0 and not erros:
        erros = [f"validar.py falhou: {r.stdout.strip() or r.stderr.strip()}"]
    # Quota de clássicos: o lote inteiro, com esta pergunta na versão candidata.
    lote = []
    for g in BANCO.glob("*.json"):
        q = json.loads(g.read_text(encoding="utf-8"))
        if q.get("lote") == candidata["lote"] and q.get("id") != candidata["id"]:
            lote.append(q)
    lote.append(candidata)
    # Aprovar uma pergunta que não é clássica não agrava a quota: só se verifica para clássicos.
    if "classico" in (candidata.get("etiquetas") or []):
        erros += [f"ERRO: {e}" for e in erros_de_lote(lote).get(candidata["lote"], [])]
    return erros


def gravar(f: Path, q: dict) -> None:
    f.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def aprovar(f: Path) -> bool:
    q = json.loads(f.read_text(encoding="utf-8"))
    if q.get("estado") != "em_verificacao":
        print(f"RECUSADA {q.get('id')}: estado '{q.get('estado')}' (só se aprova a partir de em_verificacao)")
        return False
    c = deepcopy(q)
    c["estado"] = "aprovada"
    c["historico"].append({"data": date.today().isoformat(), "evento": EVENTO_APROVACAO,
                           "agente": "aprovar.py", "nota": "validar.py sem erros"})
    erros = validar_candidata(c)
    if erros:
        print(f"NÃO APROVADA {q['id']}:")
        for e in erros:
            print(f"      {e}")
        return False
    gravar(f, c)
    print(f"APROVADA {q['id']}")
    return True


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    resultados = [aprovar(caminho(a)) for a in args]
    return 0 if all(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
