# QUIZLUX — Plano de produto (versão 1, 2026-11-24)

Dono do plano: Claude, como product manager. Decisões do Andre marcadas com [ANDRE].
Pressuposto: o "Quiznox" não é uma app existente do Andre. Se for, este plano é revisto.

## 1. O que estamos a provar
Hipótese central: amigos em Portugal jogam duelos assíncronos de quiz entre si durante pelo menos uma semana.
Se isto for falso, não há jogo social e o resto não importa.
Métrica principal: duelos concluídos por jogador ativo por semana.

## 2. Critérios do teste fechado (definidos antes de começar)
- D1 ≥ 30%, D7 ≥ 12% (instalações do teste fechado).
- ≥ 20% dos jogadores enviam pelo menos um duelo; ≥ 30% dos duelos são aceites.
- Erro de facto denunciado ≤ 1% das perguntas servidas.
- Abandono do conceito: D7 < 12% E < 20% enviam duelo, depois de uma ronda de correções.
- Risco conhecido: o teste cai no Natal; o comportamento pode ser atípico.

## 3. Âmbito da v1 (teste fechado)
Entra:
- Jogo a solo por tema ou misto (já existe, APK v3).
- Daily 10: igual para todos, a partir das perguntas verificadas.
- Duelo assíncrono com amigo por link: mesmas 10 perguntas para os dois, escolhidas no servidor.
- Botão de denúncia em cada pergunta.
- Nível/XP simples e alcunha. Sem fotografia, sem perfil público.
- 10 temas de arranque, cada um com ≥ 150 perguntas.
- Interface em pt-PT e en-US.
Não entra (decidido): torneios, ranking global, emparelhamento por nível, temporadas,
criação de desafios pelos jogadores, chat, 32 temas, anúncios no teste fechado.
Volta a discutir-se só depois do teste fechado.

## 4. Conteúdo
- Fonte principal: Open Trivia DB (CC BY-SA 4.0), importado para pacote separado com licença e origem por pergunta; atribuição nos créditos.
- Filtrar perguntas demasiado centradas nos EUA, datadas ou ambíguas.
- Tradução automática para pt-PT; o conferente cego verifica por amostra, não pergunta a pergunta.
- Auditoria por lote: amostra de 50; erro > 5% devolve o lote inteiro.
- As 57 verificadas ficam como pacote premium do Daily 10.
- Se a importação der < 2.000 perguntas limpas: gerador Wikidata (CC0), começando por Geografia.
- O motor de 29 regras deixa de produzir perguntas novas; passa a auditar amostras e denúncias.
- Parecer jurídico sobre o ShareAlike antes de qualquer lançamento público com anúncios.

## 5. Calendário
- Semana 1 (25 nov – 1 dez): importação, tradução, auditoria, pacotes na app. Andre joga o APK.
- Semana 2 (2 – 8 dez): Firebase, duelos por link, botão de denúncia, Daily 10.
- Teste fechado (9 – 22 dez): ≥ 12 testadores, 14 dias.
- 23 dez: decisão continuar / corrigir / abandonar, com os números.

## 6. Papéis e ritmo
- Andre: jogar, decidir, recrutar testadores. Objetivo ≤ 3 h por semana.
- Code: executa por ordem permanente, sem esperar ordens por lote. Relatório único à sexta.
- Claude (projeto QUIZLUX): plano, prioridades, revisão dos relatórios.
- Decisões reservadas ao Andre: dinheiro, contas, publicação, nome, merge para `main`.

## 7. Tarefas só do Andre esta semana [ANDRE]
1. Instalar o APK v3 e jogar 20 minutos; três notas (gostei, irritou, faltou).
2. Criar conta de programador Google Play (taxa e regra dos 12 testadores a confirmar no site da Google).
3. Criar projeto Firebase.
4. Lista de 12–15 amigos com Android para o teste.
5. Verificar o nome QUIZLUX (domínio, TMview, Play Store).

## Depois do teste fechado (lista de espera, não é v1)
- Criação de desafios pelos jogadores, ranking, torneios, temporadas, mais temas, anúncios.
