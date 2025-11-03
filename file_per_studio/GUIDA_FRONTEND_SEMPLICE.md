# 🎨 GUIDA FRONTEND SEMPLICE

> Come funzionano le pagine HTML del progetto

---

## 📁 PAGINE DEL PROGETTO

Il progetto ha queste pagine HTML in `templates/`:

```
templates/
├── home.html           # Homepage (prodotti)
├── login.html          # Pagina login
├── register.html       # Pagina registrazione
├── account.html        # Account utente
├── logs.html           # Dashboard admin (con grafici)
├── 404.html            # Errore "pagina non trovata"
├── 500.html            # Errore server
├── contatti.html       # Form contatti
├── privacy_policy.html # Privacy
└── terms_conditions.html # Termini e condizioni
```

**IMPORTANTE:** Ogni pagina è **INDIPENDENTE** (no template base condiviso).

---

## 🔄 COME FUNZIONA (SCHEMA BASE)

### **1. Backend mostra pagina:**
```python
# app.py
@app.route('/login')
def login():
    return render_template('login.html')
```

### **2. Browser riceve HTML:**
```html
<!-- login.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <form method="POST">
        <input type="text" name="username">
        <input type="password" name="password">
        <button type="submit">Accedi</button>
    </form>
</body>
</html>
```

### **3. User compila form e invia:**
```
User clicca "Accedi"
    ↓
Browser invia POST /login
    ↓
Backend riceve dati
    ↓
Backend risponde con redirect
    ↓
Browser mostra nuova pagina
```

---

## 📄 PAGINE PRINCIPALI

### **HOME.HTML** - Homepage

**Cosa fa:**
- Mostra 8 prodotti (e-commerce fake)
- Form contatto in fondo
- Accessibile a tutti

**Struttura:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Homepage</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <!-- Navbar -->
    <nav>
        <a href="/">Home</a>
        <a href="/login">Login</a>
        <a href="/register">Registrati</a>
    </nav>
    
    <!-- Prodotti -->
    <section class="products">
        <div class="product-card">
            <img src="...">
            <h3>Maglietta Basic</h3>
            <p class="price">€19.99</p>
        </div>
        <!-- ... altri 7 prodotti -->
    </section>
    
    <!-- Form contatto -->
    <form method="POST" action="/contact">
        <input type="text" name="nome">
        <input type="email" name="email">
        <textarea name="messaggio"></textarea>
        <button type="submit">Invia</button>
    </form>
</body>
</html>
```

---

### **LOGIN.HTML** - Login

**Cosa fa:**
- Form con username e password
- Invia dati al backend
- Backend controlla credenziali

**Struttura:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="login-box">
        <h1>Login</h1>
        
        <!-- Flash messages (messaggi di errore/successo) -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endwith %}
        
        <!-- Form -->
        <form method="POST" action="{{ url_for('login') }}">
            <input type="text" name="username" required>
            <input type="password" name="password" required>
            <button type="submit">Accedi</button>
        </form>
        
        <p>Non hai un account? <a href="/register">Registrati</a></p>
    </div>
</body>
</html>
```

**Flusso:**
```
1. User apre /login
2. Backend mostra login.html
3. User compila form
4. Click "Accedi"
5. Browser → POST /login (username + password)
6. Backend controlla credenziali:
   - OK → redirect /account + messaggio "Login riuscito"
   - NO → redirect /login + messaggio "Credenziali errate"
7. Browser mostra pagina con messaggio
```

---

### **REGISTER.HTML** - Registrazione

**Cosa fa:**
- Form registrazione
- Validazione password in tempo reale (JavaScript)
- Mostra requisiti password

**Parte HTML:**
```html
<form method="POST">
    <input type="text" name="username" required minlength="3">
    
    <input type="password" id="password" name="password" required>
    
    <!-- Requisiti password (aggiornati con JavaScript) -->
    <div class="requirements">
        <div id="req-length" class="requirement invalid">
            <i class="fas fa-times-circle"></i>
            Almeno 8 caratteri
        </div>
        <div id="req-uppercase" class="requirement invalid">
            <i class="fas fa-times-circle"></i>
            Una maiuscola
        </div>
        <!-- ... altri requisiti -->
    </div>
    
    <input type="password" name="confirm_password" required>
    
    <button type="submit">Registrati</button>
</form>
```

