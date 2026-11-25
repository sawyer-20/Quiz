# Instruções de triagem e tradução (importação Open Trivia DB → QUIZLUX)

Recebes um ficheiro JSONL de perguntas de escolha múltipla do Open Trivia DB (inglês).
Cada linha: `{"id", "cat", "dif", "q", "certa", "erradas": [3]}`.
Para cada linha escreves uma linha no ficheiro de saída (JSONL, uma linha por pergunta,
pela mesma ordem, nenhuma em falta).

## 1. Triagem (decidir se fica)

`"keep": false` com `"motivo"` (um destes códigos) quando:

- `eua` — exige conhecimento específico dos EUA que um jogador português médio não tem:
  estados, presidentes e política dos EUA, ligas e equipas americanas (NFL, NBA, MLB, NHL,
  futebol universitário), televisão e celebridades sobretudo americanas, marcas só dos EUA,
  unidades ou costumes americanos. Factos americanos de fama mundial (ex.: Apollo 11,
  Hollywood clássico, Elvis) ficam.
- `datada` — a resposta pode mudar com o tempo ou depende de quando foi escrita: «atual»,
  «mais recente», recordes, cargos, populações, classificações, «até hoje», contagens que
  crescem, factos sobre jogos/serviços que mudam com atualizações.
- `ambigua` — mais de uma opção é defensável, o enunciado é vago, a resposta certa parece
  errada ou discutível, ou depende de uma fonte/opinião.
- `lingua` — depende da língua inglesa (trocadilhos, ortografia, número de letras,
  expressões idiomáticas, «como se diz em inglês», siglas inglesas que não se traduzem).
- `trivial_obscura` — pormenor tão obscuro que ninguém sabe sem ter jogado/visto aquela
  obra específica (ex.: o peso de um objeto num videojogo, o nome de uma personagem
  secundária), ou pergunta-piada.
- `sensivel` — tragédia com menos de 10 anos, violência gratuita, tema de mau gosto, ou
  ligado ao retalho alimentar / cadeias de comida rápida / supermercados (marcas, mascotes).
- `fora_tema` — não cabe em nenhum dos 10 temas abaixo.

Na dúvida, rejeita. Preferimos perder uma pergunta boa a ficar com uma má.

## 2. Tema (se fica)

`"topic"`: exatamente um de `General Knowledge`, `Geography`, `World History`, `Science`,
`Space`, `Movies`, `Music`, `Football`, `Video Games`, `Nature & Animals`.

- `Space`: astronomia, planetas, estrelas, exploração espacial (mesmo que venha de
  «Science & Nature»).
- `Football`: só futebol (soccer). Outros desportos → `General Knowledge`.
- `Nature & Animals`: animais, plantas, ecossistemas.
- `Science`: física, química, biologia humana, matemática, informática, tecnologia.
- Mitologia, arte, literatura, línguas, comida, outros desportos → `General Knowledge`.
- Perguntas de videojogos que venham noutra categoria → `Video Games`.

## 3. Tradução para pt-PT (se fica)

- **Português europeu (Portugal), nunca do Brasil.** Ex.: «ecrã» e não «tela», «equipa» e não
  «time», «facto» e não «fato», «comboio» e não «trem», «telemóvel» e não «celular»,
  «utilizador» e não «usuário», «ficheiro» e não «arquivo», «registo» e não «registro»,
  «desporto» e não «esporte», «guarda-redes» e não «goleiro», «golo» e não «gol»,
  «Campeonato do Mundo» ou «Mundial» e não «Copa do Mundo», «económico», «género», «António»,
  «Antártida», «câmara», «contacto», «ação», «ótimo», «tu» em vez de «você». Sem gerúndio
  brasileiro («está a fazer», não «está fazendo»).
- Tradução fiel: mesmo facto, mesma pergunta, nada acrescentado nem retirado. Não corrijas
  o facto; se achares que está errado, rejeita com `ambigua`.
- **Títulos de obras** (filmes, jogos, séries, livros, álbuns, canções): mantém o título
  original tal como vem. Não inventes títulos portugueses.
- Nomes próprios de pessoas: como no original. Nomes de países, cidades, elementos, animais,
  planetas, etc.: forma portuguesa corrente em Portugal.
- Unidades: mantém as do original (não convertas números).
- Opções: traduz cada uma, **pela ordem: certa primeiro, depois as três erradas pela ordem
  recebida**. As opções traduzidas têm de continuar todas diferentes entre si e nenhuma pode
  passar a ser certa por causa da tradução.
- Se a tradução criar uma pista (género, número, concordância) que dê a resposta, reformula
  para a evitar; se não for possível, rejeita com `lingua`.
- Enunciado até 200 caracteres, opções até 60.

## Formato de saída (uma linha por pergunta)

Fica:
`{"id": "...", "keep": true, "topic": "Geography", "pt": {"q": "...", "o": ["certa", "errada1", "errada2", "errada3"]}}`

Sai:
`{"id": "...", "keep": false, "motivo": "eua"}`

JSON válido, UTF-8, sem texto fora das linhas.
