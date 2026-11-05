#!/usr/bin/env python3
"""Testes do leitor de páginas (scripts/ler_url.py).

Uso: python3 scripts/testar_ler_url.py          # sem rede: só recusas
     python3 scripts/testar_ler_url.py --rede   # também lê uma página pública

Sai com código 1 se algum teste falhar.
"""

import subprocess
import sys
import urllib.error
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import ler_url  # noqa: E402

ficheiro_banco = next((RAIZ / "banco" / "perguntas").glob("*.json"), None) or next(
    (RAIZ / "exemplos").glob("*.json"))

RECUSAR = [
    ficheiro_banco.as_uri(),                      # file:// de um ficheiro do banco
    "file:///etc/passwd",
    "FILE:///etc/hostname",
    "ftp://example.com/x",
    "gopher://example.com/",
    "http://localhost/",
    "http://localhost:8080/x",
    "http://app.localhost/",
    "http://127.0.0.1/",
    "http://127.1/",
    "http://2130706433/",                         # 127.0.0.1 em decimal
    "http://0x7f000001/",                         # 127.0.0.1 em hexadecimal
    "http://0177.0.0.1/",                         # 127.0.0.1 em octal
    "http://[::1]/",
    "http://[::ffff:127.0.0.1]/",
    "http://0.0.0.0/",
    "http://10.0.0.1/",
    "http://172.16.5.4/",
    "http://192.168.1.1/",
    "http://100.64.0.1/",                         # rede partilhada (CGNAT)
    "http://169.254.169.254/latest/meta-data/",   # metadados da cloud
    "http://[fd00::1]/",
    "http://metadata.google.internal/",
    "http://host.docker.internal/",
    "http://servico.svc.cluster.local/",
    "http://intranet/",                           # nome sem domínio
    "http://user:pass@example.com/",
]
ACEITAR = [
    "https://en.wikipedia.org/wiki/Magna_Carta",
    "https://www.legislation.gov.uk/apgb/Geo2/24/23",
    "http://8.8.8.8/",
]


def main():
    falhas = 0
    for u in RECUSAR:
        motivo = ler_url.motivo_recusa(u)
        ok = motivo is not None
        falhas += not ok
        print(f"{'OK ' if ok else 'FALHA'} recusa   {u}  ->  {motivo}")
    for u in ACEITAR:
        motivo = ler_url.motivo_recusa(u)
        ok = motivo is None
        falhas += not ok
        print(f"{'OK ' if ok else 'FALHA'} aceita   {u}  ->  {motivo}")

    # Redirecionamento de um site público para a rede local tem de ser recusado.
    h = ler_url.RedirecionamentoSeguro()
    for destino in ("http://127.0.0.1/", ficheiro_banco.as_uri(), "http://169.254.169.254/"):
        try:
            h.redirect_request(None, None, 302, "Found", {}, destino)
            ok = False
        except urllib.error.URLError:
            ok = True
        falhas += not ok
        print(f"{'OK ' if ok else 'FALHA'} recusa redirecionamento para {destino}")

    # Ponta a ponta: o comando com file:// sai com erro e não mostra o conteúdo.
    r = subprocess.run([sys.executable, str(RAIZ / "scripts" / "ler_url.py"), ficheiro_banco.as_uri()],
                       capture_output=True, text=True)
    conteudo = ficheiro_banco.read_text(encoding="utf-8")
    ok = r.returncode != 0 and '"enunciado"' not in r.stdout and conteudo[:40] not in r.stdout
    falhas += not ok
    print(f"{'OK ' if ok else 'FALHA'} comando com {ficheiro_banco.as_uri()} -> código {r.returncode}: {r.stdout.strip()[:120]}")

    if "--rede" in sys.argv:
        r = subprocess.run([sys.executable, str(RAIZ / "scripts" / "ler_url.py"),
                            "https://en.wikipedia.org/wiki/Magna_Carta", "--procurar", "Runnymede"],
                           capture_output=True, text=True, timeout=60)
        ok = r.returncode == 0 and "Runnymede" in r.stdout
        falhas += not ok
        print(f"{'OK ' if ok else 'FALHA'} leitura pública (Wikipédia) -> código {r.returncode}")

        # Caso do lote 1: a biografia de Bartolomeu Dias no SAHO nomeia Axelson e Duarte
        # Pacheco Pereira; o leitor não pode perder esse conteúdo (corte ou extração).
        saho = "https://sahistory.org.za/people/bartolomeu-dias"
        for termo in ("Axelson", "Pacheco Pereira"):
            r = subprocess.run([sys.executable, str(RAIZ / "scripts" / "ler_url.py"), saho, "--procurar", termo],
                               capture_output=True, text=True, timeout=60)
            ok = r.returncode == 0 and "excerto 1" in r.stdout and termo.lower() in r.stdout.lower()
            falhas += not ok
            print(f"{'OK ' if ok else 'FALHA'} SAHO contém '{termo}' -> código {r.returncode}")
        r = subprocess.run([sys.executable, str(RAIZ / "scripts" / "ler_url.py"), saho],
                           capture_output=True, text=True, timeout=60)
        ok = r.returncode == 0 and ("ATENÇÃO: mostra os caracteres" in r.stdout or "[… texto continua" not in r.stdout)
        falhas += not ok
        print(f"{'OK ' if ok else 'FALHA'} texto longo traz o aviso de corte no topo")

        # PDF: o leitor extrai o texto (pdftotext).
        pdf = "https://ntrs.nasa.gov/api/citations/19790012783/downloads/19790012783.pdf"
        r = subprocess.run([sys.executable, str(RAIZ / "scripts" / "ler_url.py"), pdf, "--procurar", "Axial Rotation"],
                           capture_output=True, text=True, timeout=120)
        ok = r.returncode == 0 and "243.1" in r.stdout
        falhas += not ok
        print(f"{'OK ' if ok else 'FALHA'} leitura de PDF (NASA NTRS) -> código {r.returncode}")

    print(f"\n{falhas} falha(s).")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
