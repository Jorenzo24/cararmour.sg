/* Car Armour SG — interactions. Zéro dépendance. */
(function () {
  'use strict';
  document.documentElement.classList.add('js');

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var on = function (el, ev, fn) { el && el.addEventListener(ev, fn); };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ── Header : passe en solide dès le premier scroll ─────────────────── */
  var header = $('.site-header');
  if (header) {
    var solid = function () { header.classList.toggle('is-solid', window.scrollY > 24); };
    solid();
    window.addEventListener('scroll', solid, { passive: true });
  }

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

  /* ── Reveal au scroll — fade + 20px, stagger léger ──────────────────── */
  var targets = $$('[data-reveal]');
  if (targets.length) {
    if (reduce || !('IntersectionObserver' in window)) {
      targets.forEach(function (el) { el.classList.add('is-in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var el = entry.target;
          var i = parseInt(el.getAttribute('data-reveal'), 10);
          el.style.setProperty('--reveal-delay', (isNaN(i) ? 0 : i * 90) + 'ms');
          el.classList.add('is-in');
          io.unobserve(el);
        });
      }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
      targets.forEach(function (el) { io.observe(el); });
    }
  }
})();
