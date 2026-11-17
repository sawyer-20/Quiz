# Lote 4 (primeiro lote bilingue) — 12/11/2026

## Números

- 37 perguntas criadas a partir de 40 alvos planeados (+2 canários). **15 aprovadas (40,5%)**, 22 rejeitadas. **Abaixo do limite de 55% que fixaste: o processo tem de ser revisto antes de produzir em volume.**
- Aprovadas por tópico: Science 3, World History 2, Music 2, Football 2, Space 2, Nature & Animals 1, General Knowledge 1, Geography 1, Video Games 1; **Movies 0**. Por dificuldade: 1 → 1, 2 → 2, 3 → 8, 4 → 4. **Dificuldade 1–2: 3 de 15 (20%), abaixo da meta de 30%.**
- Rejeitadas: 9 pelo orquestrador (quota de clássicos 9), 9 pelo advogado (8 por ciclo de correção esgotado, 1 por facto superado), 3 pelo verificador (sem confirmação), 1 pela originalidade (clássico em dificuldade 4).
- Clássicos: **2 de 15 aprovadas (13%)** com a definição de 17/11 (Q50, Q61); a contagem de 4 (27%) era a da definição antiga e foi corrigida na adenda de 17/11. No banco inteiro: 10 de 39 aprovadas (26%; a quota de 20% só se aplica a partir de 100 perguntas).
- Perguntas com fonte de nível 1 do pesquisador: 36 de 37 (97%); entre as aprovadas, 15 de 15.

## Tempos (sem pausas)

- Tempo de agentes: 83,7 min em 79 invocações, **5,6 min por pergunta aprovada**. Por passo: pesquisador 42,6; verificador cego 15,7; advogado 14,6; originalidade 5,6; **editor 2,1; tradutor 1,2; conferente 1,2**; auditor 0,7.
- **Custo do tradutor e do conferente: 2,4 min no total, cerca de 0,16 min por pergunta aprovada**, ou seja, a tradução bilingue é quase gratuita face à verificação do facto (que gastou 88% do tempo). Mas o conferente apanhou erros reais: pontuação americana (Q38), vírgula decimal (Q39), unidade de temperatura sem Celsius (Q84), gramática pt-PT (Q73), explicação en-US com prefixo a mais (Q52).
- Tempo de relógio: 25,1 h (inclui duas pausas por limite de utilização).

## Canários e caminho leve

- **Canários: 2 de 2 rejeitados como devia.** X1 (Silbo Gomero): marcado «Três», o verificador respondeu «Dois» (a verdadeira). X2 (fulgurito): marcado «Cerâmica de argila», o verificador respondeu a verdadeira. Nenhum passou; o lote não parou.
- **Caminho leve:** só 1 facto chegou a dificuldade 1 com fonte de nível 1 do pesquisador (Q50, osso mais longo). Auditado por um agente que não o produziu: **0 erros, 0 diferenças entre idiomas**. O teste é inconclusivo por ter amostra de 1: os pesquisadores devolveram quase tudo em dificuldade 2 ou mais.

## O que correu mal

1. **A quota de clássicos estrangulou o lote**: o agente de originalidade classificou quase todos os factos conhecidos como «clássico» (7 das 8 primeiras perguntas). Isso queimou 9 perguntas já pesquisadas e é a razão de não haver nenhuma pergunta fácil. A meio do lote acrescentei às instruções da originalidade «marca clássico só se a pergunta como tal (facto e forma de perguntar) for habitual de quizzes»: **é um desvio à regra 7**, que decidiste tu; decide se ficou.
2. **Dificuldade 1 não saiu**: os pesquisadores tendem a ≥2 e os factos realmente fáceis são clássicos. Os dois objetivos (≥30% fáceis e ≤4 clássicos) são incompatíveis com o critério atual de «clássico».
3. **Ciclo único de correção**: 8 perguntas boas foram rejeitadas por problemas pequenos (um número arredondado, uma atribuição) na segunda passagem do advogado. Os verificadores às vezes devolvem JSON truncado ou malformado; apliquei só o que li, sem inventar o resto (Q84: notas finais em falta).
4. Erros meus durante o lote: rejeitei por engano Q20, Q31 e Q43 (corrigido e registado), e transcrevi mal um pedido de conferência da Q77 (repetido).
5. Movies: nenhuma aprovada (Óscares, Technicolor e Barry Lyndon caíram por fontes de nível 1 inacessíveis ou por ciclo esgotado).

