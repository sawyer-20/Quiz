#!/usr/bin/env python3
"""Descarrega todas as perguntas verificadas do Open Trivia DB (CC BY-SA 4.0).

Respeita o limite da API (1 pedido a cada 5 s; usamos 5,5 s) e usa um token de sessão para
não repetir perguntas. Grava importacao/opentdb/bruto.json (texto descodificado, sem
entidades HTML) com a categoria, a origem e a data de descarga de cada pergunta.
Uso: python3 scripts/importar_opentdb.py
"""
import base64, json, time, urllib.request, datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "importacao" / "opentdb" / "bruto.json"
API = "https://opentdb.com"
PAUSA = 5.5

def obter(url, tentativas=6):
    for k in range(tentativas):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as e:  # rede instável: espera e repete
            if k == tentativas - 1:
                raise
            print(f"  erro de rede ({e}); nova tentativa em {10 * 2 ** k} s", flush=True)
            time.sleep(10 * 2 ** k)

def b64(s):
    return base64.b64decode(s).decode("utf-8")

def main():
    cats = obter(f"{API}/api_category.php")["trivia_categories"]
    time.sleep(PAUSA)
    token = obter(f"{API}/api_token.php?command=request")["token"]
    hoje = datetime.date.today().isoformat()
    # Retoma: guarda as categorias já completas e volta a pedir as restantes.
    todas, feitas = [], set()
    if SAIDA.exists():
        todas = json.loads(SAIDA.read_text(encoding="utf-8"))
        feitas = {x["categoria_id"] for x in todas}
    for c in cats:
        if c["id"] in feitas:
            continue
        time.sleep(PAUSA)
        n = obter(f"{API}/api_count.php?category={c['id']}")["category_question_count"]["total_question_count"]
        obtidas = 0
        while obtidas < n:
            pedir = min(50, n - obtidas)
            time.sleep(PAUSA)
            d = obter(f"{API}/api.php?amount={pedir}&category={c['id']}&token={token}&encode=base64")
            if d["response_code"] != 0:
                print(f"  categoria {c['id']}: código {d['response_code']} com {obtidas}/{n}")
                break
            for q in d["results"]:
                todas.append({
                    "categoria_id": c["id"], "categoria": b64(q["category"]),
                    "tipo": b64(q["type"]), "dificuldade": b64(q["difficulty"]),
                    "pergunta": b64(q["question"]), "certa": b64(q["correct_answer"]),
                    "erradas": [b64(x) for x in q["incorrect_answers"]],
                    "licenca": "CC BY-SA 4.0", "origem": "Open Trivia DB (https://opentdb.com)",
                    "descarregada_em": hoje,
                })
            obtidas += len(d["results"])
        print(f"{c['id']:>2} {c['name']}: {obtidas}/{n}", flush=True)
        if obtidas < n:
            todas = [x for x in todas if x["categoria_id"] != c["id"]]
            print(f"  categoria {c['id']} incompleta: não fica gravada; volta a correr o script")
        SAIDA.write_text(json.dumps(todas, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"Total: {len(todas)}")

if __name__ == "__main__":
    main()