**Parte JavaScript (validazione real-time):**
```javascript
const passwordInput = document.getElementById('password');

passwordInput.addEventListener('input', function() {
    const password = this.value;
    
    // Controlla lunghezza
    if (password.length >= 8) {
        document.getElementById('req-length').classList.add('valid');
        document.getElementById('req-length').classList.remove('invalid');
    } else {
        document.getElementById('req-length').classList.add('invalid');
        document.getElementById('req-length').classList.remove('valid');
    }
    
    // Controlla maiuscola
    if (/[A-Z]/.test(password)) {
        document.getElementById('req-uppercase').classList.add('valid');
        document.getElementById('req-uppercase').classList.remove('invalid');
    }
    // ... altri controlli
});
```

**CSS:**
```css
.requirement.valid {
    color: green;
}

.requirement.invalid {
    color: red;
}
```

---

### **ACCOUNT.HTML** - Account Utente

**Cosa fa:**
- Mostra info utente loggato
- Cambio password
- Eliminazione account

**Variabili da backend:**
```python
# app.py
@app.route('/account')
@login_required  # Solo se loggato
def account():
    # current_user è automaticamente disponibile
    return render_template('account.html')
```

**HTML:**
```html
<div class="account-info">
    <h2>Il tuo Account</h2>
    <p>Username: {{ current_user.username }}</p>
    <p>Registrato: {{ current_user.created_at.strftime('%d/%m/%Y') }}</p>
    <p>Admin: 
        {% if current_user.is_admin %}
            Sì
        {% else %}
            No
        {% endif %}
    </p>
</div>

<!-- Form cambio password -->
<form method="POST" action="/account/change-password">
    <input type="password" name="old_password" placeholder="Password attuale">
    <input type="password" name="new_password" placeholder="Nuova password">
    <button type="submit">Cambia Password</button>
</form>

<!-- Elimina account -->
<button onclick="confirmDelete()">Elimina Account</button>

<script>
function confirmDelete() {
    if (confirm('Sei sicuro? Azione irreversibile!')) {
        window.location.href = '/account/delete';
    }
}
</script>
```

---

### **LOGS.HTML** - Dashboard Admin ⭐

**Cosa fa:**
- Mostra tabella log
- 3 grafici interattivi (Chart.js)
- Filtri (tipo, IP, data)
- **SOLO ADMIN**

**Backend passa dati:**
```python
# app.py
@app.route('/logs')
@login_required
def logs():
    if not current_user.is_admin:
        abort(403)  # Non admin → bloccato
    
    # Query log
    logs = Log.query.all()
    
    # Serializza per grafici
    logs_json = [{
        'type': log.type,
        'ip': log.ip,
        'timestamp': log.timestamp.isoformat(),
        'is_error': log.is_error
    } for log in logs]
    
    # Conta tipi
    from collections import Counter
    log_type_counts = Counter([log.type for log in logs])
    
    return render_template(
        'logs.html',
        logs=logs,
        logs_json=logs_json,
        log_type_counts=log_type_counts
    )
```

**HTML Legenda:**
```html
<!-- Legenda tipi log -->
<div class="legend">
    <h3>📋 Legenda</h3>
    
    <div class="legend-category">
        <h4>🔐 Autenticazione</h4>
        <span class="badge">LOGIN_SUCCESS ({{ log_type_counts.get('LOGIN_SUCCESS', 0) }})</span>
        <span class="badge">LOGIN_FAILED ({{ log_type_counts.get('LOGIN_FAILED', 0) }})</span>
        <span class="badge">LOGOUT ({{ log_type_counts.get('LOGOUT', 0) }})</span>
    </div>
    
    <!-- ... altre categorie -->
</div>
```