## Alterações ao motor feitas neste lote

Caminho leve (`aplicar_passo.py leve`, campo `verificacao.caminho_leve`, etiqueta `caminho_leve`), `validar.py` (ordinais pt não contam como números diferentes; rejeitadas com explicações longas ou 1 fonte passam a aviso), esquema atualizado. Vão no PR #1.

## Decisões tuas

1. **Revisão do processo (limite de 55%)**: concordas em (a) redefinir «clássico» como «pergunta habitual de quizzes» (facto + forma) e manter o limite de 4 por lote, ou (b) subir o limite do lote para 8 (regra 16: 8 em 10 não clássicos)? Recomendo (a)+(b) só se a auditoria pedir.
2. **Segunda passagem do advogado**: 8 rejeições eram corrigíveis em minutos. Aceitas um segundo ciclo de correção quando o problema é só de redação ou de atribuição (sem mudar facto)?
3. Retomas (regra 15): Q63 (Torre Eiffel), Q66 (gene do doce), Q75 (peixe-papagaio), Q76 (sifr/zero), Q80 (pássaro-jardineiro), Q83 (Technicolor) voltam ao próximo lote, uma vez. Q78 (Bakhshali) fica rejeitada: a datação de 2017 foi retirada por Oxford em 2024.

## 5 perguntas aprovadas ao acaso para o teu gosto (diz «incrível», «boa» ou «fraca»)

**Q-2026-000067** (General Knowledge, dificuldade 3)
- pt-PT: Segundo a lei suíça, os braços da cruz da bandeira são mais compridos do que largos em que fração?  Opções: Metade | ✔ Um sexto | Um terço | Um quarto
  *A lei suíça define uma cruz branca sobre fundo vermelho, com os quatro braços iguais, cada um um sexto mais comprido do que largo. A bandeira nacional tem fundo quadrado, uma raridade entre as bandeiras de Estado.*
- en-US: According to Swiss law, the arms of the cross on the flag are longer than they are wide by what fraction?  Options: One half | ✔ One sixth | One third | One quarter
  Fontes: https://fedlex.data.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/2015/613/20170101/en/pdf-a/fedlex-data-admin-ch-eli-cc-2015-613-20170101-en-pdf-a.pdf

**Q-2026-000056** (Nature & Animals, dificuldade 3)
- pt-PT: Quantas folhas permanentes tem, durante toda a vida, a Welwitschia mirabilis, planta do deserto do Namibe?  Opções: ✔ Duas | Quatro | Doze | Uma
  *A Welwitschia só produz duas folhas, que crescem continuamente a partir da base da planta. Rasgam-se e desfiam-se com o tempo, mas são as mesmas durante toda a vida da planta, que pode viver séculos.*
- en-US: How many permanent leaves does Welwitschia mirabilis, a plant of the Namib Desert, have throughout its entire life?  Options: ✔ Two | Four | Twelve | One
  Fontes: https://conservatory.cals.cornell.edu/plants/welwitschia-mirabilis, https://www.guinnessworldrecords.com/world-records/84107-longest-leaf-lifespan

**Q-2026-000069** (Music, dificuldade 4)
- pt-PT: Quem pediu a Prokofiev, em 1936, «Pedro e o Lobo» para ensinar às crianças os instrumentos da orquestra?  Opções: Galina Ulanova, bailarina | Anna Akhmatova, poetisa | Nadezhda Krupskaya, pedagoga e dirigente comunista | ✔ Natalya Sats, diretora de um teatro infantil
  *Natalya Sats, diretora de um teatro infantil em Moscovo, pediu a Prokofiev uma peça para ensinar às crianças os instrumentos da orquestra. Ele escreveu «Pedro e o Lobo» para o teatro dela.*
- en-US: Who asked Prokofiev in 1936 to write "Peter and the Wolf" to teach children the instruments of the orchestra?  Options: Galina Ulanova, ballerina | Anna Akhmatova, poet | Nadezhda Krupskaya, educator and Communist leader | ✔ Natalya Sats, director of a children's theater
  Fontes: https://www.loc.gov/static/programs/national-recording-preservation-board/documents/PeterAndTheWolf.pdf, https://www.boosey.com/downloads/prokofjew_werkverzeichnis.pdf

