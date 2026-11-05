#!/usr/bin/env python3
"""Validação automática das perguntas do banco.

Uso:
    python3 scripts/validar.py                      # valida banco/perguntas/
    python3 scripts/validar.py caminho/ficheiro.json pasta/ ...
    python3 scripts/validar.py --dominio https://en.wikipedia.org/wiki/X

Sai com código 1 se houver algum ERRO. AVISO não bloqueia.
Não precisa de pacotes externos (só a biblioteca padrão do Python 3.9+).
"""

import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

TEMAS = {"historia", "geografia", "ciencia", "desporto", "cinema-tv", "musica",
         "literatura", "arte", "portugal", "atualidade"}
ESTADOS = {"rascunho", "em_verificacao", "aprovada", "publicada", "suspensa",
           "retirada", "rejeitada"}
PAPEIS = {"pesquisador", "verificador", "advogado", "auditor", "sentinela", "triagem"}
OBRIGATORIOS = ["id", "lingua", "tema", "subtema", "formato", "enunciado", "opcoes",
                "correta", "explicacao", "dificuldade_estimada", "fontes", "verificacao",
                "sensivel_ao_tempo", "valida_ate", "estado", "motivo_rejeicao", "lote",
                "criada_em", "historico"]
OPCIONAIS = ["etiquetas"]
CAMPOS_FONTE = ["url", "dominio", "titulo", "nivel", "excerto", "consultada_em", "papel"]

# Etiquetas permitidas. "classico": facto muito conhecido (já usado noutros quizzes),
# admitido com enunciado próprio; nunca em dificuldade 4 ou 5 e no máximo 20% por lote.
ETIQUETAS = {"classico"}
QUOTA_CLASSICOS = 0.20
EVENTO_APROVACAO = "aprovada por aprovar.py"

# Linguagem de dúvida na explicação (regras/fontes.md, regra 9). Recusa-se a dúvida
# SEM atribuição ("ao que parece", "diz-se", "terá sido", "possivelmente"); aceita-se a
# atribuída a alguém ("segundo os arqueólogos, terá sido…", "Barros afirma que…").
RE_DUVIDA = re.compile(
    r"\b(ao que parece|parece que|diz-se|dizem que|diz a lenda|conta-se|contam que|"
    r"consta que|segundo consta|alegadamente|supostamente|presumivelmente|"
    r"provavelmente|possivelmente|talvez|terá sido|terão sido|terá|terão)\b",
    re.IGNORECASE)
# Marcas de atribuição a uma fonte, autor ou grupo identificado.
RE_ATRIBUICAO = re.compile(
    r"\b(segundo (?!consta)|de acordo com|conforme|na opinião de|na versão de|para (o|a|os|as) "
    r"(historiador|historiadora|historiadores|arqueólogo|arqueóloga|arqueólogos|cronista|autor|autora|autores|investigadores?)\b|"
    r"(afirma|afirmam|afirmou|defende|defendem|defendeu|considera|consideram|sustenta|sustentam|"
    r"acredita|acreditam|escreve|escreveu|regista|registou|atribui|atribuem|atribuiu|contesta|contestam|contestou)\b)",
    re.IGNORECASE)


def duvida_sem_atribuicao(texto: str):
    """Devolve a primeira expressão de dúvida numa frase sem atribuição, ou None."""
    for frase in re.split(r"(?<=[.;!?])\s+", texto or ""):
        m = RE_DUVIDA.search(frase)
        if m and not RE_ATRIBUICAO.search(frase):
            return m.group(0)
    return None

# Domínios proibidos como fonte (regras/fontes.md). Qualquer domínio com "quiz" ou
# "trivia" no nome também é recusado.
PROIBIDOS = {
    "sporcle.com", "jetpunk.com", "funtrivia.com", "kahoot.com", "kahoot.it",
    "quizlet.com", "opentdb.com", "reddit.com", "quora.com", "facebook.com",
    "instagram.com", "tiktok.com", "x.com", "twitter.com", "medium.com",
    "blogspot.com", "wordpress.com", "pinterest.com", "youtube.com",
}
SUFIXOS_2_NIVEIS = {"co", "com", "gov", "org", "ac", "edu", "net", "gob", "go", "nic"}
RE_DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RE_ID = re.compile(r"^Q-\d{4}-\d{6}$")


