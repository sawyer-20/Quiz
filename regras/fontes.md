# Regras das fontes

## Níveis

**Nível 1** — fontes primárias, oficiais e obras editoriais com revisão:
- institutos de estatística e organismos públicos (INE, Pordata, Eurostat, ONU, Banco
  Mundial, governos);
- legislação, documentos oficiais e arquivos nacionais;
- agências e instituições científicas (NASA, ESA, ESO, universidades, museus);
- artigos científicos publicados;
- enciclopédias editoriais (Britannica, Infopédia, Larousse, Treccani);
- sites oficiais das próprias entidades (federações, clubes, organizações, autores)
  para factos sobre elas.

**Nível 2** — fontes secundárias de qualidade:
- imprensa de referência;
- obras de referência publicadas e bases de dados especializadas reconhecidas;
- registos reconhecidos (por exemplo, Guinness World Records);
- Wikipédia: serve para **encontrar pistas**. Cita-se a fonte original que ela refere
  sempre que estiver acessível (abre-se e lê-se essa fonte). Só conta como fonte quando
  a original não está acessível e, mesmo então, no máximo como **uma** das fontes da
  pergunta e nunca em temas recentes ou contestados.

**Proibido como fonte:**
- sites de quiz, trivia e perguntas (Sporcle, JetPunk, FunTrivia, Kahoot, Quizlet,
  Open Trivia DB e semelhantes);
- blogues, fóruns, redes sociais, sites de "curiosidades" e agregadores de factos;
- conteúdo gerado por IA e a memória do modelo.

## Regras

1. Pelo menos duas fontes de domínios diferentes: uma encontrada pelo pesquisador e
   outra, independente, pelo verificador às cegas. Pelo menos uma de nível 1 sempre
   que exista.
2. Se uma fonte cita a outra, contam como uma.
3. A fonte tem de ter sido aberta e lida (WebFetch ou `scripts/ler_url.py`), não apenas vista
   num resultado de pesquisa.
4. Datas e números, no enunciado ou na explicação, só entram com duas fontes de acordo.
   Se divergirem, a pergunta passa a uma comparação que não dependa do valor exato, ou é
   rejeitada. Se a data ou o número não forem precisos para a pergunta, saem.
5. Factos que mudam (recordes, cargos, populações, "o maior", "o mais recente") levam
   data no enunciado ("Em 2025, …") ou `valida_ate`.
6. Definições ambíguas ficam explícitas no enunciado: dia sideral ou solar; maior em
   área ou em população; cidade ou área metropolitana; assinatura ou ratificação.
7. O excerto guardado tem no máximo 300 caracteres e serve só de prova interna.
8. Duas fontes de nível 1 em desacordo: a pergunta não avança.
9. Linguagem de dúvida **sem atribuição** na explicação ("ao que parece", "diz-se",
   "terá sido", "possivelmente"…): ou se confirma com fonte e se afirma, ou se atribui a
   quem o diz ("segundo os arqueólogos…", "Barros afirma que…"), ou sai. O `validar.py`
   recusa a dúvida sem atribuição e aceita a atribuída. Uma interpretação (um motivo, uma
   intenção, uma causa) só se apresenta como facto se as fontes a derem como facto; se as
   fontes a apresentam como interpretação de alguém, atribui-se.
10. Uma página pode dar ao pesquisador até 3 factos (3 perguntas). Cada pergunta continua
    a precisar da sua própria verificação às cegas, com fonte de outro domínio.

## Fontes de nível 1 por tópico (QUIZLUX)

Ponto de partida para o pesquisador, por tópico de arranque. Qualquer fonte de nível 1 vale
**em qualquer das duas línguas** (pt-PT ou en-US). A lista não substitui as regras acima: cada
facto continua a precisar de uma fonte aberta e lida, e a segunda fonte de outro domínio.

| Tópico | Fontes de nível 1 |
|---|---|
| General Knowledge | museus e bibliotecas nacionais, universidades, institutos de estatística, organismos públicos, enciclopédias editoriais (Britannica, Larousse, Treccani) |
| Geography | institutos de estatística e cartografia (INE, IGN, USGS, Eurostat), ONU, Banco Mundial, NOAA, atlas oficiais, serviços geológicos |
| World History | arquivos nacionais, museus (British Museum, Louvre, Smithsonian), universidades, edições críticas e fontes primárias, bibliotecas nacionais |
| Science | revistas científicas (Nature, Science, PNAS) e o seu texto original, universidades, NIH/NLM, CERN, laboratórios nacionais, IUPAC, NIST |
| Space | NASA, ESA, ESO, JAXA, Roscosmos, CNES, observatórios e missões (JPL, STScI), IAU |
| Movies | AMPAS (Oscars), Cannes, Berlinale, Veneza, American Film Institute, cinematecas, bases oficiais dos estúdios e dos festivais, Library of Congress |
| Music | sítios oficiais de artistas e editoras, Grammy/Recording Academy, Billboard e Official Charts (listas), bibliotecas e museus de música, universidades |
| Football | FIFA, UEFA, CONMEBOL, federações nacionais, sítios oficiais das ligas e dos clubes (para factos sobre eles), IFFHS e RSSSF só como apoio de nível 2 |
| Video Games | sítios oficiais dos estúdios e das plataformas (Nintendo, Sony, Microsoft, Valve), Guinness World Records (nível 2), arquivos como a Library of Congress e o Strong Museum of Play, universidades |
| Nature & Animals | IUCN, NOAA, USGS, serviços de vida selvagem, museus de história natural, revistas científicas, universidades, Smithsonian |

Para perguntas de interesse português, começa pela lista de `regras/fontes-pt.md`.
