#!/usr/bin/env python3
"""Calibração das perguntas a partir das respostas reais dos jogadores.

Uso:
    python3 scripts/calibrar.py banco/respostas/<ficheiro>.csv [--min-n 30] [--saida caminho.csv]

O CSV tem de ter as colunas: jogador_id, pergunta_id, correta (1 ou 0).
Colunas extra (tempo_ms, data) são ignoradas.

Para cada pergunta calcula:
- n e taxa de acerto;
- dificuldade real de 1 a 5 (pela taxa de acerto);
- rating ao estilo Elo (modelo de Rasch: 1500 = dificuldade média do banco);
- discriminação: correlação entre acertar esta pergunta e o desempenho do jogador no
  resto. Negativa = os melhores jogadores erram mais do que os piores, o sinal típico
  de chave errada ou de ambiguidade. Abaixo de 0,05 = a pergunta não separa quem sabe
  de quem não sabe.

Testado com scripts/simular_respostas.py: assinala a pergunta com a chave errada e a
demasiado fácil, e o rating estimado acompanha a dificuldade simulada (correlação
de 0,98 nesse teste).

Não precisa de pacotes externos.
"""

import argparse
import csv
import json
import math
import sys
from datetime import date
from pathlib import Path

ESCALA_ELO = 400 / math.log(10)  # converte logits em pontos Elo


def ler_respostas(caminho: Path):
    respostas = {}  # (jogador, pergunta) -> 0/1, só a primeira resposta conta
    with caminho.open(encoding="utf-8", newline="") as f:
        leitor = csv.DictReader(f)
        falta = {"jogador_id", "pergunta_id", "correta"} - set(leitor.fieldnames or [])
        if falta:
            sys.exit(f"ERRO: faltam colunas no CSV: {', '.join(sorted(falta))}")
        for linha in leitor:
            chave = (linha["jogador_id"].strip(), linha["pergunta_id"].strip())
            if chave in respostas:
                continue
            valor = linha["correta"].strip().lower()
            if valor not in {"0", "1", "true", "false"}:
                continue
            respostas[chave] = 1 if valor in {"1", "true"} else 0
    return respostas


def rasch(respostas, iteracoes=40):
    """Estimativa conjunta simples (Newton) de capacidade dos jogadores e dificuldade
    das perguntas. Valores limitados a [-4, 4] logits."""
    jogadores = {j for j, _ in respostas}
    perguntas = {q for _, q in respostas}
    theta = dict.fromkeys(jogadores, 0.0)
    b = dict.fromkeys(perguntas, 0.0)
    por_jogador, por_pergunta = {}, {}
    for (j, q), x in respostas.items():
        por_jogador.setdefault(j, []).append((q, x))
        por_pergunta.setdefault(q, []).append((j, x))

    def p(t, d):
        return 1 / (1 + math.exp(-(t - d)))

    for _ in range(iteracoes):
        for j, itens in por_jogador.items():
            grad = sum(x - p(theta[j], b[q]) for q, x in itens)
            info = sum(p(theta[j], b[q]) * (1 - p(theta[j], b[q])) for q, _ in itens) or 1e-6
            theta[j] = max(-4, min(4, theta[j] + max(-1, min(1, grad / info))))
        for q, itens in por_pergunta.items():
            grad = sum(x - p(theta[j], b[q]) for j, x in itens)
            info = sum(p(theta[j], b[q]) * (1 - p(theta[j], b[q])) for j, _ in itens) or 1e-6
            b[q] = max(-4, min(4, b[q] - max(-1, min(1, grad / info))))
        media = sum(b.values()) / len(b)
        for q in b:
            b[q] -= media
    return b