def dominio_registavel(url_ou_host: str) -> str:
    """Domínio registável aproximado: en.wikipedia.org -> wikipedia.org,
    history.blog.gov.uk -> blog.gov.uk, www.bbc.co.uk -> bbc.co.uk."""
    host = urlparse(url_ou_host).hostname if "//" in url_ou_host else url_ou_host
    host = (host or "").lower().strip(".")
    if host.startswith("www."):
        host = host[4:]
    partes = host.split(".")
    if len(partes) >= 3 and partes[-2] in SUFIXOS_2_NIVEIS and len(partes[-1]) == 2:
        return ".".join(partes[-3:])
    return ".".join(partes[-2:])


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto or "")
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto).strip().casefold()


def data_valida(valor) -> bool:
    if not isinstance(valor, str) or not RE_DATA.match(valor):
        return False
    try:
        date.fromisoformat(valor)
        return True
    except ValueError:
        return False


def validar_pergunta(p: dict) -> tuple[list[str], list[str]]:
    erros, avisos = [], []

    if not isinstance(p, dict):
        return ["o ficheiro não contém um objeto JSON"], []

    for campo in OBRIGATORIOS:
        if campo not in p:
            erros.append(f"campo obrigatório em falta: {campo}")
    if erros:
        return erros, avisos
    extra = set(p) - set(OBRIGATORIOS) - set(OPCIONAIS)
    if extra:
        erros.append(f"campos não previstos no esquema: {', '.join(sorted(extra))}")

    if not isinstance(p["id"], str) or not RE_ID.match(p["id"]):
        erros.append("id fora do formato Q-AAAA-NNNNNN")
    if p["lingua"] != "pt-PT":
        erros.append("lingua tem de ser pt-PT")
    if p["tema"] not in TEMAS:
        erros.append(f"tema desconhecido: {p['tema']}")
    if p["formato"] != "escolha-multipla":
        erros.append("formato tem de ser escolha-multipla")
    if p["estado"] not in ESTADOS:
        erros.append(f"estado desconhecido: {p['estado']}")
    if not isinstance(p["subtema"], str) or not 2 <= len(p["subtema"]) <= 60:
        erros.append("subtema tem de ter entre 2 e 60 caracteres")
    if not isinstance(p["lote"], str) or not p["lote"]:
        erros.append("lote em falta")
    if not data_valida(p["criada_em"]):
        erros.append("criada_em não é uma data AAAA-MM-DD válida")

    # Enunciado e explicação
    enunciado = p["enunciado"] if isinstance(p["enunciado"], str) else ""
    if not 10 <= len(enunciado) <= 200:
        erros.append(f"enunciado com {len(enunciado)} caracteres (limite 10 a 200)")
    elif len(enunciado) > 120:
        avisos.append(f"enunciado com {len(enunciado)} caracteres (alvo: até 120)")
    if not enunciado.rstrip().endswith("?"):
        erros.append("o enunciado tem de terminar em '?'")
    if re.search(r"\bnão\b", enunciado, re.IGNORECASE):
        avisos.append("enunciado com negativa ('não'): confirmar que não confunde")
    explicacao = p["explicacao"] if isinstance(p["explicacao"], str) else ""
    if not 10 <= len(explicacao) <= 300:
        erros.append(f"explicação com {len(explicacao)} caracteres (limite 10 a 300)")
    duvida = duvida_sem_atribuicao(explicacao)
    if duvida:
        erros.append(f"linguagem de dúvida sem atribuição na explicação ('{duvida}'): atribuir a quem o diz, confirmar com fonte e afirmar, ou retirar")

    # Etiquetas (campo opcional)
    etiquetas = p.get("etiquetas", [])
    if not isinstance(etiquetas, list) or any(not isinstance(e, str) for e in etiquetas):
        erros.append("etiquetas tem de ser uma lista de textos")
        etiquetas = []
    elif len(set(etiquetas)) != len(etiquetas):
        erros.append("etiquetas repetidas")
    desconhecidas = set(etiquetas) - ETIQUETAS
    if desconhecidas:
        erros.append(f"etiquetas desconhecidas: {', '.join(sorted(desconhecidas))}")
    if "classico" in etiquetas and isinstance(p["dificuldade_estimada"], int) and p["dificuldade_estimada"] >= 4:
        erros.append("pergunta 'classico' com dificuldade 4 ou 5: não é permitido")

    # Opções
    opcoes = p["opcoes"]
    if not isinstance(opcoes, list) or len(opcoes) != 4:
        erros.append("tem de haver exatamente 4 opções")
        opcoes = []
    else:
        if any(not isinstance(o, str) or not o.strip() for o in opcoes):
            erros.append("há opções vazias ou que não são texto")
        normal = [normalizar(o) for o in opcoes if isinstance(o, str)]
        if len(set(normal)) != len(normal):
            erros.append("há opções repetidas")
        if any(isinstance(o, str) and len(o) > 60 for o in opcoes):
            erros.append("há opções com mais de 60 caracteres")
        if any(normalizar(o) in {"todas as anteriores", "nenhuma das anteriores"} for o in opcoes if isinstance(o, str)):
            erros.append("opções do tipo 'todas/nenhuma das anteriores' não são permitidas")
    correta = p["correta"]
    if not isinstance(correta, int) or isinstance(correta, bool) or not 0 <= correta <= 3:
        erros.append("correta tem de ser um inteiro de 0 a 3")
        correta = None
    if not isinstance(p["dificuldade_estimada"], int) or not 1 <= p["dificuldade_estimada"] <= 5:
        erros.append("dificuldade_estimada tem de ser um inteiro de 1 a 5")

    # Tempo
    if not isinstance(p["sensivel_ao_tempo"], bool):
        erros.append("sensivel_ao_tempo tem de ser true ou false")
    if p["valida_ate"] is not None and not data_valida(p["valida_ate"]):
        erros.append("valida_ate não é uma data AAAA-MM-DD válida")
    if p["sensivel_ao_tempo"] is True:
        if p["valida_ate"] is None:
            erros.append("pergunta sensível ao tempo sem valida_ate")
        elif data_valida(p["valida_ate"]) and data_valida(p["criada_em"]) and p["valida_ate"] <= p["criada_em"]:
            erros.append("valida_ate tem de ser posterior a criada_em")
        elif data_valida(p["valida_ate"]) and p["valida_ate"] < date.today().isoformat() and p["estado"] in {"aprovada", "publicada"}:
            erros.append("prazo de validade ultrapassado: passar pela sentinela")

    # Fontes
    fontes = p["fontes"] if isinstance(p["fontes"], list) else []
    if len(fontes) < 2:
        erros.append("são precisas pelo menos 2 fontes")
    dominios, wikis, papeis_dom = [], 0, {}
    for i, f in enumerate(fontes, 1):
        if not isinstance(f, dict):
            erros.append(f"fonte {i} não é um objeto")
            continue
        falta = [c for c in CAMPOS_FONTE if c not in f]
        if falta:
            erros.append(f"fonte {i} sem: {', '.join(falta)}")
            continue
        url = f["url"] if isinstance(f["url"], str) else ""
        if not url.startswith(("http://", "https://")):
            erros.append(f"fonte {i} com URL inválido")
            continue
        dom = dominio_registavel(url)
        if f["dominio"] != dom:
            erros.append(f"fonte {i}: dominio '{f['dominio']}' não corresponde ao URL ('{dom}')")
        if dom in PROIBIDOS or "quiz" in dom or "trivia" in dom:
            erros.append(f"fonte {i}: domínio proibido como fonte ({dom})")
        if dom == "wikipedia.org":
            wikis += 1
        if f["nivel"] not in (1, 2):
            erros.append(f"fonte {i}: nivel tem de ser 1 ou 2")
        if not isinstance(f["excerto"], str) or not f["excerto"].strip():
            erros.append(f"fonte {i}: excerto vazio")
        elif len(f["excerto"]) > 300:
            erros.append(f"fonte {i}: excerto com mais de 300 caracteres")
        if not data_valida(f["consultada_em"]):
            erros.append(f"fonte {i}: consultada_em não é uma data válida")
        if f["papel"] not in PAPEIS:
            erros.append(f"fonte {i}: papel desconhecido ({f['papel']})")
        dominios.append(dom)
        papeis_dom.setdefault(f["papel"], set()).add(dom)
    if fontes and len(set(dominios)) < 2:
        erros.append("as fontes têm de vir de pelo menos 2 domínios diferentes")
    if wikis > 1:
        erros.append("a Wikipédia só pode contar como uma fonte")
    if fontes and not any(isinstance(f, dict) and f.get("nivel") == 1 for f in fontes):
        avisos.append("nenhuma fonte de nível 1: confirmar que não existe")
    if wikis:
        avisos.append("Wikipédia citada: serve para pistas; confirmar que a fonte original que ela refere não estava acessível")

    # Verificação e estados
    v = p["verificacao"] if isinstance(p["verificacao"], dict) else {}
    for chave in ("verificador", "advogado", "editor"):
        if chave not in v:
            erros.append(f"verificacao sem o campo {chave}")
    ver, adv, edi = v.get("verificador"), v.get("advogado"), v.get("editor")

    if ver:
        if "pesquisador" not in papeis_dom:
            erros.append("verificação feita mas não há fonte com papel 'pesquisador'")
        if "verificador" not in papeis_dom:
            erros.append("verificação feita mas a fonte do verificador não está em 'fontes'")
        else:
            comuns = papeis_dom["verificador"] & papeis_dom.get("pesquisador", set())
            if comuns:
                erros.append(f"o verificador usou um domínio do pesquisador ({', '.join(sorted(comuns))}): não é independente")
        if ver.get("dominio") and ver.get("dominio") not in papeis_dom.get("verificador", set()):
            erros.append("verificacao.verificador.dominio não corresponde a nenhuma fonte do verificador")
        if correta is not None and opcoes and isinstance(ver.get("resposta_texto"), str):
            if normalizar(ver["resposta_texto"]) != normalizar(opcoes[correta]) and ver.get("concorda") is True:
                erros.append("o verificador 'concorda' mas a resposta dele não é a opção correta")

    if p["estado"] in {"aprovada", "publicada"}:
        if not ver or ver.get("concorda") is not True:
            erros.append("aprovada sem concordância do verificador às cegas")
        elif ver.get("confianca") == "baixa":
            erros.append("aprovada com confiança baixa do verificador")
        if not adv or adv.get("aprovado") is not True:
            erros.append("aprovada sem aprovação do advogado do diabo")
        if not edi or edi.get("aprovado") is not True:
            erros.append("aprovada sem aprovação do editor")
        elif edi.get("originalidade_ok") is not True:
            erros.append("aprovada sem confirmação de originalidade")
        elif edi.get("alteracao_factual") is True:
            if not ver or not data_valida(ver.get("data", "")) or not data_valida(edi.get("data", "")) or ver["data"] < edi["data"]:
                erros.append("mudança factual do editor sem nova verificação às cegas")
    if p["estado"] in {"aprovada", "publicada"}:
        historico_ok = isinstance(p["historico"], list) and any(
            isinstance(ev, dict) and ev.get("evento") == EVENTO_APROVACAO for ev in p["historico"])
        if not historico_ok:
            erros.append(f"aprovada sem o evento '{EVENTO_APROVACAO}' no histórico: só o scripts/aprovar.py pode aprovar")
    if p["estado"] == "rejeitada" and not (isinstance(p["motivo_rejeicao"], str) and p["motivo_rejeicao"].strip()):
        erros.append("pergunta rejeitada sem motivo_rejeicao")

    historico = p["historico"] if isinstance(p["historico"], list) else []
    if not historico:
        erros.append("historico vazio")
    for i, ev in enumerate(historico, 1):
        if not isinstance(ev, dict) or not all(k in ev for k in ("data", "evento", "agente")):
            erros.append(f"evento {i} do histórico incompleto (data, evento, agente)")

    return erros, avisos


