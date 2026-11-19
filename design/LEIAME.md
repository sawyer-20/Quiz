# Design QUIZLUX

As boards chegaram a 19/11/2026: `quizlux-design.zip` (original) e `boards/` (os ecrãs em HTML:
Brand, Splash, Home, Topics, Duels, Question, States, Result, Profile, CreateChallenge, mais `canvas.json`
e `gen.py`, o gerador). O modo solo implementa Splash, Topics (lista), Gameplay, Answer states e Result.
Ficam por fazer: Home com XP e níveis, Duels, Profile e Create a challenge (precisam de backend).

## Tokens aplicados (indicados pelo Andre em 19/11/2026)

| Papel | Cor |
|---|---|
| Fundo | `#0B1428` |
| Superfície | `#152747` e `#1C345A` |
| Dourado | `#C6A45A` e `#E5CD8F` |
| Azul | `#4389D9` |
| Texto | `#F5F5F2` |
| Secundário | `#AABBD5` |
| Linha | `#26426B` |
| Certo | `#4CC38A` |
| Errado | `#E26D6D` |

Fontes: **Manrope** na interface e **Cormorant Garamond** nos momentos de marca (título e pontuação
final). Ambas em licença SIL OFL, incluídas em `app/assets/fonts/` com as licenças.

Implementação: `app/lib/tema.dart` (cores e estilos) e `app/pubspec.yaml` (fontes).
