#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador estático do site GR & WMF Advogados.

    python3 build.py

Lê o conteúdo de content.py e escreve o site pronto em public/.
Cada página vira uma pasta com index.html, o que dá URLs limpas
(/areas/direito-imobiliario/) em qualquer hospedagem estática.
"""

import html
import json
import os
import shutil
from datetime import date

from content import (
    SITE, ADVOGADOS, AREAS, AREAS_POR_SLUG, CHIPS, PROCESSO, DIFERENCIAIS,
    FAQ_GERAL, ARTIGOS, ARTIGOS_POR_SLUG,
)

RAIZ = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(RAIZ, "public")
DOM = SITE["dominio"]
HOJE = date.today().isoformat()

paginas_geradas = []  # (path, prioridade) para o sitemap


def _hash(rel):
    """Hash curto do arquivo, usado para invalidar cache do navegador."""
    import hashlib
    caminho = os.path.join(SAIDA, rel)
    if not os.path.exists(caminho):
        return "1"
    with open(caminho, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


V_CSS = _hash("assets/css/site.css")
V_JS = _hash("assets/js/site.js")


# --------------------------------------------------------------- ícones
def _svg(corpo, tamanho=24):
    return (
        f'<svg viewBox="0 0 24 24" width="{tamanho}" height="{tamanho}" fill="none" '
        f'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true" focusable="false">{corpo}</svg>'
    )


ICONS = {
    "familia": _svg('<path d="M8 11a3.2 3.2 0 1 0 0-6.4A3.2 3.2 0 0 0 8 11Z"/>'
                    '<path d="M17 12a2.6 2.6 0 1 0 0-5.2A2.6 2.6 0 0 0 17 12Z"/>'
                    '<path d="M2.5 20v-1.3A4.7 4.7 0 0 1 7.2 14h1.6a4.7 4.7 0 0 1 4.7 4.7V20"/>'
                    '<path d="M15 14.2h1.3a4.2 4.2 0 0 1 4.2 4.2V20"/>'),
    "imovel": _svg('<path d="M3.5 10.4 12 3.6l8.5 6.8"/>'
                   '<path d="M5.6 12v8.4h12.8V12"/>'
                   '<path d="M9.9 20.4v-5h4.2v5"/>'),
    "condominio": _svg('<path d="M3.6 20.4V6.2L11 3.6v16.8"/>'
                       '<path d="M11 9.4h6.6a1.8 1.8 0 0 1 1.8 1.8v9.2"/>'
                       '<path d="M6.4 8.4h1.8M6.4 12h1.8M6.4 15.6h1.8M14 13h1.8M14 16.6h1.8"/>'
                       '<path d="M2.4 20.4h19.2"/>'),
    "contrato": _svg('<path d="M13.4 3.6H7.2a1.8 1.8 0 0 0-1.8 1.8v13.2a1.8 1.8 0 0 0 1.8 1.8h9.6a1.8 1.8 0 0 0 1.8-1.8V8.6Z"/>'
                     '<path d="M13.4 3.6v5h5.2"/>'
                     '<path d="M8.8 13h6.4M8.8 16.4h4.2"/>'),
    "empresa": _svg('<path d="M4.2 8.2h15.6a1.6 1.6 0 0 1 1.6 1.6v8.8a1.6 1.6 0 0 1-1.6 1.6H4.2a1.6 1.6 0 0 1-1.6-1.6V9.8a1.6 1.6 0 0 1 1.6-1.6Z"/>'
                    '<path d="M8.8 8.2V5.8a1.6 1.6 0 0 1 1.6-1.6h3.2a1.6 1.6 0 0 1 1.6 1.6v2.4"/>'
                    '<path d="M2.6 12.8h18.8"/>'),
    "trabalho": _svg('<path d="M12 3.4v17.2"/>'
                     '<path d="M5.2 6.6 12 5.2l6.8 1.4"/>'
                     '<path d="M8.2 20.6h7.6"/>'
                     '<path d="M5.2 6.6 2.8 13a2.6 2.6 0 0 0 4.8 0Z"/>'
                     '<path d="M18.8 6.6 16.4 13a2.6 2.6 0 0 0 4.8 0Z"/>'),
    "mediacao": _svg('<path d="M12 3.4v17.2"/><path d="M5.2 6.6 12 5.2l6.8 1.4"/>'
                     '<path d="M8.2 20.6h7.6"/><path d="M5.2 6.6 2.8 13a2.6 2.6 0 0 0 4.8 0Z"/>'
                     '<path d="M18.8 6.6 16.4 13a2.6 2.6 0 0 0 4.8 0Z"/>'),
    "resposta": _svg('<path d="M12 21a9 9 0 1 0-9-9 9 9 0 0 0 9 9Z"/><path d="M12 7v5.2l3.4 2"/>'),
    "linguagem": _svg('<path d="M20.4 14.6a1.8 1.8 0 0 1-1.8 1.8H8l-4.4 3.4V5.4a1.8 1.8 0 0 1 1.8-1.8h13.2a1.8 1.8 0 0 1 1.8 1.8Z"/>'
                      '<path d="M8 8.6h8M8 12h5"/>'),
    "whatsapp": ('<svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" '
                 'aria-hidden="true" focusable="false"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91a9.82 9.82 0 0 0 1.35 4.96L2 22l5.28-1.38a9.9 9.9 0 0 0 4.76 1.21h.01c5.46 0 9.91-4.45 9.91-9.91C21.96 6.45 17.5 2 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.18-1.15l-.3-.18-3.13.82.84-3.05-.2-.31a8.19 8.19 0 0 1-1.26-4.37c0-4.54 3.7-8.23 8.24-8.23a8.23 8.23 0 0 1 8.23 8.24c0 4.54-3.7 8.23-8.23 8.23Zm4.52-6.16c-.25-.13-1.47-.72-1.69-.8-.23-.09-.39-.13-.56.12-.16.25-.64.8-.78.97-.15.16-.29.18-.53.06a6.7 6.7 0 0 1-1.99-1.23 7.48 7.48 0 0 1-1.38-1.71c-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.44.13-.15.17-.25.25-.42.09-.16.04-.31-.02-.43-.06-.13-.56-1.35-.77-1.85-.2-.48-.4-.42-.56-.42l-.47-.01c-.16 0-.43.06-.65.31-.23.25-.86.84-.86 2.05s.88 2.38 1 2.54c.13.17 1.74 2.65 4.21 3.72.59.25 1.04.4 1.4.52.59.18 1.13.16 1.55.1.47-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.11-.23-.17-.47-.29Z"/></svg>'),
    "telefone": _svg('<path d="M21 16.4v2.6a1.8 1.8 0 0 1-2 1.8 17.8 17.8 0 0 1-7.7-2.8 17.5 17.5 0 0 1-5.4-5.4A17.8 17.8 0 0 1 3.1 5a1.8 1.8 0 0 1 1.8-2h2.6a1.8 1.8 0 0 1 1.8 1.5c.1.9.3 1.7.6 2.5a1.8 1.8 0 0 1-.4 1.9l-1.1 1.1a14.4 14.4 0 0 0 5.4 5.4l1.1-1.1a1.8 1.8 0 0 1 1.9-.4c.8.3 1.6.5 2.5.6a1.8 1.8 0 0 1 1.7 1.9Z"/>'),
    "email": _svg('<path d="M4.2 4.8h15.6a1.8 1.8 0 0 1 1.8 1.8v10.8a1.8 1.8 0 0 1-1.8 1.8H4.2a1.8 1.8 0 0 1-1.8-1.8V6.6a1.8 1.8 0 0 1 1.8-1.8Z"/>'
                  '<path d="m2.7 6.4 9.3 6.2 9.3-6.2"/>'),
    "local": _svg('<path d="M20 10.4c0 5.6-8 12-8 12s-8-6.4-8-12a8 8 0 0 1 16 0Z"/>'
                  '<path d="M12 13.2a2.8 2.8 0 1 0 0-5.6 2.8 2.8 0 0 0 0 5.6Z"/>'),
    "relogio": _svg('<path d="M12 21a9 9 0 1 0-9-9 9 9 0 0 0 9 9Z"/><path d="M12 7v5.2l3.4 2"/>'),
    "seta": _svg('<path d="M4.5 12h15"/><path d="m13 5.5 6.5 6.5-6.5 6.5"/>', 16),
    "menu": _svg('<path d="M3.5 7h17M3.5 12h17M3.5 17h17"/>'),
    "fechar": _svg('<path d="M6 6l12 12M18 6 6 18"/>'),
    "sol": _svg('<path d="M12 16.4a4.4 4.4 0 1 0 0-8.8 4.4 4.4 0 0 0 0 8.8Z"/>'
                '<path d="M12 2.6v2.2M12 19.2v2.2M4.9 4.9l1.6 1.6M17.5 17.5l1.6 1.6'
                'M2.6 12h2.2M19.2 12h2.2M4.9 19.1l1.6-1.6M17.5 6.5l1.6-1.6"/>'),
    "lua": _svg('<path d="M20.5 14.4A8.6 8.6 0 0 1 9.6 3.5a8.6 8.6 0 1 0 10.9 10.9Z"/>'),
    "escudo": _svg('<path d="M12 21s7.2-3.4 7.2-9V5.9L12 3.2 4.8 5.9V12c0 5.6 7.2 9 7.2 9Z"/>'
                   '<path d="m9.2 11.8 2 2 3.6-3.6"/>'),
    "video": _svg('<path d="M4 6.4h9.6a1.8 1.8 0 0 1 1.8 1.8v7.6a1.8 1.8 0 0 1-1.8 1.8H4a1.8 1.8 0 0 1-1.8-1.8V8.2A1.8 1.8 0 0 1 4 6.4Z"/>'
                  '<path d="m15.4 12 6.4-3.6v7.2L15.4 12Z"/>'),
}


# --------------------------------------------------------------- helpers
def e(texto):
    return html.escape(str(texto), quote=True)


def wa_link(numero, mensagem):
    from urllib.parse import quote
    return f"https://wa.me/{numero}?text={quote(mensagem)}"


WA_PADRAO = wa_link(SITE["whatsapp"], "Olá! Vim pelo site e gostaria de falar com um advogado.")


def escrever(caminho_rel, conteudo):
    destino = os.path.join(SAIDA, caminho_rel)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(conteudo)


# --------------------------------------------------------------- navegação
NAV = [
    ("/", "Início"),
    ("/escritorio/", "O escritório"),
    ("/advogados/", "Advogados"),
    ("/areas/", "Áreas de atuação"),
    ("/artigos/", "Artigos"),
    ("/contato/", "Contato"),
]


def header_html(atual):
    itens = []
    for href, rotulo in NAV:
        atual_attr = ' aria-current="page"' if href == atual else ""
        itens.append(f'<li><a class="nav__link" href="{href}"{atual_attr}>{e(rotulo)}</a></li>')
    itens.append(
        f'<li class="nav__drawer-cta"><a class="btn btn--wa btn--block" href="{WA_PADRAO}" '
        f'target="_blank" rel="noopener">{ICONS["whatsapp"]}Falar no WhatsApp</a></li>'
    )
    lista = "\n          ".join(itens)

    return f"""<a class="skip-link" href="#conteudo">Ir para o conteúdo</a>