def erros_de_lote(perguntas: list[dict]) -> dict[str, list[str]]:
    """Regras que só se veem no lote inteiro. Conta as perguntas não rejeitadas de cada
    lote: as 'classico' não podem passar de 20%."""
    por_lote: dict[str, list[dict]] = {}
    for p in perguntas:
        if isinstance(p, dict) and p.get("estado") != "rejeitada" and isinstance(p.get("lote"), str):
            por_lote.setdefault(p["lote"], []).append(p)
    erros = {}
    for lote, lista in por_lote.items():
        classicos = sum(1 for p in lista if "classico" in (p.get("etiquetas") or []))
        if classicos and classicos > QUOTA_CLASSICOS * len(lista):
            erros[lote] = [f"{classicos} clássicos em {len(lista)} perguntas não rejeitadas "
                           f"({classicos / len(lista):.0%}): o máximo é {QUOTA_CLASSICOS:.0%}"]
    return erros


def ficheiros_a_validar(argumentos: list[str]) -> list[Path]:
    alvos = argumentos or ["banco/perguntas"]
    ficheiros = []
    for a in alvos:
        caminho = Path(a)
        if caminho.is_dir():
            ficheiros.extend(sorted(caminho.glob("*.json")))
        elif caminho.is_file():
            ficheiros.append(caminho)
        else:
            print(f"ERRO  {a}: não existe")
            ficheiros.append(caminho)
    return ficheiros


