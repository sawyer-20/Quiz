#!/usr/bin/env python3
"""Aplica o resultado de um agente a banco/perguntas/<id>.json (esquema v2).

Nunca escreve texto factual: copia o que o agente devolveu. Uso:

  aplicar_passo.py verif        <id> <json>   verificador às cegas (uma pergunta do seu JSON)
  aplicar_passo.py adv          <id> <json>   advogado do diabo (só regista se aprovado)
  aplicar_passo.py leve         <id>          caminho leve (dif. 1, sem advogado; teste do lote 4)
  aplicar_passo.py reformular   <id> <json>   aplica a reformulação sugerida (volta ao verificador)
  aplicar_passo.py editor       <id> <json>   editor (só estilo: opções e ordem não mudam)
  aplicar_passo.py traducao     <id> <json>   tradutor (escreve o en-US)
  aplicar_passo.py conferencia  <id> <json>   conferente (aprova ou devolve os problemas)
  aplicar_passo.py originalidade <id> <veredicto> <nota>   regista o veredicto do agente
  aplicar_passo.py rejeitar     <id> <agente> <motivo>
  aplicar_passo.py suspender    <id> <agente> <motivo>

O <json> é o item da pergunta (um objeto, não a lista `resultados`). Sai com código 3 quando o
resultado exige uma decisão (ambiguidade, não aprovado, ciclo de correção).
"""

import json
import random
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from validar import dominio_registavel, normalizar  # noqa: E402

HOJE = date.today().isoformat()


def carregar(pid):
    f = RAIZ / "banco" / "perguntas" / f"{pid}.json"
    return f, json.loads(f.read_text(encoding="utf-8"))


def gravar(f, q):
    f.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ev(q, evento, agente, nota=""):
    q["historico"].append({"data": HOJE, "evento": evento, "agente": agente, "nota": nota})


def rejeitar(q, agente, motivo):
    q["estado"] = "rejeitada"
    q["motivo_rejeicao"] = motivo
    ev(q, "rejeitada", agente, motivo)


