(function(){
	const ADMIN = { email: 'admin@admin.it', password: 'admin123' };

	document.addEventListener('DOMContentLoaded', () => {
		const form = document.getElementById('adminLoginForm');
		const msg = document.getElementById('adminMsg');
		if (!form) return;

		form.addEventListener('submit', (e) => {
			e.preventDefault();
			const email = (document.getElementById('adminEmail')||{}).value.trim();
			const pass = (document.getElementById('adminPassword')||{}).value;

			if (email.toLowerCase() === ADMIN.email && pass === ADMIN.password) {
				sessionStorage.setItem('user', email);
				sessionStorage.setItem('isAdmin', 'true');
				msg.style.color = '#b7f5c6';
				msg.textContent = 'Accesso admin riuscito. Reindirizzamento...';
				setTimeout(() => window.location.href = 'dashboard.html', 500);
			} else {
				msg.style.color = '#ffd6da';
				msg.textContent = 'Credenziali admin non corrette.';
			}
		});
	});
})();