def main() -> int:
    args = sys.argv[1:]
    if args[:1] == ["--dominio"]:
        if len(args) != 2:
            print("uso: validar.py --dominio <url>")
            return 2
        print(dominio_registavel(args[1]))
        return 0

    ficheiros = ficheiros_a_validar(args)
    if not ficheiros:
        print("Nada para validar.")
        return 0

    total_erros, ids, enunciados, carregadas = 0, {}, {}, []
    for f in ficheiros:
        if not f.exists():
            total_erros += 1
            continue
        try:
            pergunta = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"ERRO  {f}: JSON inválido ({e})")
            total_erros += 1
            continue
        erros, avisos = validar_pergunta(pergunta)
        carregadas.append(pergunta)
        if isinstance(pergunta, dict):
            pid = pergunta.get("id")
            if pid in ids:
                erros.append(f"id repetido (também em {ids[pid]})")
            ids[pid] = f.name
            chave = normalizar(pergunta.get("enunciado", ""))
            if chave and chave in enunciados and pergunta.get("estado") != "rejeitada":
                avisos.append(f"enunciado igual ao de {enunciados[chave]}")
            if pergunta.get("estado") != "rejeitada":
                enunciados.setdefault(chave, f.name)
        estado = "OK   " if not erros else "ERRO "
        print(f"{estado} {f}")
        for e in erros:
            print(f"      ERRO: {e}")
        for a in avisos:
            print(f"      AVISO: {a}")
        total_erros += len(erros)

    # A quota de clássicos só se vê no lote inteiro: corre quando se valida uma pasta
    # (o aprovar.py verifica-a sempre sobre o lote completo do banco).
    pastas = not args or any(Path(a).is_dir() for a in args)
    for lote, erros_lote in (erros_de_lote(carregadas).items() if pastas else []):
        print(f"ERRO  lote {lote}")
        for e in erros_lote:
            print(f"      ERRO: {e}")
        total_erros += len(erros_lote)

    print(f"\n{len(ficheiros)} ficheiro(s), {total_erros} erro(s).")
    return 1 if total_erros else 0


if __name__ == "__main__":
    sys.exit(main())
