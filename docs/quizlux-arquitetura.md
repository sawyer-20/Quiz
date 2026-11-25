> Nota de 2026-11-24: as secções 1 a 4 e 6 continuam válidas. A secção 5 (plano de construção de 6–8 semanas) foi substituída pelo calendário de quizlux-plano.md. Anúncios ficam fora do teste fechado.

# QUIZLUX — arquitetura v1 e custos (Fase A)

Estado: proposta de 2026-11-11. Decisões já tomadas pelo Andre: Android primeiro, mundo, **pt-PT e en-US desde o início**, nome QUIZLUX, escolha técnica delegada em Claude.

## 1. Escolha

**Flutter (Dart) + Firebase.** Uma só base de código serve o Android agora e o iOS mais tarde. Os duelos são assíncronos e por turnos, por isso não há websockets nem servidor próprio.

Alternativas postas de lado: Kotlin nativo + Supabase (melhor para rankings, mas só Android e mais lento de construir); React Native + Supabase (sem vantagem sobre Flutter aqui).

**Idiomas:** pt-PT e en-US desde a v1. A interface usa ficheiros de tradução do Flutter. Cada pergunta traz os dois textos. A app abre no idioma do aparelho, com troca manual. Um duelo entre dois jogadores de línguas diferentes funciona porque cada um vê a mesma pergunta no seu idioma, com a mesma resposta certa.

## 2. Componentes

| Peça | Função | Nota |
|---|---|---|
| App Flutter | 4 separadores (Home, Topics, Duels, Profile), jogo, perfil | Design tokens do canvas QUIZLUX |
| Pacotes de perguntas | JSON versionado por tópico, com os textos pt-PT e en-US, em cache no telemóvel | Servem o jogo a solo e o Daily 10. Perguntas não passam pelo Firestore |
| Firebase Auth | Google Sign-In + conta anónima que se pode promover | Sem email/password na v1 |
| Firestore | users, duels (+ turns), challenges, topicStats, friendships, reports | Rankings em documentos agregados, recalculados por hora |
| Cloud Functions | criar duelo, validar turno, calcular XP e rating, rankings horários | Duelos: o servidor escolhe as perguntas, entrega-as sem resposta e corrige. Anti-batota |
| FCM | «é a tua vez», lembrete do Daily 10, novo tópico | Textos nos dois idiomas |
| Remote Config | frequência de anúncios, tópicos desbloqueados, limites | Muda comportamento sem nova versão |
| AdMob + UMP | intersticial no fim do duelo (com limite), vídeo com recompensa | Consentimento (UMP) para EEE/Reino Unido: confirmar requisitos |
| Crashlytics + Analytics | D1, D7, duelos enviados e aceites, erros | Os critérios do teste fechado saem daqui |
| Denúncia e bloqueio | botão em todo o conteúdo, fila em `reports` | Exigido pela política de UGC da Google Play quando houver conteúdo de utilizadores |

## 3. Custos de infraestrutura por jogadores ativos diários (só Firestore)

Pressupostos meus, não medidos: por jogador e por dia, 60 leituras e 15 escritas.

Preços: quota gratuita diária de 50.000 leituras e 20.000 escritas. Acima disso, tarifa conservadora de 0,06 $ por 100.000 leituras e 0,18 $ por 100.000 escritas. A tarifa regional dos EUA é metade; falta confirmar a da região europeia.

| Jogadores ativos/dia | Leituras/dia | Escritas/dia | Custo/mês (conservador) | Custo/mês (tarifa EUA) |
|---|---|---|---|---|
| 1.000 | 60.000 | 15.000 | ≈ 0,2 $ | ≈ 0,1 $ |
| 10.000 | 600.000 | 150.000 | ≈ 17 $ | ≈ 8,5 $ |
| 100.000 | 6.000.000 | 1.500.000 | ≈ 187 $ | ≈ 93,5 $ |

**Não incluído:** Cloud Functions, Cloud Storage/Hosting dos pacotes, tráfego de saída. O Cloud Storage for Firebase exige o plano Blaze; ligar alerta de orçamento no dia em que se ativa.

## 4. Receita: o que os números dizem

Intervalos globais de eCPM (Playwire, 2026): intersticial 2,50–5,00 $, vídeo com recompensa 8–18 $, banner 0,20–0,80 $. Com 3 intersticiais e 0,4 vídeos por jogador e dia, o ARPDAU fica entre 0,011 $ e 0,022 $ (320–670 $ por mês por 1.000 jogadores ativos/dia).

**O que decide o negócio é o custo por instalação.** Um jogador que joga N dias vale cerca de 0,0145 $ × N: 0,10 $ aos 7 dias, 0,22 $ aos 15, 0,43 $ aos 30. O custo por instalação do Android para este tipo de app não é conhecido: o teste de 60 € serve para o medir.

Ressalva: a receita depende do país do jogador, não do idioma. Tráfego de países de nível 1 rende cerca de 3 vezes mais.

## 5. Plano de construção — SUBSTITUÍDO (ver quizlux-plano.md)

## 6. Por confirmar

- Tarifa da região europeia do Firestore e custo de Functions/Storage.
- Requisitos de consentimento (UMP) para EEE/Reino Unido.
- Verificação do nome QUIZLUX: domínio, TMview, Play Store.
- Conta de programador: pessoal no teste fechado, empresa antes do lançamento público.

## Fontes

- Firestore: https://cloud.google.com/firestore/pricing
- Tarifas e Blaze: https://www.verdent.ai/guides/devtools/firebase-pricing
- eCPM: https://www.playwire.com/blog/admob-ecpm-benchmarks-what-publishers-should-expect