<header class="site-header">
  <div class="wrap">
    <nav class="nav" aria-label="Navegação principal">
      <a class="brand" href="/" aria-label="{e(SITE['nome'])} — página inicial">
        <span class="brand__mark" aria-hidden="true">GW</span>
        <span>
          <span class="brand__name">GR &amp; WMF</span>
          <span class="brand__sub">Advogados</span>
        </span>
      </a>
      <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="nav-list">
        <span class="icon-open">{ICONS["menu"]}</span>
        <span class="icon-close">{ICONS["fechar"]}</span>
        <span class="sr-only">Abrir menu</span>
      </button>
      <ul class="nav__list" id="nav-list">
          {lista}
      </ul>
      <button class="tema" type="button" id="alternar-tema"
              aria-label="Mudar para o tema claro" aria-pressed="false">
        <span class="tema__lua">{ICONS["lua"]}</span>
        <span class="tema__sol">{ICONS["sol"]}</span>
      </button>
      <a class="btn btn--primary nav__cta" href="/contato/">Agendar consulta</a>
    </nav>
  </div>
</header>"""


def footer_html():
    areas_links = "\n        ".join(
        f'<li><a href="/areas/{a["slug"]}/">{e(a["nome"])}</a></li>' for a in AREAS
    )
    return f"""<footer class="site-footer footer">
  <div class="wrap">
    <div class="footer__top">
      <div class="footer__brand">
        <a class="brand" href="/">
          <span class="brand__mark" aria-hidden="true">GW</span>
          <span>
            <span class="brand__name">GR &amp; WMF</span>
            <span class="brand__sub">Advogados</span>
          </span>
        </a>
        <p class="footer__about">
          Escritório de advocacia em Belo Horizonte, com atuação em Família e Sucessões,
          Imobiliário, Condominial, Contratual, Empresarial e Trabalhista.
        </p>
      </div>

      <nav aria-labelledby="rodape-areas">
        <h3 id="rodape-areas">Áreas de atuação</h3>
        <ul class="footer__list">
        {areas_links}
        </ul>
      </nav>

      <nav aria-labelledby="rodape-site">
        <h3 id="rodape-site">O escritório</h3>
        <ul class="footer__list">
          <li><a href="/escritorio/">Sobre nós</a></li>
          <li><a href="/advogados/">Advogados</a></li>
          <li><a href="/artigos/">Artigos</a></li>
          <li><a href="/perguntas-frequentes/">Perguntas frequentes</a></li>
          <li><a href="/contato/">Contato</a></li>
          <li><a href="/politica-de-privacidade/">Política de privacidade</a></li>
        </ul>
      </nav>

      <div>
        <h3>Atendimento</h3>
        <address>
          {e(SITE['endereco'])}<br>
          {e(SITE['cidade'])}/{SITE['uf']} — CEP {e(SITE['cep'])}<br><br>
          <a href="https://wa.me/{SITE['whatsapp']}" target="_blank" rel="noopener">{e(SITE['tel_exibicao'])}</a> ·
          <a href="https://wa.me/{SITE['whatsapp_2']}" target="_blank" rel="noopener">{e(SITE['tel_exibicao_2'])}</a><br>
          <a href="mailto:{SITE['email']}">{e(SITE['email'])}</a><br><br>
          {e(SITE['horario'])}
        </address>
      </div>
    </div>

    <div class="footer__bottom">
      <p>© <span data-year>{date.today().year}</span> {e(SITE['nome'])} — Todos os direitos reservados.</p>
      <p class="footer__legal">
        Conteúdo meramente informativo, nos termos do Provimento 205/2021 da OAB.
        Não constitui consulta jurídica nem oferta de serviços.
        {" · ".join(a["oab"] for a in ADVOGADOS)}
      </p>
    </div>
  </div>
</footer>"""


COOKIE_HTML = """<div class="cookie" role="dialog" aria-labelledby="cookie-titulo" aria-describedby="cookie-texto">
  <h2 id="cookie-titulo" class="sr-only">Uso de cookies</h2>
  <p id="cookie-texto">
    Usamos cookies apenas para entender como o site é usado e melhorá-lo.
    Você pode recusar sem perder nenhuma funcionalidade.
    <a href="/politica-de-privacidade/">Leia a política de privacidade</a>.
  </p>
  <div class="btn-row">
    <button class="btn btn--primary" type="button" data-consent="aceito">Aceitar</button>
    <button class="btn btn--ghost" type="button" data-consent="recusado">Recusar</button>
  </div>
