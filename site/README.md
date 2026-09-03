# Site GR & WMF Advogados

Site institucional estático, gerado a partir de conteúdo em Python. Sem framework,
sem dependências externas em produção — só HTML, CSS e ~180 linhas de JavaScript.

## Rodar

```bash
cd site && python3 build.py && python3 -m http.server 4321 --directory public
```

Abra <http://localhost:4321>. O `build.py` regrava `public/` inteiro a cada execução.

## Estrutura

```
site/
  content.py            toda a copy do site (áreas, advogados, FAQ, artigos)
  build.py              gerador: monta as 20 páginas, JSON-LD, sitemap e robots
  public/               saída pronta para publicar  ←  é isto que vai ao ar
    assets/css/site.css sistema de design (tokens, componentes)
    assets/js/site.js   menu, consentimento LGPD, validação do formulário
    assets/img/src/     fontes SVG do og:image e do ícone (para reexportar)
```

Cada página vira uma pasta com `index.html`, o que dá URLs limpas
(`/areas/direito-imobiliario/`) em qualquer hospedagem estática.

## Editar conteúdo

Quase tudo está em `content.py`:

| O que mudar | Onde |
|---|---|
| Telefones, endereço, e-mail, horário | `SITE` |
| Perfil dos sócios, OAB, formação | `ADVOGADOS` |
| Áreas: textos, serviços, FAQ, SEO | `AREAS` |
| Atalhos da primeira dobra | `CHIPS` |
| Etapas do atendimento | `PROCESSO` |
| Perguntas frequentes gerais | `FAQ_GERAL` |
| Artigos | `ARTIGOS` |

Depois de editar, rode `python3 build.py`. O sitemap e os dados estruturados
são regerados sozinhos.

Para publicar um artigo novo, copie um bloco de `ARTIGOS` e ajuste `slug`,
`titulo`, `data`, `data_exibicao` e `corpo` (lista de blocos `("p"|"h2"|"ul", …)`).

Os atalhos da primeira dobra (`CHIPS`) são independentes das áreas: mais de um
atalho pode apontar para a mesma página, que é o caso de "Divórcio" e "Inventário".
Mantenha os rótulos curtos e de comprimento parecido — é isso que faz a régua
compor como um bloco em vez de uma nuvem desalinhada.

## Temas

O site tem tema escuro (padrão) e claro, alternados pelo botão no cabeçalho. A
escolha fica no `localStorage` e um script no `<head>` a aplica antes da primeira
pintura, para a página não piscar no tema errado.

**Os dois temas vivem no mesmo `site.css` e diferem só por tokens de cor.** O
bloco `:root` traz o escuro; `[data-theme="light"]` redefine as cores. Estrutura,
responsividade, tamanhos e correções são escritos uma vez e valem para os dois —
não existe folha de estilo separada por tema, e não deve existir.

Ao mexer em cor, mude o token, nunca o valor dentro da regra do componente. Se
precisar de um valor que muda entre temas e ainda não tem token, crie um.

O rodapé e a faixa de CTA são escuros nos **dois** temas. Eles redefinem os
tokens de texto no próprio escopo (`--parchment`, `--muted`, `--brass`…), então
as regras internas continuam escritas uma vez só.

Dois valores dependem do tema e são fáceis de esquecer: `--on-brass` (texto sobre
o botão dourado — escuro no tema escuro, branco no claro, porque o dourado
inverte) e o `theme-color` do navegador, atualizado pelo JS na troca.

## Regra editorial — Provimento 205/2021 da OAB

O site foi escrito dentro dos limites da publicidade na advocacia. Ao editar
qualquer texto, mantenha:

- **sem preço** de honorários (a página de FAQ explica por quê);
- **sem promessa de resultado** ("garantimos", "você vai ganhar");
- **sem caso de êxito** e **sem depoimento** de cliente;
- **sem linguagem mercantil** ("o melhor escritório", "líder", "imperdível").

A conversão vem de clareza, conteúdo útil, qualificação demonstrada e facilidade
de contato — não de promessa.

## Aprovação de conteúdo

Parte da copy deste site foi redigida durante a construção do projeto e ainda não
passou pelos sócios. Textos, prazos de atendimento, horários e afirmações jurídicas
precisam de leitura e aprovação antes da publicação.

O levantamento item a item está em `AUDITORIA-CONTEUDO.md`, na raiz do projeto
(fora do versionamento).

## Pendências antes de ir ao ar

1. **Fotos.** O site usa placeholders com o monograma onde deveria haver imagem.
   Assim que os arquivos existirem nos caminhos abaixo, o build passa a usá-los
   automaticamente — não precisa mexer no código:
   - `public/assets/img/escritorio-hero.jpg` — 1200×1500 (retrato), primeira dobra
   - `public/assets/img/advogada-gabriella.jpg` — 800×1000 (retrato)
   - `public/assets/img/advogado-welberth.jpg` — 800×1000 (retrato)

   Exporte em WebP também, se possível, e mantenha abaixo de 250 KB cada.

2. **Logotipo.** O cabeçalho usa um monograma tipográfico provisório (`GW`).
   Com o arquivo vetorial do logo real, substitua o bloco `.brand__mark` em
   `build.py` (função `header_html`) por um `<img src="/assets/img/logo.svg">`.

3. **E-mail no domínio.** O site divulga `contato@grewmfadvogados.com` como canal
   alternativo ao WhatsApp. Criar a caixa e configurar SPF, DKIM e DMARC antes da
   publicação — senão a resposta ao cliente cai em spam.

