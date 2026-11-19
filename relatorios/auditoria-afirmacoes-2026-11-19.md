# Auditoria de afirmações nas 58 explicações — 19/11/2026

Pedido do Andre: para cada explicação, listar cada afirmação factual e confirmar que há fonte **no
ficheiro** que a suporta (regra 29). Q95 e Q98 já tinham mostrado que a resposta pode estar certa e a
explicação errada.

Método: 12 invocações do advogado do diabo (blocos de 5, a última de 3), com instruções de listar
cada afirmação, abrir ele próprio as páginas do ficheiro e classificar `total`, `parcial` ou
`nenhum`. Não podia usar fontes de fora do ficheiro. (A Q95 e a Q98 foram incluídas já na versão
corrigida.)

## Números
- 58 explicações auditadas. **9 tinham pelo menos uma afirmação sem apoio total** (16%); 49 passaram
  com todas as afirmações apoiadas.
- Nenhuma resposta estava errada. Os problemas são afirmações a mais na explicação (detalhes
  acrescentados que nenhuma fonte do ficheiro diz) ou atribuídas à pessoa errada.
- Mais duas já corrigidas antes desta auditoria: Q95 («regressar a Viena») e Q98 (data sem fonte).

## As 9 com problema
| Pergunta | Afirmação sem apoio | Origem |
|---|---|---|
| Q5 | «cerca de 70 metros» (a fonte dá 68,38 m) e «nove painéis»: só na Wikipédia | pormenor acrescentado |
| Q30 | «passou a designar» a semana: nenhuma fonte descreve essa mudança de sentido | inferência |
| Q33 | «uma metade ficava com o Tesouro, a outra com quem pagava»: nenhuma fonte atribui as metades | pormenor acrescentado |
| Q36 | «a base da gota evapora»: as fontes não localizam a evaporação | pormenor acrescentado |
| Q47 | «saliente… no topo das muralhas»; e a introdução pelos Templários atribuída a Mário Barroca (vem do Guia do IHRU) | pormenor e atribuição errada |
| Q52 | grego como chave para decifrar «as duas escritas» (só os hieróglifos têm apoio) | extrapolação |
| Q62 | Voyager 1 «seguiu uma trajetória mais rápida»: nenhuma fonte o diz | inferência |
| Q68 | «só com velas» (a Zeiss diz «sem luz adicional») e «Kubrick comprou três» (foi o produtor Jan Harlan) | pormenor e atribuição |
| Q91 | a **opção certa** diz «gradiente original» em três dias; o resumo do estudo diz que recuperaram o gradiente em 3 dias e que há «pouca diferença do original» às 2 semanas | opção, não explicação |

## Correção aplicada
As oito primeiras (Q5, Q30, Q33, Q36, Q47, Q52, Q62, Q68): editor (só explicação, tirando ou
atribuindo o que não tinha apoio), tradutor, advogado (volta a quem reprovou, regra 13), conferente
e `aprovar.py`. Resultado no fim deste ficheiro.

**Q91 por decidir (Andre):** o desvio está no texto da opção certa. Mudar uma opção obriga a repetir
a pergunta a partir do verificador cego. Recomendo reformular a opção («Voltaram a criar o gradiente
de tamanho dos objetos») em vez de a deixar mais forte do que o estudo; até lá, fica aprovada mas
fora de qualquer versão pública.

## Avisos menores (sem alteração)
- Q9: os dias da semana («quarta-feira», «quinta-feira») e «a Escócia já o fazia desde 1600» só
  têm apoio na Wikipédia.
- Q61: «apenas vestígios» de tecnécio na natureza: as fontes não são unânimes («não ocorre
  naturalmente» contra «vestígios»).
- Q84: «é o jogo com mais golos da história dos Mundiais, segundo a FIFA»: a página da FIFA é de
  2018; imprensa indica que o Mundial de 2026 não o superou, mas não há fonte de nível 1 no ficheiro.
  Sugestão: acrescentar «até 2018» na explicação.
- Q72: o «Physics FAQ da Universidade da Califórnia em Riverside» está alojado na UCR mas é
  uma página de Philip Gibbs (1997); a atribuição à universidade é de alojamento.
- Q85: a explicação fala do Copyright Office e o enunciado da Bibliotecária do Congresso; a
  Bibliotecária adotou a recomendação da Registadora (Federal Register), por isso é compatível.

## Padrão e regra
Quase todas as falhas vêm do mesmo sítio: o pesquisador ou o editor acrescenta um pormenor
verosímil que a fonte não diz («saliente», «a base da gota», «trajetória mais rápida»). A regra 29 já
obriga o advogado a conferir afirmação a afirmação; esta auditoria mostra que o controlo tem de
estar no advogado e não só no pesquisador.