**Q-2026-000077** (Geography, dificuldade 4)
- pt-PT: A fronteira que atravessa o ilhéu báltico de Märket foi redesenhada nos anos 1980. Com que objetivo?  Opções: Dar à Suécia o único ancoradouro do ilhéu | Acompanhar a subida do solo após o degelo | ✔ Pôr o farol finlandês em território da Finlândia | Separar as zonas de pesca dos dois países
  *Para pôr o farol finlandês em território da Finlândia: a fronteira dividia o ilhéu ao meio, mas o farol que a Finlândia construiu em 1885 ficara na parte sueca. Uma revisão nos anos 1980 traçou nova linha.*
- en-US: The border that runs through the Baltic islet of Märket was redrawn in the 1980s. What was the purpose?  Options: To give Sweden the islet's only anchorage | To follow the land uplift after the ice melted | ✔ To put the Finnish lighthouse on Finnish territory | To separate the two countries' fishing zones
  Fontes: https://data.riksdagen.se/dokument/G801LU16.html, https://www.atlasobscura.com/places/market-lighthouse

**Q-2026-000050** (Science, dificuldade 1)
- pt-PT: Qual destes ossos é o mais longo do corpo humano?  Opções: ✔ Fémur | Úmero | Tíbia | Rádio
  *O fémur, o osso da coxa, é o mais longo, o mais pesado e o mais forte do corpo humano. Liga a bacia ao joelho, onde articula com a tíbia e a rótula, e suporta o peso do tronco ao andar.*
- en-US: Which of these bones is the longest in the human body?  Options: ✔ Femur | Humerus | Tibia | Radius
  Fontes: https://www.ncbi.nlm.nih.gov/sites/books/NBK532982/, https://my.clevelandclinic.org/health/body/22503-femur


## Canários (detalhe, só no relatório)


- **X1** — No Silbo Gomero, língua assobiada de La Gomera, quantos assobios distintos substituem as cinco vogais do espanhol?  Opções: ['Três', 'Cinco', 'Dois', 'Um'].  Resposta errada marcada de propósito: **Três**. Verdadeira: **Dois**. Resultado do verificador: respondeu a verdadeira (canário rejeitado como devia).
- **X2** — Quando um raio atinge areia seca de quartzo, que material se forma no solo?  Opções: ['Cristais de sal', 'Cerâmica de argila', 'Vidro natural, em tubos (fulgurito)', 'Carvão vegetal'].  Resposta errada marcada de propósito: **Cerâmica de argila**. Verdadeira: **Vidro natural, em tubos (fulgurito)**. Resultado do verificador: respondeu a verdadeira (canário rejeitado como devia).

## Adenda de 17/11/2026 (decisões do Andre sobre este relatório)

- **«Clássico» redefinido** (facto E forma habituais em quizzes; limite 20% das aprovadas do lote). Recalculadas as 15 aprovadas: **2 clássicas (Q50, Q61), 13%**; Q52 e Q60 passaram a originais. As 9 rejeitadas por quota foram classificadas com a definição antiga e nunca chegaram à verificação: podem ser reabertas (ver decisões abaixo).
- **Relatórios truncados ou malformados (regra 23).** Cinco aprovadas dependiam deles (Q60, Q61, Q82, Q84, Q85). Repetidos os passos: o verificador cego confirmou as respostas de Q60, Q61 e Q84; **a repetição do advogado reprovou Q82, Q84 e Q85**, que foram reabertas e voltaram a passar o circuito inteiro. Q82, Q84 e Q85 estão aprovadas de novo, com texto alterado (Q85 com uma opção nova; Q84 sem «até 2026» e sem o calor e Lausana). Ressalva: na última passagem do advogado a Q84 e a Q85 não foram abertas páginas novas (0 consultas); a confiança vem do verificador cego do mesmo ciclo.
- **Tabela das 22 rejeitadas:** `relatorios/lote-2026-11-12-bilingue-rejeitadas.md` (9 quota, 8 ciclo esgotado, 3 sem confirmação, 1 facto superado, 1 clássico em dificuldade 4). A discrepância 8/6 explica-se: dos 8 «ciclo esgotado», 6 são não clássicas e voltam (regra 15); Q49 e Q51 eram clássicas.
- **Regras novas (CLAUDE.md):** regra 7 (definição e 20%), 14 (até dois ciclos, só redação/atribuição/arredondamento; limites de texto validados antes do advogado com `scripts/limites.py`), 16, 23. As atribuições que o advogado exigir ficam em `sources`: **atenção**, o `validar.py` continua a exigir atribuição na explicação para linguagem de dúvida (regra 9); preciso da tua decisão se queres alterá-la.
- **Ritmo:** 85 invocações e 84 min de agentes para 15 aprovadas (5,6 invocações e 5,6 min por aprovada); as 25,1 h de relógio incluem pausas por limite de utilização e esperas, não medem o ritmo possível. O ritmo real depende de lançar pesquisadores em paralelo (≤3) e de a taxa de aprovação subir de 40% para perto de 70%, o que as regras novas deverão permitir (mais 9 quota e 6 ciclos recuperáveis); é uma estimativa, não uma medição.
- 15 aprovadas para escolheres as 10 a ler: `relatorios/aprovadas-lote-4.md`.