</div>"""


def wa_float(mensagem="Olá! Vim pelo site e gostaria de falar com um advogado."):
    return (f'<a class="wa-float" href="{wa_link(SITE["whatsapp"], mensagem)}" target="_blank" '
            f'rel="noopener" aria-label="Falar com o escritório pelo WhatsApp">'
            f'{ICONS["whatsapp"]}<span>Falar no WhatsApp</span></a>')


# --------------------------------------------------------------- shell
def pagina(path, title, description, corpo, schema=None, atual=None,
           og_type="website", prioridade="0.7", no_index=False, wa_msg=None):
    """Monta o HTML completo de uma página e agenda o registro no sitemap."""
    url = DOM + "/" + (path + "/" if path else "")
    url = url.replace("//", "//", 1)
    canonical = f"{DOM}/" if not path else f"{DOM}/{path}/"

    schema_tags = ""
    for bloco in (schema or []):
        schema_tags += ('\n  <script type="application/ld+json">'
                        + json.dumps(bloco, ensure_ascii=False, separators=(",", ":"))
                        + "</script>")

    robots = '\n  <meta name="robots" content="noindex,follow">' if no_index else ""
    if not no_index:
        paginas_geradas.append((canonical, prioridade))

    doc = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{canonical}">{robots}
  <meta name="theme-color" content="#141B29">

  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{e(SITE['nome'])}">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{DOM}/assets/img/og-grwmf.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(description)}">
  <meta name="twitter:image" content="{DOM}/assets/img/og-grwmf.png">

  <link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600&family=Lato:wght@400;700&display=swap">
  <link rel="stylesheet" href="/assets/css/site.css?v={V_CSS}">
  <script>
    // roda antes da primeira pintura: sem isto a página pisca no tema errado
    try {{
      var t = localStorage.getItem("grwmf.tema");
      if (t === "light") document.documentElement.setAttribute("data-theme", "light");
    }} catch (e) {{}}
  </script>{schema_tags}
</head>
<body>
{header_html(atual)}
<main id="conteudo">
{corpo}
</main>
{footer_html()}
{wa_float(wa_msg) if wa_msg else wa_float()}
{COOKIE_HTML}
<script src="/assets/js/site.js?v={V_JS}" defer></script>
</body>
</html>
"""
    destino = "index.html" if not path else f"{path}/index.html"
    escrever(destino, doc)


# --------------------------------------------------------------- schema.org
ORG_ID = f"{DOM}/#escritorio"

SCHEMA_ORG = {
    "@context": "https://schema.org",
    "@type": "LegalService",
    "@id": ORG_ID,
    "name": SITE["nome"],
    "url": DOM + "/",
    "image": f"{DOM}/assets/img/og-grwmf.png",
    "email": SITE["email"],
    "telephone": "+55" + SITE["whatsapp"][2:],
    "priceRange": "$$",
    "areaServed": [
        {"@type": "City", "name": "Belo Horizonte"},
        {"@type": "State", "name": "Minas Gerais"},
    ],
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Rua Flávio Marques Lisboa, 511, 2º andar",
        "addressLocality": "Belo Horizonte",
        "addressRegion": "MG",
        "postalCode": SITE["cep"],
        "addressCountry": "BR",
    },
    "geo": {"@type": "GeoCoordinates",
            "latitude": SITE["geo"]["lat"], "longitude": SITE["geo"]["lng"]},
    "openingHours": SITE["horario_schema"],
    "knowsLanguage": "pt-BR",
    "makesOffer": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": a["nome"],
                                           "url": f"{DOM}/areas/{a['slug']}/"}}
        for a in AREAS
    ],
    "employee": [
        {"@type": "Attorney", "name": a["nome"], "url": f"{DOM}/advogados/{a['slug']}/",
         "identifier": a["oab"], "jobTitle": "Advogado(a)"}
        for a in ADVOGADOS
    ],
}


def schema_breadcrumb(itens):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": nome,
             "item": DOM + href if href else DOM + "/"}
            for i, (href, nome) in enumerate(itens)
        ],
    }


def schema_faq(pares):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": p,
             "acceptedAnswer": {"@type": "Answer", "text": r}}
            for p, r in pares
        ],
    }


# --------------------------------------------------------------- componentes
def crumbs(itens):
    """itens: lista de (href|None, rótulo). O último é a página atual."""
    partes = []
    for href, rotulo in itens:
        if href:
            partes.append(f'<li><a href="{href}">{e(rotulo)}</a></li>')
        else:
            partes.append(f'<li><span aria-current="page">{e(rotulo)}</span></li>')
    return f'<ol class="crumbs">{"".join(partes)}</ol>'


def bloco_faq(pares, titulo="Perguntas frequentes", eyebrow="Dúvidas comuns",
              intro=None, fundo="section--white"):
    itens = ""
    for pergunta, resposta in pares:
        itens += f"""
      <details class="faq__item">
        <summary>{e(pergunta)}</summary>
        <div class="faq__answer"><p>{e(resposta)}</p></div>
      </details>"""
    intro_html = f'<p class="lead">{e(intro)}</p>' if intro else ""
    return f"""<section class="section {fundo}">
  <div class="wrap wrap--narrow">
    <div class="section-head reveal">
      <span class="eyebrow">{e(eyebrow)}</span>
      <h2>{e(titulo)}</h2>
      {intro_html}
    </div>
    <div class="faq reveal">{itens}
    </div>
  </div>
</section>"""


def cta_band(titulo, texto, msg_wa, botao_secundario=True):
    sec = ('<a class="btn btn--onDark" href="/contato/">Enviar formulário</a>'
           if botao_secundario else "")
    return f"""<section class="cta-band">
  <span class="ghost" aria-hidden="true">Contato</span>
  <div class="wrap">
    <div class="reveal" style="position:relative;z-index:1">
      <span class="eyebrow">Próximo passo</span>
      <h2>{e(titulo)}</h2>
      <p>{e(texto)}</p>
      <div class="btn-row">
        <a class="btn btn--wa" href="{wa_link(SITE['whatsapp'], msg_wa)}" target="_blank" rel="noopener">
          {ICONS['whatsapp']}Falar no WhatsApp
        </a>
        {sec}
      </div>
    </div>
  </div>
</section>"""


def card_area(a):
    return f"""<article class="card card--link reveal">
      <div class="card__body">
        <span class="card__icon" aria-hidden="true">{ICONS[a['icone']]}</span>
        <h3><a href="/areas/{a['slug']}/">{e(a['nome'])}</a></h3>
        <p class="card__dor">{e(a['dor'])}</p>
        <p>{e(a['resumo'])}</p>
        <span class="link-arrow">Ver como atuamos {ICONS['seta']}</span>
      </div>
    </article>"""


def foto_ou_placeholder(src, alt, iniciais, classe=""):
    """Usa a foto real se ela existir em public/; senão, um placeholder digno."""
    caminho = os.path.join(SAIDA, src.lstrip("/"))
    if os.path.exists(caminho):
        return f'<img src="{src}" alt="{e(alt)}" loading="lazy" decoding="async" class="{classe}">'
    return (f'<div class="ph" role="img" aria-label="{e(alt)}">'
            f'<span class="ph__mark">{e(iniciais)}</span></div>')


