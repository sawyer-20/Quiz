---
name: auditar
description: Audita às cegas uma amostra aleatória de perguntas aprovadas ou publicadas, calcula a taxa de erro e ativa o travão se passar de 1%. Usar todas as semanas (n=30) e antes de cada lançamento (n=100), por exemplo "/auditar n=30".
---

# Auditoria do banco

Argumento: `n` (por defeito 30; 100 antes de lançar uma versão). Lê `CLAUDE.md` e
`regras/fontes.md` antes de começar. Os agentes não leem ficheiros: em cada invocação,
inclui no pedido o texto completo de `regras/fontes.md`.

## 1. Amostra

1. Lista as perguntas com `estado` `aprovada` ou `publicada` em `banco/perguntas/`.
2. Tira uma amostra aleatória de `n` (ou todas, se houver menos) com Python, usando como
   semente a data de hoje em `AAAAMMDD`, e regista a semente no relatório para a amostra
   poder ser repetida.

## 2. Verificação às cegas

Para cada pergunta, invoca o agente `auditor` com **apenas**: o enunciado, as opções numa
ordem aleatória nova e os domínios das fontes já registadas. Até 3 em paralelo.

Compara a resposta do auditor com a resposta do banco:
- igual e com confiança `alta` ou `media`, sem ambiguidade e `ainda_atual: true`: passa;
- tudo o resto (diferente, confiança `baixa`, ambiguidade ou `ainda_atual: false`): vai
  à triagem.

## 3. Triagem das discordâncias

Invoca o agente `triagem` com a pergunta completa e a resposta, fonte e notas do auditor.

- `pergunta_certa`: conta como certa (regista `erro_do_auditor` se for o caso).
- `pergunta_errada`, `ambigua` ou `desatualizada`: **erro confirmado**. Passa a pergunta a
  `suspensa` (ou `retirada`, se a triagem disser), com evento no histórico, e aplica a
  correção proposta só depois de nova passagem pelo `verificador-cego`.

## 4. Taxa de erro e travão

Taxa de erro = erros confirmados / perguntas auditadas.

- Acima de 1%: escreve `TRAVÃO ATIVO` no relatório. Nenhuma pergunta passa a `publicada`
  até haver causa identificada e aprovação do Andre. Com uma amostra de 30, um único erro
  já ativa o travão: é intencional.
- Para levantar o travão, num relatório posterior, escreve `TRAVÃO LEVANTADO`, a causa e
  a correção aplicada (por exemplo, regra nova para o pesquisador).

## 5. Relatório

Grava `relatorios/auditoria-AAAA-MM-DD.md` (uma página): n, semente, taxa de erro,
estado do travão, cada erro com a causa raiz e a ação, padrões (agente, fonte ou tema que
se repetem) e o que muda no motor. Mostra o resumo ao Andre.
