---
name: produzir-lote
description: Produz um lote de perguntas verificadas pela linha completa - pesquisador, originalidade, verificador às cegas, advogado do diabo, editor e scripts/aprovar.py, com canários. Usar quando o Andre pedir perguntas novas, por exemplo "/produzir-lote tema=historia n=10".
---

# Produzir um lote de perguntas (motor v1.1)

Argumentos (todos opcionais): `tema` (um dos temas do esquema; por defeito, misto),
`subtema`, `n` (por defeito 10) e `mistura` de dificuldade (por defeito 30% fáceis 1–2,
40% médias 3, 30% difíceis 4–5).

Lê primeiro `CLAUDE.md` e `regras/fontes.md`. Os agentes não leem ficheiros: em cada
invocação de um agente que pesquisa, inclui no pedido o texto completo de
`regras/fontes.md`.

**Linha:** pesquisador → originalidade → verificador às cegas → advogado do diabo →
editor → `scripts/aprovar.py`. Nenhum passo se salta.

**Regras do orquestrador (tu):**
- Nunca escreves texto factual (enunciados, opções, explicações, fontes). Só copias para
  os ficheiros o que os agentes devolvem, baralhas opções e mudas estados.
- Só o `scripts/aprovar.py` aprova. Nunca escreves `estado: "aprovada"` à mão.
- Se uma etapa for interrompida (limite de utilização, erro), a pergunta fica em
  `em_verificacao` e retoma-se essa etapa; nunca se dá a etapa por feita.
- Regista cada invocação de agente em `relatorios/<lote>-tempos.csv`
  (`agente,refs,duracao_ms`, com a duração que a notificação do agente indica).
- Se os agentes do motor não estiverem registados na sessão, lança-os como
  `general-purpose` com o texto integral do ficheiro do agente e cria
  `.claude/hooks/LOTE_ATIVO` durante o lote (o travão passa a proteger também os agentes
  genéricos). Apaga o ficheiro no fim.

## 0. Preparar

1. Procura em `relatorios/` o relatório de auditoria mais recente. Se tiver
   `TRAVÃO ATIVO` sem um `TRAVÃO LEVANTADO` posterior, avisa o Andre: o lote pode
   produzir perguntas aprovadas, mas nenhuma será publicada.
2. Lista os enunciados existentes (`banco/perguntas/*.json` e `exemplos/*.json`) para
   evitar repetições, e o maior número de id em uso.
3. Define o nome do lote: `lote-AAAA-MM-DD-<tema>` (acrescenta `-2`, `-3` se já existir).
4. Planeia os `n` alvos: tema, subtema e dificuldade de cada um, variados. Planeia
   também **2 alvos extra para canários** (ver passo 1).
5. Cria já `relatorios/<lote>.md` com uma secção `## Canários` vazia.

## 1. Pesquisador

Invoca o agente `pesquisador` (até 3 em paralelo) com tema, subtema, dificuldade,
quantas perguntas queres (1 a 3: pode tirar até 3 factos da mesma página) e a lista de
enunciados existentes.

- Se devolver `rejeitar`, regista o alvo como rejeitado (motivo `sem fonte`) no relatório.
  Não crias ficheiro para alvos que nunca tiveram pergunta.
- **Canários.** Das perguntas dos 2 alvos extra, escolhe 2 ao acaso para canários. Em
  cada uma, marca como "certa" um dos distratores (escolhido ao acaso com Python): fica
  uma pergunta com a resposta errada de propósito. Os canários **nunca** entram em
  `banco/`: guardas o enunciado, as opções, a resposta errada marcada e a verdadeira só
  na secção `## Canários` do relatório.
- Para as outras perguntas, monta o ficheiro:
  - `opcoes` = resposta + 3 distratores, **baralhadas** (`python3 -c "import random; …"`);
    `correta` = índice da resposta;
  - cada fonte com `papel: "pesquisador"`, `consultada_em` = hoje e `dominio` dado por
    `python3 scripts/validar.py --dominio <url>`;
  - `estado: "em_verificacao"`, `verificacao` com os três campos a `null`,
    `motivo_rejeicao: null`, `lote`, `criada_em` = hoje, `lingua: "pt-PT"`,
    `formato: "escolha-multipla"`, `etiquetas: []`;
  - `historico`: `{"data": hoje, "evento": "criada", "agente": "pesquisador", "nota": riscos}`.
  - Grava em `banco/perguntas/<id>.json`.

## 2. Originalidade

Invoca o agente `originalidade` com blocos de até 5 perguntas (`ref`, enunciado e
opções; sem indicar a certa). Os canários não passam por aqui.

- `copiada`: rejeita com motivo `copiada` e o alvo volta ao passo 1 (novo pedido ao
  pesquisador, com outro facto ou outro texto).
- `classico`: acrescenta `"classico"` a `etiquetas`. Se a dificuldade for 4 ou 5, ou se
  o lote já tiver 20% de clássicos entre as perguntas não rejeitadas, rejeita com motivo
  `classico fora da quota` e o alvo volta ao passo 1.