**HTML Filtri:**
```html
<form method="GET" action="/logs">
    <!-- Filtra per tipo -->
    <select name="type">
        <option value="">Tutti</option>
        <option value="LOGIN_SUCCESS">Login Success</option>
        <option value="LOGIN_FAILED">Login Failed</option>
        <!-- ... -->
    </select>
    
    <!-- Filtra per IP -->
    <input type="text" name="ip" placeholder="Es: 192.168.1.1">
    
    <!-- Filtra per data -->
    <input type="date" name="date_from">
    <input type="date" name="date_to">
    
    <!-- Solo errori -->
    <label>
        <input type="checkbox" name="show_errors" value="1">
        Solo errori
    </label>
    
    <button type="submit">Filtra</button>
</form>
```

**HTML Tabella:**
```html
<table>
    <thead>
        <tr>
            <th>ID</th>
            <th>Data</th>
            <th>Tipo</th>
            <th>IP</th>
            <th>Utente</th>
        </tr>
    </thead>
    <tbody>
        {% for log in logs %}
        <tr>
            <td>{{ log.id }}</td>
            <td>{{ log.timestamp.strftime('%d/%m/%Y %H:%M') }}</td>
            <td>{{ log.type }}</td>
            <td>{{ log.ip }}</td>
            <td>{{ log.user.username if log.user else 'N/A' }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

**JavaScript Grafici (Chart.js):**
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>
<script>
    // 1. Ricevi dati da backend
    const logs = {{ logs_json | tojson }};
    
    // 2. GRAFICO 1: Torta - Distribuzione tipi
    const logTypes = logs.map(log => log.type);
    const typeCounts = {};
    logTypes.forEach(type => {
        typeCounts[type] = (typeCounts[type] || 0) + 1;
    });
    
    const ctx1 = document.getElementById('chart1').getContext('2d');
    new Chart(ctx1, {
        type: 'pie',
        data: {
            labels: Object.keys(typeCounts),
            datasets: [{
                data: Object.values(typeCounts),
                backgroundColor: ['#f59e0b', '#3b82f6', '#10b981', '#ef4444']
            }]
        }
    });
    
    // 3. GRAFICO 2: Barre - Top 10 IP
    const ipCounts = {};
    logs.forEach(log => {
        ipCounts[log.ip] = (ipCounts[log.ip] || 0) + 1;
    });
    
    const topIPs = Object.entries(ipCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
    
    const ctx2 = document.getElementById('chart2').getContext('2d');
    new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: topIPs.map(item => item[0]),
            datasets: [{
                label: 'Eventi',
                data: topIPs.map(item => item[1]),
                backgroundColor: '#f59e0b'
            }]
        }
    });
    
    // 4. GRAFICO 3: Linee - Attività per ora
    const hourCounts = Array(24).fill(0);
    logs.forEach(log => {
        const hour = new Date(log.timestamp).getHours();
        hourCounts[hour]++;
    });
    
    const ctx3 = document.getElementById('chart3').getContext('2d');
    new Chart(ctx3, {
        type: 'line',
        data: {
            labels: Array.from({length: 24}, (_, i) => i + ':00'),
            datasets: [{
                label: 'Eventi per ora',
                data: hourCounts,
                borderColor: '#f59e0b',
                fill: false
            }]
        }
    });
</script>
```

---

## 🎨 CSS - DARK THEME

**File:** `static/style.css` (o `styles.css`)

**Variabili colori:**
```css
:root {
    --bg: #121212;         /* Sfondo nero */
    --card: #1e1e1e;       /* Card grigio scuro */
    --primary: #f59e0b;    /* Arancione */
    --text: #e0e0e0;       /* Testo grigio chiaro */
    --border: #333;        /* Bordi */
    --error: #ef4444;      /* Rosso */
    --success: #10b981;    /* Verde */
}

body {
    background: var(--bg);
    color: var(--text);
    font-family: Arial, sans-serif;
}

.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
}

.btn {
    background: var(--primary);
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

.btn:hover {
    background: #d97706;
}
```

---

## 📝 JINJA2 - SINTASSI BASE

### **1. Stampa variabile:**
```html
{{ variabile }}
{{ user.username }}
{{ logs|length }}  <!-- Numero elementi in lista -->
```