def correlacao(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return None
    return sxy / math.sqrt(sxx * syy)


def dificuldade_real(taxa):
    if taxa >= 0.80:
        return 1
    if taxa >= 0.65:
        return 2
    if taxa >= 0.45:
        return 3
    if taxa >= 0.25:
        return 4
    return 5


def dificuldade_estimada(pergunta_id):
    ficheiro = Path("banco/perguntas") / f"{pergunta_id}.json"
    if not ficheiro.exists():
        return None
    try:
        return json.loads(ficheiro.read_text(encoding="utf-8")).get("dificuldade_estimada")
    except (json.JSONDecodeError, OSError):
        return None


def main():
    ap = argparse.ArgumentParser(description="Calibra as perguntas a partir das respostas.")
    ap.add_argument("csv", type=Path)
    ap.add_argument("--min-n", type=int, default=30, help="respostas mínimas para alertar (por defeito 30)")
    ap.add_argument("--saida", type=Path, default=None)
    args = ap.parse_args()

    if not args.csv.exists():
        sys.exit(f"ERRO: {args.csv} não existe")
    respostas = ler_respostas(args.csv)
    if not respostas:
        sys.exit("ERRO: nenhuma resposta válida no ficheiro")

    totais = {}
    for (j, _), x in respostas.items():
        acertos, n = totais.get(j, (0, 0))
        totais[j] = (acertos + x, n + 1)
    b = rasch(respostas)

    por_pergunta = {}
    for (j, q), x in respostas.items():
        por_pergunta.setdefault(q, []).append((j, x))

    linhas, alertas = [], []
    for q in sorted(por_pergunta):
        itens = por_pergunta[q]
        n = len(itens)
        taxa = sum(x for _, x in itens) / n
        xs, resto = [], []
        for j, x in itens:
            acertos, total = totais[j]
            if total >= 2:
                xs.append(x)
                resto.append((acertos - x) / (total - 1))
        disc = correlacao(xs, resto)
        real = dificuldade_real(taxa)
        estimada = dificuldade_estimada(q)
        alerta = ""
        if n >= args.min_n:
            if disc is not None and disc < 0:
                alerta = "SUSPEITA"
            elif taxa < 0.05:
                alerta = "QUASE NINGUÉM ACERTA"
            elif taxa > 0.98:
                alerta = "DEMASIADO FÁCIL"
            elif disc is not None and disc < 0.05:
                alerta = "DISCRIMINA POUCO"
        nota = "amostra pequena" if n < args.min_n else ""
        if estimada is not None and abs(estimada - real) >= 2:
            nota = (nota + "; " if nota else "") + f"estimada {estimada} vs real {real}"
        linha = {
            "pergunta_id": q,
            "n": n,
            "acerto": f"{taxa:.3f}",
            "dificuldade_real": real,
            "dificuldade_estimada": "" if estimada is None else estimada,
            "rating": round(1500 + ESCALA_ELO * b[q]),
            "discriminacao": "" if disc is None else f"{disc:.3f}",
            "alerta": alerta,
            "nota": nota,
        }
        linhas.append(linha)
        if alerta:
            alertas.append(linha)

    saida = args.saida or Path("relatorios") / f"calibracao-{date.today().isoformat()}.csv"
    saida.parent.mkdir(parents=True, exist_ok=True)
    with saida.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        escritor.writeheader()
        escritor.writerows(linhas)

    print(f"{len(respostas)} respostas, {len(totais)} jogadores, {len(linhas)} perguntas.")
    print(f"Resultado gravado em {saida}")
    if not alertas:
        print("Sem alertas.")
        return
    print(f"\n{len(alertas)} alerta(s):")
    ordem = {"SUSPEITA": 0, "QUASE NINGUÉM ACERTA": 1, "DEMASIADO FÁCIL": 2, "DISCRIMINA POUCO": 3}
    for l in sorted(alertas, key=lambda l: (ordem.get(l["alerta"], 9), l["pergunta_id"])):
        print(f"  {l['alerta']:<22} {l['pergunta_id']}  n={l['n']}  acerto={l['acerto']}  "
              f"discriminação={l['discriminacao'] or 'n/d'}")


if __name__ == "__main__":
    main()
