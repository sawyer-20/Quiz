# QUIZLUX — Estado a 2026-11-24

Substitui quiz-app.md, quizlux-motor-migracao.md e a secção F-26 do estado.md do projeto Projetos.

## Decisões em vigor
- Produto: app Android na Google Play, quiz social (duelos assíncronos, Daily 10, solo). Nome de trabalho QUIZLUX, lema "THE GAME OF KNOWLEDGE" (nome ainda por verificar).
- Línguas: interface e perguntas em pt-PT e en-US desde a v1. Perguntas importadas traduzidas por máquina e conferidas por amostra.
- Tecnologia: Flutter + Firebase (ver quizlux-arquitetura.md).
- Conta Google Play pessoal no teste fechado; conta de empresa antes do lançamento público.
- Publicidade: teste único de 60 € no teste fechado para medir o custo por instalação.
- Plano de 2026-11-24 (quizlux-plano.md) substitui as fases A–E antigas e o plano de construção de 6–8 semanas.

Decisões antigas que caducaram: 32 temas (agora 10), "mundo em inglês primeiro" (agora pt-PT e en-US), desafios criados pelos jogadores na v1 (agora depois do teste), produção de perguntas pelo circuito completo (agora só auditoria).

## O que existe
- Repositório sawyer-20/Quiz: motor de factos (agentes, scripts validar.py, aprovar.py, exportar_app.py, regras 1–29 no CLAUDE.md) e a app em app/.
- APK v3 (cerca de 46 MB): jogo a solo offline, pt-PT e en-US, tema ou misto, até 10 perguntas, 4 opções, temporizador de 10 s (a tornar proporcional ao texto), ecrã de resultado com revisão, logótipo. Ainda não jogado num telemóvel.
- Design: quizlux-design.zip (10 quadros). Paleta: fundo #0B1428, dourado #C6A45A, azul #4389D9, texto #F5F5F2. Letras Manrope e Cormorant Garamond.
- Banco verificado: 57 perguntas aprovadas (nenhuma publicada); 5 com confirmação pendente fora do Daily 10. Ficam como pacote premium do Daily 10.
- PR #2 por fundir (aguarda o Andre).

## Fontes de perguntas (verificado a 2026-11-24)
- Open Trivia DB: CC BY-SA 4.0, API grátis, 1 pedido a cada 5 s, 50 perguntas por pedido. Exige atribuição e partilha nos mesmos termos. Contagem real por confirmar.
- Wikidata: CC0, uso comercial livre. Reserva para geração em Geografia se o Open Trivia DB der menos de 2.000 perguntas limpas.
- Não usar: The Trivia API (CC BY-NC, comercial pago), API Ninjas (comercial só premium), TriviaQA (licença desconhecida), QuizBase (só programação).
- Antes de lançamento público com anúncios: parecer jurídico sobre o ShareAlike.

## Em aberto
- Contagem real do Open Trivia DB.
- Tarifa europeia do Firestore, custo de Functions e Storage, requisitos UMP.
- Nome QUIZLUX: domínio, TMview, Play Store.
- Taxa da conta Google Play e regra dos testadores: confirmar no site da Google.
