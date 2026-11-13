# Lote 4 (primeiro lote bilingue) — 12/11/2026

## Números

- 37 perguntas criadas a partir de 40 alvos planeados (+2 canários). **15 aprovadas (40,5%)**, 22 rejeitadas. **Abaixo do limite de 55% que fixaste: o processo tem de ser revisto antes de produzir em volume.**
- Aprovadas por tópico: Science 3, World History 2, Music 2, Football 2, Space 2, Nature & Animals 1, General Knowledge 1, Geography 1, Video Games 1; **Movies 0**. Por dificuldade: 1 → 1, 2 → 2, 3 → 8, 4 → 4. **Dificuldade 1–2: 3 de 15 (20%), abaixo da meta de 30%.**
- Rejeitadas: 9 pelo orquestrador (quota de clássicos 9), 9 pelo advogado (8 por ciclo de correção esgotado, 1 por facto superado), 3 pelo verificador (sem confirmação), 1 pela originalidade (clássico em dificuldade 4).
- Clássicos: 4 de 15 aprovadas (27%), no limite combinado; 12 de 40 no banco inteiro (30%; a quota de 20% só se aplica a partir de 100 perguntas).
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