- `original`: segue.
- `completa: false` (pesquisas interrompidas): a pergunta fica em `em_verificacao` e o
  passo repete-se para ela antes de avançar.

Evento no histórico em todos os casos, com as provas e as pesquisas.

## 3. Verificador às cegas

Invoca o agente `verificador-cego` com blocos de até 5 perguntas, misturando os 2
canários com as perguntas reais por ordem aleatória. Para cada uma passas **apenas**:
`ref`, o enunciado, as opções numa **nova** ordem aleatória e os domínios das fontes do
pesquisador como domínios proibidos. Nunca passas a resposta, as fontes, a explicação, o
caminho do ficheiro nem a indicação de que há canários.

**Canários.** Se o verificador escolher num canário a resposta errada marcada, o canário
**passou**: para o lote de imediato, regista-o no relatório e explica ao Andre (o
verificador está a ver respostas ou a adivinhar). Se o verificador der a resposta
verdadeira, ou nenhuma, o canário foi rejeitado como devia: anota no relatório.

Para as perguntas reais, rejeita (`estado: "rejeitada"` e `motivo_rejeicao`) se:
- a resposta dele for diferente da resposta da pergunta (`discorda`);
- a confiança for `baixa` ou a resposta vier `null` (`sem confirmação`);
- a fonte dele for de um domínio do pesquisador (`fonte não independente`);
- indicar uma ambiguidade que torne outra opção defensável (`ambígua`);
- disser que as fontes não confirmam algo que o enunciado afirma (`sem confirmação`).

Se passar: acrescenta a fonte dele a `fontes` com `papel: "verificador"`, preenche
`verificacao.verificador` (`resposta_texto`, `concorda: true`, `confianca`, `dominio`,
`data`, `notas`) e um evento no histórico.

**Travão do lote:** se, depois de pelo menos 5 perguntas verificadas, mais de 30% tiverem
sido rejeitadas por `discorda`, para o lote, grava o relatório e explica ao Andre.

## 4. Advogado do diabo

Invoca o agente `advogado-do-diabo` com blocos de até 5 rascunhos completos (incluindo a
resposta e as fontes do pesquisador e do verificador).

- `aprovado: true`: preenche `verificacao.advogado` e segue.
- Algum problema `bloqueia`: rejeita com o motivo.
- Só problemas `corrigivel` com `reformulacao_sugerida`: aplica **exatamente** a
  reformulação do advogado (não escreves texto teu) e volta ao passo 3 (nova verificação
  às cegas) e depois a este passo. Só há **um** ciclo de correção por pergunta; à
  segunda, rejeita.
- `fontes_substitutas`: substitui a fonte da Wikipédia pela original indicada.
- Fontes que o advogado use para justificar problemas podem ser guardadas com
  `papel: "advogado"`.

## 5. Editor

Invoca o agente `editor` com blocos de até 5 perguntas aprovadas pelo advogado.

- `aprovado: false` com `motivo: "reescrever"` (ou qualquer outro): rejeita com esse
  motivo; o alvo volta ao passo 1.
- Caso contrário: aplica enunciado, explicação, dificuldade e subtema. As **opções e a
  ordem ficam como estão** (o editor não lhes mexe). Preenche `verificacao.editor` com
  `alteracao_factual: false` e `originalidade_ok: true` (a originalidade foi decidida no
  passo 2).
- Se o novo enunciado mudar o que se pergunta (compara-o com o anterior), não o aplicas:
  rejeita com motivo `reescrever`.

## 6. Aprovação

Corre `python3 scripts/aprovar.py <id>` para cada pergunta que chegou aqui. O script
corre o `validar.py` e só aprova se passar; se falhar, mostra os erros e a pergunta fica
em `em_verificacao`.

- Erro de formato (ex.: subtema com mais de 60 caracteres): pede a correção ao agente
  da etapa respetiva (editor para estilo e subtema) e volta a correr o `aprovar.py`.
- Erro de conteúdo (fontes insuficientes, domínios repetidos, linguagem de dúvida,
  quota de clássicos): rejeita.

## 7. Relatório

Corre `python3 scripts/estatisticas_lote.py <lote>` e grava `relatorios/<lote>.md` (uma
página):

- números: alvos, perguntas criadas, aprovadas, rejeitadas por etapa e por motivo,
  clássicos, **percentagem de perguntas com fonte de nível 1 do pesquisador** e
  **tempo de agentes por pergunta aprovada (sem pausas)**;
- **canários**: as 2 perguntas, a resposta errada marcada, a verdadeira e o que o
  verificador respondeu;
- problemas que se repetem (por exemplo, o pesquisador a usar sempre a mesma fonte);
- **5 perguntas aprovadas ao acaso para o gosto do Andre**: enunciado, opções com a
  certa assinalada, explicação e fontes; pede-lhe um veredicto por pergunta
  ("incrível", "boa", "fraca").

Mostra ao Andre o resumo e as 5 perguntas na conversa. Não publiques nada sem ordem dele.
