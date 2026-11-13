#!/usr/bin/env python3
"""Validação automática das perguntas do banco.

Uso:
    python3 scripts/validar.py                      # valida banco/perguntas/
    python3 scripts/validar.py caminho/ficheiro.json pasta/ ...
    python3 scripts/validar.py --dominio https://en.wikipedia.org/wiki/X

Sai com código 1 se houver algum ERRO. AVISO não bloqueia.
Não precisa de pacotes externos (só a biblioteca padrão do Python 3.9+).
"""

import hashlib
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

TOPICS = {"General Knowledge", "Geography", "World History", "Science", "Space", "Movies",
          "Music", "Football", "Video Games", "Nature & Animals"}
MERCADOS = {"pt", "us"}
IDIOMAS = ("pt-PT", "en-US")
ESTADOS = {"rascunho", "em_verificacao", "aprovada", "publicada", "suspensa",
           "retirada", "rejeitada"}
PAPEIS = {"pesquisador", "verificador", "advogado", "auditor", "sentinela", "triagem"}
OBRIGATORIOS = ["id", "topic", "text", "correct", "difficulty", "daily_eligible", "valid_until",
                "sources", "fontes", "verificacao", "estado", "motivo_rejeicao", "lote",
                "criada_em", "historico"]
OPCIONAIS = ["etiquetas", "subtopic", "markets", "options_lock"]
CAMPOS_FONTE = ["url", "dominio", "titulo", "nivel", "excerto", "consultada_em", "papel"]

# Etiquetas permitidas. "classico": facto muito conhecido (já usado noutros quizzes),
# admitido com enunciado próprio; nunca em dificuldade 4 ou 5. Quota: no máximo 20% das
# perguntas aprovadas e publicadas do banco, aplicada a partir de 100 perguntas.
ETIQUETAS = {"classico", "caminho_leve"}
QUOTA_CLASSICOS = 0.20       # máximo de clássicos no banco (aprovadas + publicadas)
BANCO_MINIMO_QUOTA = 100     # a quota só bloqueia a partir de 100 perguntas; abaixo, só se mede
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


RE_DUVIDA_EN = re.compile(
    r"\b(apparently|allegedly|supposedly|reportedly|presumably|probably|possibly|perhaps|maybe|"
    r"is said to|are said to|was said to|it is believed|it is thought|legend has it|rumou?r has it|"
    r"may have|might have|could have been)\b", re.IGNORECASE)
RE_ATRIBUICAO_EN = re.compile(
    r"\b(according to|per the|as (?:stated|reported|argued|claimed) by|in the (?:view|opinion) of|"
    r"historians?|archaeologists?|researchers?|scholars?|the authors?|"
    r"(?:states?|stated|says|said|argues?|argued|claims?|claimed|suggests?|suggested|writes|wrote|"
    r"records?|recorded|attributes?|attributed|maintains?|maintained) that)\b", re.IGNORECASE)


def duvida_sem_atribuicao(texto: str, idioma: str = "pt-PT"):
    """Devolve a primeira expressão de dúvida numa frase sem atribuição, ou None."""
    re_d, re_a = (RE_DUVIDA_EN, RE_ATRIBUICAO_EN) if idioma == "en-US" else (RE_DUVIDA, RE_ATRIBUICAO)
    for frase in re.split(r"(?<=[.;!?])\s+", texto or ""):
        m = re_d.search(frase)
        if m and not re_a.search(frase):
            return m.group(0)
    return None


# Formas do português do Brasil que não servem em pt-PT (aviso; o conferente decide).
RE_BRASIL = re.compile(r"\b(ônibus|celular|geladeira|trem|gramado|goleiro|equipe|time de futebol|"
                       r"pelo menos você|vocês|você|a gente|ator principal|filme de terror|banheiro|"
                       r"café da manhã|fato de que)\b", re.IGNORECASE)
# Grafias britânicas que não servem em en-US (aviso).
RE_BRITANICO = re.compile(r"\b(colour|favourite|centre|metre|kilometre|litre|grey|programme|"
                          r"theatre|honour|neighbour|travelled|defence|organis\w+|realis\w+|"
                          r"analys\w+|whilst|football pitch)\b", re.IGNORECASE)


