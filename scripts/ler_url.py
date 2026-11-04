#!/usr/bin/env python3
"""Lê uma página web e devolve o texto, para os agentes que pesquisam.

Existe porque, no ambiente cloud, o WebFetch não chega à rede: tudo passa pelo
proxy definido em HTTPS_PROXY, que o urllib respeita. Só aceita http(s) e nunca
lê ficheiros locais. É o único comando que o hook .claude/hooks/travao_agentes.py
deixa os agentes de pesquisa e verificação correr.

Uso:
    python3 scripts/ler_url.py 'https://…'
    python3 scripts/ler_url.py 'https://…' --procurar 'termo'   # excertos à volta do termo
    python3 scripts/ler_url.py 'https://…' --inicio 12000       # continuar o texto
"""

import argparse
import ipaddress
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlparse

LIMITE_BYTES = 5_000_000
JANELA = 12_000
AGENTE = "Mozilla/5.0 (compatible; MotorDeFactos/1.0; verificacao de factos)"
IGNORAR = {"script", "style", "noscript", "svg", "template"}
BLOCOS = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
          "section", "article", "table", "dd", "dt", "blockquote", "figcaption"}


class Texto(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.partes, self.titulo, self._ignorar, self._no_titulo = [], "", 0, False

    def handle_starttag(self, tag, attrs):
        if tag in IGNORAR:
            self._ignorar += 1
        elif tag == "title":
            self._no_titulo = True
        elif tag in BLOCOS:
            self.partes.append("\n")

    def handle_endtag(self, tag):
        if tag in IGNORAR and self._ignorar:
            self._ignorar -= 1
        elif tag == "title":
            self._no_titulo = False
        elif tag in BLOCOS:
            self.partes.append("\n")

    def handle_data(self, data):
        if self._no_titulo:
            self.titulo += data
        elif not self._ignorar:
            self.partes.append(data)

    def texto(self):
        bruto = "".join(self.partes)
        linhas = [re.sub(r"[ \t\r\f\v]+", " ", l).strip() for l in bruto.split("\n")]
        return "\n".join(l for l in linhas if l)


def sem_acentos(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).casefold()


def url_permitido(url):
    p = urlparse(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        return False
    host = p.hostname.lower()
    if host in ("localhost",) or host.endswith(".local") or host.endswith(".internal"):
        return False
    try:
        ip = ipaddress.ip_address(host)
        return not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved)
    except ValueError:
        return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--procurar", default=None)
    ap.add_argument("--inicio", type=int, default=0)
    a = ap.parse_args()

    if not url_permitido(a.url):
        print("ERRO: só são aceites URLs http(s) públicos.")
        return 2
    pedido = urllib.request.Request(a.url, headers={"User-Agent": AGENTE,
                                                    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8"})
    try:
        with urllib.request.urlopen(pedido, timeout=30) as r:
            final, tipo = r.geturl(), r.headers.get("Content-Type", "")
            dados = r.read(LIMITE_BYTES + 1)
            charset = r.headers.get_content_charset() or "utf-8"
    except urllib.error.HTTPError as e:
        print(f"ERRO HTTP {e.code} em {a.url} (o site recusou; tenta outra fonte)")
        return 1
    except Exception as e:  # rede, TLS, timeout
        print(f"ERRO de rede em {a.url}: {e}")
        return 1

    if "pdf" in tipo.lower():
        print(f"ERRO: {final} é um PDF; este leitor só lê HTML e texto. Procura a versão HTML.")
        return 1
    corpo = dados[:LIMITE_BYTES].decode(charset, errors="replace")
    if "html" in tipo.lower() or corpo.lstrip()[:15].lower().startswith(("<!doctype", "<html")):
        p = Texto()
        p.feed(corpo)
        titulo, texto = p.titulo.strip(), p.texto()
    else:
        titulo, texto = "", corpo

    print(f"URL: {final}\nTÍTULO: {titulo}\nCARACTERES: {len(texto)}\n")
    if a.procurar:
        alvo, base = sem_acentos(a.procurar), sem_acentos(texto)
        posicoes, i = [], base.find(alvo)
        while i != -1 and len(posicoes) < 10:
            posicoes.append(i)
            i = base.find(alvo, i + len(alvo))
        if not posicoes:
            print(f"'{a.procurar}' não aparece no texto.")
        for n, pos in enumerate(posicoes, 1):
            print(f"--- excerto {n} (posição {pos}) ---")
            print(texto[max(0, pos - 400): pos + 400].replace("\n", " "))
        return 0
    trecho = texto[a.inicio: a.inicio + JANELA]
    print(trecho)
    if a.inicio + JANELA < len(texto):
        print(f"\n[… texto continua: usa --inicio {a.inicio + JANELA}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
