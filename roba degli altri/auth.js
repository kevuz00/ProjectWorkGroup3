(function(){
  // credenziali admin demo
  const ADMIN = { email: 'admin@admin.it', password: 'admin123' };

  function showMessage(msg, ok){
    const el = document.getElementById('loginMessage');
    if (!el) { alert(msg); return; }
    el.textContent = msg;
    el.style.color = ok ? '#b7f5c6' : '#ffd6da';
  }

  const form = document.getElementById('loginForm');
  if (!form) return;

  form.addEventListener('submit', function(e){
    e.preventDefault();
    const email = (document.getElementById('email')||{}).value.trim();
    const password = (document.getElementById('password')||{}).value;

    // Accept any credentials: treat as admin only if exactly matches ADMIN
    const isAdmin = (email.toLowerCase() === ADMIN.email && password === ADMIN.password);

    // salva sessione demo
    sessionStorage.setItem('user', email || '');
    sessionStorage.setItem('isAdmin', isAdmin ? 'true' : 'false');

    showMessage('Login effettuato. Reindirizzamento...', true);

    setTimeout(() => {
      window.location.href = 'pw.html';
    }, 600);
  });
})();
