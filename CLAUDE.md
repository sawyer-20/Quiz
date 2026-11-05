# Motor de factos — app de quiz (versão 1.1)

Este projeto produz perguntas de cultura geral verificadas para a app de quiz.
O CEO é o Andre: decide e dá o gosto editorial. Tu orquestras os agentes, escreves os
ficheiros e nunca tomas decisões de produto sozinho.

## Regras invioláveis

1. Nenhum facto vem da memória do modelo. Todos vêm de fontes abertas e lidas nesta
   sessão (WebSearch e WebFetch), segundo `regras/fontes.md`.
2. Cada pergunta passa, por esta ordem, por: `pesquisador` → `originalidade` →
   `verificador-cego` → `advogado-do-diabo` → `editor` → `python3 scripts/aprovar.py`.
   Nenhum passo se salta. O verificador, o advogado e o editor recebem até 5 perguntas
   por invocação; o pesquisador pode tirar até 3 factos da mesma página.
3. O `verificador-cego` e o `auditor` nunca recebem a resposta, as fontes nem o ficheiro
   da pergunta. Recebem só o enunciado, as opções baralhadas e os domínios a evitar.
4. Qualquer mudança factual feita depois do verificador (pela triagem ou por correção)
   volta ao `verificador-cego`. O editor só mexe no estilo: não muda o que se pergunta
   nem as opções; se for preciso, a pergunta é rejeitada com motivo `reescrever` e o alvo
   volta ao pesquisador.
5. Na dúvida, rejeita. Uma pergunta rejeitada com motivo vale mais do que uma pergunta
   errada publicada.
6. Português europeu (pt-PT) em tudo: perguntas, explicações e relatórios.
7. Nunca copiar perguntas de concursos (Joker, Dr. Why, Trivial Pursuit, Quem Quer Ser
   Milionário), de outras apps ou de sites de quiz. A originalidade mede o **texto**,
   não o facto: um facto clássico pode entrar com enunciado próprio e leva a etiqueta
   `classico` (nunca em dificuldade 4 ou 5). Quota: no máximo 20% de clássicos entre as
   perguntas aprovadas e publicadas do **banco**, aplicada a partir de 100 perguntas;
   abaixo disso, só se mede. No lote, a percentagem de clássicos é um indicador do
   pesquisador (meta: até 20%), não um bloqueio. Originalidade interrompida (limite de
   utilização ou erro): a pergunta fica em `em_verificacao`.
8. Nada ligado ao retalho alimentar (temas, marcas, patrocínios).
9. Os agentes não leem nem escrevem ficheiros (é isso que protege a verificação às
   cegas): devolvem JSON. Só tu escreves em `banco/` e em `relatorios/`. Por isso, em
   cada invocação de um agente que pesquisa, inclui no pedido o texto completo de
   `regras/fontes.md`. Os agentes leem páginas só com `scripts/ler_url.py`; o hook
   `.claude/hooks/travao_agentes.py` recusa-lhes qualquer outro comando e os ficheiros.
10. **Tu nunca escreves texto factual** (enunciados, opções, explicações, fontes): as
    correções vêm sempre de um agente e tu só as aplicas tal como vieram.
11. **Só o `scripts/aprovar.py` aprova.** Corre o `validar.py` e, só se passar, muda o
    estado para `aprovada` e junta ao histórico o evento `aprovada por aprovar.py`. O
    `validar.py` recusa perguntas aprovadas sem esse evento.
12. **Canários.** Em cada lote, 2 perguntas com a resposta errada de propósito,
    guardadas só no relatório e nunca no banco, vão misturadas ao verificador às cegas.
    Se uma passar, o lote para.
13. **Nunca registas um veredicto que nenhum agente deu**, mesmo que o texto não mude.
    Se um agente devolveu `aprovado: false` e aplicaste a correção dele (incluindo trocar
    ou tirar uma fonte), a pergunta volta a esse agente, e só o veredicto que ele der fica
    registado em `verificacao`.
14. **Um ciclo de correção por pergunta, na produção.** Uma pergunta reaberta por mudança
    de regra ou por auditoria tem direito a um ciclo novo.

## Onde estão as coisas

- `banco/perguntas/<id>.json` — uma pergunta por ficheiro, no formato de
  `esquema/pergunta.schema.json`. As rejeitadas ficam também, com `estado: rejeitada`
  e motivo: são dados para melhorar o motor.
- `banco/respostas/` — exportações de respostas dos jogadores (CSV) para o calibrador.
- `banco/reportes.csv` — reportes de erro dos jogadores (`pergunta_id,data,jogador_id,texto`).
- `relatorios/` — relatórios de lote, auditoria e manutenção.
- `regras/fontes.md` — hierarquia de fontes.
- `scripts/validar.py` — validação automática.
  `python3 scripts/validar.py --dominio <url>` devolve o domínio a registar numa fonte.
- `scripts/aprovar.py` — a única forma de aprovar (corre o `validar.py`).
- `scripts/ler_url.py` — leitor de páginas dos agentes (só http/https públicos; lê HTML,
  texto e PDF); `scripts/testar_ler_url.py` testa as recusas e as leituras.
- `scripts/testar_validar.py` — testes das regras de texto do `validar.py`.
- `scripts/estatisticas_lote.py` — números do relatório de um lote.
- `scripts/calibrar.py` — dificuldade real e perguntas suspeitas a partir das respostas.
- `scripts/simular_respostas.py` — gera respostas fictícias para testar o calibrador.

## Comandos

- `/produzir-lote` — perguntas novas pela linha completa.
- `/auditar` — auditoria às cegas de uma amostra aleatória.
- `/manutencao` — sentinela (prazos), triagem de reportes e calibração.

## Estados

`rascunho` → `em_verificacao` → `aprovada` (só pelo `aprovar.py`) → `publicada`, e ainda
`suspensa`, `retirada` e `rejeitada`. Só passa a `publicada` com ordem expressa do Andre e sem travão
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

Curtos, em pt-PT, para ler em 2 minutos: números primeiro (incluindo o tempo de agentes
por pergunta aprovada, sem pausas, e a percentagem de perguntas com fonte de nível 1 do
pesquisador), depois os canários, os problemas e as decisões que o Andre tem de tomar.
Nunca mais de uma página.