def pt(q):
    return q["text"]["pt-PT"]


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    cmd, pid = sys.argv[1:3]
    f, q = carregar(pid)

    if cmd == "originalidade":
        veredicto, nota = sys.argv[3], (sys.argv[4] if len(sys.argv) > 4 else "")
        if veredicto == "classico":
            q["etiquetas"] = sorted(set(q.get("etiquetas", [])) | {"classico"})
        ev(q, f"originalidade: {veredicto}", "originalidade", nota)
        if veredicto == "copiada":
            rejeitar(q, "originalidade", f"copiada: {nota}")
        gravar(f, q)
        print(f"{pid}: originalidade {veredicto}")
        return 0

    if cmd == "leve":
        if q.get("difficulty") != 1 or q.get("estado") != "em_verificacao" or not q["verificacao"].get("verificador"):
            print("RECUSADO: o caminho leve exige dificuldade 1, em_verificacao e verificador às cegas já registado"); return 3
        q["verificacao"]["caminho_leve"] = True
        q["etiquetas"] = sorted(set(q.get("etiquetas", [])) | {"caminho_leve"})
        ev(q, "caminho leve (sem advogado do diabo)", "orquestrador", sys.argv[3])
        gravar(f, q); print("CAMINHO LEVE", pid)
        return 0

    if cmd in ("rejeitar", "suspender"):
        agente, motivo = sys.argv[3], sys.argv[4]
        if cmd == "rejeitar":
            rejeitar(q, agente, motivo)
        else:
            q["estado"], q["motivo_rejeicao"] = "suspensa", motivo
            ev(q, "suspensa", agente, motivo)
        gravar(f, q)
        print(("REJEITADA" if cmd == "rejeitar" else "SUSPENSA"), pid)
        return 0

    r = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))

    if cmd == "verif":
        certa = pt(q)["options"][q["correct"]]
        pesq = {x["dominio"] for x in q["fontes"] if x["papel"] == "pesquisador"}
        rt, fonte = r.get("resposta_texto"), r.get("fonte") or {}
        dom = dominio_registavel(fonte["url"]) if fonte.get("url") else None
        if rt is None or r.get("confianca") == "baixa":
            rejeitar(q, "verificador-cego", f"sem confirmação: {r.get('notas', '')}"[:500]); res = "REJEITADA sem confirmação"
        elif normalizar(rt) != normalizar(certa):
            rejeitar(q, "verificador-cego", f"discorda: verificador respondeu '{rt}' ({r.get('notas', '')})"[:500]); res = "REJEITADA discorda"
        elif dom in pesq:
            rejeitar(q, "verificador-cego", f"fonte não independente ({dom})"); res = "REJEITADA fonte não independente"
        elif r.get("ambiguidade"):
            print("AMBIGUIDADE ASSINALADA — decidir:", r["ambiguidade"])
            return 3
        else:
            q["fontes"] = [x for x in q["fontes"] if x["papel"] != "verificador"]
            q["fontes"].append({"url": fonte["url"], "dominio": dom, "titulo": fonte["titulo"], "nivel": fonte["nivel"],
                                "excerto": fonte["excerto"][:300], "consultada_em": HOJE, "papel": "verificador"})
            q["verificacao"]["verificador"] = {"resposta_texto": certa, "concorda": True, "confianca": r["confianca"],
                                               "dominio": dom, "data": HOJE, "notas": r.get("notas", "")}
            ev(q, "verificada às cegas", "verificador-cego", f"confiança {r['confianca']}; fonte {dom}")
            res = f"PASSA (confiança {r['confianca']}, {dom}, nível {fonte['nivel']})"
        gravar(f, q); print(res)
        return 0

    if cmd == "adv":
        if not r.get("aprovado"):
            print("NÃO APROVADO — decidir à parte (reformulação, ou rejeitar se já houve um ciclo)")
            return 3
        urls = {x["url"] for x in q["fontes"]}
        for fo in r.get("fontes_guardar", []):
            if fo["url"] not in urls:
                q["fontes"].append({"url": fo["url"], "dominio": dominio_registavel(fo["url"]), "titulo": fo["titulo"],
                                    "nivel": fo["nivel"], "excerto": fo["excerto"][:300], "consultada_em": HOJE,
                                    "papel": "advogado"})
        q["verificacao"]["advogado"] = {"aprovado": True, "notas": r.get("notas", ""), "data": HOJE}
        ev(q, "aprovada pelo advogado do diabo", "advogado-do-diabo")
        gravar(f, q); print("ADVOGADO APROVA")
        return 0

    if cmd == "reformular":
        certa = pt(q)["options"][q["correct"]]
        if r.get("enunciado"):
            pt(q)["question"] = r["enunciado"]
        if r.get("opcoes_texto"):
            ops = list(r["opcoes_texto"])
            nova = r.get("resposta", certa)
            assert nova in ops, "a resposta tem de estar nas novas opções"
            random.SystemRandom().shuffle(ops)
            pt(q)["options"], q["correct"] = ops, ops.index(nova)
        if r.get("explicacao"):
            pt(q)["explanation"] = r["explicacao"]
        q["text"].pop("en-US", None)
        q["verificacao"]["verificador"] = None
        q["verificacao"]["advogado"] = None
        for k in ("tradutor", "conferente"):
            q["verificacao"].pop(k, None)
        q["fontes"] = [x for x in q["fontes"] if x["papel"] != "verificador"]
        ev(q, "reformulada", r.get("agente", "advogado-do-diabo"), r.get("nota", ""))
        gravar(f, q)
        cego = pt(q)["options"][:]; random.SystemRandom().shuffle(cego)
        print(json.dumps({"enunciado": pt(q)["question"], "opcoes_cego": cego,
                          "dominios_proibidos": sorted({x["dominio"] for x in q["fontes"] if x["papel"] == "pesquisador"}),
                          "titulos_a_evitar": [x["titulo"] for x in q["fontes"] if x["papel"] == "pesquisador"]},
                         ensure_ascii=False))
        return 0

    if cmd == "editor":
        if not r.get("originalidade_ok"):
            rejeitar(q, "editor", "copiada: " + r.get("notas", "")); gravar(f, q); print("REJEITADA copiada"); return 0
        if not r.get("aprovado"):
            rejeitar(q, "editor", r.get("notas", "editor não aprovou")); gravar(f, q); print("REJEITADA editor"); return 0
        if r.get("alteracao_factual"):
            print("ALTERAÇÃO FACTUAL — volta ao verificador"); return 3
        atuais = pt(q)["options"]
        novas = r.get("opcoes", atuais)
        if novas != atuais:
            print("RECUSADO: o editor não pode mudar o texto nem a ordem das opções (regra 3/19); a pergunta passa a 'reescrever' se for preciso")
            return 3
        pt(q)["question"], pt(q)["explanation"] = r["enunciado"], r["explicacao"]
        q["difficulty"] = r["dificuldade_estimada"]
        if r.get("subtema") or r.get("subtopic"):
            q["subtopic"] = (r.get("subtopic") or r["subtema"])[:60]
        q["verificacao"]["editor"] = {"aprovado": True, "originalidade_ok": True, "alteracao_factual": False,
                                      "notas": r.get("notas", ""), "data": HOJE}
        ev(q, "revista pelo editor", "editor")
        gravar(f, q); print("EDITOR APLICADO")
        return 0

    if cmd == "traducao":
        if r.get("traduzivel") is False:
            print("NÃO TRADUZÍVEL — decidir:", r.get("motivo") or r.get("notas")); return 3
        if len(r.get("options", [])) != 4:
            print("RECUSADO: o en-US tem de ter 4 opções"); return 3
        q["text"]["en-US"] = {"question": r["question"], "options": r["options"], "explanation": r["explanation"]}
        q["verificacao"]["tradutor"] = {"data": HOJE, "notas": r.get("notas", "")}
        q["verificacao"].pop("conferente", None)
        ev(q, "traduzida (en-US)", "tradutor", r.get("notas", ""))
        gravar(f, q); print("TRADUÇÃO APLICADA")
        return 0

    if cmd == "conferencia":
        if not r.get("aprovado"):
            ev(q, "conferência recusada", "conferente", json.dumps(r.get("problemas", []), ensure_ascii=False)[:500])
            q["verificacao"]["conferente"] = {"aprovado": False, "notas": r.get("notas", ""), "data": HOJE}
            gravar(f, q); print("CONFERENTE NÃO APROVA — decidir:", r.get("problemas")); return 3
        q["verificacao"]["conferente"] = {"aprovado": True, "notas": r.get("notas", ""), "data": HOJE}
        ev(q, "conferida (pt-PT = en-US)", "conferente")
        gravar(f, q); print("CONFERENTE APROVA")
        return 0

    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
