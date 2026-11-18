# QUIZLUX: demonstração do modo solo (Flutter)

Modo solo offline, pt-PT e en-US: escolher tópico (ou misto), até 10 perguntas com 4 opções,
temporizador de 20 s, pontuação (100 por resposta certa + até 100 de bónus pela rapidez) e ecrã
de resultado com revisão. Tudo em JSON local (`assets/perguntas.json`), sem backend.

## Dados
`python3 scripts/exportar_app.py` (na raiz do repositório) copia do banco só as perguntas
`aprovada` ou `publicada`, nos dois idiomas. As suspensas, rejeitadas e em verificação ficam de fora.
Não escreve texto factual: copia o que está no banco.

## Compilar
```bash
cd app
flutter pub get
flutter test
flutter build web --release --no-web-resources-cdn   # web
flutter build apk --release                          # Android (APK assinado com a chave de debug)
```
Testado com Flutter 3.50.0 e Android SDK 35.

## Paleta
Provisória, em `lib/tema.dart`. A paleta e as boards oficiais do design não estão no repositório.