4. **Imagem de compartilhamento.** `public/assets/img/og-grwmf.png` é uma versão
   tipográfica provisória. Com o logo real, reexporte a partir de
   `assets/img/src/og-grwmf.svg` mantendo 1200×630.

5. **Medição.** Nenhuma tag de analytics foi instalada — por decisão do projeto,
   mídia paga é tratada à parte. Quando entrar, o carregamento deve acontecer
   **dentro** do bloco de consentimento em `site.js` (procure o comentário
   "Tags de medição"), nunca antes do aceite: é o que mantém o banner de cookies
   em conformidade com a LGPD.

## Como o formulário funciona

Não há backend. O formulário de `/contato/` é um **montador de mensagem**: valida os
campos no navegador, monta o texto e abre `wa.me` com ele pronto. Nada trafega para
servidor nenhum, e nada é armazenado — o que simplifica a conformidade com a LGPD e
elimina custo de infraestrutura.

O `<select>` de assunto carrega `data-wa` e `data-adv` em cada opção, gerados a partir
do campo `areas` de cada sócio em `content.py`. Ou seja: **o roteamento se mantém
sozinho**. Se um sócio passar a atender outra área, basta editar a lista `areas` dele
e rodar o build.

| Área | Vai para |
|---|---|
| Família e Sucessões, Imobiliário, Condominial | Dra. Gabriella |
| Contratual, Empresarial, Trabalhista | Dr. Welberth |
| "Não sei / outro assunto" | número padrão (`data-wa-padrao` no `<form>`) |

Duas consequências a ter em mente:

- **O lead só existe se a pessoa tocar em "enviar" dentro do WhatsApp.** Quem desistir
  nessa tela não deixa rastro. Se um dia isso incomodar, o caminho é acrescentar um
  endpoint que registre o lead no clique — sem tirar o WhatsApp do fluxo.
- **Parte do público de Família não quer usar WhatsApp.** Por isso a página mantém
  e-mail e telefone visíveis logo abaixo do formulário, e a política de privacidade
  explica a diferença entre os canais. Não remova esse bloco.

## Publicar

`public/` é um site estático puro. Serve em qualquer lugar (Netlify, Vercel,
Cloudflare Pages, S3, Apache). Duas configurações importam:

- **404**: apontar para `/404.html`.
- **Cache**: `assets/` pode ter cache longo — CSS e JS já são versionados por
  hash na URL (`site.css?v=…`), então uma publicação nova invalida sozinha.

Depois de publicar: enviar `https://www.grewmfadvogados.com/sitemap.xml` no
Google Search Console e conferir o cartão de compartilhamento no WhatsApp.

## O que este site corrige do diagnóstico

| Diagnóstico | Como foi resolvido |
|---|---|
| E-01 primeira dobra vazia | H1 com área + cidade, subtítulo, dois CTAs e linha de credenciais |
| E-02 WhatsApp com número inválido | Todos os links em E.164 (`wa.me/5531…`), com mensagem pré-preenchida por página |
| E-04 notícias da ConJur | Substituídas por 3 artigos autorais, com autor e data |
| E-05 sem sinais de confiança | OAB visível, formação, processo de atendimento, sigilo explicado |
| E-06 seis áreas em uma página | Seis páginas próprias, cada uma com FAQ e CTA |
| E-07 formulário genérico | Monta a mensagem e abre o WhatsApp do sócio da área; validação, honeypot e canal alternativo por e-mail |
| C-01 texto de rascunho | Toda a copy reescrita e finalizada |
| C-02 jurídiquês | Textos partem do problema do cliente |
| C-04 sem FAQ | 30 perguntas: 6 gerais + 4 por área, com JSON-LD |
| C-05 texto dentro de imagem | Nenhum texto em imagem |
| C-06 sem menção local | Cidade e bairro em títulos, textos, rodapé e dados estruturados |
| D-01 logos sobrepostos | Cabeçalho único, sticky, com menu funcional |
| D-02 template genérico | Identidade própria: creme/dourado, EB Garamond + Lato |
| D-04 banner de cookies | Compacto, com opção de recusar |
| D-05 zoom bloqueado | `maximum-scale` removido; alvos de toque e tamanhos revisados |
| D-07 404 em inglês | Página 404 própria, em português, com saídas |
| S-01 a S-04 | H1, description, Open Graph e JSON-LD em todas as páginas |
| S-05 sitemap 404 | `sitemap.xml` e `robots.txt` gerados no build |
| S-06 títulos genéricos | Títulos por intenção de busca |
| S-08 sem conteúdo | Seção de artigos com estrutura pronta para crescer |
| T-01 6s de carregamento | Sem jQuery, Bootstrap ou Font Awesome: 1 CSS, 1 JS, ícones SVG inline |
| T-02 site em domínio de terceiro | Código-fonte próprio, publicável em qualquer lugar |
| T-04 imagens sem otimização | `loading="lazy"`, `decoding="async"` e dimensões orientadas |
| T-05 rodapé de 2017 | Ano dinâmico; sem link administrativo público |
| T-06 newsletter sem destino | Campo removido |
| L-01 consentimento inválido | Aceitar/Recusar, escolha registrada, tags só após aceite |
| L-02 política genérica | Política reescrita: controlador, encarregado, bases legais, prazos, direitos |
| L-03 conformidade OAB | Regra editorial aplicada e documentada acima |
