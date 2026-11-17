# Motor de factos — QUIZLUX (versão 2.0: pt-PT e en-US)

Este projeto produz perguntas de cultura geral verificadas para a app QUIZLUX, **cada
uma em pt-PT e en-US**, prontas para o jogo (a solo, duelos e Daily 10).
O CEO é o Andre: decide e dá o gosto editorial. Tu orquestras os agentes, escreves os
ficheiros e nunca tomas decisões de produto sozinho.

## Regras invioláveis

1. Nenhum facto vem da memória do modelo. Todos vêm de fontes abertas e lidas nesta
   sessão (WebSearch e WebFetch), segundo `regras/fontes.md`.
2. Cada pergunta passa, por esta ordem, por: `pesquisador` → `originalidade` →
   `verificador-cego` → `advogado-do-diabo` → `editor` → `tradutor` → `conferente` →
   `python3 scripts/aprovar.py`. Nenhum passo se salta. O verificador, o advogado e o editor recebem até 5 perguntas
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
   não o facto. **Definição de «clássico» (decisão do Andre, 17/11/2026): o facto e a forma
   de o perguntar são habituais em concursos, apps e sites de quiz.** Um facto conhecido,
   perguntado com um ângulo próprio que não aparece em quizzes, é `original`. O clássico
   pode entrar com enunciado próprio e leva a etiqueta `classico` (nunca em dificuldade 4
   ou 5): as perguntas clássicas e fáceis mantêm o jogador nos primeiros níveis; o limite
   serve só para o banco não ser de trivia genérica. Limites: no máximo **20% das
   aprovadas do lote** (arredondado para baixo, em percentagem e não em número absoluto) e
   20% das aprovadas e publicadas do **banco**, esta aplicada a partir de 100 perguntas;
   abaixo disso, só se mede. Originalidade interrompida (limite de utilização ou erro): a
   pergunta fica em `em_verificacao`.
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
14. **Ciclos de correção por pergunta, na produção.** Há um ciclo de correção. Um **segundo
    ciclo** só é permitido quando o que falta é de redação, atribuição ou arredondamento e
    **não muda o facto, a resposta nem as opções**; qualquer mudança ao facto reinicia a
    pergunta no verificador cego. Máximo de dois ciclos. As atribuições que o advogado
    exigir ficam no campo `sources` (a explicação só atribui quando for necessário para a
    regra das fontes). Antes de a pergunta ir ao advogado, o orquestrador valida os limites
    de texto (explicação até 300 caracteres e 2 frases, opções até 60, enunciado até 200)
    com `python3 scripts/limites.py <ids>`: foi o limite de 300 caracteres que reabriu e
    matou perguntas do lote 4. Uma pergunta reaberta por mudança de regra ou por auditoria
    tem direito a ciclos novos.
15. **Alvos a retomar.** Uma pergunta não clássica que esgota o ciclo de correção gera um
    alvo a retomar no lote seguinte, **uma única vez**, com ângulo novo e as notas do
    advogado. A lista está em `relatorios/alvos-a-retomar.md`. Um alvo já retomado que
    volta a falhar não regressa à lista.
16. **Clássicos no plano do lote.** Pelo menos 8 em cada 10 alvos têm ângulo não clássico.
    O lote não pode ter mais de 20% de clássicos entre as aprovadas (regra 7): quando o
    acréscimo de um clássico novo ultrapassaria esse limite no fim do lote, o clássico fica
    em espera (`em_verificacao`, nota no histórico) e só avança se sobrar vaga; no fim do
    lote, os que ficarem em espera são rejeitados com motivo `quota de clássicos do lote`.
17. **Mudanças ao motor entram por pedido de merge para o `main`** (regras, agentes,
    skills, scripts). O banco e os relatórios de lote seguem no ramo de trabalho.