### **2. Condizionale:**
```html
{% if utente_loggato %}
    <p>Benvenuto!</p>
{% else %}
    <p>Fai login</p>
{% endif %}
```

### **3. Loop:**
```html
{% for log in logs %}
    <tr>
        <td>{{ log.id }}</td>
        <td>{{ log.type }}</td>
    </tr>
{% endfor %}
```

### **4. Filtri:**
```html
{{ text|upper }}                    <!-- MAIUSCOLO -->
{{ data|tojson }}                   <!-- Converti in JSON -->
{{ timestamp.strftime('%d/%m/%Y') }} <!-- Formatta data -->
```

---

## 🔄 COMUNICAZIONE BACKEND ↔ FRONTEND

### **1. Form POST → Backend**

**Frontend:**
```html
<form method="POST" action="/login">
    <input type="text" name="username">
    <input type="password" name="password">
    <button type="submit">Accedi</button>
</form>
```

**Backend:**
```python
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Controlla credenziali...
    if valid:
        flash('Login riuscito!', 'success')
        return redirect('/account')
    else:
        flash('Credenziali errate', 'error')
        return redirect('/login')
```

### **2. Backend → Frontend (variabili)**

**Backend:**
```python
@app.route('/account')
def account():
    return render_template('account.html')
    # current_user è automatico (Flask-Login)
```

**Frontend:**
```html
<p>Username: {{ current_user.username }}</p>
<p>Admin: {{ current_user.is_admin }}</p>
```

### **3. Backend → Frontend (JSON per grafici)**

**Backend:**
```python
logs_json = [{'type': 'LOGIN', 'ip': '192.168.1.1'}]
return render_template('logs.html', logs_json=logs_json)
```

**Frontend:**
```html
<script>
    const logs = {{ logs_json | tojson }};
    // Ora logs è array JavaScript
    console.log(logs[0].type);  // 'LOGIN'
</script>
```

### **4. Flash Messages**

**Backend:**
```python
flash('Operazione riuscita!', 'success')
flash('Errore!', 'error')
```

**Frontend (in ogni pagina):**
```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
        <div class="alert alert-{{ category }}">
            {{ message }}
        </div>
    {% endfor %}
{% endwith %}
```

---

## 📊 CHART.JS - GRAFICI (SEMPLIFICATO)

### **Setup:**
```html
<!-- Includi libreria -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>

<!-- Canvas per grafico -->
<canvas id="myChart"></canvas>
```

### **Grafico Torta:**
```javascript
const ctx = document.getElementById('myChart').getContext('2d');
new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['LOGIN', 'LOGOUT', 'ERRORE'],
        datasets: [{
            data: [45, 30, 25],
            backgroundColor: ['#10b981', '#f59e0b', '#ef4444']
        }]
    }
});
```

### **Grafico Barre:**
```javascript
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['IP 1', 'IP 2', 'IP 3'],
        datasets: [{
            label: 'Eventi',
            data: [100, 80, 60],
            backgroundColor: '#f59e0b'
        }]
    }
});
```

### **Grafico Linee:**
```javascript
new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['0:00', '6:00', '12:00', '18:00'],
        datasets: [{
            label: 'Attività',
            data: [10, 50, 80, 30],
            borderColor: '#f59e0b',
            fill: false
        }]
    }
});
```

---

## ✅ RIASSUNTO VELOCE

### **Ogni pagina HTML:**
1. Ha `<head>` con link al CSS
2. Ha `<body>` con contenuto
3. Può usare `{{ variabili }}` da backend
4. Può avere `<script>` per JavaScript

### **Flusso tipico:**
```
User apre URL
    ↓
Backend → render_template('page.html', variabili...)
    ↓
Jinja2 sostituisce {{ variabili }}
    ↓
Browser riceve HTML finale
    ↓
Carica CSS e JavaScript
    ↓
User interagisce (form, click)
    ↓
Browser invia dati al backend
    ↓
Backend processa e risponde
```

### **File importanti:**
- `templates/*.html` - Pagine HTML
- `static/style.css` - Stili CSS
- `app.py` - Backend (route)

---

**Fatto! Guida frontend semplice e chiara! 🎨**