# =============================================================== PÁGINAS
def build_home():
    cards = "\n    ".join(card_area(a) for a in AREAS)

    # atalhos da primeira dobra: a palavra que o cliente usa, não o nome da disciplina
    chips = "\n            ".join(
        f'<li><a href="/areas/{slug}/">{e(rotulo)}</a></li>' for rotulo, slug in CHIPS
    )

    pilares = ""
    for icone, titulo, texto in DIFERENCIAIS:
        pilares += f"""
      <article class="pillar reveal">
        <span class="pillar__icon" aria-hidden="true">{ICONS[icone]}</span>
        <h3>{e(titulo)}</h3>
        <p>{e(texto)}</p>
      </article>"""

    passos = ""
    for titulo, texto in PROCESSO:
        passos += f"""
      <article class="step reveal">
        <h3>{e(titulo)}</h3>
        <p>{e(texto)}</p>
      </article>"""

    perfis = ""
    for adv in ADVOGADOS:
        areas_adv = " · ".join(AREAS_POR_SLUG[s]["nome"] for s in adv["areas"])
        perfis += f"""
      <article class="card reveal">
        <div class="card__media">{foto_ou_placeholder(adv['foto'], adv['nome'] + ' — ' + adv['cargo'], adv['iniciais'])}</div>
        <div class="card__body">
          <span class="profile__oab">{e(adv['oab'])}</span>
          <h3>{e(adv['trato'])} {e(adv['nome'])}</h3>
          <p class="card__dor">{e(areas_adv)}</p>
          <p>{e(adv['resumo'])}</p>
          <a class="link-arrow" href="/advogados/{adv['slug']}/">Ver perfil completo {ICONS['seta']}</a>
        </div>
      </article>"""

    artigos = ""
    for art in ARTIGOS[:3]:
        area = AREAS_POR_SLUG[art["area"]]
        artigos += f"""
      <article class="card card--link article-card reveal">
        <div class="card__body">
          <span class="article-card__tag">{e(area['nome'])}</span>
          <h3><a href="/artigos/{art['slug']}/">{e(art['titulo'])}</a></h3>
          <p>{e(art['resumo'])}</p>
          <p class="article-card__meta">{e(art['data_exibicao'])} · {e(art['leitura'])} de leitura</p>
        </div>
      </article>"""

    corpo = f"""<section class="hero">
  <span class="ghost" aria-hidden="true">Advocacia</span>
  <div class="wrap">
    <div class="hero__grid">
      <div class="hero__media">
        {foto_ou_placeholder('/assets/img/escritorio-hero.jpg',
                             'Equipe do escritório GR & WMF Advogados em atendimento', 'GR & WMF')}
      </div>
      <div class="hero__texto">
        <span class="eyebrow">Belo Horizonte · Barreiro</span>
        <h1>Advocacia de Família, Sucessões e Imobiliário em Belo Horizonte</h1>
        <p class="hero__lead">
          Explicamos os caminhos em português e buscamos o acordo antes do processo,
          sempre que ele for possível.
        </p>

        <nav class="hero__chips" aria-label="Atalhos por assunto">
          <span class="hero__chips-rotulo">Comece por</span>
          <ul>
            {chips}
          </ul>
        </nav>

        <div class="btn-row hero__acoes">
          <a class="btn btn--wa" href="{wa_link(SITE['whatsapp'], 'Olá! Vim pelo site e gostaria de falar sobre o meu caso.')}" target="_blank" rel="noopener">
            {ICONS['whatsapp']}Falar no WhatsApp
          </a>
          <a class="btn btn--ghost" href="/contato/">Agendar consulta</a>
        </div>

        <ul class="hero__trust">
          <li>{ICONS['escudo']}<span>{e(ADVOGADOS[0]['oab'])} · {e(ADVOGADOS[1]['oab'])}</span></li>
          <li>{ICONS['relogio']}<span>Resposta em 1 dia útil</span></li>
          <li class="hero__trust-extra">{ICONS['video']}<span>Presencial ou por videochamada</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section--tight">
  <div class="facts">
    <div class="fact"><span class="fact__n">6</span><span class="fact__l">áreas de atuação</span></div>
    <div class="fact"><span class="fact__n">2</span><span class="fact__l">sócios inscritos na OAB/MG</span></div>
    <div class="fact"><span class="fact__n">1 dia útil</span><span class="fact__l">para o primeiro retorno</span></div>
    <div class="fact"><span class="fact__n">BH</span><span class="fact__l">e região metropolitana</span></div>
  </div>
</section>

<section class="section">
  <span class="ghost" aria-hidden="true">Atuação</span>
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Como podemos ajudar</span>
      <h2>Encontre a sua situação</h2>
      <p class="lead">
        Cada área começa por um problema real de cliente, não por um nome de disciplina jurídica.
        Escolha o que mais se parece com o que você está vivendo.
      </p>
    </div>
    <div class="grid grid--3">
    {cards}
    </div>
  </div>
</section>

<section class="section section--cream2">
  <div class="wrap">
    <div class="section-head section-head--center reveal">
      <span class="eyebrow">Como trabalhamos</span>
      <h2>Três compromissos que valem para todo caso</h2>
    </div>
    <div class="grid grid--3">{pilares}
    </div>
  </div>
</section>

<section class="section">
  <span class="ghost" aria-hidden="true">Processo</span>
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Do primeiro contato ao caso em andamento</span>
      <h2>O que acontece depois que você chama</h2>
      <p class="lead">
        Quatro etapas, nesta ordem. Você sempre sabe em qual delas o seu caso está.
      </p>
    </div>
    <div class="steps">{passos}
    </div>
  </div>
</section>

<section class="section section--cream2">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Quem vai cuidar do seu caso</span>
      <h2>Os advogados</h2>
      <p class="lead">
        O escritório nasceu da união entre a GR Advocacia e a WMF Advocacia. Você fala
        diretamente com quem conduz o caso — não com um intermediário.
      </p>
    </div>
    <div class="grid grid--2">{perfis}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Conteúdo</span>
      <h2>Artigos do escritório</h2>
      <p class="lead">
        Escrevemos sobre as dúvidas que mais chegam no atendimento. Material informativo,
        sem substituir a análise do seu caso.
      </p>
    </div>
    <div class="grid grid--3">{artigos}
    </div>
    <p class="section-more"><a class="link-arrow" href="/artigos/">Ver todos os artigos {ICONS['seta']}</a></p>
  </div>
</section>

{bloco_faq(FAQ_GERAL[:4], titulo="Antes de entrar em contato",
           eyebrow="Perguntas frequentes",
           intro="As dúvidas que mais recebemos sobre como o atendimento funciona.",
           fundo="section--cream2")}

{cta_band("Conte o que está acontecendo",
          "A primeira conversa serve para entender o seu caso e dizer, com honestidade, "
          "se e como podemos ajudar. Retornamos em até 1 dia útil.",
          "Olá! Vim pelo site e gostaria de agendar uma consulta.")}"""

    pagina(
        "", "Advogados em Belo Horizonte | Família, Sucessões e Imobiliário",
        "Advocacia em Belo Horizonte: Família e Sucessões, Imobiliário, Condominial, "
        "Contratual, Empresarial e Trabalhista. Atendimento no Barreiro ou por vídeo.",
        corpo,
        schema=[SCHEMA_ORG, schema_faq(FAQ_GERAL[:4])],
        atual="/", prioridade="1.0",
        wa_msg="Olá! Vim pelo site e gostaria de falar sobre o meu caso.",
    )


def build_escritorio():
    corpo = f"""<section class="page-hero">
  <span class="ghost" aria-hidden="true">Escritório</span>
  <div class="wrap wrap--narrow">
    {crumbs([("/", "Início"), (None, "O escritório")])}
    <h1>Dois escritórios que decidiram caminhar juntos</h1>
    <p class="lead">
      A GR &amp; WMF Advogados nasceu da união entre a GR Advocacia, de Gabriella Reis
      Antunes Ferreira, e a WMF Advocacia, de Welberth Martins Ferreira. A soma cobre as
      duas frentes que mais aparecem na vida das pessoas e das empresas: o patrimônio
      familiar e as relações de trabalho e negócio.
    </p>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--narrow">
    <div class="prose reveal">
      <h2>O que orienta o trabalho</h2>
      <p>
        A atuação do escritório se concentra em Direito de Família e Sucessões, Direito
        Imobiliário, Direito Condominial, Direito Contratual, Direito Empresarial e Direito
        Trabalhista, tanto na frente consultiva e preventiva quanto no contencioso judicial
        e extrajudicial.
      </p>
      <p>
        Duas escolhas definem como conduzimos os casos. A primeira é priorizar a solução
        consensual: conciliação e mediação resolvem boa parte das disputas de forma mais
        rápida e menos desgastante do que anos de processo — e quando não resolvem, o
        litígio segue com o terreno já mapeado. A segunda é explicar. Cliente que entende o
        que está sendo feito decide melhor, cobra melhor e se frustra menos.
      </p>

      <h2>Atendimento presencial e online</h2>
      <p>
        O escritório fica na {e(SITE['endereco'])}, em {e(SITE['cidade'])}. Boa parte dos
        casos também é conduzida à distância, por videochamada, e-mail e assinatura
        eletrônica — o que atende quem mora em outra região de Minas ou simplesmente não
        consegue se deslocar no horário comercial.
      </p>

      <h2>Sobre o que você lê aqui</h2>
      <p>
        Todo o conteúdo deste site é informativo. Seguindo o Provimento 205/2021 e o Código
        de Ética da advocacia, não divulgamos valores de honorários, não publicamos casos de
        êxito, não usamos depoimentos de clientes e não prometemos resultado — nem aqui, nem
        na consulta. O que oferecemos é análise honesta e trabalho técnico.
      </p>
    </div>

    <div class="callout reveal">
      <p><strong>Sigilo profissional.</strong> Tudo o que você contar, na consulta ou pelo
      WhatsApp, é protegido por sigilo — inclusive se o caso não for adiante.</p>
    </div>
  </div>
</section>

<section class="section section--cream2">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Método</span>
      <h2>Como o caso caminha</h2>
    </div>
    <div class="steps">
      {"".join(f'<article class="step reveal"><h3>{e(t)}</h3><p>{e(x)}</p></article>' for t, x in PROCESSO)}
    </div>
  </div>
</section>

{cta_band("Quer entender se o seu caso é da nossa área?",
          "Conte em poucas linhas o que está acontecendo. Se não for a nossa área, dizemos "
          "isso na primeira resposta — e, quando possível, indicamos o caminho.",
          "Olá! Gostaria de saber se o meu caso é da área de atuação de vocês.")}"""

    pagina(
        "escritorio", f"O escritório | {SITE['nome']}",
        "A GR & WMF Advogados nasceu da união entre a GR Advocacia e a WMF Advocacia. "
        "Conheça a forma de atuação do escritório em Belo Horizonte.",
        corpo,
        schema=[schema_breadcrumb([("/", "Início"), ("/escritorio/", "O escritório")])],
        atual="/escritorio/", prioridade="0.8",
    )


