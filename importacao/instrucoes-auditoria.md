# Instruções da auditoria por amostra (pacote importado)

Recebes 50 perguntas de escolha múltipla, cada uma em pt-PT e en-US, **sem a resposta**.
O pt-PT é tradução automática do en-US (ou, nas perguntas `wd-…`, gerado a partir do
Wikidata). As opções estão pela mesma ordem nos dois idiomas (índices 0 a 3).

Para cada pergunta:

1. **Responde às cegas**: escolhe o índice da opção certa. Se não tiveres a certeza absoluta,
   pesquisa na web (WebSearch/WebFetch) e regista o URL que usaste. Não adivinhes: se não
   conseguires confirmar, `resposta: null`.
2. **Avalia**, sem favores:
   - `ambigua`: mais de uma opção é defensável, ou o enunciado é vago/enganador.
   - `nenhuma_certa`: nenhuma opção está certa (segundo fontes fiáveis).
   - `datada`: a resposta pode já ter mudado ou depende da data.
   - `traducao`: o pt-PT não diz o mesmo que o en-US (facto, pergunta ou sentido de uma opção),
     ou uma tradução torna a pergunta errada.
   - `brasil`: o pt-PT tem formas do português do Brasil (ex.: «time», «tela», «você»,
     «fato», «registro», «econômico», gerúndio «está fazendo», «Copa do Mundo»).
   - `pista`: género, número, concordância ou uma palavra do enunciado dá a resposta num só
     idioma.
   - `eua`: exige conhecimento específico dos EUA.
   - `texto`: erro de ortografia, gramática ou concordância em pt-PT que não seja `brasil`.
3. `nota`: uma frase curta quando assinalas alguma coisa (o que está mal e, se souberes, o que
   seria certo, com fonte).

Não leias nem escrevas nenhum ficheiro além da amostra que te indicam e do ficheiro de saída.

## Saída

Um ficheiro JSON com uma lista de 50 objetos, pela ordem da amostra:

`{"id": "...", "resposta": 2, "certeza": "alta|media|baixa", "fonte": "URL ou null", "problemas": ["traducao"], "nota": "..."}`

`problemas` é uma lista (vazia se nada). JSON válido.