## Adenda de 17/11/2026 (2.ª ronda: revisão editorial do Andre)

- **Histórico da Q84 e das outras 14.** Q84: aprovada a 13/11 (conferente reprovou o en-US, tradutor juntou «Celsius», segunda conferência aprovou); reaberta a 17/11 porque a repetição do advogado (regra 23) a reprovou; texto reescrito, nova verificação, advogado, editor, tradução e conferência; aprovada de novo. Auditoria pergunta a pergunta em `relatorios/auditoria-historico-lote-4.md`. O histórico não guarda impressão digital do texto, por isso a confirmação foi feita **repetindo a conferência cega sobre o texto final de cada ficheiro: as 15 passaram** (6 nesta ronda mais as 9 inalteradas, Q50, Q52, Q56, Q60, Q61, Q67, Q69, Q72, Q77).
- **Relatórios malformados (ponto 2).** Cinco aprovadas dependiam deles: Q60, Q61, Q82, Q84, Q85. Passos repetidos na ronda anterior; nenhuma das 15 depende agora de um. Nesta ronda nenhum relatório de agente veio truncado ou malformado.
- **Seis correções:** Q73, Q79, Q82, Q84, Q85 reescritas pelo pesquisador, verificadas às cegas, passadas no advogado e no editor, traduzidas e conferidas, e aprovadas outra vez pelo `aprovar.py`. **Q70 parou**: o verificador cego não achou fonte independente de nível 1 ou 2 (só Wikipédia e um blogue, em duas tentativas); está `suspensa` à espera da tua decisão.
  - Q73: o conferente apanhou uma pista («curva» no enunciado e na opção certa, só em pt-PT); o editor trocou para «forma errada» e a conferência repetida aprovou.
  - Q79 e Q82 precisaram de três passagens do advogado (atribuição: o enunciado da Q82 passou a «Segundo a Universidade do Colorado»; da Q79 saiu «1846» e o texto passou a atribuir NASA, Jamieson e Kowal e Drake). **Na terceira passagem o advogado declarou que só leu os excertos que lhe passei e não reabriu as páginas.** Eu conferi à mão que as páginas da NASA e de Jamieson abrem e dizem o que o excerto diz. A Q82 tem um verificador de confiança média, que não confirma a atribuição «segundo a Universidade do Colorado» fora de colorado.edu.
  - Q85: «Bibliotecária do Congresso» e «já não disponíveis no mercado» (depois «indisponíveis», pelo editor), com a regra do Federal Register como fonte de nível 1; `valid_until` 2027-10-28 (ciclo trienal).
- **Reavaliação das 11 perdidas** (9 por quota mais Q49 e Q51), pela originalidade com a definição de 17/11: **5 passam a originais** (Q51, Q54, Q58, Q62, Q68) e entram no lote 5 como retoma única, sem repetir a pesquisa; 6 mantêm-se clássicas (Q49, Q53, Q55, Q57, Q59, Q71). Notas: Q57 está na fronteira com «copiada» (as quatro direções aparecem em exercícios escolares); Q71 é quase tradução de uma pergunta do RemNote.
- **Tempos desta ronda:** não registei invocação a invocação (as durações vieram em notificações misturadas); o quadro de tempos do lote 4 não inclui esta ronda.
- **Alteração ao motor por fazer:** nenhuma foi feita ao motor nesta ronda. O `reformular` baralha sempre as opções, por isso a ordem crescente da Q84 (7, 8, 9, 10) só foi possível porque o pesquisador a devolveu em `ordem_opcoes` e eu a gravei com um script meu fora do repositório. Se quiseres que o motor o suporte, é uma mudança de script para PR.
