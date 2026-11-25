# Instruções da revisão (2.ª passagem, depois da auditoria 1)

A auditoria 1 devolveu 7 dos 10 lotes. Os defeitos encontrados foram estes, e é isto que
procuras em **todas** as perguntas do teu ficheiro:

1. **Nomes próprios em pt-PT errados ou do Brasil** (sobretudo nas perguntas `wd-…`, que vêm
   de etiquetas do Wikidata): «Managua» em vez de «Manágua», «São João» para St. John's
   (fica «Saint John's»), «Netuno» em vez de «Neptuno», nomes de animais brasileiros ou
   inventados («coruja-pequena» para Asio otus, que em Portugal é «bufo-pequeno»).
   Corrige só se tiveres a certeza da forma usada em Portugal; se não tiveres, **tira a
   pergunta**.
2. **Calques e erros de pt-PT**: «Batalha do Bulge» (é «Batalha das Ardenas»), «Que posição
   joga» (é «Em que posição joga»), concordância de género e número, «Nenhuns dos
   anteriores» (é «Nenhuma das anteriores»).
3. **Títulos**: mantém o título original de filmes, jogos, séries, álbuns e canções. Para
   obras de arte e clássicos da literatura com título português consagrado (ex.: «A Criação
   de Adão», «O Senhor das Moscas»), usa o título português **só se tiveres a certeza**.
4. **Pista num só idioma**: género, número, uma palavra comum ao enunciado e a uma só opção,
   ou a opção certa ser a única com forma diferente das outras, num idioma e não no outro.
5. **Ambiguidade**: mais de uma opção defensável (ex.: «animal mais rápido» sem dizer em
   voo ou em terra; «estreou» quando a estreia em Portugal foi noutro ano; «fundado» sem
   dizer que marco). Se não se resolve sem mudar o facto, **tira**.
6. **Datada** (a resposta pode ter mudado: nomes de séries de jogos, «é desenvolvido por»,
   recordes), **centrada nos EUA**, ou **trivial/obscura**: tira.
7. **Erros no en-US**: corrige gralhas evidentes de ortografia no en-US (ex.: «Lichtenstein» →
   «Liechtenstein», «H20» → «H2O», «Scorcese» → «Scorsese», espaços a mais). Não mudes o
   sentido, a resposta nem o facto.

Recebes, para cada pergunta, o texto nos dois idiomas e o índice da resposta certa (`c`).
Não mudes nunca qual é a resposta certa nem a ordem das opções. Não acrescentes factos.

## Saída (JSONL, uma linha por pergunta de entrada, pela mesma ordem)

- Fica igual: `{"id": "...", "acao": "manter"}`
- Corrigida: `{"id": "...", "acao": "corrigir", "pt": {"q": "...", "o": [4 opções]}, "en": {"q": "...", "o": [4 opções]}, "nota": "o que mudou"}`
  (dá sempre os dois idiomas completos, mesmo que só um mude)
- Tirada: `{"id": "...", "acao": "tirar", "motivo": "nome_pt|calque|pista|ambigua|datada|eua|trivial|facto", "nota": "..."}`

Na dúvida, tira. Enunciado até 200 caracteres, opções até 60, as quatro diferentes.