def n_frases(texto: str) -> int:
    """Número de frases, sem contar o ponto de iniciais (D. João, Michael E. Smith), de
    abreviaturas (Dr., St., a.C.) nem de números (1.5)."""
    s = (texto or "").strip()
    s = re.sub(r"\b([A-ZÀ-Ý]|Dr|Dra|Sr|Sra|Mr|Mrs|Ms|St|Jr|Mt|Ft|Prof|Eng|Av|Pe|Fr|vs|etc|a\.C|d\.C)\.", "\\1\u2024", s)
    return len([f for f in re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-Ý«\"0-9])", s) if f])


def numeros(texto: str) -> list[str]:
    """Sequências de dígitos de um texto, normalizadas (2,4 e 2.4 -> 2.4; 350 000 e 350,000 -> 350000)."""
    # Ordinais em pt («1.ª parte», «3.º andar») não têm dígitos equivalentes em inglês («first half»).
    s = re.sub(r"\b\d+\.?\s?[ªº]", "", texto or "")
    s = re.sub(r"(?<=\d)[\s\u00a0\u202f,.](?=\d{3}(?!\d))", "", s)
    s = re.sub(r"(?<=\d),(?=\d)", ".", s)
    return sorted(re.findall(r"\d+(?:\.\d+)?", s))


