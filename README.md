# Motor de factos (versão 1.1)

A linha de verificação da app de quiz: 9 agentes do Claude Code, 3 comandos, um esquema
de pergunta e os scripts de validação, aprovação e leitura. Nenhuma pergunta chega ao
banco sem duas fontes de domínios diferentes, uma verificação de originalidade, uma
verificação às cegas (testada com canários), um advogado do diabo e uma aprovação
automática.

## O que mudou na 1.1

- Nova linha: pesquisador → **originalidade** → verificador às cegas → advogado do diabo
  → editor → **`scripts/aprovar.py`**.
- A originalidade mede o texto, não o facto: factos clássicos entram com enunciado
  próprio e a etiqueta `classico` (nunca em dificuldade 4 ou 5; no máximo 20% do banco,
  aplicado a partir de 100 perguntas; no lote é só um indicador).
- O editor só mexe no estilo; se for preciso mudar o que se pergunta, a pergunta é
  rejeitada com motivo `reescrever`.
- O verificador, o advogado e o editor trabalham em blocos de até 5 perguntas; o
  pesquisador pode tirar até 3 factos da mesma página.
- O orquestrador nunca escreve texto factual, nunca regista um veredicto que nenhum
  agente deu, e só o `aprovar.py` aprova.
- Wikipédia só para pistas; datas e números com duas fontes; sem linguagem de dúvida sem
  atribuição; interpretações só como facto se as fontes as derem como facto.
- 2 canários por lote (perguntas com a resposta errada de propósito) para testar o
  verificador às cegas.
- Os agentes leem páginas com `scripts/ler_url.py` (só http/https públicos) e um hook
  recusa-lhes qualquer outro comando.

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
tempo e quanta utilização da subscrição cada pergunta gasta: cada uma passa por 5
agentes com pesquisa na web. O relatório traz o tempo de agentes por pergunta aprovada.

Depois do primeiro lote, pede também: "passa as três perguntas de `exemplos/` pela
linha". Foram verificadas na sessão de desenho, sem verificador independente, e por isso
estão em `em_verificacao`.

## Comandos

| Comando | Quando | O que faz |
| --- | --- | --- |
| `/produzir-lote tema=… n=…` | Sempre que precisares de perguntas | Pesquisador → originalidade → verificador às cegas → advogado do diabo → editor → `aprovar.py` |
| `/auditar n=30` | Todas as semanas (n=100 antes de lançar) | Reverifica às cegas uma amostra; acima de 1% de erro, trava a publicação |
| `/manutencao` | Todas as semanas | Sentinela das perguntas com prazo, triagem dos reportes, calibração |

## Os 9 agentes

| Agente | Papel | Ferramentas |
| --- | --- | --- |
| `pesquisador` | Até 3 factos por página, em fontes de nível 1 ou 2 → pergunta, resposta, 3 distratores, explicação; redige correções | WebSearch, WebFetch, Bash* |
| `originalidade` | Mede o texto (não o facto): `original`, `classico` ou `copiada`, em blocos de até 5 | WebSearch, WebFetch, Bash* |
| `verificador-cego` | Responde sem ver a resposta, com fonte de outro domínio, em blocos de até 5 | WebSearch, WebFetch, Bash* |
| `advogado-do-diabo` | Procura segunda resposta, ambiguidades, datas e números sem segunda fonte, linguagem de dúvida; blocos de até 5 | WebSearch, WebFetch, Bash* |
| `editor` | Só estilo: pt-PT, concisão, explicação, dificuldade; não muda o que se pergunta nem as opções | WebSearch, WebFetch, Bash* |
| `auditor` | Reverificação às cegas, com exigência de nível 1 | WebSearch, WebFetch, Bash* |
| `sentinela` | Factos com prazo (recordes, cargos, populações) | WebSearch, WebFetch, Bash* |
| `triagem` | Juiz final dos reportes e discordâncias, com causa raiz | WebSearch, WebFetch, Bash* |
| `calibrador` | Lê as respostas reais e assinala perguntas suspeitas | Bash, Read |

\* O Bash serve só para o leitor de páginas `scripts/ler_url.py`: no ambiente cloud o
WebFetch não tem rede. O hook `.claude/hooks/travao_agentes.py` recusa a estes agentes
qualquer outro comando e qualquer ferramenta de ficheiros, por isso o verificador às
cegas e o auditor continuam sem conseguir espreitar a resposta no banco. O leitor só
aceita http/https públicos: recusa `file://`, `localhost` e endereços de rede privada
(`python3 scripts/testar_ler_url.py` testa-o). Lê HTML, texto e PDF (com o `pdftotext`,
se estiver instalado) e avisa no topo quando o texto é cortado. Só o orquestrador (a sessão principal)
escreve ficheiros, e nunca texto factual.

Ideia a testar: correr o `verificador-cego` e o `auditor` com um modelo diferente do
`pesquisador` (campo `model:` no ficheiro do agente) para que os erros de um não se
repitam no outro. É uma suposição, não um facto medido.

## Scripts

```
python3 scripts/validar.py                      # valida banco/perguntas/
python3 scripts/validar.py exemplos             # valida os exemplos
python3 scripts/validar.py --dominio <url>      # domínio a registar numa fonte
python3 scripts/aprovar.py Q-2026-000005        # a única forma de aprovar
python3 scripts/estatisticas_lote.py <lote>     # números do relatório
python3 scripts/testar_ler_url.py [--rede]      # testes do leitor de páginas
python3 scripts/testar_validar.py               # testes das regras de texto

python3 scripts/simular_respostas.py            # respostas fictícias para testar
python3 scripts/calibrar.py banco/respostas/simulado.csv
```

O `validar.py` recusa, entre outras coisas: menos de 2 fontes ou de 2 domínios, sites de
quiz ou trivia como fonte, a Wikipédia contada duas vezes, um verificador que usou um
domínio do pesquisador, opções repetidas, perguntas aprovadas sem as três aprovações,
mudanças factuais do editor sem nova verificação, perguntas sensíveis ao tempo sem
prazo, linguagem de dúvida sem atribuição na explicação, clássicos em dificuldade 4 ou 5 ou acima de 20%
do banco (a partir de 100 perguntas) e perguntas aprovadas sem o evento `aprovada por aprovar.py`.

O `calibrar.py` calcula, por pergunta, a taxa de acerto, a dificuldade real (1 a 5), um
rating ao estilo Elo e a discriminação. Discriminação negativa (os melhores jogadores a
errar mais do que os piores) é o sinal típico de chave errada. No teste com respostas
simuladas, assinalou a pergunta com a chave errada e a demasiado fácil, e o rating
acompanhou a dificuldade simulada (correlação de 0,98).

## Pastas

```
CLAUDE.md                  regras do projeto para o Claude Code
.claude/agents/            os 9 agentes
.claude/hooks/             travão de independência dos agentes
.claude/skills/            /produzir-lote, /auditar, /manutencao
esquema/pergunta.schema.json
regras/fontes.md           hierarquia de fontes
scripts/                   validar.py, aprovar.py, ler_url.py, estatisticas_lote.py,
                           calibrar.py, simular_respostas.py, testar_ler_url.py
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
