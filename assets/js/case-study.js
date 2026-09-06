/* Scrolly text swap.
   Exactly one text block is visible at a time, chosen from which media item
   is currently at the top of the viewport. Hiding the inactive blocks (rather
   than relying on an opaque block covering the one behind) is what guarantees
   nothing bleeds through, whichever direction you scroll. */
(function () {
  var groups = [].map.call(document.querySelectorAll('.scrolly'), function (sc) {
    return {
      el: sc,
      texts:  [].filter.call(sc.children, function (c) { return c.classList.contains('st'); }),
      medias: [].filter.call(sc.children, function (c) { return c.tagName === 'FIGURE'; })
    };
  }).filter(function (g) { return g.texts.length > 1 && g.texts.length === g.medias.length; });

  if (!groups.length) return;
  groups.forEach(function (g) { g.el.classList.add('swap'); });

  var PIN = 80;          // matches .st { top: 80px }
  var wide = function () { return window.innerWidth > 1040; };

  function update() {
    groups.forEach(function (g) {
      var active = 0;
      if (wide()) {
        // the last media whose top has reached (or passed) the pin line
        for (var i = 0; i < g.medias.length; i++) {
          // small tolerance so the swap lands as the image meets the pin,
          // rather than a pixel or two after it
          if (g.medias[i].getBoundingClientRect().top <= PIN + 8) active = i;
        }
      }
      g.texts.forEach(function (t, i) { t.classList.toggle('is-on', i === active); });
    });
  }

  var queued = false;
  function schedule() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () { queued = false; update(); });
  }

  /* Driven by IntersectionObserver rather than scroll events: the root is
     collapsed to a 1px band sitting on the pin line, so a media item entering
     or leaving that band is an intersection change and fires reliably — no
     dependence on scroll events reaching the window, and no work while
     nothing is crossing. The scroll listener stays as a cheap belt-and-braces. */
  var io = null;
  function observe() {
    if (io) io.disconnect();
    var below = Math.max(0, window.innerHeight - PIN - 1);
    io = new IntersectionObserver(schedule, {
      rootMargin: '-' + PIN + 'px 0px -' + below + 'px 0px',
      threshold: 0
    });
    groups.forEach(function (g) { g.medias.forEach(function (m) { io.observe(m); }); });
  }

  observe();
  update();
  window.addEventListener('scroll', schedule, { passive: true });
  var rt;
  window.addEventListener('resize', function () {
    clearTimeout(rt);
    rt = setTimeout(function () { observe(); update(); }, 120);
  });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(update);
})();

/* Autoplay each video when it scrolls into view, pause when it leaves.
   Needs muted (browsers block autoplay with sound). Controls stay on so the
   viewer can pause or scrub. Skipped entirely under prefers-reduced-motion,
   where the poster + controls are the experience. */
(function () {
  var vids = document.querySelectorAll('video');
  if (!vids.length || !('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var vo = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      var v = en.target;
      if (en.isIntersecting) {
        // preload="none" means the first play() also starts the download
        var p = v.play();
        if (p && p.catch) p.catch(function () { /* autoplay refused — poster stays */ });
      } else if (!v.paused) {
        v.pause();
      }
    });
  }, { threshold: 0.35 });

  vids.forEach(function (v) { vo.observe(v); });
})();

var rv = document.querySelectorAll('.rv');
if (!matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, { rootMargin: '0px 0px -6% 0px', threshold: 0.05 });
  rv.forEach(function (el) { io.observe(el); });
} else { rv.forEach(function (el) { el.classList.add('in'); }); }

var ids = ['context','research','insight','design','impact'];
var links = {};
ids.forEach(function (id) { links[id] = document.querySelector('.dock-links a[href="#' + id + '"]'); });
var spy = new IntersectionObserver(function (es) {
  es.forEach(function (en) {
    if (en.isIntersecting) {
      ids.forEach(function (id) { links[id] && links[id].classList.remove('active'); });
      links[en.target.id] && links[en.target.id].classList.add('active');
    }
  });
}, { rootMargin: '-45% 0px -50% 0px' });
ids.forEach(function (id) { var el = document.getElementById(id); if (el) spy.observe(el); });

/* Before/after reveal: set --reveal-p (0 -> 1) from how far the AFTER frame
   has risen up the viewport, so it crossfades over the BEFORE frame. */
(function () {
  var sections = document.querySelectorAll('.reveal');
  if (!sections.length) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  function paint() {
    sections.forEach(function (sec) {
      var after = sec.querySelector('.pane.is-after');
      if (!after) return;
      var travel = window.innerHeight || 1;
      var p = 1 - (after.getBoundingClientRect().top / travel);
      sec.style.setProperty('--reveal-p', Math.min(1, Math.max(0, p)).toFixed(3));
    });
  }
  var queued = false;
  function schedule() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () { queued = false; paint(); });
  }
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule);
  if ('IntersectionObserver' in window) {
    var steps = []; for (var i = 0; i <= 20; i++) steps.push(i / 20);
    var io = new IntersectionObserver(schedule, { threshold: steps });
    sections.forEach(function (s) { var a = s.querySelector('.pane.is-after'); if (a) io.observe(a); });
  }
  paint();
})();
