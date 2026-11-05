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
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import unicodedata
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

LIMITE_BYTES = 5_000_000      # HTML e texto
LIMITE_PDF = 25_000_000       # PDF (só se aceita inteiro: cortado não se lê)
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


SUFIXOS_INTERNOS = (".local", ".localhost", ".internal", ".localdomain", ".lan",
                    ".home", ".corp", ".intranet", ".svc", ".cluster.local")


def ip_literal(host):
    """Devolve o endereço IP se `host` for um IP escrito de qualquer forma (incluindo as
    formas curtas, decimais, octais e hexadecimais que o sistema aceita, como 127.1,
    2130706433 ou 0x7f.0.0.1); senão None."""
    h = host.strip("[]")
    try:
        return ipaddress.ip_address(h)
    except ValueError:
        pass
    try:
        return ipaddress.ip_address(socket.inet_aton(h))
    except (OSError, ValueError):
        return None


def pdf_para_texto(dados):
    """Texto de um PDF com o pdftotext (poppler), num ficheiro temporário, com limite de
    tempo. None se não houver pdftotext ou se a extração falhar."""
    if not shutil.which("pdftotext"):
        return None
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "doc.pdf"
        f.write_bytes(dados)
        try:
            r = subprocess.run(["pdftotext", "-enc", "UTF-8", "-l", "60", str(f), "-"],
                               capture_output=True, timeout=60)
        except (subprocess.TimeoutExpired, OSError):
            return None
    if r.returncode != 0:
        return None
    texto = r.stdout.decode("utf-8", errors="replace")
    linhas = [re.sub(r"[ \t\r\f\v]+", " ", l).strip() for l in texto.split("\n")]
    texto = "\n".join(l for l in linhas if l)
    return texto or None


def motivo_recusa(url):
    """None se o URL pode ser lido; senão, o motivo da recusa."""
    try:
        p = urlparse(url)
    except ValueError:
        return "URL inválido"
    if p.scheme not in ("http", "https"):
        return f"esquema '{p.scheme or '(nenhum)'}' recusado: só http e https"
    if p.username or p.password:
        return "URL com credenciais recusado"
    host = (p.hostname or "").lower().rstrip(".")
    if not host:
        return "URL sem servidor"
    if host == "localhost" or host.endswith(SUFIXOS_INTERNOS) or "." not in host.strip("[]") and ip_literal(host) is None:
        return f"servidor interno recusado ({host})"
    ip = ip_literal(host)
    if ip is not None and not ip.is_global:
        return f"endereço de rede privada, local ou reservada recusado ({ip})"
    if urllib.request.proxy_bypass(host):
        return f"servidor fora do proxy de saída recusado ({host})"
    return None


def url_permitido(url):
    return motivo_recusa(url) is None


class RedirecionamentoSeguro(urllib.request.HTTPRedirectHandler):
    """Valida cada redirecionamento: um site público não pode mandar o leitor para
    file://, localhost ou a rede privada."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        motivo = motivo_recusa(newurl)
        if motivo:
            raise urllib.error.URLError(f"redirecionamento recusado para {newurl}: {motivo}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--procurar", default=None)
    ap.add_argument("--inicio", type=int, default=0)
    a = ap.parse_args()

    motivo = motivo_recusa(a.url)
    if motivo:
        print(f"ERRO: {motivo}. Só são aceites URLs http(s) públicos.")
        return 2
    pedido = urllib.request.Request(a.url, headers={"User-Agent": AGENTE,
                                                    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8"})
    try:
        abridor = urllib.request.build_opener(RedirecionamentoSeguro)
        with abridor.open(pedido, timeout=30) as r:
            final, tipo = r.geturl(), r.headers.get("Content-Type", "")
            dados = r.read(LIMITE_PDF + 1)
            charset = r.headers.get_content_charset() or "utf-8"
    except urllib.error.HTTPError as e:
        print(f"ERRO HTTP {e.code} em {a.url} (o site recusou; tenta outra fonte)")
        return 1
    except Exception as e:  # rede, TLS, timeout
        print(f"ERRO de rede em {a.url}: {e}")
        return 1

    e_pdf = "pdf" in tipo.lower() or dados[:5] == b"%PDF-"
    if not e_pdf and len(dados) > LIMITE_BYTES:
        print(f"AVISO: documento com mais de {LIMITE_BYTES // 1_000_000} MB; só se lê o início.")
    if e_pdf:
        if len(dados) > LIMITE_PDF:
            print(f"ERRO: {final} é um PDF com mais de {LIMITE_PDF // 1_000_000} MB; procura outra fonte.")
            return 1
        titulo, texto = "", pdf_para_texto(dados)
        if texto is None:
            print(f"ERRO: {final} é um PDF e não foi possível extrair o texto (pdftotext ausente, PDF protegido ou só com imagens).")
            return 1
    elif "html" in tipo.lower() or dados.lstrip()[:15].lower().startswith((b"<!doctype", b"<html")):
        corpo = dados[:LIMITE_BYTES].decode(charset, errors="replace")
        p = Texto()
        p.feed(corpo)
        titulo, texto = p.titulo.strip(), p.texto()
    else:
        titulo, texto = "", dados[:LIMITE_BYTES].decode(charset, errors="replace")

    print(f"URL: {final}\nTÍTULO: {titulo}\nCARACTERES: {len(texto)}")
    if not a.procurar and len(texto) > JANELA:
        fim = min(a.inicio + JANELA, len(texto))
        print(f"ATENÇÃO: mostra os caracteres {a.inicio}–{fim} de {len(texto)}. O resto não aparece aqui: "
              f"usa --procurar 'termo' (procura no texto todo) ou --inicio {fim}.")
    print()
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
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # saída cortada (ex.: | head) sem erro
    sys.exit(main())
