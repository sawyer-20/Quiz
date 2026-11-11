# Lote 2026-11-11 — misto

## Números

- 20 alvos (4 retomados + 16 novos), 25 perguntas criadas, **16 aprovadas** e 9 rejeitadas. Aprovadas por alvo: 16 de 20.
- Aprovadas: Q24, Q25, Q26, Q30, Q31, Q32, Q33, Q36, Q37, Q38, Q39, Q40, Q43, Q45, Q47, Q48. **Tema `portugal`: 4 aprovadas** (Q26, Q30, Q31, Q45; meta ≥4, cumprida), mais Q25 (música portuguesa).
- Rejeitadas: Q27 (retoma do Coubertin, 2.º ciclo), Q28 (Elevador da Glória: acidente com mortos em 2025), Q29 (fonte do verificador igual à do pesquisador), Q35 (opção «Obersee» defensável), Q34 (cópia: mesmo conjunto de opções que um quiz), Q41, Q42, Q44, Q46 (quota de clássicos do lote, regra 16).
- Fáceis (d1–2): 4 (Q31 trocou de 2 para 3 no editor; ficam Q36, Q38 e mais duas de dificuldade 2) — rever na calibração.
- Fonte de nível 1 do pesquisador: 21 de 25 (84%); nas aprovadas, 14 de 16 (88%).
- **Clássicos: 2 de 16 não rejeitadas (12%; meta ≤20%, cumprida). No banco inteiro: 8 de 27 aprovadas (30%)**; a quota só se aplica a partir de 100.
- Tempo de agentes por pergunta aprovada: **5,7 min** (90,6 min em 65 invocações, correções incluídas). **Tempo de relógio do lote: 4,9 h**, com uma pausa por limite de utilização.
- `validar.py`: 0 erros.

## Problemas

- A **independência da verificação** falhou várias vezes: o verificador devolveu o mesmo artigo republicado noutro domínio (Q30: BiblioAsia/Embaixada; Q37: Nature/PMC) ou o mesmo artigo do pesquisador (Q29). O advogado apanhou-os; a regra de domínios não chega.
- **Sensibilidade só apanhada no advogado:** Q28 (acidente do elevador) passou pesquisador, originalidade e verificador. Proponho verificar «tragédia recente» já no passo 0.
- **Verificação fraca em factos de nicho:** 11 das 16 aprovadas têm a fonte do verificador só de nível 2 e confiança média (Q39, Q40, Q45 e Q48 sem nível 1 de ponta a ponta).
- O editor acrescentou um ponto final a uma opção (Q36); corrigi antes de aprovar. O texto das opções não pode mudar.
- Alvo 12 (geografia fácil) falhou 3 vezes (cópia, clássico, clássico) e ficou por preencher.
- A **edição crítica do *Esmeraldo* (Gulbenkian) não abriu**: Q26 apoia-se no texto português de 1892 (archive.org), que o advogado leu.

## Fontes portuguesas de nível 1

- **Abertas:** DGPC (imovel.patrimoniocultural.gov.pt), Univ. Coimbra (visit.uc.pt), BNP (purl.pt), revista Ler (U. Porto), ISCTE-IUL, Museu de Marinha, Enciclopédia da Expansão (FCSH-NOVA), DHLab (FCSH-NOVA), LNEG, Governo dos Açores, DGT, Geoparque Açores, U. Aveiro (Comunicarte), mnmusica.gov.pt (institucional).
- **Recusadas ou com falha:** monumentos.gov.pt (DNS/reset), uc.pt e noticias.uc.pt (403), baes.uc.pt (502), Infopédia (403), geossitios.progeo.pt (404), museunacionaldamusica.gov.pt (404), siaram.azores.gov.pt (403), repositorio.lneg.pt e repositorium.uminho.pt (reset), matrizpci e ccmm.madeira (timeout). Lista completa em `regras/fontes-pt.md`.

## Decisões para o Andre

1. **`main` como ramo por omissão:** criei o `main` (igual ao estado do ramo de trabalho), mas as ferramentas desta sessão não mudam o ramo por omissão: faz-se em Settings → Branches. O pedido de merge das regras novas é o [PR #1](https://github.com/sawyer-20/Quiz/pull/1).
2. **Q29** (horizonte artificial de Gago Coutinho): há 2.ª fonte independente (Boletim da SPM). Retomo no lote 4, mesmo fora da regra 15?
3. **Alvo 12** (geografia fácil): desisto ou tento outro ângulo (países/capitais) no lote 4?
4. **Regras novas a aprovar:** (a) o verificador não pode usar republicações da fonte do pesquisador (o orquestrador passa também o título do artigo, não só os domínios); (b) sensibilidade (tragédias recentes) verificada no passo 0; (c) o `passo` de edição recusa mudanças às opções. Entram por PR para o `main`?
5. **Q26 e a edição da Gulbenkian:** aceitas o texto de 1892 como fonte, ou fico à espera da edição crítica?

## Cinco perguntas ao acaso (diz «incrível», «boa» ou «fraca»)

- Q-2026-000026 — Segundo Pacheco Pereira, o que viu Dias que o levou a dar o nome «Boa Esperança» ao cabo? (a costa a virar para norte e nordeste)
- Q-2026-000030 — De que palavra portuguesa vem o malaio «minggu»? (domingo)
- Q-2026-000033 — Que objeto serviu de recibo fiscal no Tesouro inglês e, queimado em 1834, incendiou o Parlamento? (varas de madeira entalhadas)
- Q-2026-000037 — Que ave dorme em pleno voo, segundo o EEG de 2016? (fragata-grande)
- Q-2026-000036 — O que mantém a gota afastada da chapa muito quente? (almofada de vapor, efeito Leidenfrost)

## Canários

Perguntas com a resposta errada marcada de propósito. Nunca entram no banco.

- **C1.** Que parte do olho humano não tem vasos sanguíneos e obtém oxigénio diretamente do ar?
  Opções: Íris · Coroide · Córnea · Retina
  Resposta errada marcada: **Coroide** · Resposta verdadeira: Córnea (fontes do pesquisador: PMC/NIH; EyeWiki da Academia Americana de Oftalmologia)
  Resultado do verificador: respondeu **Córnea** (a verdadeira), confiança alta, fonte Duane's Ophthalmology. **Rejeitou o canário.**

- **C2.** Porque é que no fundo do mar Negro há naufrágios de madeira com milhares de anos tão bem conservados?
  Opções: As águas profundas não têm oxigénio · As águas do fundo são aquecidas por vulcões · A salinidade é altíssima, como no mar Morto · O fundo está coberto de gelo todo o ano
  Resposta errada marcada: **O fundo está coberto de gelo todo o ano** · Resposta verdadeira: As águas profundas não têm oxigénio (fontes do pesquisador: Universidade de Southampton; National Geographic)
  Resultado do verificador: respondeu **As águas profundas não têm oxigénio** (a verdadeira), confiança alta, fonte Smithsonian Magazine. **Rejeitou o canário.**
