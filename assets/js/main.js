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
  /* Filtres de la page avis */
  $$('.chips').forEach(function (group) {
    var chips = $$('.chip', group), quotes = $$('.quote');
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        var f = chip.getAttribute('data-filter');
        chips.forEach(function (c) { var on = c === chip; c.classList.toggle('is-on', on); c.setAttribute('aria-pressed', on); });
        quotes.forEach(function (q) { q.hidden = f !== 'all' && (' ' + q.getAttribute('data-tags') + ' ').indexOf(' ' + f + ' ') < 0; });
      });
    });
  });

  /* Formulaire de contact. Sans endpoint (preproduction), il ne part pas :
     on le dit clairement et on renvoie vers WhatsApp. */
  $$('.contact-form').forEach(function (form) {
    var status = $('.contact-form__status', form);
    var say = function (msg) { status.textContent = msg; status.hidden = false; };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      if (form.website && form.website.value) return;
      var endpoint = form.getAttribute('data-endpoint');
      if (!endpoint) { say('The form is not connected yet on this preview. Please message us on WhatsApp in the meantime.'); return; }
      var btn = $('button[type="submit"]', form); btn.disabled = true;
      fetch(endpoint, { method: 'POST', body: new FormData(form) })
        .then(function (r) { if (!r.ok) throw r; form.reset(); say('Thank you. We will get back to you shortly, usually within the hour during opening hours.'); })
        .catch(function () { say('Sorry, the message could not be sent. Please message us on WhatsApp instead.'); })
        .then(function () { btn.disabled = false; });
    });
  });

  /* Comparateur avant / apres : le curseur deplace la decoupe */
  $$('.ba__range').forEach(function (range) {
    var fig = range.closest('.ba');
    range.addEventListener('input', function () { fig.style.setProperty('--pos', range.value + '%'); });
  });

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

  /* Voiture : traverse l'ecran de droite a gauche pendant que le footer entre
     dans la vue, et se gare au debut du contenu quand on atteint le bas de la
     page. Les roues tournent de la distance parcourue. Mouvement reduit :
     garee d'office. */
  var road = $('.road');
  if (road) {
    var car = $('.road__car', road), wheels = $$('.road-car__wheel', road),
        foot = road.parentNode, inner = $('.container', foot), queued = false;
    var place = function () {
      queued = false;
      var vh = window.innerHeight, top = foot.getBoundingClientRect().top,
          span = Math.min(foot.offsetHeight, vh) * 0.9,
          p = reduce ? 1 : Math.min(1, Math.max(0, (vh - top) / span));
      p = 1 - (1 - p) * (1 - p);                       // ralentit en se garant
      var start = road.clientWidth,
          end = inner.getBoundingClientRect().left + parseFloat(getComputedStyle(inner).paddingLeft),
          x = start + (end - start) * p,
          radius = car.getBoundingClientRect().width * 22 / 400,
          deg = -(start - x) / radius * 57.2958;
      car.style.transform = 'translateX(' + x + 'px)';
      wheels.forEach(function (w) { w.style.transform = 'rotate(' + deg + 'deg)'; });
    };
    var queue = function () { if (!queued) { queued = true; requestAnimationFrame(place); } };
    window.addEventListener('scroll', queue, { passive: true });
    window.addEventListener('resize', queue);
    place();
  }
})();
