/* Mining Stock Report — main.js */

document.addEventListener('DOMContentLoaded', function () {

  // ── AJAX subscribe form (subscribe bar) ──────────────────────────────────
  const subscribeForm = document.getElementById('subscribeBarForm');
  if (subscribeForm) {
    subscribeForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const btn = subscribeForm.querySelector('button[type=submit]');
      const originalText = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Sending…';

      fetch(subscribeForm.action, {
        method: 'POST',
        body: new FormData(subscribeForm),
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
      })
        .then(r => r.json())
        .then(data => {
          if (data.status === 'ok') {
            btn.textContent = '✓ You\'re in!';
            btn.classList.replace('btn-warning', 'btn-success');
            subscribeForm.reset();
            if (data.download_url) {
              window.location.href = data.download_url;
            }
          } else {
            btn.textContent = 'Try again';
            btn.disabled = false;
          }
        })
        .catch(() => {
          btn.textContent = originalText;
          btn.disabled = false;
        });
    });
  }

  // ── Auto-dismiss alerts after 5 seconds ─────────────────────────────────
  document.querySelectorAll('.alert.alert-dismissible').forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // ── Active nav link highlighting ─────────────────────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.navbar-nav .nav-link, .navbar-nav .dropdown-item').forEach(function (link) {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
      link.setAttribute('aria-current', 'page');
    }
  });

});