18. **O facto verifica-se uma vez, o texto escreve-se duas.** O pesquisador, o verificador,
    o advogado e o editor trabalham no texto pt-PT (a referência). O `tradutor` escreve o
    en-US a partir do pt-PT aprovado e da ficha de facto; o `conferente` (cego: vê só os
    dois textos) confirma que dizem o mesmo, que a resposta certa é a mesma, que as opções
    não mudaram de sentido e que o pt-PT não tem formas do português do Brasil. Rejeita na
    dúvida. Quem altera o pt-PT depois da verificação obriga a nova verificação (regra 4).
19. **O texto das opções é imutável depois da aprovação.** O `aprovar.py` grava o
    `options_lock` (SHA-256 das opções nos dois idiomas) e o `validar.py` recusa qualquer
    mudança. Para mudar uma opção, a pergunta volta a `em_verificacao`.
20. **Verificador independente.** O verificador não pode usar uma republicação ou cópia da
    fonte do pesquisador (o mesmo artigo noutro domínio, num repositório ou numa agência):
    o orquestrador passa-lhe, além dos domínios, os títulos das fontes a evitar.
21. **Sensibilidade no passo 0.** Antes de planear um alvo, verifica-se se o tema está ligado
    a uma tragédia com menos de 10 anos (acidentes, atentados, desastres); se estiver, o
    alvo muda.
22. **Mercados.** `markets` (ex.: `["pt"]`) só se usa em perguntas de interesse local; sem
    valor = global. `daily_eligible` só para factos estáveis (sem `valid_until`).

23. **Relatórios truncados ou malformados não se aplicam.** Um relatório de agente cortado a
    meio ou com JSON inválido pode ter perdido uma objeção no fim. O orquestrador não o
    reconstrói: pede ao agente que o devolva completo ou repete o passo. Nunca aprova uma
    pergunta que dependa de um relatório assim.

## Onde estão as coisas

- `banco/perguntas/<id>.json` — uma pergunta por ficheiro, no formato (v2, bilingue) de
  `esquema/pergunta.schema.json`. Campos do jogo: `topic`, `subtopic`, `markets`, `text`
  (`pt-PT` e `en-US`: `question`, `options`, `explanation`), `correct`, `difficulty`,
  `daily_eligible`, `valid_until`, `sources`. As rejeitadas ficam também, com `estado: rejeitada`
  e motivo: são dados para melhorar o motor.
- `banco/respostas/` — exportações de respostas dos jogadores (CSV) para o calibrador.
- `banco/reportes.csv` — reportes de erro dos jogadores (`pergunta_id,data,jogador_id,texto`).
- `relatorios/` — relatórios de lote, auditoria e manutenção.
- `regras/fontes.md` — hierarquia de fontes.
- `regras/fontes-pt.md` — fontes portuguesas de nível 1 que os agentes já conseguiram abrir
  (e as que recusam); o pesquisador começa por aqui nas perguntas de tema `portugal`.
- `relatorios/alvos-a-retomar.md` — alvos que voltam uma vez ao lote seguinte.
- `scripts/validar.py` — validação automática.
  `python3 scripts/validar.py --dominio <url>` devolve o domínio a registar numa fonte.
- `scripts/aprovar.py` — a única forma de aprovar (corre o `validar.py`; grava `options_lock`).
- `scripts/migrar_v2.py` — migrou o banco do esquema v1.1 (só pt-PT) para o v2.
- `scripts/ler_url.py` — leitor de páginas dos agentes (só http/https públicos; lê HTML,
  texto e PDF); `scripts/testar_ler_url.py` testa as recusas e as leituras.
- `scripts/testar_validar.py` — testes das regras de texto do `validar.py`.
- `scripts/estatisticas_lote.py` — números do relatório de um lote (tempo de agentes, tempo
  de relógio e percentagem de clássicos no banco inteiro).
- `scripts/registar_tempo.py` — acrescenta uma linha ao registo de tempos do lote.
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
por pergunta aprovada, sem pausas, o tempo de relógio do lote, a percentagem de clássicos
no lote e no banco inteiro e a percentagem de perguntas com fonte de nível 1 do
pesquisador), depois os canários, os problemas e as decisões que o Andre tem de tomar.
Nunca mais de uma página.
