/* Car Armour SG — interactions. Zéro dépendance. */
(function () {
  'use strict';
  /* la classe .js est posée par un script en ligne dans le <head> */

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var on = function (el, ev, fn) { el && el.addEventListener(ev, fn); };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ── Navigation mobile ──────────────────────────────────────────────── */
  var burger = $('.burger');
  var panel = $('#mobile-nav');
  if (burger && panel) {
    var setNav = function (open) {
      burger.setAttribute('aria-expanded', String(open));
      panel.classList.toggle('is-open', open);
      panel.setAttribute('aria-hidden', String(!open));
      document.body.classList.toggle('is-locked', open);
    };
    on(burger, 'click', function () {
      setNav(burger.getAttribute('aria-expanded') !== 'true');
    });
    on(document, 'keydown', function (e) {
      if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') {
        setNav(false); burger.focus();
      }
    });
    // Sous-menus du panneau mobile
    $$('[data-subnav]', panel).forEach(function (btn) {
      on(btn, 'click', function () {
        var sub = document.getElementById(btn.getAttribute('aria-controls'));
        var open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', String(!open));
        sub && sub.classList.toggle('is-open', !open);
      });
    });
  }

  /* ── Dropdown desktop : clavier + clic hors zone ────────────────────── */
  $$('.nav__item--has-panel').forEach(function (item) {
    var trigger = $('.nav__link', item);
    var list = $('.nav__panel', item);
    if (!trigger || !list) return;
    on(trigger, 'click', function (e) {
      e.preventDefault();
      var open = trigger.getAttribute('aria-expanded') === 'true';
      trigger.setAttribute('aria-expanded', String(!open));
      list.classList.toggle('is-open', !open);
    });
    on(item, 'focusout', function (e) {
      if (!item.contains(e.relatedTarget)) {
        trigger.setAttribute('aria-expanded', 'false');
        list.classList.remove('is-open');
      }
    });
  });
  on(document, 'click', function (e) {
    if (!e.target.closest || e.target.closest('.nav__item--has-panel')) return;
    $$('.nav__item--has-panel').forEach(function (item) {
      $('.nav__link', item).setAttribute('aria-expanded', 'false');
      $('.nav__panel', item).classList.remove('is-open');
    });
  });

  /* ── Accordéons (FAQ) — hauteur animée, accessible ──────────────────── */
  $$('.accordion__trigger').forEach(function (trigger) {
    var body = document.getElementById(trigger.getAttribute('aria-controls'));
    if (!body) return;
    if (trigger.getAttribute('aria-expanded') !== 'true') body.style.height = '0px';
    else body.style.height = 'auto';
    on(trigger, 'click', function () {
      var open = trigger.getAttribute('aria-expanded') === 'true';
      trigger.setAttribute('aria-expanded', String(!open));
      if (reduce) { body.style.height = open ? '0px' : 'auto'; return; }
      if (open) {
        body.style.height = body.scrollHeight + 'px';
        requestAnimationFrame(function () { body.style.height = '0px'; });
      } else {
        body.style.height = body.scrollHeight + 'px';
        body.addEventListener('transitionend', function te(ev) {
          if (ev.propertyName !== 'height') return;
          body.style.height = 'auto';
          body.removeEventListener('transitionend', te);
        });
      }
    });
  });

  /* ── Reveal : fade + 20px, cascade légère ───────────────────────────────
     data-reveal="n"  -> rang dans la cascade (n x 90 ms de décalage)
     data-reveal-on="load" -> joué à l'ouverture, sans attendre le scroll.
     Nécessaire pour la séquence du haut de page : le dernier élément de la
     suite se trouve sous la ligne de flottaison, l'observateur ne le verrait
     jamais et la cascade s'interromprait en chemin. */
  var targets = $$('[data-reveal]');
  var delayOf = function (el) {
    var i = parseInt(el.getAttribute('data-reveal'), 10);
    return (isNaN(i) ? 0 : i * 90) + 'ms';
  };
  var show = function (el) {
    el.style.setProperty('--reveal-delay', delayOf(el));
    el.classList.add('is-in');
  };

  if (targets.length) {
    if (reduce || !('IntersectionObserver' in window)) {
      targets.forEach(function (el) { el.classList.add('is-in'); });
    } else {
      var onLoad = [], onScroll = [];
      targets.forEach(function (el) {
        (el.getAttribute('data-reveal-on') === 'load' ? onLoad : onScroll).push(el);
      });
      requestAnimationFrame(function () { onLoad.forEach(show); });
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          show(entry.target);
          io.unobserve(entry.target);
        });
      }, { rootMargin: '0px 0px -12% 0px', threshold: 0 });
      onScroll.forEach(function (el) { io.observe(el); });

      /* Filet de securite. Un element que l'observateur manque reste a
         opacity 0, donc invisible pour toujours : le contenu disparait sans
         erreur ni trace. Ce balayage revele tout ce qui est entre dans le
         champ, quoi qu'ait fait l'observateur, et se desarme une fois la
         page entierement revelee. */
      var sweep = function () {
        var vh = window.innerHeight || 0;
        var left = 0;
        onScroll.forEach(function (el) {
          if (el.classList.contains('is-in')) return;
          var r = el.getBoundingClientRect();
          if (r.top < vh * 0.95 && r.bottom > 0) { show(el); io.unobserve(el); }
          else left++;
        });
        if (!left) {
          window.removeEventListener('scroll', sweep);
          window.removeEventListener('resize', sweep);
        }
      };
      window.addEventListener('scroll', sweep, { passive: true });
      window.addEventListener('resize', sweep, { passive: true });
      window.addEventListener('load', sweep);
      setTimeout(sweep, 1200);
    }
  }
})();
