# Relatório do lote 5 (`lote-2026-11-18-retomas`), 18/11/2026

## Números
- 21 perguntas no circuito (11 retomas, 9 alvos novos e 1 substituto da Q94): **19 aprovadas (90%)**, 2 rejeitadas. Acima do limite de 55%.
- Retomas: **10 de 11** aprovadas (Q51, Q54, Q58, Q62, Q68 sem repetir a pesquisa; Q86, Q89, Q90, Q91, Q93 com pesquisador novo). Só a Q63 (Eiffel) não passou: o novo texto (Q92) foi reprovado duas vezes pelo conferente.
- Alvos novos: **9 de 9** (Q87, Q88, Q95 a Q101). A Q94 (planeta mais quente) foi rejeitada como **copiada** (as mesmas 4 opções aparecem em quizzes) e substituída pela Q101.
- Por tópico: Movies 5, Nature & Animals 3, Music 2, General Knowledge 2, Football 2, Geography, Space, World History, Science, Video Games 1 cada.
- Dificuldade: 1 → 1, 2 → 5, 3 → 9, 4 → 4. **Fáceis (1 e 2): 6 de 19 (32%)**, no limite dos 30%: o editor subiu a dificuldade de várias.
- Clássicos: 3 de 19 (16%): Q87, Q98, Q100. No banco: 13 de 59 (22%; a quota só se aplica a partir de 100).
- Fonte de nível 1 do pesquisador: 15 das 19 aprovadas (79%).
- Tempo de agentes (só as invocações que registei, 40): 45,6 min, **2,4 min por aprovada**. Tempo de relógio: 3,1 h, incluindo uma pausa por limite de utilização. Não registei todas as invocações (por exemplo, as repetições de conferente e de editor), por isso o tempo real é um pouco maior.

## Canários
Os dois passaram pelo verificador cego misturados com as perguntas reais e **foram rejeitados como devia**: CAN-1 (planeta menos denso do que a água, marcada errada «Júpiter»): respondeu Saturno. CAN-2 (país com mais fusos horários, marcada errada «Rússia»): respondeu França. Ficam só aqui, nunca no banco.

## O que correu mal
1. **Caminho leve só em 1** (Q58): os alvos de dificuldade 1 pedidos (N1 e N7) saíram a 2 ou mais e a Q51 não tem fonte de nível 1 do pesquisador. A Q58 deve ser auditada por agente que não a produziu.
2. **Q92 (retoma da Q63)**: o conferente reprovou primeiro a concordância de género («nenhuma»/«quantos») e, corrigida, a palavra «sábios» (masculino) como pista só em pt-PT. Rejeitada (ciclos esgotados); a Q63 já era retoma única e não regressa à lista.
3. **Verificação frágil, aprovadas com confiança média**: Q89, Q90, Q93, Q95, Q96, Q98, Q100, Q101 (uma só fonte de nível 2 aberta pelo verificador). Q88 e Q92 usaram o Palais des Festivals / a imprensa porque as fontes do Festival e do museu eram as do pesquisador.
4. **A regra 24 obrigou a repetir o verificador** 6 vezes (editor a mexer em enunciados): Q86, Q90, Q96 depois do editor; Q87, Q88, Q89, Q91, Q92, Q93, Q95, Q97, Q98, Q99, Q100 depois do advogado (reformuladas); e a Q85/Q79/Q73 no ciclo anterior. Do 2.º ciclo em diante instruí o editor a **não mexer em enunciados** (só explicação, dificuldade e subtema), o que evitou mais repetições. Número de repetições do lote 5: 3 por mudança do editor, 11 por reformulação do advogado.
5. **O advogado declarou páginas lidas em todas as passagens** (regra 25), com uma exceção ao início do ciclo anterior (Q79/Q82) já registada.
6. **Fontes de nível 1 que não abriram** (403): Britannica, toureiffel.paris, o artigo original de Current Biology; ficam como pendentes para o `/auditar`.

## Decisões do Andre
1. Ler as 19 (`relatorios/aprovadas-lote-5.md`) e as seis do lote 4 corrigidas.
2. Lote 6: reabrir a Q92/Q63 com outro ângulo? Recomendo que não (já falhou 2 vezes).
3. Reordenar o editor antes do verificador, para evitar repetições (regra 24)? Recomendo manter a regra e continuar a proibir o editor de mexer em enunciados depois do verificador.
4. Fundir o PR #2 (motor, regras 24 a 26) antes do lote 6.
