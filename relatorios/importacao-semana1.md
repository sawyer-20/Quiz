# Importação da Semana 1 — relatório (25/11/2026)

## Números

**1.999 perguntas limpas, pt-PT e en-US**, em pacote separado (`importacao/pacote.json` e
`app/assets/importadas.json`). As 57 verificadas continuam à parte, como pacote do Daily 10.

| Tema | Total | Open Trivia DB | Wikidata | ≥ 150 |
|---|---:|---:|---:|:-:|
| Cultura geral | 308 | 308 | 0 | sim |
| Geografia | 287 | 194 | 93 | sim |
| Ciência | 281 | 281 | 0 | sim |
| Música | 255 | 255 | 0 | sim |
| Futebol | 187 | 37 | 150 | sim |
| Videojogos | 186 | 186 | 0 | sim |
| História | 181 | 181 | 0 | sim |
| Cinema | 151 | 151 | 0 | sim |
| Espaço | 88 | 35 | 53 | **não** |
| Natureza e animais | 75 | 39 | 36 | **não** |

Funil (facto verificado nos ficheiros): 5.299 verificadas no Open Trivia DB → 2.961 após o
pré-filtro (sem V/F, 8 categorias fora dos temas, palavras dos EUA/datadas, 542 videojogos
excedentes) → 1.826 após triagem e tradução → mais 681 do gerador Wikidata (com tetos por
molde) → 1.999 após revisão e auditorias (662 corrigidas; 169 triviais, 26 ambíguas, 24 nomes
pt incertos e 77 tiradas por auditoria, entre outras; as outras 16 assinaladas já tinham saído na revisão).

Espaço e Natureza ficam abaixo de 150 por decisão de âmbito de 25/11: reforço depois do teste.

## Auditorias (cegas, 50 por lote, erro > 5% devolve o lote)

O auditor responde sem a chave e assinala ambiguidade, datada, tradução, formas do Brasil,
pista num só idioma, EUA e erros de texto em pt-PT. Gralhas só no en-US contam à parte.

| Ronda | Lotes | Aceites | Devolvidos | Erro médio | Gralhas só en-US |
|---|---:|---:|---:|---:|---:|
| 1 | 10 | 3 | 7 (Futebol 22%, Natureza 20%, Espaço 16%, História 12%, Cultura geral 10%, Geografia 6%, Videojogos 6%) | 10,2% | não medido |
| 2 (depois da revisão, amostras novas) | 10 | 9 | 1 (Ciência 6%) | 3,0% | 4,2% |
| 3 (Ciência, depois de 3.º ciclo) | 1 | 1 | 0 | 2% | 8% |

- **Respostas erradas: 0 em 1.050.** Em nenhuma pergunta auditada a resposta às cegas
  contrariou a chave. Os defeitos foram ambiguidade, tradução e texto, não a resposta.
- Causa da ronda 1: sobretudo o gerador Wikidata (anéis e sondas tratados como luas, Bola de
  Ouro feminina, nomes de clubes e etiquetas pt do Brasil, gramática dos moldes) e pt-PT pouco
  natural. Corrigi o gerador, tirei o molde «nome científico» e revi o pacote todo.
- Todas as perguntas assinaladas em qualquer ronda saíram do pacote.

## Problemas conhecidos

1. **Gralhas no en-US** (4,2% na ronda 2; 8% na Ciência da ronda 3): vêm do original do Open
   Trivia DB. Não afetam o teste fechado em pt-PT; recomendo uma revisão do en-US antes de
   qualquer lançamento público. (Estimativa, a partir das amostras.)
2. **Perguntas repetidas entre fontes** no Futebol (ex.: Euro 2016 no Open Trivia DB e no
   Wikidata). A deduplicação só apanha enunciados iguais.
3. **Moldes do Wikidata** são repetitivos (capitais, luas, vencedores): 332 das 1.999.
4. **Explicação**: as importadas não têm explicação; a app mostra só a fonte.
5. A app foi alterada para ler o pacote, mas **não foi compilada nesta sessão** (sem Flutter).

## Decisões do Andre

1. Fundir o PR (motor de importação, pacote e ligação à app).
2. Nada mais: a decisão sobre Espaço e Natureza já foi tomada (ficam abaixo de 150 no teste).
