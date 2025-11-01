(function(){
  document.addEventListener('DOMContentLoaded', function(){
    const logoutBtn = document.getElementById('logoutBtn');
    const securityBtn = document.getElementById('securityBtn');

    // Logout: cancella sessione e torna al login
    if (logoutBtn) {
      logoutBtn.addEventListener('click', function(){
        sessionStorage.removeItem('user');
        sessionStorage.removeItem('isAdmin');
        window.location.href = 'login.html';
      });
    }

    // Collega l'evento al pulsante "Sicurezza" esistente (se presente)
    if (securityBtn) {
      // rimuove eventuali handler precedenti per sicurezza
      securityBtn.replaceWith(securityBtn.cloneNode(true));
      const btn = document.getElementById('securityBtn');

      btn.addEventListener('click', () => {
        const isAdmin = sessionStorage.getItem('isAdmin') === 'true';
        if (isAdmin) {
          window.location.href = 'dashboard.html';
        } else {
          window.location.href = 'adminlog.html';
        }
      });
    }

    // check session
    const user = sessionStorage.getItem('user');
    const isAdmin = sessionStorage.getItem('isAdmin') === 'true';

    // if logged in and admin -> add "Sicurezza" button to the right of Accedi
    if (user && isAdmin && securityBtn) {
      const btn = document.getElementById('securityBtn');
      btn.addEventListener('click', () => {
        window.location.href = 'dashboard.html';
      });
    }

    // optional: if logged in (any user), you might change Accedi text to "Accedi" or show username
    // (kept minimal per spec)
  });
})();
