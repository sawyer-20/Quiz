# Auditoria do histórico das 15 aprovadas do lote 4 (17/11/2026)

Pergunta a pergunta: sequência final de agentes antes de `aprovar.py`, veredicto de cada agente e dependência de relatórios malformados (regra 23).

| Pergunta | Sequência final (último evento de cada agente) | Verificador | Advogado | Editor | Conferente | Malformado? |
|---|---|---|---|---|---|---|
| Q50 | pesquisador → originalidade → verificador-cego → orquestrador → editor → tradutor → conferente → aprovar.py | True (media) | — | True | True 2026-11-13 | não |
| Q52 | pesquisador → originalidade → verificador-cego → advogado-do-diabo → editor → tradutor → conferente → aprovar.py | True (media) | True | True | True 2026-11-13 | não |
| Q56 | pesquisador → originalidade → verificador-cego → advogado-do-diabo → editor → tradutor → conferente → aprovar.py | True (alta) | True | True | True 2026-11-13 | não |
| Q60 | pesquisador → originalidade → verificador-cego → advogado-do-diabo → editor → tradutor → conferente → aprovar.py | True (media) | True | True | True 2026-11-13 | sim, repetido |
| Q61 | pesquisador → originalidade → verificador-cego → advogado-do-diabo → editor → tradutor → conferente → aprovar.py | True (alta) | True | True | True 2026-11-13 | sim, repetido |
| Q67 | pesquisador → originalidade → verificador-cego → advogado-do-diabo → editor → tradutor → conferente → aprovar.py | True (alta) | True | True | True 2026-11-13 | não |
| Q69 | pesquisador → originalidade → verificador-cego → advogado-do-diabo → editor → tradutor → conferente → aprovar.py | True (media) | True | True | True 2026-11-13 | não |
| Q70 | pesquisador → originalidade → verificador-cego → advogado-do-diabo → editor → tradutor → conferente → aprovar.py | True (media) | True | True | True 2026-11-13 | não |
| Q72 | pesquisador → originalidade → verificador-cego → advogado-do-diabo → editor → tradutor → conferente → aprovar.py | True (media) | True | True | True 2026-11-13 | não |
| Q73 | pesquisador → originalidade → verificador-cego → advogado-do-diabo → editor → tradutor → conferente → aprovar.py | True (alta) | True | True | True 2026-11-13 | não |
| Q77 | pesquisador → originalidade → verificador-cego → advogado-do-diabo → editor → tradutor → conferente → aprovar.py | True (alta) | True | True | True 2026-11-13 | não |
| Q79 | pesquisador → originalidade → verificador-cego → advogado-do-diabo → editor → tradutor → conferente → aprovar.py | True (alta) | True | True | True 2026-11-13 | não |
| Q82 | pesquisador → originalidade → orquestrador → editor → verificador-cego → advogado-do-diabo → tradutor → conferente → aprovar.py | True (media) | True | True | True 2026-11-17 | sim, repetido |
| Q84 | pesquisador → originalidade → orquestrador → editor → verificador-cego → advogado-do-diabo → tradutor → conferente → aprovar.py | True (media) | True | True | True 2026-11-17 | sim, repetido |
| Q85 | pesquisador → originalidade → orquestrador → editor → verificador-cego → advogado-do-diabo → tradutor → conferente → aprovar.py | True (alta) | True | True | True 2026-11-17 | sim, repetido |

Limitação: o histórico regista o evento e a data, não uma impressão digital do texto que cada agente viu. Por isso a confirmação de que o conferente viu o texto aprovado é feita repetindo a conferência cega sobre o texto final de cada ficheiro (ver relatório do lote).