def build_advogados():
    cards = ""
    for adv in ADVOGADOS:
        areas_adv = " · ".join(AREAS_POR_SLUG[s]["nome"] for s in adv["areas"])
        cards += f"""
      <article class="card card--link reveal">
        <div class="card__media">{foto_ou_placeholder(adv['foto'], adv['nome'] + ' — ' + adv['cargo'], adv['iniciais'])}</div>
        <div class="card__body">
          <span class="profile__oab">{e(adv['oab'])}</span>
          <h3><a href="/advogados/{adv['slug']}/">{e(adv['trato'])} {e(adv['nome'])}</a></h3>
          <p class="card__dor">{e(areas_adv)}</p>
          <p>{e(adv['resumo'])}</p>
          <span class="link-arrow">Ver perfil completo {ICONS['seta']}</span>
        </div>
      </article>"""

    corpo = f"""<section class="page-hero">
  <span class="ghost" aria-hidden="true">Equipe</span>
  <div class="wrap">
    {crumbs([("/", "Início"), (None, "Advogados")])}
    <h1>Os advogados</h1>
    <p class="lead">
      Escritório de dois sócios. Quem atende é quem conduz o caso — e você sabe desde o
      primeiro dia com quem está falando.
    </p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid grid--2">{cards}
    </div>
  </div>
</section>

{cta_band("Fale diretamente com quem vai cuidar do caso",
          "Cada sócio atende as próprias áreas. Se preferir, escreva pelo formulário e "
          "direcionamos internamente.",
          "Olá! Vim pelo site e gostaria de falar com um dos advogados.")}"""

    pagina(
        "advogados", f"Advogados | {SITE['nome']}",
        "Conheça os advogados da GR & WMF: Gabriella Reis Antunes Ferreira (OAB/MG 224.424) "
        "e Welberth Martins Ferreira (OAB/MG 183.884), em Belo Horizonte.",
        corpo,
        schema=[schema_breadcrumb([("/", "Início"), ("/advogados/", "Advogados")])],
        atual="/advogados/", prioridade="0.8",
    )

    for adv in ADVOGADOS:
        build_advogado(adv)


def build_advogado(adv):
    bio = "".join(f"<p>{e(p)}</p>" for p in adv["bio"])
    creds = "".join(f"<li>{e(c)}</li>" for c in adv["formacao"])
    areas_links = "".join(
        f'<li><a href="/areas/{s}/">{e(AREAS_POR_SLUG[s]["nome"])}</a></li>' for s in adv["areas"]
    )
    msg = f"Olá, {adv['nome'].split()[0]}! Vim pelo site e gostaria de falar sobre o meu caso."

    corpo = f"""<section class="page-hero">
  <div class="wrap">
    {crumbs([("/", "Início"), ("/advogados/", "Advogados"), (None, adv["nome"])])}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="profile">
      <div class="profile__photo reveal">
        {foto_ou_placeholder(adv['foto'], adv['nome'] + ' — ' + adv['cargo'], adv['iniciais'])}
      </div>
      <div class="reveal">
        <span class="profile__oab">{e(adv['oab'])}</span>
        <h1>{e(adv['trato'])} {e(adv['nome'])}</h1>
        <p class="profile__role">{e(adv['cargo'])}</p>

        <ul class="creds">{creds}</ul>

        <div class="prose">{bio}</div>

        <h2 style="font-size:var(--fs-xl);margin:32px 0 14px">Áreas em que atua</h2>
        <ul class="footer__list" style="gap:8px">{areas_links}</ul>

        <div class="btn-row" style="margin-top:32px">
          <a class="btn btn--wa" href="{wa_link(adv['whatsapp'], msg)}" target="_blank" rel="noopener">
            {ICONS['whatsapp']}Falar no WhatsApp
          </a>
          <a class="btn btn--ghost" href="/contato/">Enviar formulário</a>
        </div>
      </div>
    </div>
  </div>
</section>

{cta_band("Prefere explicar por escrito?",
          "O formulário de contato permite descrever o caso com calma e anexar o contexto "
          "que for necessário. Retornamos em até 1 dia útil.",
          msg)}"""

    schema_pessoa = {
        "@context": "https://schema.org",
        "@type": "Attorney",
        "name": adv["nome"],
        "url": f"{DOM}/advogados/{adv['slug']}/",
        "jobTitle": adv["cargo"],
        "identifier": adv["oab"],
        "telephone": "+" + adv["whatsapp"],
        "worksFor": {"@id": ORG_ID},
        "knowsAbout": [AREAS_POR_SLUG[s]["nome"] for s in adv["areas"]],
        "address": SCHEMA_ORG["address"],
    }

    pagina(
        f"advogados/{adv['slug']}",
        f"{adv['trato']} {adv['nome'].split()[0]} {adv['nome'].split()[-1]} | GR & WMF",
        f"{adv['nome']} ({adv['oab']}), advogado(a) em Belo Horizonte com atuação em "
        + ", ".join(AREAS_POR_SLUG[s]["nome"] for s in adv["areas"]) + ".",
        corpo,
        schema=[schema_pessoa,
                schema_breadcrumb([("/", "Início"), ("/advogados/", "Advogados"),
                                   (f"/advogados/{adv['slug']}/", adv["nome"])])],
        atual="/advogados/", prioridade="0.6", og_type="profile", wa_msg=msg,
    )


def build_areas():
    cards = "\n    ".join(card_area(a) for a in AREAS)
    corpo = f"""<section class="page-hero">
  <span class="ghost" aria-hidden="true">Áreas</span>
  <div class="wrap">
    {crumbs([("/", "Início"), (None, "Áreas de atuação")])}
    <h1>Áreas de atuação</h1>
    <p class="lead">
      Seis áreas, uma lógica em comum: entender o objetivo antes de escolher o caminho
      jurídico. Cada página explica quando procurar, o que fazemos e responde as dúvidas
      mais frequentes daquele tema.
    </p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid grid--3">
    {cards}
    </div>
  </div>
</section>

{cta_band("Não tem certeza de qual é a sua área?",
          "Descreva a situação em poucas linhas. Identificamos a área e dizemos como "
          "costumamos conduzir casos parecidos.",
          "Olá! Vim pelo site e não sei em qual área o meu caso se encaixa.")}"""

    pagina(
        "areas", f"Áreas de atuação | {SITE['nome']}",
        "Família e Sucessões, Imobiliário, Condominial, Contratual, Empresarial e "
        "Trabalhista. Conheça as áreas de atuação da GR & WMF Advogados em Belo Horizonte.",
        corpo,
        schema=[schema_breadcrumb([("/", "Início"), ("/areas/", "Áreas de atuação")])],
        atual="/areas/", prioridade="0.9",
    )

    for area in AREAS:
        build_area(area)


