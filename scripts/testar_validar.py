#!/usr/bin/env python3
"""Testes das regras de texto do validar.py.

Uso: python3 scripts/testar_validar.py      (sai com código 1 se algum falhar)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validar import duvida_sem_atribuicao, quota_classicos  # noqa: E402

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
    # Quota de clássicos sobre o banco: só bloqueia a partir de 100 aprovadas/publicadas.
    def banco(n, classicos, estado="aprovada"):
        return [{"estado": estado, "etiquetas": ["classico"] if i < classicos else []} for i in range(n)]
    QUOTA = [
        ("99 aprovadas, 50 clássicos: só mede", banco(99, 50), False),
        ("100 aprovadas, 20 clássicos (20%): passa", banco(100, 20), False),
        ("100 aprovadas, 21 clássicos (21%): bloqueia", banco(100, 21), True),
        ("rejeitadas não contam", banco(100, 10) + banco(50, 50, "rejeitada"), False),
        ("em_verificacao não conta", banco(100, 20) + banco(10, 10, "em_verificacao"), False),
    ]
    for nome, perguntas, bloquear in QUOTA:
        _, _, erro = quota_classicos(perguntas)
        ok = (erro is not None) == bloquear
        falhas += not ok
        print(f"{'OK ' if ok else 'FALHA'} quota: {nome}")

    print(f"\n{falhas} falha(s).")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
