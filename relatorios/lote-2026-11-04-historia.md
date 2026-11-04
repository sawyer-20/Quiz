# Lote 2026-11-04 — História

## Números

| | |
| --- | --- |
| Alvos | 10 (ids Q-2026-000004 a 000013) |
| Perguntas criadas | 10 (nenhum alvo ficou sem fonte) |
| **Aprovadas** | **7** — 000005, 000006, 000008, 000009, 000010, 000012, 000013 |
| Rejeitadas | 3: 1 no verificador às cegas, 1 no advogado do diabo e 1 no editor |
| Discordâncias do verificador às cegas | 0 em 13 verificações (travão de 30 % longe de ser ativado) |
| Correções pedidas pelo advogado | 4 (000004, 000007, 000008 e 000009), todas na explicação; a resposta nunca mudou |
| Dificuldade das aprovadas | 2: uma · 3: quatro · 4: duas (alvo: 3 fáceis, 4 médias e 3 difíceis) |
| Tempo total | cerca de 4 h 30, incluindo uma pausa forçada pelo limite de utilização |

**Rejeitadas**
- **000004 (Pedra de Roseta), no editor, por cópia.** O enunciado é quase igual ao de vários quizzes (ProProfs, FunTrivia, ThatQuiz). O editor reescreveu-o, mas a reescrita mudou o que se perguntava e deixou de bater certo com as opções.
- **000007 (Bloqueio de Berlim), no advogado, ao segundo ciclo de correção.** O erro foi meu: na primeira correção escrevi que a ponte aérea durou "até ao fim do bloqueio", mas ela continuou até outubro de 1949.
- **000011 (cacau asteca), no verificador às cegas, sem confirmação.** O editor reescreveu a pergunta para fugir a um clássico de quiz. Depois disso, o verificador não conseguiu confirmar em fonte independente nem a "cera" nem a fiscalização em Tenochtitlán.

## Problemas que se repetem

1. **Wikipédia em 9 das 10 perguntas.** A Britannica, a Infopédia, o British Museum e a Library of Congress recusam pedidos automáticos (erro 403). Por isso há menos fontes de nível 1 do que seria desejável. O verificador compensou: 11 das 13 verificações usaram fontes de nível 1 (museus, legislação, universidades).
2. **Números que só uma fonte dá** (53 milhões de ânforas, um avião a cada 45 segundos). O advogado apanhou-os todos.
3. **Factos clássicos são muitas vezes perguntas de quiz já existentes.** Quando o editor muda o ângulo, a pergunta pode deixar de estar verificada (aconteceu na 000004 e na 000011). Convém que o pesquisador fuja à partida dos factos "de manual".
4. **Ambiente.** O WebFetch não tem rede neste ambiente cloud e os agentes do motor não ficaram registados com Bash. Os agentes leem as páginas com `scripts/ler_url.py`, e o hook `.claude/hooks/travao_agentes.py` recusa-lhes qualquer outro comando e qualquer ferramenta de ficheiros. Testei o hook com um agente real: recusou `ls`, `cat`, `Read` e `Grep`.

## Intervenções minhas, além de aplicar o que os agentes devolveram

- **000006:** mantive o enunciado já verificado. O editor queria pôr no enunciado que foi D. João II a rebatizar o cabo, e essa autoria é disputada.
- **000012:** mantive "nacionalidade" em vez de "país", para concordar com as opções.
- **000009:** chegou a ficar aprovada antes de a validação passar. Detetei o erro, reverti a aprovação, corrigi o subtema e só aprovei depois de o `validar.py` passar.
- **000011:** a rejeição foi uma decisão minha ("na dúvida, rejeita"). O verificador deu confiança média e não baixa.

## Decisões para o Andre

1. **O teu veredicto** nas 5 perguntas abaixo: "incrível", "boa" ou "fraca".
2. **000011:** a versão original ("que sementes serviam de moeda aos astecas?") estava verificada numa fonte de nível 1 (Universidade de Cornell), mas é um clássico de quiz. Recuperamo-la ou fica rejeitada?
3. **000008:** a pesquisa de originalidade ficou a meio, por causa do limite de utilização. Tem de ser repetida antes de a publicar.
4. **Leitor e travão:** mantemos esta solução como padrão do motor no ambiente cloud?

## 5 aprovadas ao acaso, para o teu gosto

**Q-2026-000006**: *Segundo a tradição, que nome deu Bartolomeu Dias em 1488 ao cabo que hoje se chama da Boa Esperança?*
Cabo das Agulhas · Cabo dos Ventos · Cabo Bojador · **Cabo das Tormentas ✅**
Explicação: Dias chamou-lhe Cabo das Tormentas por causa das tempestades que enfrentou ao dobrá-lo. Segundo o cronista João de Barros, D. João II rebatizou-o de Boa Esperança, porque a passagem do Atlântico para o Índico prometia o caminho marítimo para a Índia.
Fontes: Wikipédia; South African History Online; History.com; Museu de Marinha.

**Q-2026-000008**: *O Monte Testaccio, em Roma, é uma colina artificial. De que é feita quase por inteiro?*
Escória de fornos de fundição · Cacos de ânforas de vinho · **Cacos de ânforas de azeite ✅** · Entulho do incêndio de 64 d.C.
Explicação: de cacos de ânforas de azeite deitadas fora na época imperial, na grande maioria vindas da Bética, no sul da Hispânia. Ao que parece, os romanos espalhavam cal sobre os cacos para disfarçar o cheiro do azeite rançoso.
Fontes: Blázquez, *Greece & Rome* (1992); Archaeology Magazine; Wikipédia; CEIPAC (Universidade de Barcelona).

**Q-2026-000009**: *Na passagem ao calendário gregoriano, em 1752, que dia se seguiu a 2 de setembro na Grã-Bretanha?*
12 de setembro · 11 de setembro · **14 de setembro ✅** · 13 de setembro
Explicação: 14 de setembro. Foram suprimidos 11 dias (de 3 a 13), e a quarta-feira, dia 2, foi seguida pela quinta-feira, dia 14. A mesma lei mudou o início do ano de 25 de março para 1 de janeiro em Inglaterra, no País de Gales e nas colónias; a Escócia já o fazia desde 1600.
Fontes: Royal Museums Greenwich; Wikipédia; legislation.gov.uk (texto da lei).

**Q-2026-000010**: *Ao criar o metro, a França revolucionária fê-lo igual a 1/10 000 000 de que distância?*
O diâmetro da Terra, de polo a polo · **Do polo Norte ao equador ✅** · O perímetro da Terra no equador · De Paris ao polo Norte
Explicação: do polo Norte ao equador, pelo meridiano de Paris. Delambre e Méchain mediram o arco entre Dunquerque e Barcelona, mas erros no cálculo da curvatura da Terra deixaram o metro-padrão original 0,2 mm mais curto.
Fontes: NIST; Wikipédia; LNE (metrologia francesa).

**Q-2026-000012**: *A ilha artificial de Dejima, em Nagasaki, foi construída na década de 1630 para confinar mercadores de que nacionalidade?*
Ingleses · **Portugueses ✅** · Neerlandeses · Chineses
Explicação: portugueses. O xogunato começou a construir Dejima em 1634 para os confinar e travar o cristianismo. Em 1639 foram proibidos de vir ao Japão e, em 1641, a feitoria neerlandesa de Hirado mudou-se para a ilha, onde ficou mais de dois séculos.
Fontes: site oficial de Dejima (Cidade de Nagasaki); Wikipédia; Governo Metropolitano de Tóquio.

Nada foi publicado: as 7 perguntas estão em `aprovada` e só passam a `publicada` com ordem tua.