def build_area(area):
    quando = "".join(f"<li>{e(q)}</li>" for q in area["quando"])
    servicos = "".join(
        f'<div class="service"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in area["servicos"]
    )
    msg = f"Olá! Vim pelo site, na página de {area['nome']}, e gostaria de falar sobre o meu caso."

    outras = [a for a in AREAS if a["slug"] != area["slug"]][:3]
    outras_html = "\n    ".join(card_area(a) for a in outras)

    corpo = f"""<section class="page-hero">
  <span class="ghost" aria-hidden="true">{e(area['nome'].split()[0])}</span>
  <div class="wrap wrap--narrow">
    {crumbs([("/", "Início"), ("/areas/", "Áreas de atuação"), (None, area["nome"])])}
    <h1>{e(area['h1'])}</h1>
    <p class="lead">{e(area['lead'])}</p>
    <div class="btn-row" style="margin-top:26px">
      <a class="btn btn--wa" href="{wa_link(SITE['whatsapp'], msg)}" target="_blank" rel="noopener">
        {ICONS['whatsapp']}Falar no WhatsApp
      </a>
      <a class="btn btn--ghost" href="/contato/">Agendar consulta</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--narrow">
    <div class="section-head reveal">
      <span class="eyebrow">Quando procurar</span>
      <h2>Situações em que costumamos ser chamados</h2>
    </div>
    <ul class="checklist reveal">{quando}</ul>
  </div>
</section>

<section class="section section--cream2">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">O que fazemos</span>
      <h2>Serviços em {e(area['nome'])}</h2>
    </div>
    <div class="services reveal">{servicos}</div>
    <p class="note" style="margin-top:26px">
      Esta lista é informativa e não representa oferta de serviços nem garantia de
      resultado. A viabilidade de cada medida depende da análise do caso concreto.
    </p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Como conduzimos</span>
      <h2>Do primeiro contato ao caso resolvido</h2>
    </div>
    <div class="steps">
      {"".join(f'<article class="step reveal"><h3>{e(t)}</h3><p>{e(x)}</p></article>' for t, x in PROCESSO)}
    </div>
  </div>
</section>

{bloco_faq(area["faq"], titulo=f"Dúvidas sobre {area['nome']}",
           eyebrow="Perguntas frequentes", fundo="section--cream2")}

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Outras áreas</span>
      <h2>Talvez o seu caso envolva mais de um tema</h2>
    </div>
    <div class="grid grid--3">
    {outras_html}
    </div>
  </div>
</section>

{cta_band(f"Conte o seu caso de {area['nome']}",
          "Na primeira conversa avaliamos os documentos, explicamos os caminhos possíveis "
          "e os riscos de cada um. Retornamos em até 1 dia útil.",
          msg)}"""

    schema_servico = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": area["nome"],
        "serviceType": area["nome"],
        "url": f"{DOM}/areas/{area['slug']}/",
        "description": area["resumo"],
        "provider": {"@id": ORG_ID},
        "areaServed": {"@type": "City", "name": "Belo Horizonte"},
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": area["nome"],
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": d}}
                for t, d in area["servicos"]
            ],
        },
    }

    pagina(
        f"areas/{area['slug']}",
        f"{area['meta_title']} | GR & WMF",
        area["meta_desc"],
        corpo,
        schema=[schema_servico, schema_faq(area["faq"]),
                schema_breadcrumb([("/", "Início"), ("/areas/", "Áreas de atuação"),
                                   (f"/areas/{area['slug']}/", area["nome"])])],
        atual="/areas/", prioridade="0.9", wa_msg=msg,
    )


def build_artigos():
    cards = ""
    for art in ARTIGOS:
        area = AREAS_POR_SLUG[art["area"]]
        cards += f"""
      <article class="card card--link article-card reveal">
        <div class="card__body">
          <span class="article-card__tag">{e(area['nome'])}</span>
          <h3><a href="/artigos/{art['slug']}/">{e(art['titulo'])}</a></h3>
          <p>{e(art['resumo'])}</p>
          <p class="article-card__meta">{e(art['data_exibicao'])} · {e(art['leitura'])} de leitura</p>
        </div>
      </article>"""

    corpo = f"""<section class="page-hero">
  <span class="ghost" aria-hidden="true">Artigos</span>
  <div class="wrap">
    {crumbs([("/", "Início"), (None, "Artigos")])}
    <h1>Artigos</h1>
    <p class="lead">
      Escrevemos sobre as dúvidas que mais chegam no atendimento — em linguagem de quem
      precisa decidir, não de quem escreve petição. Conteúdo informativo, que não substitui
      a análise do caso concreto.
    </p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid grid--3">{cards}
    </div>
  </div>
</section>

{cta_band("Sua dúvida não estava aqui?",
          "Mande a pergunta. Se ela for comum, provavelmente vira o próximo artigo — e "
          "de qualquer forma você recebe uma resposta.",
          "Olá! Li um artigo no site e fiquei com uma dúvida.")}"""

    pagina(
        "artigos", f"Artigos | {SITE['nome']}",
        "Artigos sobre inventário, divórcio, compra de imóvel, condomínio, contratos e "
        "direito do trabalho, escritos pela equipe da GR & WMF Advogados.",
        corpo,
        schema=[schema_breadcrumb([("/", "Início"), ("/artigos/", "Artigos")])],
        atual="/artigos/", prioridade="0.7",
    )

    for art in ARTIGOS:
        build_artigo(art)


def build_artigo(art):
    area = AREAS_POR_SLUG[art["area"]]
    autor = next(a for a in ADVOGADOS if a["slug"] == art["autor"])

    corpo_html = ""
    for tipo, valor in art["corpo"]:
        if tipo == "p":
            corpo_html += f"<p>{e(valor)}</p>"
        elif tipo == "h2":
            corpo_html += f"<h2>{e(valor)}</h2>"
        elif tipo == "ul":
            corpo_html += "<ul>" + "".join(f"<li>{e(i)}</li>" for i in valor) + "</ul>"

    outros = [a for a in ARTIGOS if a["slug"] != art["slug"]][:2]
    outros_html = ""
    for o in outros:
        oa = AREAS_POR_SLUG[o["area"]]
        outros_html += f"""
      <article class="card card--link article-card reveal">
        <div class="card__body">
          <span class="article-card__tag">{e(oa['nome'])}</span>
          <h3><a href="/artigos/{o['slug']}/">{e(o['titulo'])}</a></h3>
          <p>{e(o['resumo'])}</p>
        </div>
      </article>"""

    msg = f"Olá! Li o artigo \"{art['titulo']}\" no site e gostaria de tirar uma dúvida."

    corpo = f"""<section class="page-hero">
  <div class="wrap wrap--narrow">
    {crumbs([("/", "Início"), ("/artigos/", "Artigos"), (None, art["titulo"])])}
    <span class="tag">{e(area['nome'])}</span>
    <h1 style="margin-top:14px">{e(art['titulo'])}</h1>
    <p class="article-card__meta" style="margin-top:16px">
      Por <a href="/advogados/{autor['slug']}/">{e(autor['trato'])} {e(autor['nome'])}</a>
      · <time datetime="{art['data']}">{e(art['data_exibicao'])}</time>
      · {e(art['leitura'])} de leitura
    </p>
  </div>
</section>

<article class="section">
  <div class="wrap wrap--narrow">
    <div class="prose reveal">{corpo_html}</div>

    <div class="callout reveal">
      <p><strong>Este texto é informativo.</strong> Ele explica a regra geral e não substitui
      a análise do seu caso, que pode ter particularidades relevantes.</p>
      <p><a class="link-arrow" href="/areas/{area['slug']}/">Ver como atuamos em {e(area['nome'])} {ICONS['seta']}</a></p>
    </div>
  </div>
</article>

<section class="section section--cream2">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Continue lendo</span>
      <h2>Outros artigos</h2>
    </div>
    <div class="grid grid--2">{outros_html}
    </div>
  </div>
</section>

{cta_band("Ficou com dúvida sobre o seu caso?",
          "Um artigo explica a regra. A consulta diz o que ela significa para a sua "
          "situação específica.",
          msg)}"""

    schema_artigo = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": art["titulo"],
        "description": art["resumo"],
        "datePublished": art["data"],
        "dateModified": art["data"],
        "inLanguage": "pt-BR",
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{DOM}/artigos/{art['slug']}/"},
        "author": {"@type": "Person", "name": autor["nome"],
                   "url": f"{DOM}/advogados/{autor['slug']}/"},
        "publisher": {"@id": ORG_ID},
        "about": area["nome"],
    }

    pagina(
        f"artigos/{art['slug']}",
        # títulos longos de artigo perdem a marca no corte do Google: melhor sem sufixo
        art["titulo"] if len(art["titulo"]) > 52 else f"{art['titulo']} | GR & WMF",
        art["resumo"],
        corpo,
        schema=[schema_artigo,
                schema_breadcrumb([("/", "Início"), ("/artigos/", "Artigos"),
                                   (f"/artigos/{art['slug']}/", art["titulo"])])],
        atual="/artigos/", prioridade="0.6", og_type="article", wa_msg=msg,
    )


