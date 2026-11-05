#!/usr/bin/env python3
"""Testes das regras de texto do validar.py.

Uso: python3 scripts/testar_validar.py      (sai com código 1 se algum falhar)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validar import duvida_sem_atribuicao  # noqa: E402

# texto da explicação -> True se tem de ser recusado (dúvida sem atribuição)
CASOS = {
    "Ao que parece, os romanos espalhavam cal sobre os cacos.": True,
    "Diz-se que Dias lhe chamou Cabo Tormentoso.": True,
    "Terá sido construída em 1634.": True,
    "Possivelmente veio da Bética.": True,
    "Segundo consta, foi D. João II.": True,
    "Segundo a tradição, D. João II rebatizou-o. Talvez tenha sido o próprio Dias.": True,
    "Segundo os arqueólogos, os romanos terão espalhado cal.": False,
    "Barros afirma que o rei terá mudado o nome.": False,
    "De acordo com Axelson, foi possivelmente o próprio Dias.": False,
    "Os romanos cobriam os cacos com cal.": False,
    "Segundo o cronista João de Barros, Dias chamou-lhe Cabo Tormentoso.": False,
}


def main() -> int:
    falhas = 0
    for texto, recusar in CASOS.items():
        recusado = duvida_sem_atribuicao(texto) is not None
        ok = recusado == recusar
        falhas += not ok
        print(f"{'OK ' if ok else 'FALHA'} {'recusa' if recusar else 'aceita'}: {texto}")
    print(f"\n{falhas} falha(s).")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
