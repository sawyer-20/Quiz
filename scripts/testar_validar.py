#!/usr/bin/env python3
"""Testes das regras de texto do validar.py.

Uso: python3 scripts/testar_validar.py      (sai com código 1 se algum falhar)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validar import (duvida_sem_atribuicao, n_frases, numeros, opcoes_lock, quota_classicos,  # noqa: E402
                     validar_pergunta)

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

    # Dúvida em inglês (en-US): recusa-se sem atribuição, aceita-se atribuída.
    EN = {
        "Apparently the Romans spread lime over the shards.": True,
        "It is believed that Dias named the cape.": True,
        "He probably named it himself.": True,
        "According to Axelson, Dias probably named it himself.": False,
        "Historians say that the king renamed the cape.": False,
        "The Romans covered the shards with lime.": False,
    }
    for texto, recusar in EN.items():
        ok = (duvida_sem_atribuicao(texto, "en-US") is not None) == recusar
        falhas += not ok
        print(f"{'OK ' if ok else 'FALHA'} en-US {'recusa' if recusar else 'aceita'}: {texto}")

    # Frases e números (paridade entre os dois textos).
    for texto, n in [("Uma frase. Outra frase.", 2), ("Uma. Duas. Três.", 3), ("Só uma, com 1.5 km.", 1)]:
        ok = n_frases(texto) == n
        falhas += not ok
        print(f"{'OK ' if ok else 'FALHA'} frases: {texto!r} -> {n_frases(texto)}")
    for a, b, igual in [("2,4 km²", "2.4 km²", True), ("350 000 ducados", "350,000 ducats", True),
                        ("em 1845", "in 1854", False), ("1993 m", "1,993 m", True)]:
        ok = (numeros(a) == numeros(b)) == igual
        falhas += not ok
        print(f"{'OK ' if ok else 'FALHA'} números: {a!r} ~ {b!r}")

    # Pergunta bilingue completa e as regras da v2.
    def base(estado="em_verificacao"):
        return {
            "id": "Q-2026-999999", "topic": "Geography", "subtopic": "teste",
            "text": {"pt-PT": {"question": "Qual é a capital de Portugal?",
                               "options": ["Lisboa", "Porto", "Coimbra", "Braga"],
                               "explanation": "É Lisboa, a maior cidade do país."},
                     "en-US": {"question": "What is the capital of Portugal?",
                               "options": ["Lisbon", "Porto", "Coimbra", "Braga"],
                               "explanation": "It is Lisbon, the country's largest city."}},
            "correct": 0, "difficulty": 1, "daily_eligible": True, "valid_until": None,
            "sources": ["https://www.ine.pt/x"],
            "fontes": [{"url": "https://www.ine.pt/x", "dominio": "ine.pt", "titulo": "INE", "nivel": 1,
                        "excerto": "Lisboa é a capital.", "consultada_em": "2026-11-11", "papel": "pesquisador"},
                       {"url": "https://www.cm-lisboa.pt/y", "dominio": "cm-lisboa.pt", "titulo": "CML", "nivel": 1,
                        "excerto": "Lisboa.", "consultada_em": "2026-11-11", "papel": "verificador"}],
            "verificacao": {"verificador": {"resposta_texto": "Lisboa", "concorda": True, "confianca": "alta",
                                            "dominio": "cm-lisboa.pt", "data": "2026-11-11"},
                            "advogado": {"aprovado": True, "data": "2026-11-11"},
                            "editor": {"aprovado": True, "originalidade_ok": True, "alteracao_factual": False,
                                       "data": "2026-11-11"},
                            "tradutor": {"data": "2026-11-11"},
                            "conferente": {"aprovado": True, "data": "2026-11-11"}},
            "estado": estado, "motivo_rejeicao": None, "lote": "teste", "criada_em": "2026-11-11",
            "historico": [{"data": "2026-11-11", "evento": "criada", "agente": "pesquisador"}],
        }

    def aprovada():
        q = base("aprovada")
        q["historico"].append({"data": "2026-11-11", "evento": "aprovada por aprovar.py", "agente": "aprovar.py"})
        q["options_lock"] = opcoes_lock(q)
        return q

    def erros_de(q):
        return validar_pergunta(q)[0]

    def com(q, f):
        f(q)
        return q

    CASOS_V2 = [
        ("em_verificacao completa: sem erros", base(), None),
        ("aprovada completa: sem erros", aprovada(), None),
        ("aprovada sem en-US", com(aprovada(), lambda q: q["text"].pop("en-US")), "sem texto en-US"),
        ("aprovada sem conferente", com(aprovada(), lambda q: q["verificacao"].pop("conferente")), "conferente"),
        ("aprovada sem tradutor", com(aprovada(), lambda q: q["verificacao"].pop("tradutor")), "tradutor"),
        ("opção mudada depois de aprovada", com(aprovada(), lambda q: q["text"]["en-US"]["options"].__setitem__(1, "Oporto")), "options_lock"),
        ("aprovada sem options_lock", com(aprovada(), lambda q: q.pop("options_lock")), "options_lock"),
        ("números diferentes entre idiomas", com(base(), lambda q: q["text"]["en-US"].__setitem__("question", "What was the capital of Portugal in 1755?")), "números"),
        ("explicação com 3 frases aprovada", com(aprovada(), lambda q: q["text"]["pt-PT"].__setitem__("explanation", "Uma frase. Outra frase. Mais uma.")), "frases"),
        ("daily_eligible com valid_until", com(base(), lambda q: q.update(valid_until="2027-01-01", daily_eligible=True)), "daily_eligible"),
        ("topic desconhecido", com(base(), lambda q: q.update(topic="Sports")), "topic desconhecido"),
        ("markets inválido", com(base(), lambda q: q.update(markets=["br"])), "markets"),
        ("sources fora de fontes", com(base(), lambda q: q.update(sources=["https://exemplo.org/z"])), "não está em 'fontes'"),
        ("dúvida em inglês sem atribuição", com(base(), lambda q: q["text"]["en-US"].__setitem__("explanation", "It is probably Lisbon.")), "dúvida"),
    ]
    for nome, q, esperado in CASOS_V2:
        erros = erros_de(q)
        ok = (not erros) if esperado is None else any(esperado in e for e in erros)
        falhas += not ok
        print(f"{'OK ' if ok else 'FALHA'} v2: {nome}" + ("" if ok else f"  -> {erros}"))

    print(f"\n{falhas} falha(s).")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
