---
name: produzir-lote
description: Produz um lote de perguntas bilingues (pt-PT e en-US) verificadas pela linha completa - pesquisador, originalidade, verificador às cegas, advogado do diabo, editor, tradutor, conferente e scripts/aprovar.py, com canários. Usar quando o Andre pedir perguntas novas, por exemplo "/produzir-lote topic=Science n=10".
---

# Produzir um lote de perguntas (motor v2: pt-PT e en-US)

Argumentos (todos opcionais): `topic` (um dos 10 tópicos do esquema; por defeito, misto),
`subtopic`, `markets`, `n` (por defeito 10) e `mistura` de dificuldade (por defeito 30% fáceis 1–2,
40% médias 3, 30% difíceis 4–5).

Lê primeiro `CLAUDE.md`, `regras/fontes.md` e `relatorios/alvos-a-retomar.md`. Os agentes
não leem ficheiros: em cada invocação de um agente que pesquisa, inclui no pedido o texto
completo de `regras/fontes.md` (inclui as fontes de nível 1 por tópico) e, nos alvos de
interesse português (`markets: ["pt"]`), também o de `regras/fontes-pt.md` (o pesquisador
começa por essas fontes).

**Linha:** pesquisador → originalidade → verificador às cegas → advogado do diabo →
editor → tradutor → conferente → `scripts/aprovar.py`. Nenhum passo se salta. O facto
verifica-se uma vez (no pt-PT); o texto escreve-se duas (o tradutor escreve o en-US).

**Regras do orquestrador (tu):**
- Nunca escreves texto factual (perguntas, opções, explicações, fontes). Só copias para
  os ficheiros o que os agentes devolvem, baralhas opções e mudas estados. Usa
  `scripts/montar_pergunta.py` (cria o ficheiro v2 e imprime a entrada às cegas) e
  `scripts/aplicar_passo.py` (aplica o resultado de cada agente) em vez de escrever JSON à mão.
- Só o `scripts/aprovar.py` aprova. Nunca escreves `estado: "aprovada"` à mão.
- Se uma etapa for interrompida (limite de utilização, erro), a pergunta fica em
  `em_verificacao` e retoma-se essa etapa; nunca se dá a etapa por feita.
- Regista **todas** as invocações de agente, incluindo as de correção (pesquisador a
  corrigir, segundas passagens do advogado, verificações repetidas), com
  `python3 scripts/registar_tempo.py <lote> <agente> <refs> <duracao_ms>` (a duração que a
  notificação do agente indica). Antes do relatório, confirma que há uma linha por
  notificação de agente recebida.
- Regista o tempo de relógio: no passo 0 escreve `relatorios/<lote>-relogio.txt` com
  `inicio=<hora UTC ISO 8601>` e, ao gravar o relatório, acrescenta `fim=<…>`.
- Se os agentes do motor não estiverem registados na sessão, lança-os como
  `general-purpose` com o texto integral do ficheiro do agente e cria
  `.claude/hooks/LOTE_ATIVO` durante o lote (o travão passa a proteger também os agentes
  genéricos). Apaga o ficheiro no fim.

## 0. Preparar

1. Procura em `relatorios/` o relatório de auditoria mais recente. Se tiver
   `TRAVÃO ATIVO` sem um `TRAVÃO LEVANTADO` posterior, avisa o Andre: o lote pode
   produzir perguntas aprovadas, mas nenhuma será publicada.
2. Lista as perguntas existentes (`banco/perguntas/*.json`, campo `text`) para evitar
   repetições, e o maior número de id em uso.
3. Define o nome do lote: `lote-AAAA-MM-DD-<tema>` (acrescenta `-2`, `-3` se já existir).
4. Planeia os `n` alvos: tópico, subtópico, mercado e dificuldade de cada um, variados.
   **Sensibilidade (regra 21):** descarta os alvos ligados a tragédias com menos de 10 anos. Entram primeiro
   os **alvos a retomar** de `relatorios/alvos-a-retomar.md` (com o ângulo novo e as notas
   do advogado; cada um só uma vez) e os alvos fixados pelo Andre. **Pelo menos 8 em cada
   10 alvos têm ângulo não clássico** (regra 16); escreve no plano qual é o ângulo.
   Planeia também **2 alvos extra para canários** (ver passo 1).
5. Cria já `relatorios/<lote>.md` com uma secção `## Canários` vazia.

## 1. Pesquisador

Invoca o agente `pesquisador` (até 3 em paralelo) com tópico, subtópico, mercado, dificuldade,
quantas perguntas queres (1 a 3: pode tirar até 3 factos da mesma página) e a lista de
enunciados existentes.

- Se devolver `rejeitar`, regista o alvo como rejeitado (motivo `sem fonte`) no relatório.
  Não crias ficheiro para alvos que nunca tiveram pergunta.
- **Canários.** Das perguntas dos 2 alvos extra, escolhe 2 ao acaso para canários. Em
  cada uma, marca como "certa" um dos distratores (escolhido ao acaso com Python): fica
  uma pergunta com a resposta errada de propósito. Os canários **nunca** entram em
  `banco/`: guardas o enunciado, as opções, a resposta errada marcada e a verdadeira só
  na secção `## Canários` do relatório.
- Para as outras perguntas, corre `python3 scripts/montar_pergunta.py <pesquisador.json> <indice>
  <id> <lote>`: cria `banco/perguntas/<id>.json` (esquema v2: `text.pt-PT`, `correct`, opções
  **baralhadas**, `sources`, `daily_eligible`, `estado: em_verificacao`, histórico) e
  imprime a entrada às cegas para o verificador.

## 2. Originalidade

