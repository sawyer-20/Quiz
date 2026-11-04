# Motor de factos — app de quiz

Este projeto produz perguntas de cultura geral verificadas para a app de quiz.
O CEO é o Andre: decide e dá o gosto editorial. Tu orquestras os agentes, escreves os
ficheiros e nunca tomas decisões de produto sozinho.

## Regras invioláveis

1. Nenhum facto vem da memória do modelo. Todos vêm de fontes abertas e lidas nesta
   sessão (WebSearch e WebFetch), segundo `regras/fontes.md`.
2. Cada pergunta passa, por esta ordem, por: `pesquisador` → `verificador-cego` →
   `advogado-do-diabo` → `editor` → `python3 scripts/validar.py`. Nenhum passo se salta.
3. O `verificador-cego` e o `auditor` nunca recebem a resposta, as fontes nem o ficheiro
   da pergunta. Recebem só o enunciado, as opções baralhadas e os domínios a evitar.
4. Qualquer mudança factual feita depois do verificador (pelo editor, pela triagem ou
   por correção) volta ao `verificador-cego`.
5. Na dúvida, rejeita. Uma pergunta rejeitada com motivo vale mais do que uma pergunta
   errada publicada.
6. Português europeu (pt-PT) em tudo: perguntas, explicações e relatórios.
7. Nunca copiar perguntas de concursos (Joker, Dr. Why, Trivial Pursuit, Quem Quer Ser
   Milionário), de outras apps ou de sites de quiz.
8. Nada ligado ao retalho alimentar (temas, marcas, patrocínios).
9. Os agentes não leem nem escrevem ficheiros (é isso que protege a verificação às
   cegas): devolvem JSON. Só tu escreves em `banco/` e em `relatorios/`. Por isso, em
   cada invocação de um agente que pesquisa, inclui no pedido o texto completo de
   `regras/fontes.md`.

## Onde estão as coisas

- `banco/perguntas/<id>.json` — uma pergunta por ficheiro, no formato de
  `esquema/pergunta.schema.json`. As rejeitadas ficam também, com `estado: rejeitada`
  e motivo: são dados para melhorar o motor.
- `banco/respostas/` — exportações de respostas dos jogadores (CSV) para o calibrador.
- `banco/reportes.csv` — reportes de erro dos jogadores (`pergunta_id,data,jogador_id,texto`).
- `relatorios/` — relatórios de lote, auditoria e manutenção.
- `regras/fontes.md` — hierarquia de fontes.
- `scripts/validar.py` — validação automática, obrigatória antes de aprovar.
  `python3 scripts/validar.py --dominio <url>` devolve o domínio a registar numa fonte.
- `scripts/calibrar.py` — dificuldade real e perguntas suspeitas a partir das respostas.
- `scripts/simular_respostas.py` — gera respostas fictícias para testar o calibrador.

## Comandos

- `/produzir-lote` — perguntas novas pela linha completa.
- `/auditar` — auditoria às cegas de uma amostra aleatória.
- `/manutencao` — sentinela (prazos), triagem de reportes e calibração.

## Estados

`rascunho` → `em_verificacao` → `aprovada` → `publicada`, e ainda `suspensa`,
`retirada` e `rejeitada`. Só passa a `publicada` com ordem expressa do Andre e sem travão
ativo. Cada mudança de estado acrescenta um evento a `historico` (data, evento, agente,
nota).

## Identificadores

`Q-AAAA-NNNNNN` (ex.: `Q-2026-000004`), sequencial. Antes de criar, procura o maior
número existente em `banco/perguntas/` e em `exemplos/`.

## Travões

- Auditoria com erro confirmado acima de 1%: nenhuma pergunta passa a `publicada` até
  haver causa identificada e aprovação do Andre. O relatório da auditoria leva a linha
  `TRAVÃO ATIVO`; o fim do travão leva a linha `TRAVÃO LEVANTADO` num relatório posterior.
- Mais de 30% de discordâncias do verificador num lote: o lote para e o relatório explica.
- 3 reportes independentes na mesma pergunta: `suspensa` até à triagem.

## Relatórios

Curtos, em pt-PT, para ler em 2 minutos: números primeiro, depois os problemas e as
decisões que o Andre tem de tomar. Nunca mais de uma página.
