/* GR & WMF Advogados — comportamento do site. Sem dependências. */
(function () {
  "use strict";

  /* ---------------------------------------------------- menu mobile */
  var toggle = document.querySelector(".nav__toggle");
  var list = document.getElementById("nav-list");

  function closeMenu() {
    if (!toggle || !list) return;
    toggle.setAttribute("aria-expanded", "false");
    list.classList.remove("is-open");
    document.body.classList.remove("is-locked");
  }

  if (toggle && list) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      list.classList.toggle("is-open", !open);
      document.body.classList.toggle("is-locked", !open);
    });

    list.addEventListener("click", function (e) {
      if (e.target.closest("a")) closeMenu();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });

    // ao voltar para desktop, desfaz o estado do drawer
    var mq = window.matchMedia("(min-width: 920px)");
    (mq.addEventListener ? mq.addEventListener.bind(mq, "change") : mq.addListener.bind(mq))(closeMenu);
  }

  /* ---------------------------------------------------- tema claro/escuro */
  var CHAVE_TEMA = "grwmf.tema";
  var botaoTema = document.getElementById("alternar-tema");
  var metaCor = document.querySelector('meta[name="theme-color"]');

  function aplicarTema(tema) {
    var claro = tema === "light";
    if (claro) document.documentElement.setAttribute("data-theme", "light");
    else document.documentElement.removeAttribute("data-theme");

    if (metaCor) metaCor.setAttribute("content", claro ? "#FBF8F3" : "#141B29");
    if (botaoTema) {
      botaoTema.setAttribute("aria-pressed", String(claro));
      botaoTema.setAttribute(
        "aria-label",
        claro ? "Mudar para o tema escuro" : "Mudar para o tema claro"
      );
    }
  }

  if (botaoTema) {
    var salvo = null;
    try { salvo = localStorage.getItem(CHAVE_TEMA); } catch (e) {}
    aplicarTema(salvo === "light" ? "light" : "dark");

    botaoTema.addEventListener("click", function () {
      var claroAgora = document.documentElement.getAttribute("data-theme") === "light";
      var novo = claroAgora ? "dark" : "light";
      aplicarTema(novo);
      try { localStorage.setItem(CHAVE_TEMA, novo); } catch (e) {}
    });
  }

  /* ---------------------------------------------------- sombra do header */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------------------------------------------------- ano do rodapé */
  var year = document.querySelector("[data-year]");
  if (year) year.textContent = String(new Date().getFullYear());

  /* ---------------------------------------------------- revelação no scroll */
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var targets = document.querySelectorAll(".reveal");

  if (reduced || !("IntersectionObserver" in window)) {
    Array.prototype.forEach.call(targets, function (el) { el.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
    Array.prototype.forEach.call(targets, function (el) { io.observe(el); });
  }

  /* --------------------------- botão flutuante x CTAs já visíveis na tela */
  // Some quando o rodapé ou os botões da primeira dobra estão à vista:
  // dois botões verdes na mesma tela só competem entre si.
  var float = document.querySelector(".wa-float");
  if (float && "IntersectionObserver" in window) {
    var concorrentes = [
      document.querySelector(".hero__acoes"),
      document.querySelector("#form-contato"),
      document.querySelector(".site-footer")
    ].filter(Boolean);

    // guardamos o estado por elemento: um contador se anularia quando os dois
    // alvos chegassem no mesmo callback
    var naTela = new WeakMap();
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        naTela.set(entry.target, entry.isIntersecting);
      });
      var algumVisivel = concorrentes.some(function (el) { return naTela.get(el); });
      float.classList.toggle("is-hidden", algumVisivel);
    }, { rootMargin: "0px 0px -40px 0px" });

    concorrentes.forEach(function (el) { obs.observe(el); });
  }

  /* ---------------------------------------------------- consentimento LGPD */
  var KEY = "grwmf.consent.v1";
  var banner = document.querySelector(".cookie");

  function readConsent() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function writeConsent(value) {
    try { localStorage.setItem(KEY, value + "|" + new Date().toISOString()); } catch (e) {}
  }

  if (banner) {
    if (!readConsent()) banner.classList.add("is-visible");
    banner.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-consent]");
      if (!btn) return;
      writeConsent(btn.getAttribute("data-consent"));
      banner.classList.remove("is-visible");
      // Tags de medição só devem ser carregadas aqui, quando data-consent === "aceito".
    });
  }

  /* ------------------------------------------- formulário -> WhatsApp */
  var form = document.getElementById("form-contato");
  if (form) {
    var status = form.querySelector(".form-status");
    var submit = form.querySelector("[type=submit]");

    var setError = function (field, message) {
      var input = field.querySelector("input, select, textarea");
      var slot = field.querySelector(".error");
      if (!input || !slot) return;
      input.setAttribute("aria-invalid", message ? "true" : "false");
      slot.textContent = message || "";
    };

    var validate = function () {
      var first = null;

      Array.prototype.forEach.call(form.querySelectorAll(".field"), function (field) {
        var input = field.querySelector("input, select, textarea");
        if (!input || input.classList.contains("hp-input")) return;

        var value = input.value.trim();
        var message = "";

        if (input.required && !value) {
          message = input.tagName === "SELECT"
            ? "Escolha o assunto para direcionarmos a mensagem."
            : "Preencha este campo para continuarmos.";
        } else if (input.name === "mensagem" && value.length < 20) {
          message = "Conte um pouco mais — duas linhas já nos ajudam a direcionar.";
        }

        setError(field, message);
        if (message && !first) first = input;
      });

      return first;
    };

    // Monta o texto e devolve também o número do sócio responsável pela área.
    var montar = function () {
      var area = form.querySelector("#area");
      var opcao = area.options[area.selectedIndex];
      var numero = (opcao && opcao.getAttribute("data-wa")) || form.getAttribute("data-wa-padrao");
      var advogado = opcao && opcao.getAttribute("data-adv");

      var texto = "Olá! Vim pelo site.\n\n"
        + "Nome: " + form.querySelector("#nome").value.trim() + "\n"
        + "Assunto: " + area.value + "\n\n"
        + form.querySelector("#mensagem").value.trim();

      return {
        url: "https://wa.me/" + numero + "?text=" + encodeURIComponent(texto),
        advogado: advogado
      };
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      // honeypot: preenchido significa robô — encerramos sem abrir nada
      var hp = form.querySelector(".hp-input");
      if (hp && hp.value) return;

      var invalid = validate();
      if (invalid) {
        if (status) {
          status.hidden = false;
          status.setAttribute("data-state", "err");
          status.textContent = "Faltou preencher alguns campos. Confira os destacados acima.";
        }
        invalid.focus();
        return;
      }

      var msg = montar();

      // aberto de forma síncrona no clique, senão o bloqueador de pop-up barra
      var aba = window.open(msg.url, "_blank", "noopener");

      if (status) {
        status.hidden = false;
        status.setAttribute("data-state", "ok");
        if (aba) {
          status.textContent = "Abrimos o WhatsApp com sua mensagem pronta"
            + (msg.advogado ? ", para " + msg.advogado : "")
            + ". Confira o texto e toque em enviar — só assim ela chega até nós.";
        } else {
          // pop-up bloqueado: oferecemos o link para o visitante abrir manualmente
          status.innerHTML = "";
          status.appendChild(document.createTextNode("Seu navegador bloqueou a abertura automática. "));
          var link = document.createElement("a");
          link.href = msg.url;
          link.target = "_blank";
          link.rel = "noopener";
          link.textContent = "Abrir o WhatsApp com a mensagem pronta";
          status.appendChild(link);
        }
      }

      if (submit) submit.blur();
    });

    Array.prototype.forEach.call(form.querySelectorAll("input, select, textarea"), function (input) {
      input.addEventListener("blur", function () {
        if (input.getAttribute("aria-invalid") === "true") validate();
      });
    });
  }
})();