Invoca o agente `originalidade` com blocos de até 5 perguntas (`ref`, enunciado e
opções; sem indicar a certa). Os canários não passam por aqui.

- `copiada` (formulação distintiva igual ou traduzida de outro quiz, ou o mesmo
  conjunto de opções): rejeita com motivo `copiada` e o alvo volta ao passo 1 (novo
  pedido ao pesquisador, com outro facto ou outro texto).
- `classico` (a forma natural de perguntar um facto conhecido, com opções nossas):
  acrescenta `"classico"` a `etiquetas`. Se a dificuldade for 4 ou 5, rejeita com motivo
  `classico com dificuldade alta` e o alvo volta ao passo 1. A percentagem de clássicos
  no lote é um indicador do pesquisador (meta: até 20%), não um bloqueio; a quota de 20%
  conta sobre o banco e o `aprovar.py` aplica-a a partir de 100 perguntas.
  **Regra 16:** quando o lote já tem 2 clássicos, um clássico novo é trocado por outro
  alvo (novo pedido ao pesquisador, com ângulo não clássico) já aqui, antes da
  verificação; o rejeitado fica com motivo `quota de clássicos do lote`.
- `original`: segue.
- `completa: false` (pesquisas interrompidas): a pergunta fica em `em_verificacao` e o
  passo repete-se para ela antes de avançar.

Evento no histórico em todos os casos, com as provas e as pesquisas.

## 3. Verificador às cegas

Invoca o agente `verificador-cego` com blocos de até 5 perguntas, misturando os 2
canários com as perguntas reais por ordem aleatória. Para cada uma passas **apenas**:
`ref`, o enunciado, as opções numa **nova** ordem aleatória, os domínios das fontes do
pesquisador como domínios proibidos e os **títulos** dessas fontes (o verificador não pode
usar uma republicação do mesmo artigo noutro domínio: regra 20). Nunca passas a resposta, as fontes, a explicação, o
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
- Algum problema `bloqueia`: rejeita com o motivo. Se a pergunta não é clássica e esgotou
  o ciclo de correção, acrescenta-a a `relatorios/alvos-a-retomar.md` (regra 15), a menos
  que o alvo já seja um alvo retomado.
- Só problemas `corrigivel` com `reformulacao_sugerida`: aplica **exatamente** a
  reformulação do advogado (não escreves texto teu) e volta ao passo 3 (nova verificação
  às cegas) e depois a este passo. Só há **um** ciclo de correção por pergunta; à
  segunda, rejeita e, se não é clássica, regista-a em `relatorios/alvos-a-retomar.md`
  (regra 15; só uma retoma por alvo). (Uma pergunta reaberta por mudança de regra ou por auditoria tem
  direito a um ciclo novo.)
- `fontes_substitutas` ou outra correção só de fontes: aplica-a e volta a invocar o
  advogado sobre a versão corrigida (sem nova verificação às cegas se o texto não mudou).
  Nunca registas `aprovado: true` por ele: só o veredicto que ele der fica registado.
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

## 5b. Tradutor e conferente (en-US)

1. **Tradutor.** Invoca o agente `tradutor` com blocos de até 5 perguntas já editadas: `ref`,
   `topic`, `difficulty`, `markets`, o texto pt-PT (pergunta, 4 opções com a certa assinalada,
   explicação) e os excertos das fontes. Aplica com `scripts/aplicar_passo.py traducao`. Se
   devolver `traduzivel: false`, decide com o Andre (a pergunta pode precisar de outro facto).
2. **Conferente.** Invoca o agente `conferente` com blocos de até 5 perguntas: **só** os dois
   textos e o índice da certa; nunca fontes, ficha nem ficheiro. Aplica com
   `scripts/aplicar_passo.py conferencia`. Se não aprovar, os problemas voltam ao tradutor
   (um ciclo); se o problema for no pt-PT, a pergunta volta ao editor e ao conferente. Na
   dúvida, rejeita. Mudança ao pt-PT que altere o facto obriga a nova verificação (regra 4).
3. A explicação tem **1 a 2 frases** em cada idioma (o `validar.py` bloqueia a aprovação com
   mais); o editor encurta-a no pt-PT antes de a traduzires.

## 6. Aprovação

Corre `python3 scripts/aprovar.py <id>` para cada pergunta que chegou aqui (com en-US e
conferente aprovado). O script grava `options_lock`: depois disto o texto das opções é imutável. O script
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
  clássicos no lote (indicador: meta até 20%) **e no banco inteiro**
  (`estatisticas_lote.py` calcula ambos), tempo de relógio do lote, **percentagem de perguntas com fonte de
  nível 1 do pesquisador** e **tempo de agentes por pergunta aprovada (sem pausas)**;
- **fontes portuguesas de nível 1**: quais os agentes conseguiram abrir e quais recusaram
  (403, 429, erro de rede, PDF ilegível); pede a cada agente que as liste nas `notas`;
- **canários**: as 2 perguntas, a resposta errada marcada, a verdadeira e o que o
  verificador respondeu;
- problemas que se repetem (por exemplo, o pesquisador a usar sempre a mesma fonte);
- **5 perguntas aprovadas ao acaso para o gosto do Andre** (as 5 em pt-PT, com o en-US ao lado):
  pergunta, opções com a certa assinalada, explicação e fontes; pede-lhe um veredicto por pergunta
  ("incrível", "boa", "fraca").

Atualiza `relatorios/alvos-a-retomar.md` (retomados que passaram, retomados que falharam e
novos alvos a retomar). Mostra ao Andre o resumo e as 5 perguntas na conversa. Não publiques nada sem ordem dele.
