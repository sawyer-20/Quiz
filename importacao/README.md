# Pacote importado (Semana 1)

Perguntas de fontes abertas, **separadas do banco verificado** (`banco/`). Não passam pelo
circuito de 29 regras do motor: entram por tradução automática, revisão automática e
auditoria cega por amostra (plano, secção 4). As 57 perguntas do banco continuam a ser o
pacote premium do Daily 10; as importadas nunca entram no Daily 10 (`daily: false`).

## Licenças e origem (por pergunta)

- `otdb-…`: Open Trivia DB (https://opentdb.com), **CC BY-SA 4.0**. O en-US é o texto
  original com gralhas corrigidas; o pt-PT é tradução automática revista. Ambos são obras
  derivadas e ficam sob CC BY-SA 4.0. Atribuição na app (ecrã inicial e «Fontes:
  opentdb.com» em cada pergunta).
- `wd-…`: gerado a partir do Wikidata (https://www.wikidata.org), **CC0 1.0**. A fonte de
  cada pergunta é a página da entidade.

Cada pergunta em `pacote.json` tem `licenca` e `origem`. Antes de qualquer lançamento
público com anúncios: parecer jurídico sobre o ShareAlike (plano, secção 4).

## Ficheiros

| Ficheiro | O que é |
|---|---|
| `opentdb/bruto.json` | Descarga completa das 5.299 perguntas verificadas (25/11/2026) |
| `opentdb/prefiltro.json` | Contagens do pré-filtro mecânico |
| `opentdb/lotes/entrada-NN.jsonl`, `saida-NN.jsonl` | Triagem e tradução (1.ª passagem) |
| `wikidata/geradas.json` | Saída do gerador Wikidata |
| `revisao/entrada-*.jsonl`, `saida-*.jsonl` | Revisão (2.ª passagem e 3.º ciclo de Ciência) |
| `auditoria/amostra-*.json`, `resultado-*.json`, `chave-*.json`, `pontuacao-r*.json` | Auditorias cegas |
| `auditoria/rejeitadas.json` | Perguntas tiradas por qualquer auditoria |
| `pacote.json` | Pacote final, com licença e origem por pergunta |
| `../app/assets/importadas.json` | O mesmo pacote no formato da app |
| `instrucoes-*.md` | Instruções dadas a cada passo automático |

## Refazer

```
python3 scripts/importar_opentdb.py        # ~15 min (1 pedido / 5,5 s)
python3 scripts/preparar_traducao.py 200
# triagem e tradução: um agente por ficheiro, segundo instrucoes-triagem-traducao.md
python3 scripts/gerar_wikidata.py
python3 scripts/montar_pacote.py
# revisão segundo instrucoes-revisao.md; auditoria segundo instrucoes-auditoria.md
python3 scripts/pontuar_auditoria.py importacao/auditoria/chave-r1.json 1
```