def build_faq():
    corpo = f"""<section class="page-hero">
  <span class="ghost" aria-hidden="true">Dúvidas</span>
  <div class="wrap wrap--narrow">
    {crumbs([("/", "Início"), (None, "Perguntas frequentes")])}
    <h1>Perguntas frequentes</h1>
    <p class="lead">
      O que mais nos perguntam antes da primeira consulta. Se a sua dúvida não estiver
      aqui, mande pelo WhatsApp — respondemos em até 1 dia útil.
    </p>
  </div>
</section>

{bloco_faq(FAQ_GERAL, titulo="Sobre o atendimento", eyebrow="Geral", fundo="section--white")}

{"".join(bloco_faq(a["faq"], titulo=a["nome"], eyebrow="Por área", fundo="section--cream2" if i % 2 == 0 else "section--white") for i, a in enumerate(AREAS))}

{cta_band("Continua com dúvida?",
          "Perguntar não custa nada e não compromete você a nada. Se não for a nossa área, "
          "dizemos na primeira resposta.",
          "Olá! Vi as perguntas frequentes no site e queria tirar uma dúvida.")}"""

    todas = FAQ_GERAL + [par for a in AREAS for par in a["faq"]]

    pagina(
        "perguntas-frequentes", f"Perguntas frequentes | {SITE['nome']}",
        "Como funciona a primeira consulta, atendimento online, documentos necessários, "
        "honorários e dúvidas por área de atuação. GR & WMF Advogados, Belo Horizonte.",
        corpo,
        schema=[schema_faq(todas),
                schema_breadcrumb([("/", "Início"),
                                   ("/perguntas-frequentes/", "Perguntas frequentes")])],
        atual=None, prioridade="0.8",
    )


def build_contato():
    # cada área já sabe para qual sócio a mensagem deve ir
    dono = {}
    for adv in ADVOGADOS:
        for slug in adv["areas"]:
            dono[slug] = adv
    opcoes = "".join(
        f'<option value="{e(a["nome"])}" data-wa="{dono[a["slug"]]["whatsapp"]}" '
        f'data-adv="{e(dono[a["slug"]]["trato"])} {e(dono[a["slug"]]["nome"].split()[0])}">'
        f'{e(a["nome"])}</option>'
        for a in AREAS
    )

    corpo = f"""<section class="page-hero">
  <span class="ghost" aria-hidden="true">Contato</span>
  <div class="wrap">
    {crumbs([("/", "Início"), (None, "Contato")])}
    <h1>Fale com o escritório</h1>
    <p class="lead">
      Conte em poucas linhas o que está acontecendo. Respondemos em até 1 dia útil, no
      canal que você preferir. Tudo o que você escrever aqui é protegido por sigilo
      profissional.
    </p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="contact-grid">
      <div class="reveal">
        <h2 style="font-size:var(--fs-2xl);margin-bottom:24px">Canais diretos</h2>
        <ul class="contact-list">
          <li>{ICONS['whatsapp']}<div>
            <strong>WhatsApp</strong>
            <a href="{wa_link(SITE['whatsapp'], 'Olá! Vim pelo site e gostaria de falar sobre o meu caso.')}" target="_blank" rel="noopener">{e(SITE['tel_exibicao'])}</a> —
            Dra. Gabriella (Família, Sucessões, Imobiliário e Condominial)<br>
            <a href="{wa_link(SITE['whatsapp_2'], 'Olá! Vim pelo site e gostaria de falar sobre o meu caso.')}" target="_blank" rel="noopener">{e(SITE['tel_exibicao_2'])}</a> —
            Dr. Welberth (Trabalhista, Empresarial e Contratual)
          </div></li>
          <li>{ICONS['email']}<div>
            <strong>E-mail</strong>
            <a href="mailto:{SITE['email']}">{e(SITE['email'])}</a>
          </div></li>
          <li>{ICONS['local']}<div>
            <strong>Endereço</strong>
            {e(SITE['endereco'])}<br>{e(SITE['cidade'])}/{SITE['uf']} — CEP {e(SITE['cep'])}
          </div></li>
          <li>{ICONS['relogio']}<div>
            <strong>Horário</strong>
            {e(SITE['horario'])}<br>Atendimento presencial com hora marcada
          </div></li>
          <li>{ICONS['video']}<div>
            <strong>Atendimento online</strong>
            Consulta por videochamada e assinatura eletrônica de documentos, para quem
            está em outra região ou não pode se deslocar.
          </div></li>
        </ul>

        <div class="map-frame reveal" style="margin-top:32px">
          <iframe
            title="Mapa com a localização do escritório GR &amp; WMF Advogados no Barreiro, Belo Horizonte"
            src="https://www.google.com/maps?q=Rua+Fl%C3%A1vio+Marques+Lisboa,+511,+Barreiro,+Belo+Horizonte,+MG&output=embed"
            loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
      </div>

      <div class="reveal">
        <h2 style="font-size:var(--fs-2xl);margin-bottom:8px">Montar sua mensagem</h2>
        <p style="margin-bottom:24px">
          Preencha e o WhatsApp abre com o texto pronto, já direcionado ao sócio da área.
          Você lê antes de enviar. Campos com <abbr title="obrigatório">*</abbr> são obrigatórios.
        </p>

        <form class="form" id="form-contato" novalidate
              data-wa-padrao="{SITE['whatsapp']}">
          <div class="field">
            <label for="nome">Seu nome <abbr title="obrigatório">*</abbr></label>
            <input type="text" id="nome" name="nome" autocomplete="name" required>
            <span class="error" role="alert"></span>
          </div>

          <div class="field">
            <label for="area">Assunto <abbr title="obrigatório">*</abbr>
              <span class="hint">Define para qual advogado a mensagem vai.</span>
            </label>
            <select id="area" name="area" required>
              <option value="">Selecione a área</option>
              {opcoes}
              <option value="Não sei / outro assunto">Não sei / outro assunto</option>
            </select>
            <span class="error" role="alert"></span>
          </div>

          <div class="field">
            <label for="mensagem">O que está acontecendo? <abbr title="obrigatório">*</abbr>
              <span class="hint">Não precisa de termos jurídicos. Conte com suas palavras.</span>
            </label>
            <textarea id="mensagem" name="mensagem" required></textarea>
            <span class="error" role="alert"></span>
          </div>

          <div class="hp" aria-hidden="true">
            <label for="site-url">Não preencha este campo</label>
            <input class="hp-input" type="text" id="site-url" name="site-url" tabindex="-1" autocomplete="off">
          </div>

          <button class="btn btn--wa btn--block" type="submit">
            {ICONS['whatsapp']}Falar no WhatsApp
          </button>

          <p class="form-status" role="status" aria-live="polite" hidden></p>

          <p class="note">
            Nada é gravado neste site: a mensagem é montada no seu navegador e só existe
            depois que você a envia pelo WhatsApp. O envio não cria relação
            advogado-cliente — ele serve para agendarmos uma conversa.
          </p>
        </form>

        <div class="callout" style="margin-top:28px">
          <p><strong>Prefere não usar o WhatsApp?</strong> Escreva para
          <a href="mailto:{SITE['email']}?subject=Contato%20pelo%20site">{e(SITE['email'])}</a>
          ou ligue em horário comercial. Entendemos que nem todo assunto pode ficar
          registrado no celular — e o sigilo profissional vale igual em qualquer canal.</p>
        </div>
      </div>
    </div>
  </div>
</section>

{bloco_faq(FAQ_GERAL[:3], titulo="Antes de escrever", eyebrow="Perguntas frequentes",
           fundo="section--cream2")}"""

    schema_contato = {
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "url": f"{DOM}/contato/",
        "mainEntity": {"@id": ORG_ID},
    }

    pagina(
        "contato", "Contato | Advogados no Barreiro, Belo Horizonte",
        "Fale com a GR & WMF Advogados: WhatsApp, e-mail e atendimento presencial no "
        "Barreiro, em Belo Horizonte, ou por videochamada. Resposta em até 1 dia útil.",
        corpo,
        schema=[schema_contato, SCHEMA_ORG,
                schema_breadcrumb([("/", "Início"), ("/contato/", "Contato")])],
        atual="/contato/", prioridade="0.9",
    )