def opcoes_lock(p: dict) -> str:
    """SHA-256 das opções nos dois idiomas (o texto das opções é imutável depois da aprovação)."""
    t = p.get("text", {})
    base = {i: t.get(i, {}).get("options") for i in IDIOMAS}
    return hashlib.sha256(json.dumps(base, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()

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


def validar_texto(idioma: str, tx, estado: str, erros: list, avisos: list):
    """Valida o texto de um idioma e devolve (question, options, explanation)."""
    if not isinstance(tx, dict):
        erros.append(f"text.{idioma} não é um objeto")
        return "", [], ""
    for c in ("question", "options", "explanation"):
        if c not in tx:
            erros.append(f"text.{idioma} sem: {c}")
    extra = set(tx) - {"question", "options", "explanation"}
    if extra:
        erros.append(f"text.{idioma}: campos não previstos: {', '.join(sorted(extra))}")
    q = tx.get("question") if isinstance(tx.get("question"), str) else ""
    ex = tx.get("explanation") if isinstance(tx.get("explanation"), str) else ""
    op = tx.get("options")
    if not 10 <= len(q) <= 200:
        erros.append(f"{idioma}: pergunta com {len(q)} caracteres (limite 10 a 200)")
    elif len(q) > 120:
        avisos.append(f"{idioma}: pergunta com {len(q)} caracteres (alvo: até 120)")
    if not q.rstrip().endswith("?"):
        erros.append(f"{idioma}: a pergunta tem de terminar em '?'")
    negativa = r"\bnão\b" if idioma == "pt-PT" else r"\bnot\b|\bnever\b"
    if re.search(negativa, q, re.IGNORECASE):
        avisos.append(f"{idioma}: pergunta com negativa: confirmar que não confunde")
    if not 10 <= len(ex) <= 300:
        # Em perguntas rejeitadas ou suspensas é só um aviso (são dados para melhorar o motor).
        (avisos if estado in ("rejeitada", "suspensa") else erros).append(
            f"{idioma}: explicação com {len(ex)} caracteres (limite 10 a 300)")
    if n_frases(ex) > 2:
        # No ecrã «Why» cabem 1 a 2 frases: bloqueia a aprovação, não o trabalho em curso.
        (erros if estado in {"aprovada", "publicada"} else avisos).append(
            f"{idioma}: explicação com {n_frases(ex)} frases (limite: 1 a 2)")
    duvida = duvida_sem_atribuicao(ex, idioma)
    if duvida:
        erros.append(f"{idioma}: linguagem de dúvida sem atribuição na explicação ('{duvida}'): atribuir a quem o diz, confirmar com fonte e afirmar, ou retirar")
    if idioma == "pt-PT":
        for campo, valor in (("pergunta", q), ("explicação", ex), ("opções", " ".join(o for o in (op or []) if isinstance(o, str)))):
            m = RE_BRASIL.search(valor)
            if m:
                avisos.append(f"pt-PT: forma do português do Brasil na {campo} ('{m.group(0)}')")
    else:
        for campo, valor in (("question", q), ("explanation", ex), ("options", " ".join(o for o in (op or []) if isinstance(o, str)))):
            m = RE_BRITANICO.search(valor)
            if m:
                avisos.append(f"en-US: grafia britânica na {campo} ('{m.group(0)}')")
    if not isinstance(op, list) or len(op) != 4:
        erros.append(f"{idioma}: tem de haver exatamente 4 opções")
        op = []
    else:
        if any(not isinstance(o, str) or not o.strip() for o in op):
            erros.append(f"{idioma}: há opções vazias ou que não são texto")
        normal = [normalizar(o) for o in op if isinstance(o, str)]
        if len(set(normal)) != len(normal):
            erros.append(f"{idioma}: há opções repetidas")
        if any(isinstance(o, str) and len(o) > 60 for o in op):
            erros.append(f"{idioma}: há opções com mais de 60 caracteres")
        if any(normalizar(o) in {"todas as anteriores", "nenhuma das anteriores", "all of the above", "none of the above"}
               for o in op if isinstance(o, str)):
            erros.append(f"{idioma}: opções do tipo 'todas/nenhuma das anteriores' não são permitidas")
    return q, op, ex


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

    estado = p["estado"]
    final = estado in {"aprovada", "publicada"}
    if not isinstance(p["id"], str) or not RE_ID.match(p["id"]):
        erros.append("id fora do formato Q-AAAA-NNNNNN")
    if p["topic"] not in TOPICS:
        erros.append(f"topic desconhecido: {p['topic']}")
    if estado not in ESTADOS:
        erros.append(f"estado desconhecido: {estado}")
    if "subtopic" in p and (not isinstance(p["subtopic"], str) or not 2 <= len(p["subtopic"]) <= 60):
        erros.append("subtopic tem de ter entre 2 e 60 caracteres")
    mercados = p.get("markets")
    if mercados is not None:
        if (not isinstance(mercados, list) or not mercados or len(set(mercados)) != len(mercados)
                or any(m not in MERCADOS for m in mercados)):
            erros.append(f"markets tem de ser uma lista não vazia, sem repetições, de {sorted(MERCADOS)}")
    if not isinstance(p["lote"], str) or not p["lote"]:
        erros.append("lote em falta")
    if not data_valida(p["criada_em"]):
        erros.append("criada_em não é uma data AAAA-MM-DD válida")

    # Texto nos dois idiomas
    texto = p["text"] if isinstance(p["text"], dict) else {}
    if not isinstance(p["text"], dict):
        erros.append("text tem de ser um objeto com pt-PT e en-US")
    for i in set(texto) - set(IDIOMAS):
        erros.append(f"text: idioma não previsto: {i}")
    if "pt-PT" not in texto:
        erros.append("text sem pt-PT")
    if "en-US" not in texto and final:
        erros.append("aprovada sem texto en-US: a pergunta tem de existir nos dois idiomas")
    por_idioma = {}
    for idioma in IDIOMAS:
        if idioma in texto:
            por_idioma[idioma] = validar_texto(idioma, texto[idioma], estado, erros, avisos)
    if len(por_idioma) == 2:
        (qp, op_p, ex_p), (qe, op_e, ex_e) = por_idioma["pt-PT"], por_idioma["en-US"]
        if numeros(qp + " " + " ".join(op_p)) != numeros(qe + " " + " ".join(op_e)):
            erros.append("os números da pergunta/opções diferem entre pt-PT e en-US")
        if numeros(ex_p) != numeros(ex_e):
            avisos.append("os números da explicação diferem entre pt-PT e en-US: confirmar")
    correta = p["correct"]
    if not isinstance(correta, int) or isinstance(correta, bool) or not 0 <= correta <= 3:
        erros.append("correct tem de ser um inteiro de 0 a 3")
        correta = None
    opcoes = por_idioma.get("pt-PT", ("", [], ""))[1]

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
    if ("classico" in etiquetas and estado != "rejeitada"
            and isinstance(p["difficulty"], int) and p["difficulty"] >= 4):
        erros.append("pergunta 'classico' com dificuldade 4 ou 5: não é permitido")
    if not isinstance(p["difficulty"], int) or isinstance(p["difficulty"], bool) or not 1 <= p["difficulty"] <= 5:
        erros.append("difficulty tem de ser um inteiro de 1 a 5")

    # Tempo
    if not isinstance(p["daily_eligible"], bool):
        erros.append("daily_eligible tem de ser true ou false")
    if p["valid_until"] is not None and not data_valida(p["valid_until"]):
        erros.append("valid_until não é uma data AAAA-MM-DD válida")
    if p["valid_until"] is not None:
        if p["daily_eligible"] is True:
            erros.append("daily_eligible só para factos estáveis: uma pergunta com valid_until não pode ser do Daily 10")
        if data_valida(p["valid_until"]) and data_valida(p["criada_em"]) and p["valid_until"] <= p["criada_em"]:
            erros.append("valid_until tem de ser posterior a criada_em")
        elif data_valida(p["valid_until"]) and p["valid_until"] < date.today().isoformat() and final:
            erros.append("prazo de validade ultrapassado: passar pela sentinela")

    # Fontes
    fontes = p["fontes"] if isinstance(p["fontes"], list) else []
    inativa = p.get("estado") in ("rejeitada", "suspensa")
    if len(fontes) < 2:
        (avisos if inativa else erros).append("são precisas pelo menos 2 fontes")
    dominios, wikis, papeis_dom, urls = [], 0, {}, {}
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
        urls[url] = f
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
        (avisos if inativa else erros).append("as fontes têm de vir de pelo menos 2 domínios diferentes")
    if wikis > 1:
        erros.append("a Wikipédia só pode contar como uma fonte")
    if fontes and not any(isinstance(f, dict) and f.get("nivel") == 1 for f in fontes):
        avisos.append("nenhuma fonte de nível 1: confirmar que não existe")
    if wikis:
        avisos.append("Wikipédia citada: serve para pistas; confirmar que a fonte original que ela refere não estava acessível")

    # Fontes mostradas ao jogador
    src = p["sources"]
    if not isinstance(src, list) or not 1 <= len(src) <= 3 or len(set(src)) != len(src):
        erros.append("sources tem de ser uma lista de 1 a 3 URLs diferentes")
    else:
        for u in src:
            if u not in urls:
                erros.append(f"sources: {u} não está em 'fontes'")
            elif dominio_registavel(u) == "wikipedia.org":
                erros.append("sources: a Wikipédia não se mostra ao jogador")
        if urls and not any(u in urls and urls[u].get("nivel") == 1 for u in src) and any(f.get("nivel") == 1 for f in urls.values()):
            avisos.append("sources sem nenhuma fonte de nível 1 embora exista uma em 'fontes'")

    # Verificação e estados
    v = p["verificacao"] if isinstance(p["verificacao"], dict) else {}
    for chave in ("verificador", "advogado", "editor"):
        if chave not in v:
            erros.append(f"verificacao sem o campo {chave}")
    ver, adv, edi = v.get("verificador"), v.get("advogado"), v.get("editor")
    tra, conf = v.get("tradutor"), v.get("conferente")

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

    if final:
        if not ver or ver.get("concorda") is not True:
            erros.append("aprovada sem concordância do verificador às cegas")
        elif ver.get("confianca") == "baixa":
            erros.append("aprovada com confiança baixa do verificador")
        if v.get("caminho_leve") is True:
            if p.get("difficulty") != 1:
                erros.append("caminho leve só vale para dificuldade 1")
            if "caminho_leve" not in (p.get("etiquetas") or []):
                erros.append("caminho leve sem a etiqueta 'caminho_leve'")
            if not any(f.get("papel") == "pesquisador" and f.get("nivel") == 1 for f in p.get("fontes", [])):
                erros.append("caminho leve exige fonte de nível 1 do pesquisador")
        elif not adv or adv.get("aprovado") is not True:
            erros.append("aprovada sem aprovação do advogado do diabo")
        if not edi or edi.get("aprovado") is not True:
            erros.append("aprovada sem aprovação do editor")
        elif edi.get("originalidade_ok") is not True:
            erros.append("aprovada sem confirmação de originalidade")
        elif edi.get("alteracao_factual") is True:
            if not ver or not data_valida(ver.get("data", "")) or not data_valida(edi.get("data", "")) or ver["data"] < edi["data"]:
                erros.append("mudança factual do editor sem nova verificação às cegas")
        if not tra:
            erros.append("aprovada sem o passo do tradutor (en-US)")
        if not conf or conf.get("aprovado") is not True:
            erros.append("aprovada sem aprovação do conferente (os dois textos dizem o mesmo)")
        historico_ok = isinstance(p["historico"], list) and any(
            isinstance(ev, dict) and ev.get("evento") == EVENTO_APROVACAO for ev in p["historico"])
        if not historico_ok:
            erros.append(f"aprovada sem o evento '{EVENTO_APROVACAO}' no histórico: só o scripts/aprovar.py pode aprovar")
        lock = p.get("options_lock")
        if not lock:
            erros.append("aprovada sem options_lock: só o scripts/aprovar.py grava as opções aprovadas")
        elif lock != opcoes_lock(p):
            erros.append("o texto das opções mudou depois da aprovação (options_lock não bate)")
    if estado == "rejeitada" and not (isinstance(p["motivo_rejeicao"], str) and p["motivo_rejeicao"].strip()):
        erros.append("pergunta rejeitada sem motivo_rejeicao")
    if estado == "suspensa" and not (isinstance(p["motivo_rejeicao"], str) and p["motivo_rejeicao"].strip()):
        erros.append("pergunta suspensa sem motivo (motivo_rejeicao)")

    historico = p["historico"] if isinstance(p["historico"], list) else []
    if not historico:
        erros.append("historico vazio")
    for i, ev in enumerate(historico, 1):
        if not isinstance(ev, dict) or not all(k in ev for k in ("data", "evento", "agente")):
            erros.append(f"evento {i} do histórico incompleto (data, evento, agente)")

    return erros, avisos


def quota_classicos(perguntas: list[dict]) -> tuple[int, int, str | None]:
    """Quota de clássicos sobre o BANCO: perguntas aprovadas e publicadas. Devolve
    (clássicos, total, erro). Só há erro a partir de BANCO_MINIMO_QUOTA perguntas e acima de
    QUOTA_CLASSICOS; abaixo disso, só se mede."""
    ativas = [p for p in perguntas if isinstance(p, dict) and p.get("estado") in ("aprovada", "publicada")]
    classicos = sum(1 for p in ativas if "classico" in (p.get("etiquetas") or []))
    total = len(ativas)
    erro = None
    if total >= BANCO_MINIMO_QUOTA and classicos > QUOTA_CLASSICOS * total:
        erro = (f"{classicos} clássicos em {total} perguntas aprovadas ou publicadas "
                f"({classicos / total:.0%}): o máximo é {QUOTA_CLASSICOS:.0%}")
    return classicos, total, erro


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
            chave = normalizar(((pergunta.get("text") or {}).get("pt-PT") or {}).get("question", ""))
            if chave and chave in enunciados and pergunta.get("estado") != "rejeitada":
                avisos.append(f"pergunta pt-PT igual à de {enunciados[chave]}")
            if pergunta.get("estado") != "rejeitada":
                enunciados.setdefault(chave, f.name)
        estado = "OK   " if not erros else "ERRO "
        print(f"{estado} {f}")
        for e in erros:
            print(f"      ERRO: {e}")
        for a in avisos:
            print(f"      AVISO: {a}")
        total_erros += len(erros)

    # Quota de clássicos sobre o banco: corre quando se valida uma pasta (o aprovar.py
    # verifica-a sempre sobre o banco inteiro).
    if not args or any(Path(a).is_dir() for a in args):
        classicos, total, erro = quota_classicos(carregadas)
        if total:
            print(f"\nClássicos no banco: {classicos} de {total} aprovadas/publicadas ({classicos / total:.0%}); "
                  f"quota de {QUOTA_CLASSICOS:.0%} aplicada a partir de {BANCO_MINIMO_QUOTA}.")
        if erro:
            print(f"ERRO  banco: {erro}")
            total_erros += 1

    print(f"\n{len(ficheiros)} ficheiro(s), {total_erros} erro(s).")
    return 1 if total_erros else 0


if __name__ == "__main__":
    sys.exit(main())
