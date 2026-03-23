// ── Auto-close flash messages ──────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert[data-auto-close]');
  alerts.forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity .4s ease, transform .4s ease';
      el.style.opacity = '0';
      el.style.transform = 'translateY(-6px)';
      setTimeout(function () { el.remove(); }, 400);
    }, 4000);
  });

  // Close button on alerts
  document.querySelectorAll('.alert .close-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const alert = this.closest('.alert');
      alert.style.opacity = '0';
      setTimeout(function () { alert.remove(); }, 300);
    });
  });

  // ── Confirm Delete Buttons ────────────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      const msg = this.dataset.confirm || 'Êtes-vous sûr de vouloir supprimer cet élément ?';
      if (!confirm(msg)) {
        e.preventDefault();
      }
    });
  });

  // ── Active nav link ────────────────────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.sidebar-nav a').forEach(function (link) {
    const href = link.getAttribute('href');
    if (href && currentPath.startsWith(href) && href !== '/') {
      link.classList.add('active');
    } else if (href === '/' && currentPath === '/') {
      link.classList.add('active');
    }
  });

  // ── Live search table filter ──────────────────────────────
  const liveSearch = document.getElementById('live-search');
  if (liveSearch) {
    liveSearch.addEventListener('input', function () {
      const term = this.value.toLowerCase().trim();
      const rows = document.querySelectorAll('tbody tr[data-searchable]');
      let visibleCount = 0;
      rows.forEach(function (row) {
        const text = row.textContent.toLowerCase();
        const show = text.includes(term);
        row.style.display = show ? '' : 'none';
        if (show) visibleCount++;
      });
      const emptyRow = document.getElementById('empty-search-row');
      if (emptyRow) {
        emptyRow.style.display = visibleCount === 0 ? '' : 'none';
      }
    });
  }

  // ── Quantity auto-validation in livre form ─────────────────
  const qteTotal = document.getElementById('id_quantite_totale');
  const qteDispo = document.getElementById('id_quantite_disponible');
  if (qteTotal && qteDispo) {
    qteTotal.addEventListener('change', function () {
      const total = parseInt(this.value) || 0;
      const dispo = parseInt(qteDispo.value) || 0;
      if (dispo > total) qteDispo.value = total;
      qteDispo.max = total;
    });
  }

  // ── Tooltip init (Bootstrap) ──────────────────────────────
  if (typeof bootstrap !== 'undefined') {
    const tooltipEls = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipEls.forEach(function (el) {
      new bootstrap.Tooltip(el);
    });
  }
});
