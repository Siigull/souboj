// Odpočet do dalšího turnaje série — sekce „turnaj“ pod úvodním logem.
//
// Rozvrh turnajů (jména, starty včetně časové zóny a odkazy) generuje build.py
// do <script id="tournament-schedule"> z data.py (COUNTDOWN). Texty stavů
// (nadpisy, popisky, označení odkazů) jsou v data-* atributech sekce.
//
// Stavy:
//   1. do dalšího kola zbývá — běžící odpočet + odkaz na registraci
//   2. turnaj právě probíhá   — zhruba 6 hodin od startu, odkaz na živé výsledky
//   3. série je u konce       — po odehrání všech kol, odkaz na výsledky série
(function () {
  "use strict";

  var WEEKDAYS = ["neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota"];

  function pad(n) {
    return (n < 10 ? "0" : "") + n;
  }

  // České skloňování: 1 hodina, 2 hodiny, 5 hodin (11–14 vždy „množné“).
  function plural(n, one, few, many) {
    if (n === 1) return one;
    if (n >= 2 && n <= 4) return few;
    return many;
  }

  var LABELS = {
    days: ["den", "dny", "dní"],
    hours: ["hodina", "hodiny", "hodin"],
    minutes: ["minuta", "minuty", "minut"],
    seconds: ["sekunda", "sekundy", "sekund"],
  };

  // „neděle 4. 10. v 17.30“
  function formatStart(ms) {
    var d = new Date(ms);
    return (
      WEEKDAYS[d.getDay()] +
      " " +
      d.getDate() +
      ". " +
      (d.getMonth() + 1) +
      ". v " +
      d.getHours() +
      "." +
      pad(d.getMinutes())
    );
  }

  // Nastaví číslo v elementu po znacích; mění se jen skutečně změněné číslice,
  // které dostanou krátkou animaci (restart přes reflow).
  function setNumber(el, text) {
    while (el.children.length < text.length) {
      el.appendChild(document.createElement("span"));
    }
    while (el.children.length > text.length) {
      el.removeChild(el.lastChild);
    }
    for (var i = 0; i < text.length; i++) {
      var span = el.children[i];
      var ch = text.charAt(i);
      if (span.textContent !== ch) {
        span.textContent = ch;
        span.classList.remove("cd-in");
        void span.offsetWidth;
        span.classList.add("cd-in");
      }
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    var section = document.querySelector(".tournament-section");
    if (!section) return;

    var schedule = [];
    try {
      schedule = JSON.parse(
        document.getElementById("tournament-schedule").textContent
      );
    } catch (err) {
      return; // bez rozvrhu zůstane statické předvyplnění z build.py
    }
    if (!schedule.length) return;

    var windowMs =
      (parseFloat(section.getAttribute("data-running-hours")) || 6) *
      60 *
      60 *
      1000;

    var counter = section.querySelector("[data-countdown]");
    var headline = section.querySelector("[data-headline]");
    var headlineText = section.querySelector("[data-headline-text]");
    var liveDot = section.querySelector("[data-live-dot]");
    var eyebrow = section.querySelector("[data-eyebrow]");
    var caption = section.querySelector("[data-caption]");
    var register = section.querySelector("[data-register]");
    var registerLabel = section.querySelector("[data-register-label]");
    var dates = Array.prototype.slice.call(section.querySelectorAll("[data-date]"));

    var units = {};
    var unitLabels = {};
    ["days", "hours", "minutes", "seconds"].forEach(function (key) {
      if (counter) {
        units[key] = counter.querySelector('[data-unit="' + key + '"]');
        unitLabels[key] = counter.querySelector('[data-label="' + key + '"]');
      }
    });

    function setState(options) {
      // eyebrow / headline / caption / cta podle stavu sekce
      if (eyebrow) eyebrow.textContent = options.eyebrow;
      if (counter) counter.hidden = !!options.hideCounter;
      if (headline) headline.hidden = !!options.hideHeadline;
      if (liveDot) liveDot.hidden = !!options.hideDot;
      if (headlineText && options.title) headlineText.textContent = options.title;
      if (caption) caption.textContent = options.caption;
      if (register) register.href = options.href;
      if (registerLabel && options.label) registerLabel.textContent = options.label;
    }

    function updateDates(now, nextIndex, runningIndex) {
      dates.forEach(function (el, i) {
        var start = Date.parse(schedule[i].start);
        if (isNaN(start)) return;
        el.classList.remove("is-past", "is-next", "is-future");
        if (i === runningIndex || i === nextIndex) {
          el.classList.add("is-next"); // právě probíhající / nejbližší kolo
        } else if (now >= start + windowMs) {
          el.classList.add("is-past");
        } else {
          el.classList.add("is-future");
        }
      });
    }

    function tick() {
      var now = Date.now();
      var running = null;
      var runningIndex = -1;
      var next = null;
      var nextIndex = -1;

      for (var i = 0; i < schedule.length; i++) {
        var start = Date.parse(schedule[i].start);
        if (isNaN(start)) continue;
        if (now >= start && now < start + windowMs) {
          running = schedule[i];
          runningIndex = i;
          break;
        }
        if (now < start) {
          next = schedule[i];
          nextIndex = i;
          break;
        }
      }

      if (running) {
        // 2 — turnaj právě probíhá
        setState({
          eyebrow: section.getAttribute("data-eyebrow-live"),
          title: section.getAttribute("data-live-title"),
          caption: section.getAttribute("data-caption-live"),
          href: running.url,
          label: section.getAttribute("data-register-live"),
          hideCounter: true,
          hideHeadline: false,
          hideDot: false,
        });
      } else if (next) {
        // 1 — odpočet do dalšího kola
        setState({
          eyebrow: section.getAttribute("data-eyebrow-next"),
          caption:
            next.name +
            " — " +
            formatStart(Date.parse(next.start)) +
            " • " +
            section.getAttribute("data-venue"),
          href: next.url,
          label: section.getAttribute("data-register-next"),
          hideCounter: false,
          hideHeadline: true,
          hideDot: true,
        });

        var total = Math.max(
          0,
          Math.floor((Date.parse(next.start) - now) / 1000)
        );
        var values = {
          days: Math.floor(total / 86400),
          hours: Math.floor((total % 86400) / 3600),
          minutes: Math.floor((total % 3600) / 60),
          seconds: total % 60,
        };
        Object.keys(values).forEach(function (key) {
          if (units[key]) setNumber(units[key], pad(values[key]));
          var label = unitLabels[key];
          if (label) {
            var forms = LABELS[key];
            label.textContent = plural(
              values[key],
              forms[0],
              forms[1],
              forms[2]
            );
          }
        });
      } else {
        // 3 — všechna kola odehrána
        setState({
          eyebrow: section.getAttribute("data-eyebrow-done"),
          title: section.getAttribute("data-done-title"),
          caption: section.getAttribute("data-caption-done"),
          href: section.getAttribute("data-results-url"),
          label: section.getAttribute("data-register-done"),
          hideCounter: true,
          hideHeadline: false,
          hideDot: true,
        });
      }

      updateDates(now, nextIndex, runningIndex);
    }

    tick();
    setInterval(tick, 1000);
  });
})();
