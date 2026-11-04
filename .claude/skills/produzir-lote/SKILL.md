---
name: produzir-lote
description: Produz um lote de perguntas verificadas pela linha completa - pesquisador, verificador às cegas, advogado do diabo, editor e validação automática. Usar quando o Andre pedir perguntas novas, por exemplo "/produzir-lote tema=historia n=10".
---

# Produzir um lote de perguntas

Argumentos (todos opcionais): `tema` (um dos temas do esquema; por defeito, misto),
`subtema`, `n` (por defeito 10) e `mistura` de dificuldade (por defeito 30% fáceis 1–2,
40% médias 3, 30% difíceis 4–5).

Lê primeiro `CLAUDE.md` e `regras/fontes.md`. Os agentes não leem ficheiros: em cada
invocação, inclui no pedido o texto completo de `regras/fontes.md`. Segue os passos por
ordem.

## 0. Preparar

1. Procura em `relatorios/` o relatório de auditoria mais recente. Se tiver
   `TRAVÃO ATIVO` sem um `TRAVÃO LEVANTADO` posterior, avisa o Andre: o lote pode
   produzir perguntas aprovadas, mas nenhuma será publicada.
2. Lista os enunciados existentes (`banco/perguntas/*.json` e `exemplos/*.json`) para
   evitar repetições, e o maior número de id em uso.
3. Define o nome do lote: `lote-AAAA-MM-DD-<tema>` (acrescenta `-2`, `-3` se já existir).
4. Planeia os `n` alvos: tema, subtema e dificuldade de cada um, variados.

## 1. Pesquisador

Para cada alvo, invoca o agente `pesquisador` (até 3 em paralelo) com tema, subtema,
dificuldade e a lista de enunciados existentes.

- Se devolver `rejeitar`, regista o alvo como rejeitado (motivo `sem fonte`) no relatório
  e passa ao seguinte. Não crias ficheiro para alvos que nunca tiveram pergunta.
- Caso contrário, monta o ficheiro da pergunta:
  - `opcoes` = resposta + 3 distratores, **baralhadas** (usa
    `python3 -c "import random; …"`); `correta` = índice da resposta;
  - cada fonte com `papel: "pesquisador"`, `consultada_em` = hoje e `dominio` dado por
    `python3 scripts/validar.py --dominio <url>`;
  - `estado: "em_verificacao"`, `verificacao` com os três campos a `null`,
    `motivo_rejeicao: null`, `lote`, `criada_em` = hoje, `lingua: "pt-PT"`,
    `formato: "escolha-multipla"`;
  - `historico`: `{"data": hoje, "evento": "criada", "agente": "pesquisador", "nota": riscos}`.
  - Grava em `banco/perguntas/<id>.json`.

## 2. Verificador às cegas

Invoca o agente `verificador-cego` com **apenas**: o enunciado, as opções numa **nova**
ordem aleatória e os domínios das fontes do pesquisador como domínios proibidos. Nunca
lhe passes a resposta, as fontes, a explicação ou o caminho do ficheiro.

Rejeita a pergunta (`estado: "rejeitada"` e `motivo_rejeicao`) se:
- a resposta dele for diferente da resposta da pergunta (`discorda`);
- a confiança for `baixa` ou a resposta vier `null` (`sem confirmação`);
- a fonte dele for de um domínio do pesquisador (`fonte não independente`);
- indicar uma ambiguidade que torne outra opção defensável (`ambígua`).

Se passar: acrescenta a fonte dele a `fontes` com `papel: "verificador"`, preenche
`verificacao.verificador` (`resposta_texto`, `concorda: true`, `confianca`, `dominio`,
`data`, `notas`) e um evento no histórico.

**Travão do lote:** se, depois de pelo menos 5 perguntas verificadas, mais de 30% tiverem
sido rejeitadas por `discorda`, para o lote, grava o relatório e explica ao Andre.

## 3. Advogado do diabo

Invoca o agente `advogado-do-diabo` com o rascunho completo (incluindo a resposta e as
fontes do pesquisador e do verificador).

- `aprovado: true`: preenche `verificacao.advogado` e segue.
- Algum problema `bloqueia`: rejeita com o motivo.
- Só problemas `corrigivel` com `reformulacao_sugerida`: aplica a reformulação e volta
  ao passo 2 (nova verificação às cegas). Só há **um** ciclo de correção por pergunta;
  à segunda, rejeita.
- Fontes que o advogado use para justificar problemas podem ser guardadas com
  `papel: "advogado"`.

## 4. Editor

Invoca o agente `editor` com a pergunta aprovada pelo advogado.

- `originalidade_ok: false` ou `aprovado: false`: rejeita (`copiada` ou o motivo dado).
- `alteracao_factual: true`: aplica, marca e volta ao passo 2.
- Caso contrário: aplica enunciado, opções (mesma ordem), explicação, dificuldade e
  subtema; preenche `verificacao.editor`.

## 5. Validação automática

Corre `python3 scripts/validar.py banco/perguntas/<id>.json`.

- Com erros: corrige só o que for de formato (nunca factos) e volta a correr; se o
  erro for de conteúdo (fontes insuficientes, domínios repetidos), rejeita.
- Sem erros: `estado: "aprovada"` e evento no histórico.

## 6. Relatório

Grava `relatorios/<nome do lote>.md` (uma página):

- números: alvos, perguntas criadas, aprovadas, rejeitadas por etapa e por motivo, e
  tempo total;
- problemas que se repetem (por exemplo, o pesquisador a usar sempre a mesma fonte);
- **5 perguntas aprovadas ao acaso para o gosto do Andre**: enunciado, opções com a
  certa assinalada, explicação e fontes; pede-lhe um veredicto por pergunta
  ("incrível", "boa", "fraca").

Mostra ao Andre o resumo e as 5 perguntas na conversa. Não publiques nada sem ordem dele.
