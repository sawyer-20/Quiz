# Lote 2026-11-06 — misto

## Números

- 10 perguntas criadas (Q-2026-000014 a 000023): **6 aprovadas** (14, 16, 19, 20, 21, 22) e **4 rejeitadas**.
- Rejeições: Q23 (verificador: medalha de arte, o COI não a reconhece como olímpica, sem nível 1); Q15, Q17 e Q18 (advogado, no 2.º ciclo de correção: regra 14).
- Dificuldade das aprovadas: 1 fácil (Q16), 2 fáceis-médias (Q14, Q19, Q22), 3 médias (Q20, Q21). **Fáceis (d1–2): 4** (meta ≥3: cumprida).
- Fonte de nível 1 do pesquisador: 9 de 10 (90%); nas aprovadas, 6 de 6.
- Clássicos (indicador, meta até 20%): **3 de 6 não rejeitadas (50%)**: Q14, Q16, Q20. Meta falhada. No banco: 6 de 11 (55%); a quota só se aplica a partir de 100.
- Tempo de agentes por pergunta aprovada: **6,3 min** (37,8 min em 27 invocações, sem pausas por limite). Registo de tempos incompleto nalgumas invocações de correção.
- Canários: **2 de 2 rejeitados** pelo verificador (ver abaixo). O lote não parou.
- `validar.py`: 0 erros no banco.

## Problemas

- Duas passagens do advogado esgotaram o ciclo: Q15, Q17, Q18 foram reformuladas e voltaram com novas fragilidades. Q15: a 2.ª fonte independente é só uma citação indireta (USP); Q17: o motivo do sufixo «-ium» é interpretação (RSC afirma, LANL e Jensen 2004 dizem que não está documentado); Q18: «dedicou» impreciso (dedicatória «à memória»).
- Q19 e Q20 têm fonte do verificador só de nível 2 (filmSPOT; EBSCO). Q19 perdeu o blogue apaladewalsh.com como fonte e foi reverificada.
- Duas explicações reformuladas pelo advogado passaram o limite de 300 caracteres (Q15, Q17); o pesquisador encurtou-as.

## Fontes portuguesas de nível 1

- **Abertas e lidas:** DGEG (Roteiro das Minas), Geopark Estrela (PDF), cinemateca.pt, RTP Arquivos, Lusopédia, BNP, ciencia.ucp.pt, livros.fcsh.unl.pt (CHAM), maislisboa.fcsh.unl.pt, institutodehistoriadaarte.com (NOVA FCSH), mediacoes.ese.ips.pt (IPS), repositorio-aberto.up.pt, portugal.gov.pt, museusemonumentos.pt (instável), culturaportugal.gov.pt, casadasciencias.org, mic.pt (nível 2).
- **Recusadas ou com falha:** Infopédia (403, sistemática), Britannica (403), parquesnaturais.azores.gov.pt (403), repositorioaberto.uab.pt (403), repositorio.ucp.pt (403), sigarra.up.pt (403), repositorio.ipcb.pt (403), tnsc.pt (404), museunacionaldoazulejo.pt (404), comiteolimpicoportugal.pt (404), museudoazulejo.gov.pt e nautilus.fis.uc.pt (erro de rede), run.unl.pt (ENOTFOUND), visitportugal.com (anti-bot), homepages.uc.edu (certificado inválido; não contornado), revistas.usp.br (redirecionamento recusado pelo leitor, mas lido noutro URL).
- Não tentadas: INE, Pordata, Museu do Fado, Gulbenkian, ICA, IPDJ.

## Decisões para o Andre

1. **Merge.** Pediste o merge da v1.1 quando o banco validasse sem erros: valida (0 erros). Mas o repositório só tem o ramo `claude/wizardly-shannon-stwi4b` (sem ramo principal para onde fundir). Queres que crie um ramo principal, ou que abra um pedido de merge noutro destino?
2. **Alvo Dias / Pacheco Pereira (Q15)** falhou por falta de 2.ª fonte independente. Proponho voltar ao pesquisador com a edição crítica do Esmeraldo (Barradas de Carvalho, Gulbenkian) como fonte. Autorizas?
3. **Sinédrio (000013):** continua rejeitada; não apareceu fonte de nível 1 acessível para 1818.
4. **Q17, Q18 e Q23** podem voltar como alvos novos com outro ângulo (por ex. Q23 sem «medalha olímpica»). Queres?
5. **Clássicos a 50% no lote:** o pesquisador continua a preferir factos de manual (Q14 foi alvo teu). Reforço a regra ou aceitas?

## Cinco perguntas ao acaso (diz «incrível», «boa» ou «fraca»)

- Q-2026-000020 — Nobel da Literatura de 1902 (Mommsen): «Que obra a Academia Sueca destacou?»
- Q-2026-000019 — incêndio de 1981 na Cinemateca: «Qual foi a origem do incêndio?»
- Q-2026-000014 — cacau como moeda nos mercados astecas.
- Q-2026-000021 — país de origem do professor do Real Instituto de Surdos-Mudos e Cegos.
- Q-2026-000016 — serra do ponto mais alto de Portugal continental.

## Canários


Perguntas com a resposta errada marcada de propósito. Nunca entram no banco. Vão misturadas ao verificador às cegas, sem resposta.

- **C1.** Que mar é o único do mundo sem qualquer costa, delimitado apenas por correntes oceânicas?
  Opções: Mar da Arábia · Mar de Coral · Mar dos Sargaços · Mar de Barents
  Resposta errada marcada: **Mar de Coral** · Resposta verdadeira: Mar dos Sargaços (fontes do pesquisador: NOAA National Ocean Service; Sargasso Sea Commission)
  Resultado do verificador: respondeu **Mar dos Sargaços** (a verdadeira), confiança alta, fonte da Convenção sobre a Diversidade Biológica (ONU). **Rejeitou o canário** (não escolheu a errada marcada).

- **C2.** Para estimar a idade dos tubarões-da-gronelândia, os cientistas dataram por carbono proteínas de que parte do corpo?
  Opções: Dos dentes · Das vértebras · Do fígado · Dos olhos (cristalino)
  Resposta errada marcada: **Do fígado** · Resposta verdadeira: Dos olhos (cristalino) (fontes do pesquisador: NOAA National Ocean Service; Nielsen et al., Science 2016 (Oxford Research Archive))
  Resultado do verificador: respondeu **Dos olhos (cristalino)** (a verdadeira), confiança alta, fonte da Universidade de Copenhaga. **Rejeitou o canário** (não escolheu a errada marcada).

