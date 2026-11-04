# Motor de factos

A linha de verificação da app de quiz: 8 agentes do Claude Code, 3 comandos, um esquema
de pergunta e dois scripts. Nenhuma pergunta chega ao banco sem duas fontes de domínios
diferentes, uma verificação às cegas, um advogado do diabo e uma validação automática.

## O que precisas

- Claude Code com pesquisa na web (WebSearch e WebFetch) ativa.
- Python 3.9 ou mais recente. Os scripts não precisam de pacotes externos.

## Instalar

1. Descompacta a pasta `motor-de-factos` onde quiseres.
2. Abre um terminal nessa pasta e corre `claude`.
3. O Claude Code lê o `CLAUDE.md` e encontra sozinho os agentes (`.claude/agents/`) e os
   comandos (`.claude/skills/`).

## Primeiro lote (1 a 2 horas tuas, a maior parte à espera)

```
/produzir-lote tema=historia n=10
```

No fim recebes um relatório em `relatorios/` e 5 perguntas aprovadas ao acaso para dares
o teu veredicto de gosto ("incrível", "boa", "fraca"). Mede no primeiro lote quanto
tempo e quanta utilização da subscrição cada pergunta gasta: cada uma passa por 4
agentes com pesquisa na web.

Depois do primeiro lote, pede também: "passa as três perguntas de `exemplos/` pela
linha". Foram verificadas na sessão de desenho, sem verificador independente, e por isso
estão em `em_verificacao`.

## Comandos

| Comando | Quando | O que faz |
| --- | --- | --- |
| `/produzir-lote tema=… n=…` | Sempre que precisares de perguntas | Pesquisador → verificador às cegas → advogado do diabo → editor → `validar.py` |
| `/auditar n=30` | Todas as semanas (n=100 antes de lançar) | Reverifica às cegas uma amostra; acima de 1% de erro, trava a publicação |
| `/manutencao` | Todas as semanas | Sentinela das perguntas com prazo, triagem dos reportes, calibração |

## Os 8 agentes

| Agente | Papel | Ferramentas |
| --- | --- | --- |
| `pesquisador` | Facto numa fonte de nível 1 ou 2 → pergunta, resposta, 3 distratores, explicação | WebSearch, WebFetch |
| `verificador-cego` | Responde sem ver a resposta, com fonte de outro domínio | WebSearch, WebFetch |
| `advogado-do-diabo` | Procura uma segunda resposta defensável e ambiguidades | WebSearch, WebFetch |
| `editor` | pt-PT, concisão, dificuldade, originalidade; não muda factos | WebSearch, WebFetch |
| `auditor` | Reverificação às cegas, com exigência de nível 1 | WebSearch, WebFetch |
| `sentinela` | Factos com prazo (recordes, cargos, populações) | WebSearch, WebFetch |
| `triagem` | Juiz final dos reportes e discordâncias, com causa raiz | WebSearch, WebFetch |
| `calibrador` | Lê as respostas reais e assinala perguntas suspeitas | Bash, Read |

A independência está garantida pelas ferramentas: nenhum agente de verificação consegue
ler ficheiros, por isso o verificador às cegas e o auditor não podem espreitar a
resposta no banco. Só o orquestrador (a sessão principal) escreve ficheiros.

Ideia a testar: correr o `verificador-cego` e o `auditor` com um modelo diferente do
`pesquisador` (campo `model:` no ficheiro do agente) para que os erros de um não se
repitam no outro. É uma suposição, não um facto medido.

## Scripts

```
python3 scripts/validar.py                      # valida banco/perguntas/
python3 scripts/validar.py exemplos             # valida os exemplos
python3 scripts/validar.py --dominio <url>      # domínio a registar numa fonte

python3 scripts/simular_respostas.py            # respostas fictícias para testar
python3 scripts/calibrar.py banco/respostas/simulado.csv
```

O `validar.py` recusa, entre outras coisas: menos de 2 fontes ou de 2 domínios, sites de
quiz ou trivia como fonte, a Wikipédia contada duas vezes, um verificador que usou um
domínio do pesquisador, opções repetidas, perguntas aprovadas sem as três aprovações,
mudanças factuais do editor sem nova verificação e perguntas sensíveis ao tempo sem
prazo.

O `calibrar.py` calcula, por pergunta, a taxa de acerto, a dificuldade real (1 a 5), um
rating ao estilo Elo e a discriminação. Discriminação negativa (os melhores jogadores a
errar mais do que os piores) é o sinal típico de chave errada. No teste com respostas
simuladas, assinalou a pergunta com a chave errada e a demasiado fácil, e o rating
acompanhou a dificuldade simulada (correlação de 0,98).

## Pastas

```
CLAUDE.md                  regras do projeto para o Claude Code
.claude/agents/            os 8 agentes
.claude/skills/            /produzir-lote, /auditar, /manutencao
esquema/pergunta.schema.json
regras/fontes.md           hierarquia de fontes
scripts/                   validar.py, calibrar.py, simular_respostas.py
banco/perguntas/           uma pergunta por ficheiro JSON
banco/respostas/           respostas dos jogadores (CSV)
banco/reportes.csv         reportes de erro dos jogadores (criado quando houver)
relatorios/                relatórios de lote, auditoria e manutenção
exemplos/                  3 perguntas de exemplo
```

## Limites que convém saber

- Nenhum sistema garante 0% de erros: este mede o erro, trava a publicação e corrige.
- As fontes de nível 1 também erram; quando duas discordam, a pergunta não avança.
- A qualidade do "gosto" (se a pergunta é incrível) continua a ser tua: os agentes
  garantem que está certa, não que é memorável.
