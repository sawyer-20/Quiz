# Auditoria nível 1 ao banco inteiro — 18/11/2026

**n = 59** (todas as aprovadas; 0 publicadas). Sem amostragem: as 13 de confiança média/prioritárias (Q89, Q90, Q93, Q95, Q96, Q98, Q100, Q101, Q43, Q1, Q79, Q85, Q70) foram à frente nos blocos 1 a 3; ordem aleatória com semente 20261118 nas restantes. 12 blocos de 5, auditor cego (só enunciado, opções baralhadas e domínios a evitar).

(Nota: o revisor falava em 34 aprovadas; o banco tem 59.)

## Números

| | |
|---|---|
| Resposta do auditor ≠ resposta do banco | **0 em 59** (Q82: o auditor escreveu «pintada a ouro», fonte de terceiros; o banco diz «pulverizada com tinta dourada», como o Colorado — diferença de redação, não de facto) |
| Erros confirmados pela triagem | **0** |
| Taxa de erro | **0%** — **sem travão** |
| Confiança do auditor | 38 alta, 21 média, 0 baixa |
| Fonte do auditor | 33 de nível 1, 26 só de nível 2 |
| Com ambiguidade/ressalva assinalada | 23 |
| Enviadas à triagem | 9 (Q82, Q25, Q38, Q88, Q12, Q19, Q70, Q79, Q85): **as 9 `pergunta_certa`**, todas erro do auditor (não abriu a fonte que já estava no banco) |

## As que «falham» e a causa

Nenhuma falha de **facto**. As falhas são de **confirmação**, e a causa é a mesma em quase todas: o auditor não conseguiu abrir fonte de nível 1 (403/429/ENOTFOUND em Britannica, Smithsonian, Met, UNESCO) ou os domínios a evitar excluíam a fonte oficial.

Triadas e mantidas, com a lacuna que a triagem encontrou:
- **Q85** — resposta confirmada (VGHF, nível 1). A 2.ª frase da explicação («regra que limita o acesso às instalações… não ficou demonstrado») **não foi confirmada** no texto oficial (secção 6(b) não abriu). Ponto por confirmar; ver abaixo.
- **Q88** — só 1 fonte (festival-cannes.com, mesmo domínio duas vezes). A regra 1 pede 2 domínios. Falta fonte independente.
- **Q38** — duas fontes de nível 2 concordam; sem nível 1. «A partir de 1886» é a adoção pela RFU (antes havia sistemas locais).
- **Q12** — cronologia confirmada no site oficial; «mais de dois séculos» sem verificação.
- **Q19** — nível 1 (Cinemateca) confirma; «cabine de projeção» e «frágil e inflamável» não estão nessa página.
- **Q70** — IFAB 2015 + Irish FA confirmam; as atas originais de 1890/1891 continuam por abrir.
- **Q25, Q79, Q82** — atribuições (Peralta García, NASA/Jamieson/Kowal e Drake, Colorado) confirmadas por leitura direta.

Sem triagem, mas com fonte de nível 1 **não aberta** pelo auditor (resposta correta e consistente com tudo o resto): **Q58** (Met, 429), **Q87** (Smithsonian, 403), **Q60** (só nível 2 aberto), **Q10** (Observatório de Paris não diz «polo ao equador» expressamente). Só nível 2 aberto, resposta sem dúvida: Q5, Q20, Q30, Q39, Q45, Q50, Q52, Q54, Q68, Q84, Q90, Q91, Q93, Q95, Q96, Q98, Q99, Q100, Q72.

## Padrões

1. **A confirmação de nível 1 é o ponto fraco, não o facto.** 26 de 59 só têm nível 2 aberto pelo auditor.
2. **Domínios a evitar** impedem o auditor de usar a fonte oficial (festival, IFAB, Cinemateca, Smithsonian); a triagem, que pode ver as fontes do banco, resolveu 8 de 9.
3. **Afirmações da explicação além da pergunta** (Q85, Q12, Q19, Q38): é aí que sobram frases sem suporte. Candidata a regra: cada afirmação da explicação precisa de fonte aberta, ou sai.

## Decisões para o Andre

1. Q85: tirar a 2.ª frase da explicação ou confirmar a secção 6(b). Qualquer mudança passa pelo verificador cego.
2. Q88: aceitar 1 fonte (o festival é o dono do troféu) ou pedir segunda fonte.
3. Antes de lançar: repetir a auditoria das 7 sem nível 1 aberto quando Met/Smithsonian/Britannica abrirem, ou aceitá-las.

Pelo critério do revisor («mais de 3 factos errados → corrigir o circuito primeiro») **não há factos errados**; o circuito falha em documentar a fonte, não em acertar. Lote 6 aguarda ordem do Andre.

TRAVÃO: ausente (0 erros em 59).

## Tempos
Registados em `auditoria-2026-11-18-tempos.csv` (31 invocações de reparação e auditoria). Não estão registados os blocos 1 a 4 do auditor (devolvidos antes de o registo ser iniciado); contam como lacuna, não como zero.

## Estado após o fecho das lacunas (18/11)
- Q12, Q19: cláusulas sem fonte retiradas (editor, tradutor, conferente com hash).
- Q85: 2.ª frase mantida, atribuída à VGHF; reaprovada com verificador, advogado (regra 29), editor, tradutor e conferente.
- Q38: data de 1886 retirada (só tinha uma fonte); fontes de nível 2 mantidas; independência entre Irish Times e rugbyfootballhistory.com não provada, só «até onde se verifica». Reaprovada.
- Q22: a opção en-US «Azulejo (glazed tile)» era pista só num idioma (regra 28); corrigida e reaprovada.
- Q88: **suspensa** (sem segunda fonte independente do festival).
- Hashes: conferente com hash em todas as aprovadas; verificador com hash repetido em Q8, Q9, Q33, Q22, Q38, Q85 (as que mudaram enunciado ou opções depois do verificador). As restantes 28 anteriores à regra 24 ficam com aviso, mas o auditor cego desta auditoria viu o enunciado e as opções atuais das 59 e concordou com todas.
