#!/usr/bin/env python3
"""Migra o banco do esquema v1.1 (só pt-PT) para o esquema v2 (pt-PT e en-US).

Uso:
    python3 scripts/migrar_v2.py            # migra banco/perguntas/*.json (idempotente)
    python3 scripts/migrar_v2.py --ver      # mostra o que mudaria, sem gravar

O facto já está verificado: o texto pt-PT passa para text["pt-PT"] tal como está. As
perguntas aprovadas ou publicadas voltam a "em_verificacao" até terem o en-US (tradutor) e a
conferência (conferente); depois o aprovar.py aprova-as de novo. Q26 e Q40 ficam "suspensa".
"""

import json
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from validar import dominio_registavel  # noqa: E402

TOPIC_POR_TEMA = {
    "historia": "World History", "geografia": "Geography", "ciencia": "Science",
    "cinema-tv": "Movies", "musica": "Music", "desporto": "General Knowledge",
    "literatura": "General Knowledge", "arte": "General Knowledge",
    "portugal": "General Knowledge", "atualidade": "General Knowledge",
}
# Decisões editoriais por pergunta (as outras seguem TOPIC_POR_TEMA).
TOPIC_POR_ID = {
    "Q-2026-000016": "Geography", "Q-2026-000019": "Movies", "Q-2026-000024": "Science",
    "Q-2026-000026": "World History", "Q-2026-000031": "Geography", "Q-2026-000032": "World History",
    "Q-2026-000036": "Science", "Q-2026-000037": "Nature & Animals", "Q-2026-000047": "World History",
    "Q-2026-000025": "Music", "Q-2026-000048": "Music", "Q-2026-000040": "Movies",
}
# Interesse local (só aparecem nos mercados indicados).
MERCADOS_POR_ID = {
    "Q-2026-000016": ["pt"],  # Serra da Estrela
    "Q-2026-000019": ["pt"],  # Cinemateca Portuguesa
    "Q-2026-000021": ["pt"],  # Real Instituto de Surdos-Mudos e Cegos
    "Q-2026-000022": ["pt"],  # Grande Panorama de Lisboa
    "Q-2026-000025": ["pt"],  # Bomtempo
    "Q-2026-000026": ["pt"],  # Bartolomeu Dias / Pacheco Pereira
    "Q-2026-000031": ["pt"],  # Capelinhos (Açores)
    "Q-2026-000045": ["pt"],  # Biblioteca Joanina
    "Q-2026-000047": ["pt"],  # hurdício nos castelos portugueses
    "Q-2026-000048": ["pt"],  # Liszt em Lisboa
}
SUSPENSAS = {
    "Q-2026-000026": "em espera: falta fonte de nível 1 do texto do Esmeraldo ou reformulação atribuída («segundo Duarte Pacheco Pereira…»)",
    "Q-2026-000040": "em espera: falta fonte de nível 1 (só fontes de nível 2)",
}


def sources(fontes):
    """Até 3 URLs para o jogador: nível 1 primeiro (pesquisador antes dos outros), sem Wikipédia."""
    ordem = sorted((f for f in fontes if dominio_registavel(f["url"]) != "wikipedia.org"),
                   key=lambda f: (f["nivel"], f["papel"] != "pesquisador"))
    urls, vistos = [], set()
    for f in ordem:
        if dominio_registavel(f["url"]) in vistos:
            continue
        vistos.add(dominio_registavel(f["url"]))
        urls.append(f["url"])
        if len(urls) == 3:
            break
    return urls


def migrar(q):
    pid = q["id"]
    estado = q["estado"]
    novo = {
        "id": pid,
        "topic": TOPIC_POR_ID.get(pid) or TOPIC_POR_TEMA[q["tema"]],
        "subtopic": q["subtema"],
    }
    if pid in MERCADOS_POR_ID:
        novo["markets"] = MERCADOS_POR_ID[pid]
    novo["text"] = {"pt-PT": {"question": q["enunciado"], "options": q["opcoes"],
                              "explanation": q["explicacao"]}}
    novo["correct"] = q["correta"]
    novo["difficulty"] = q["dificuldade_estimada"]
    novo["valid_until"] = q["valida_ate"]
    novo["daily_eligible"] = q["valida_ate"] is None and not q["sensivel_ao_tempo"]
    novo["sources"] = sources(q["fontes"])
    novo["fontes"] = q["fontes"]
    novo["verificacao"] = q["verificacao"]
    motivo = q["motivo_rejeicao"]
    hoje = date.today().isoformat()
    historico = list(q["historico"])
    if pid in SUSPENSAS:
        novo["estado"] = "suspensa"
        motivo = SUSPENSAS[pid]
        historico.append({"data": hoje, "evento": "migrada para v2 e suspensa", "agente": "orquestrador",
                          "nota": motivo})
    elif estado in ("aprovada", "publicada"):
        novo["estado"] = "em_verificacao"
        historico.append({"data": hoje, "evento": "migrada para v2", "agente": "orquestrador",
                          "nota": "facto já verificado; aguarda o en-US (tradutor) e a conferência (conferente)"})
    else:
        novo["estado"] = estado
        historico.append({"data": hoje, "evento": "migrada para v2", "agente": "orquestrador",
                          "nota": "só pt-PT (pergunta rejeitada ou em curso)"})
    novo["motivo_rejeicao"] = motivo
    novo["lote"] = q["lote"]
    novo["criada_em"] = q["criada_em"]
    novo["historico"] = historico
    if q.get("etiquetas"):
        novo["etiquetas"] = q["etiquetas"]
    return novo


def main():
    ver = "--ver" in sys.argv
    n = 0
    for f in sorted((RAIZ / "banco" / "perguntas").glob("*.json")):
        q = json.loads(f.read_text(encoding="utf-8"))
        if "topic" in q:
            continue
        novo = migrar(q)
        n += 1
        print(f"{q['id']}: {q['estado']} -> {novo['estado']}; {novo['topic']}"
              + (f"; markets {novo['markets']}" if "markets" in novo else ""))
        if not ver:
            f.write_text(json.dumps(novo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{n} pergunta(s) {'a migrar' if ver else 'migradas'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
