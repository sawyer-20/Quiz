---
name: manutencao
description: Manutenção semanal do banco - sentinela das perguntas com prazo, triagem dos reportes dos jogadores e calibração com as respostas reais. Usar uma vez por semana, por exemplo "/manutencao".
---

# Manutenção semanal

Lê `CLAUDE.md` e `regras/fontes.md` antes de começar. Os agentes não leem ficheiros: em
cada invocação da sentinela e da triagem, inclui no pedido o texto completo de
`regras/fontes.md`. Os três blocos são independentes: se um não tiver dados, salta-o e
diz isso no relatório.

## 1. Sentinela

1. Seleciona as perguntas `aprovada` ou `publicada` com `sensivel_ao_tempo: true` e
   `valida_ate` nos próximos 30 dias ou já passada.
2. Para cada uma, invoca o agente `sentinela` com a pergunta completa.
3. Aplica: `manter` → atualiza `valida_ate`; `reformular` → aplica a reformulação da
   sentinela, passa a pergunta a `em_verificacao` e leva-a de novo pelo
   `verificador-cego`, pelo `advogado-do-diabo` e pelo `editor`; só o
   `scripts/aprovar.py` a volta a aprovar; `retirar` → `estado: "retirada"`. Evento no
   histórico em todos os casos.

## 2. Triagem de reportes

1. Lê `banco/reportes.csv` (`pergunta_id,data,jogador_id,texto`), só as linhas que ainda
   não constam de um relatório de manutenção anterior.
2. Agrupa por pergunta. Com 3 ou mais reportes de jogadores diferentes, passa logo a
   pergunta a `suspensa`.
3. Para cada pergunta reportada, invoca o agente `triagem` com a pergunta completa e os
   textos dos reportes. Aplica a ação e regista a causa raiz.

## 3. Calibração

Se houver ficheiros em `banco/respostas/`, invoca o agente `calibrador` com o mais
recente. Aplica as ações propostas: suspender e mandar à triagem as `SUSPEITA`, corrigir
`dificuldade_estimada` quando a diferença para a real for de 2 ou mais.

## 4. Relatório

Grava `relatorios/manutencao-AAAA-MM-DD.md` (uma página): perguntas revistas pela
sentinela e o que mudou, reportes tratados com veredicto e causa raiz, alertas da
calibração e ações, e padrões a corrigir no motor. Mostra o resumo ao Andre.