def build_politica():
    corpo = f"""<section class="page-hero">
  <div class="wrap wrap--narrow">
    {crumbs([("/", "Início"), (None, "Política de privacidade")])}
    <h1>Política de privacidade</h1>
    <p class="lead">
      Como tratamos os dados pessoais recebidos por este site, nos termos da Lei
      13.709/2018 (LGPD). Última atualização: {e(date.today().strftime('%d/%m/%Y'))}.
    </p>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--narrow">
    <div class="prose reveal">
      <h2>Quem é o controlador dos dados</h2>
      <p>
        {e(SITE['nome'])}, com endereço na {e(SITE['endereco'])}, {e(SITE['cidade'])}/{SITE['uf']},
        CEP {e(SITE['cep'])}, é o controlador dos dados pessoais coletados neste site.
      </p>
      <p><strong>Encarregado pelo tratamento de dados (DPO):</strong>
        <a href="mailto:{SITE['email']}">{e(SITE['email'])}</a>.
        Este é o canal para dúvidas e para o exercício dos seus direitos.
      </p>

      <h2>Quais dados coletamos</h2>
      <p>
        <strong>Este site não armazena o que você escreve.</strong> O formulário de
        contato funciona apenas como um montador de texto: os campos são processados
        dentro do seu próprio navegador e transformados em uma mensagem de WhatsApp,
        que só existe depois que você a envia. Nada é gravado em nossos servidores
        nesse processo, e nenhum campo é transmitido ao clicar no botão.
      </p>
      <ul>
        <li><strong>Dados que chegam até nós:</strong> apenas o que você efetivamente
        enviar por WhatsApp, e-mail ou telefone. A partir daí, o conteúdo passa a ser
        tratado sob sigilo profissional.</li>
        <li><strong>Dados de navegação:</strong> páginas visitadas e origem do acesso,
        de forma agregada e somente se você aceitar os cookies de análise.</li>
      </ul>
      <p>
        Pedimos que informações detalhadas e documentos sobre o seu caso sejam tratados
        na consulta, e não na mensagem inicial.
      </p>

      <h2>Para que usamos</h2>
      <ul>
        <li>Responder ao seu contato e agendar atendimento — base legal: procedimentos
        preliminares relacionados a contrato, a seu pedido (art. 7º, V, da LGPD).</li>
        <li>Entender o uso do site e melhorá-lo — base legal: consentimento, manifestado
        no banner de cookies (art. 7º, I).</li>
      </ul>
      <p>Não vendemos, alugamos nem compartilhamos seus dados com terceiros para fins
      publicitários.</p>

      <h2>Se você prefere não usar o WhatsApp</h2>
      <p>
        As mensagens trocadas por WhatsApp ficam registradas no seu aparelho e são
        transmitidas pela infraestrutura do próprio aplicativo, sobre a qual não temos
        controle. Se o assunto exigir discrição, use o e-mail
        <a href="mailto:{SITE['email']}">{e(SITE['email'])}</a> ou o telefone — o sigilo
        profissional vale igualmente em qualquer canal.
      </p>

      <h2>Cookies</h2>
      <p>
        Cookies necessários ao funcionamento do site são usados sempre. Cookies de análise
        só são ativados se você clicar em “Aceitar” no banner — se recusar, o site funciona
        normalmente. Sua escolha fica registrada no seu navegador e pode ser alterada a
        qualquer momento limpando os dados do site.
      </p>

      <h2>Por quanto tempo guardamos</h2>
      <p>
        Mensagens recebidas por WhatsApp ou e-mail que não resultam em atendimento são
        eliminadas em até 12 meses.
        Dados de clientes são mantidos pelo prazo exigido pela legislação e pelo dever de
        guarda profissional da advocacia.
      </p>

      <h2>Seus direitos</h2>
      <p>
        Você pode solicitar confirmação de tratamento, acesso, correção, anonimização,
        portabilidade, eliminação e informação sobre compartilhamento, além de revogar o
        consentimento a qualquer momento. Basta escrever para
        <a href="mailto:{SITE['email']}">{e(SITE['email'])}</a>. Respondemos em até 15 dias.
      </p>

      <h2>Segurança e sigilo</h2>
      <p>
        O site usa conexão criptografada (HTTPS). Além das medidas técnicas, todo o conteúdo
        recebido está protegido pelo sigilo profissional do advogado, previsto no Estatuto
        da Advocacia — inclusive quando o caso não é aceito.
      </p>

      <h2>Alterações</h2>
      <p>
        Esta política pode ser atualizada. A data no início da página indica a versão vigente.
      </p>
    </div>
  </div>
</section>"""

    pagina(
        "politica-de-privacidade", f"Política de privacidade | {SITE['nome']}",
        "Como a GR & WMF Advogados trata os dados pessoais recebidos pelo site, "
        "conforme a LGPD: finalidades, bases legais, cookies, prazos e seus direitos.",
        corpo, atual=None, prioridade="0.3",
    )


def build_404():
    cards = "\n    ".join(card_area(a) for a in AREAS[:3])
    corpo = f"""<section class="page-hero">
  <span class="ghost" aria-hidden="true">404</span>
  <div class="wrap wrap--narrow">
    <span class="eyebrow">Erro 404</span>
    <h1>Esta página não existe mais</h1>
    <p class="lead">
      O endereço pode ter mudado ou o link pode estar incompleto. Abaixo estão os caminhos
      mais procurados — e o contato direto, se você preferir resolver logo.
    </p>
    <div class="btn-row" style="margin-top:26px">
      <a class="btn btn--primary" href="/">Voltar para o início</a>
      <a class="btn btn--ghost" href="/contato/">Falar com o escritório</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Talvez você procure</span>
      <h2>Áreas de atuação</h2>
    </div>
    <div class="grid grid--3">
    {cards}
    </div>
    <p class="section-more"><a class="link-arrow" href="/areas/">Ver todas as áreas {ICONS['seta']}</a></p>
  </div>
</section>"""

    pagina("404", f"Página não encontrada | {SITE['nome']}",
           "A página que você procura não foi encontrada. Veja as áreas de atuação ou "
           "fale com a GR & WMF Advogados.",
           corpo, atual=None, no_index=True)
    # hospedagens estáticas procuram /404.html na raiz
    origem = os.path.join(SAIDA, "404", "index.html")
    with open(origem, encoding="utf-8") as f:
        escrever("404.html", f.read())
    shutil.rmtree(os.path.join(SAIDA, "404"))


def build_sitemap_robots():
    urls = ""
    for url, prio in paginas_geradas:
        urls += (f"\n  <url><loc>{url}</loc><lastmod>{HOJE}</lastmod>"
                 f"<changefreq>monthly</changefreq><priority>{prio}</priority></url>")
    escrever("sitemap.xml",
             '<?xml version="1.0" encoding="UTF-8"?>\n'
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
             + urls + "\n</urlset>\n")

    escrever("robots.txt",
             "User-agent: *\n"
             "Allow: /\n\n"
             "# Rastreadores de IA: conteúdo liberado para citação\n"
             "User-agent: GPTBot\nAllow: /\n\n"
             "User-agent: PerplexityBot\nAllow: /\n\n"
             "User-agent: Google-Extended\nAllow: /\n\n"
             f"Sitemap: {DOM}/sitemap.xml\n")


def build_favicon():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
           '<rect width="64" height="64" rx="6" fill="#1C2537"/>'
           '<text x="32" y="43" text-anchor="middle" font-family="Georgia,serif" '
           'font-size="30" fill="#C9A567">GW</text></svg>')
    escrever("assets/img/favicon.svg", svg)


def main():
    build_home()
    build_escritorio()
    build_advogados()
    build_areas()
    build_artigos()
    build_faq()
    build_contato()
    build_politica()
    build_404()
    build_sitemap_robots()
    build_favicon()

    print(f"OK — {len(paginas_geradas)} páginas indexáveis geradas em public/")
    for url, _ in paginas_geradas:
        print("   ", url)


if __name__ == "__main__":
    main()
