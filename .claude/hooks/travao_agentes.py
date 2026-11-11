#!/usr/bin/env python3
"""Travão de independência dos agentes (PreToolUse).

Os agentes que pesquisam e verificam não podem ler o banco. No ambiente cloud o
WebFetch não tem rede, por isso têm Bash, mas só para correr o leitor:
    python3 scripts/ler_url.py '<url>' [--procurar '<termo>'] [--inicio N]
Qualquer outro comando, e qualquer ferramenta de ficheiros, é recusado.
A sessão principal (sem agent_type) e os outros agentes não são afetados.
"""

import json
import os
import re
import shlex
import sys

PROTEGIDOS = {"pesquisador", "originalidade", "verificador-cego", "advogado-do-diabo", "editor",
              "tradutor", "conferente", "auditor", "sentinela", "triagem"}
# Ferramentas sem acesso a ficheiros: pesquisa web e entrega do relatório ao orquestrador.
FERRAMENTAS_LIVRES = {"WebSearch", "WebFetch", "ToolSearch", "SubagentHandback",
                      "StructuredOutput"}
PROIBIDOS = re.compile(r"[;&|`$<>\n\r(){}\\*?\[\]~!]")


def recusar(motivo):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": motivo}}))
    sys.exit(0)


def fora_de_aspas(cmd):
    """Texto fora de aspas simples (onde a shell interpreta caracteres).
    Devolve None se houver aspas simples por fechar."""
    fora, dentro = [], False
    for c in cmd:
        if c == "'":
            dentro = not dentro
        elif not dentro:
            fora.append(c)
    return None if dentro else "".join(fora)


def comando_valido(cmd):
    cmd = cmd.strip()
    fora = fora_de_aspas(cmd)
    if fora is None or PROIBIDOS.search(fora) or '"' in fora:
        return False
    try:
        t = shlex.split(cmd)
    except ValueError:
        return False
    if len(t) < 3 or t[0] != "python3" or t[1] != "scripts/ler_url.py":
        return False
    resto, url_visto = t[2:], False
    i = 0
    while i < len(resto):
        x = resto[i]
        if x in ("--procurar", "--inicio"):
            if i + 1 >= len(resto):
                return False
            if x == "--inicio" and not resto[i + 1].isdigit():
                return False
            i += 2
            continue
        if x.startswith(("https://", "http://")) and not url_visto:
            url_visto = True
            i += 1
            continue
        return False
    return url_visto


def lote_ativo(d):
    """Enquanto existir .claude/hooks/LOTE_ATIVO, qualquer subagente genérico também é
    protegido: serve para quando os agentes do motor não estão registados na sessão e o
    orquestrador lança os papéis como general-purpose."""
    base = os.environ.get("CLAUDE_PROJECT_DIR") or d.get("cwd") or "."
    return os.path.exists(os.path.join(base, ".claude", "hooks", "LOTE_ATIVO"))


def main():
    d = json.load(sys.stdin)
    agente = d.get("agent_type")
    protegido = agente in PROTEGIDOS or (agente == "general-purpose" and lote_ativo(d))
    if not protegido:
        sys.exit(0)
    ferramenta = d.get("tool_name", "")
    if ferramenta in FERRAMENTAS_LIVRES:
        sys.exit(0)
    if ferramenta == "Bash":
        cmd = (d.get("tool_input") or {}).get("command", "")
        if comando_valido(cmd):
            sys.exit(0)
        recusar("Travão de independência: o único comando permitido é "
                "python3 scripts/ler_url.py '<url>' [--procurar '<termo>'] [--inicio N], "
                "sem outros caracteres de shell.")
    recusar(f"Travão de independência: o agente {agente} não pode usar {ferramenta}.")


if __name__ == "__main__":
    main()
