# 📚 GUIDA STUDIO COMPLETA - Security SIEM Project

## 🎯 Obiettivo di questa guida
Questa guida ti aiuterà a comprendere **OGNI SINGOLO DETTAGLIO** del progetto, dall'architettura generale fino alle singole funzioni.

---

## 📋 INDICE

1. [Architettura Generale](#1-architettura-generale)
2. [Flusso di Esecuzione](#2-flusso-di-esecuzione)
3. [Database e Modelli](#3-database-e-modelli)
4. [Sistema di Sicurezza](#4-sistema-di-sicurezza)
5. [Routing e Pagine](#5-routing-e-pagine)
6. [Frontend e Stili](#6-frontend-e-stili)
7. [Testing e Debugging](#7-testing-e-debugging)

---

## 1. ARCHITETTURA GENERALE

### 1.1 Struttura del Progetto
```
ProjectWorkGroup3/
├── app.py                      # File principale Flask (routing + logica)
├── requirements.txt            # Dipendenze Python
├── recreate_db.py             # Script per ricreare il database
├── db_utils.py                # Utility per gestire DB da terminale
│
├── model/                     # Modelli dati e logica business
│   ├── __init__.py           # Inizializza db e bcrypt
│   ├── user.py               # Modello User + CRUD operations
│   ├── log.py                # Modello Log + CRUD operations
│   ├── validator.py          # Validazione input malevoli (SQL Injection, XSS, ecc.)
│   ├── password_validator.py # Validazione forza password
│   └── analyzer.py           # Analisi log per rilevare attacchi
│
├── templates/                 # Template HTML (Jinja2)
│   ├── base.html             # Template base con navbar
│   ├── home.html             # Homepage (prodotti vetrina)
│   ├── login.html            # Pagina login
│   ├── register.html         # Pagina registrazione
│   ├── account.html          # Account utente (cambio password, eliminazione)
│   ├── logs.html             # Dashboard admin security logs
│   ├── 404.html              # Pagina errore 404
│   └── 500.html              # Pagina errore 500
│
├── static/                    # File statici (CSS, JS, immagini)
│   └── styles.css            # Stili CSS globali
│
└── instance/                  # Database SQLite (creato automaticamente)
    └── users.db              # File database
```

### 1.2 Stack Tecnologico

**Backend:**
- **Flask 2.x**: Framework web Python
- **SQLAlchemy**: ORM per gestione database
- **Flask-Login**: Gestione autenticazione utenti
- **Flask-Bcrypt**: Hashing password (bcrypt algorithm)
- **SQLite**: Database relazionale leggero

**Frontend:**
- **Jinja2**: Template engine (integrato in Flask)
- **HTML5 + CSS3**: Struttura e stili
- **JavaScript Vanilla**: Interattività (validazione form, grafici)
- **Chart.js 4.4.0**: Libreria per grafici interattivi
- **Font Awesome 6.5.0**: Icone vettoriali

**Sicurezza:**
- **Regex patterns**: Rilevamento SQL Injection, XSS, Command Injection, Path Traversal
- **Bcrypt**: Hash password con salt automatico
- **Flask sessions**: Gestione sessioni lato server
- **CSRF protection**: (implementabile con Flask-WTF)

---

## 2. FLUSSO DI ESECUZIONE

### 2.1 Avvio Applicazione

```
1. python app.py
   └─> Flask carica app.py
       ├─> Importa model/__init__.py
       │   └─> Inizializza db (SQLAlchemy) e bcrypt
       ├─> Importa model/user.py, model/log.py, ecc.
       ├─> Configura Flask-Login (login_manager)
       ├─> Registra route (@app.route)
       └─> Avvia server su http://127.0.0.1:5000
```

### 2.2 Ciclo Richiesta-Risposta (esempio: Login)

```
1. Utente accede a http://127.0.0.1:5000/login
   └─> Flask chiama funzione login() decorata con @app.route('/login')
       
2. Metodo GET:
   └─> return render_template('login.html')
       └─> Jinja2 renderizza template con navbar e form
       
3. Utente compila form e clicca "Login"
   └─> Browser invia POST a /login con username e password
   
4. Metodo POST:
   ├─> Estrae dati: username = request.form.get('username')
   ├─> VALIDAZIONE SQL Injection:
   │   └─> InputValidator.validate_sql_only(username)
   │       ├─> Se malevolo: crea log MALICIOUS_INPUT_*, blocca richiesta
   │       └─> Se safe: continua
   │
   ├─> Cerca utente: user = get_user_by_username(username)
   │   └─> Query SQLAlchemy: User.query.filter_by(username=username).first()
   │
   ├─> Verifica password: user.check_password(password)
   │   └─> bcrypt.check_password_hash(user.password, password)
   │
   ├─> Se credenziali corrette:
   │   ├─> login_user(user) -> Flask-Login crea sessione
   │   ├─> create_log(ip, 'LOGIN_SUCCESS', user) -> Salva log
   │   └─> redirect('/account')
   │
   └─> Se credenziali errate:
       ├─> create_log(ip, 'LOGIN_FAILED', is_error=True)
       └─> flash('Credenziali non valide', 'error')
```

### 2.3 Gestione Sessioni (Flask-Login)

```
Flask-Login usa cookie sicuri per tracciare utenti:

1. login_user(user)
   └─> Crea cookie "remember_token" (firmato con SECRET_KEY)
   
2. @login_required decorator
   └─> Controlla se cookie è valido
       ├─> Valido: continua con richiesta
       └─> Non valido: redirect a /login
       
3. current_user
   └─> Oggetto globale che rappresenta utente loggato
       ├─> current_user.username
       ├─> current_user.is_admin
       └─> current_user.id
       
4. logout_user()
   └─> Elimina cookie e sessione
```

---

## 3. DATABASE E MODELLI

### 3.1 Modello User (model/user.py)

```python
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    # Campi
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hash bcrypt
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Metodi
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
```

**Dettagli:**
- `UserMixin`: Fornisce metodi per Flask-Login (is_authenticated, is_active, get_id)
- `db.Model`: Classe base SQLAlchemy
- `unique=True`: Username deve essere unico (no duplicati)
- `nullable=False`: Campo obbligatorio
- `password`: NON memorizza password in chiaro, solo hash bcrypt (60 caratteri)
- `created_at`: Timestamp automatico alla creazione

**CRUD Operations:**
```python
create_user(username, password, is_admin=False)  # Crea utente con hash password
get_user_by_username(username)                   # Cerca per username
get_user_by_id(user_id)                         # Cerca per ID
update_user(user_id, **kwargs)                  # Aggiorna campi dinamici
delete_user(user_id)                            # Elimina utente
```

### 3.2 Modello Log (model/log.py)

```python
class Log(db.Model):
    __tablename__ = 'logs'
    
    # Campi
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(45), nullable=False)        # IPv4 o IPv6
    type = db.Column(db.String(50), nullable=False)      # Tipo evento
    timestamp = db.Column(db.DateTime, default=datetime.now)
    is_error = db.Column(db.Boolean, default=False)
    
    # Relazione con User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', backref='logs')
```

**Tipi di Log (type):**
```
AUTENTICAZIONE:
├─ LOGIN_SUCCESS
├─ LOGIN_FAILED
├─ LOGOUT
└─ REGISTER_SUCCESS

GESTIONE ACCOUNT:
├─ PASSWORD_CHANGE
└─ ACCOUNT_DELETED

ACCESSO PAGINE:
├─ PAGE_ACCESS_HOME
├─ PAGE_ACCESS_LOGIN
├─ PAGE_ACCESS_REGISTER
├─ PAGE_ACCESS_ACCOUNT
├─ PAGE_ACCESS_LOGS
├─ PAGE_NOT_FOUND (404)
└─ INTERNAL_SERVER_ERROR (500)

ATTACCHI SICUREZZA:
├─ MALICIOUS_INPUT_SQL_INJECTION
├─ MALICIOUS_INPUT_XSS
├─ MALICIOUS_INPUT_COMMAND_INJECTION
└─ MALICIOUS_INPUT_PATH_TRAVERSAL
```

**Relazione User-Log:**
```python
# Un utente può avere molti log
user.logs  # Lista di tutti i log dell'utente

# Un log appartiene a un utente (o None se non autenticato)
log.user   # Oggetto User associato al log
```

### 3.3 Query SQLAlchemy (Esempi)

```python
# SELECT * FROM users WHERE username = 'admin'
User.query.filter_by(username='admin').first()

# SELECT * FROM logs ORDER BY timestamp DESC LIMIT 20
Log.query.order_by(Log.timestamp.desc()).limit(20).all()

# SELECT COUNT(*) FROM logs WHERE is_error = True
Log.query.filter_by(is_error=True).count()

# SELECT * FROM logs WHERE type LIKE 'PAGE_ACCESS%'
Log.query.filter(Log.type.like('PAGE_ACCESS%')).all()

# JOIN: SELECT logs.*, users.username FROM logs JOIN users ON logs.user_id = users.id
Log.query.join(User).all()

# GROUP BY con aggregazione
db.session.query(
    Log.ip,
    func.count(Log.id).label('total')
).group_by(Log.ip).all()
```

---

## 4. SISTEMA DI SICUREZZA

### 4.1 Validazione Input (model/validator.py)

**Architettura:**
```python
class InputValidator:
    SQL_PATTERNS = [...]      # Lista di regex per SQL Injection
    XSS_PATTERNS = [...]      # Lista di regex per XSS
    COMMAND_PATTERNS = [...]  # Lista di regex per Command Injection
    PATH_PATTERNS = [...]     # Lista di regex per Path Traversal
    
    @staticmethod
    def validate(input_string, field_name="input"):
        # Controlla TUTTI i pattern
        # Ritorna: {'is_safe': bool, 'attack_type': str, ...}
    
    @staticmethod
    def validate_sql_only(input_string, field_name="input"):
        # Controlla SOLO SQL Injection (più leggero per login/register)
```

**Esempio Pattern SQL Injection:**
```python
r"(\bOR\b|\bAND\b)\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?"
# Rileva: OR 1=1, AND 1=1, OR '1'='1'

r"UNION\s+SELECT"
# Rileva: UNION SELECT

r"'\s*OR\s*'"
# Rileva: ' OR '

r"admin'\s*--"
# Rileva: admin'--
```

**Flusso di Validazione:**
```
Input utente: "admin' OR '1'='1"
    ↓
InputValidator.validate_sql_only(input, 'username')
    ↓
Itera su SQL_PATTERNS:
    ↓
Pattern r"'\s*OR\s*'" trova MATCH!
    ↓
Ritorna:
{
    'is_safe': False,
    'attack_type': 'SQL_INJECTION',
    'pattern_matched': r"'\s*OR\s*'",
    'field': 'username',
    'input_sample': "admin' OR '1'='1"
}
    ↓
app.py crea log MALICIOUS_INPUT_SQL_INJECTION
    ↓
Blocca richiesta con flash('Input sospetto rilevato')
```

### 4.2 Password Hashing (Bcrypt)

**Come funziona Bcrypt:**
```
Password in chiaro: "MySecurePass123!"
    ↓
bcrypt.generate_password_hash(password)
    ↓
1. Genera SALT casuale (16 byte random)
2. Combina password + salt
3. Applica algoritmo bcrypt (2^cost round)
4. Output: $2b$12$randomsalt....hashedpassword (60 caratteri)
    ↓
Salva in DB: "$2b$12$N9qo8uLOickgx2ZMRZoMyu.Tz6GR9.oXQ5zDwqkBXGsYVPKVqPhPG"
```

**Verifica Password:**
```
Password utente: "MySecurePass123!"
Hash DB: "$2b$12$N9qo8uLOickgx2ZMRZoMyu..."
    ↓
bcrypt.check_password_hash(hash_db, password_utente)
    ↓
1. Estrae SALT dall'hash ($2b$12$N9qo8uLO...)
2. Applica bcrypt a password_utente con STESSO salt
3. Confronta risultato con hash_db
4. Ritorna True/False
```

**Perché è sicuro:**
- SALT casuale: Due utenti con stessa password hanno hash diversi
- Slow algorithm: 2^12 = 4096 iterazioni (difficile brute force)
- No reversibile: Impossibile ottenere password da hash

### 4.3 Analisi Log per Attacchi (model/analyzer.py)

```python
class SecurityAnalyzer:
    
    @staticmethod
    def detect_brute_force(minutes=5, threshold=5):
        """
        Rileva tentativi brute force:
        - Cerca LOGIN_FAILED negli ultimi N minuti
        - Raggruppa per IP
        - Se IP ha >= threshold tentativi -> ALERT
        """
        
    @staticmethod
    def detect_suspicious_ips(hours=24, threshold=10):
        """
        Rileva IP sospetti:
        - Cerca is_error=True nelle ultime N ore
        - Raggruppa per IP
        - Se IP ha >= threshold errori -> WARNING
        """
        
    @staticmethod
    def detect_malicious_inputs(hours=24):
        """
        Conta attacchi per tipo:
        - SQL_INJECTION: quanti tentativi, da quali IP
        - XSS: quanti tentativi, da quali IP
        - COMMAND_INJECTION: ...
        - PATH_TRAVERSAL: ...
        """
```

**Esempio Query Brute Force:**
```python
time_threshold = datetime.now() - timedelta(minutes=5)

results = db.session.query(
    Log.ip,                              # Raggruppa per IP
    func.count(Log.id).label('attempts') # Conta tentativi
).filter(
    Log.type == 'LOGIN_FAILED',         # Solo login falliti
    Log.timestamp >= time_threshold      # Ultimi 5 minuti
).group_by(Log.ip).all()

# Output: [('192.168.1.100', 8), ('10.0.0.5', 12), ...]
```

---

## 5. ROUTING E PAGINE

### 5.1 Route Pubbliche (no login richiesto)

```python
@app.route('/')
def home():
    """Homepage con prodotti vetrina"""
    # Crea log PAGE_ACCESS_HOME
    # Renderizza templates/home.html
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login utente"""
    # GET: mostra form
    # POST: valida credenziali, crea sessione
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registrazione nuovo utente"""
    # POST: valida dati, crea utente con password hash
```

### 5.2 Route Protette (login richiesto)

```python
@app.route('/account')
@login_required  # Decorator Flask-Login
def account():
    """Pagina account utente"""
    # Solo se current_user.is_authenticated
    # Mostra: cambio password, eliminazione account
    
@app.route('/logout')
@login_required
def logout():
    """Logout utente"""
    # logout_user() -> elimina sessione
    # redirect a /login
```

### 5.3 Route Admin (solo admin)

```python
@app.route('/logs')
@login_required
def logs():
    """Dashboard security logs (SOLO ADMIN)"""
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    # Filtra log per:
    # - Tipo (type)
    # - IP (ip)
    # - Data (date_from, date_to)
    # - Errore (show_errors)
    
    # Crea grafici con Chart.js:
    # - Distribuzione tipi log (pie chart)
    # - Top 10 IP attivi (horizontal bar)
    # - Attività per ora (line chart)
```

### 5.4 Error Handlers

```python
@app.errorhandler(404)
def not_found(error):
    """Pagina 404 personalizzata"""
    # Crea log PAGE_NOT_FOUND
    # Renderizza templates/404.html
    
@app.errorhandler(500)
def internal_error(error):
    """Pagina 500 personalizzata"""
    # db.session.rollback() -> annulla transazioni fallite
    # Crea log INTERNAL_SERVER_ERROR
    # Renderizza templates/500.html
```

---

## 6. FRONTEND E STILI

### 6.1 Template Base (templates/base.html)

```jinja2
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}SIEM Security{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navbar con menu dinamico -->
    <nav>
        {% if current_user.is_authenticated %}
            <a href="/account">Account</a>
            {% if current_user.is_admin %}
                <a href="/logs">Security Logs</a>
            {% endif %}
            <a href="/logout">Logout</a>
        {% else %}
            <a href="/login">Login</a>
            <a href="/register">Registrati</a>
        {% endif %}
    </nav>
    
    <!-- Flash messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">{{ message }}</div>
        {% endfor %}
    {% endwith %}
    
    <!-- Contenuto pagina -->
    {% block content %}{% endblock %}
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

**Concetti Jinja2:**
- `{% block %}`: Blocco sovrascrivibile da template figli
- `{{ variable }}`: Output variabile
- `{% if %}`: Condizionale
- `{% for %}`: Loop
- `url_for('static', filename='...')`: Genera URL file statico

### 6.2 Chart.js per Grafici (logs.html)

```javascript
// Dati passati da Flask (serializzati JSON)
const logs = {{ logs_json | tojson }};

// Estrae tipi di log
const logTypes = logs.map(log => log.type);

// Conta occorrenze
const typeCounts = logTypes.reduce((acc, type) => {
    acc[type] = (acc[type] || 0) + 1;
    return acc;
}, {});

// Crea grafico a torta
new Chart(ctx, {
    type: 'pie',
    data: {
        labels: Object.keys(typeCounts),
        datasets: [{
            data: Object.values(typeCounts),
            backgroundColor: ['#f59e0b', '#3b82f6', '#10b981', ...]
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { position: 'bottom' }
        }
    }
});
```

### 6.3 Dark Theme CSS

```css
:root {
    --bg: #121212;           /* Background nero
    --card: #1e1e1e;         /* Card grigio scuro */
    --primary: #f59e0b;      /* Arancione */
    --text: #e0e0e0;         /* Grigio chiaro */
    --border: #333;          /* Bordi grigi */
    --error: #ef4444;        /* Rosso errori */
    --success: #10b981;      /* Verde successo */
}

body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Segoe UI', Tahoma, sans-serif;
}

.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
}

button.primary {
    background: var(--primary);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

button.primary:hover {
    background: #d97706;  /* Arancione più scuro */
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}
```

---

## 7. TESTING E DEBUGGING

### 7.1 Come Testare il Progetto

**1. Test Registrazione:**
```
1. Vai su http://127.0.0.1:5000/register
2. Prova username: "test_user"
3. Prova password debole: "123" -> Deve mostrare errori requisiti
4. Prova password forte: "SecurePass123!"
5. Verifica nel DB: python db_utils.py -> Opzione 1 (mostra utenti)
```

**2. Test SQL Injection:**
```
1. Vai su /login
2. Username: admin' OR '1'='1
3. Deve bloccare e mostrare: "Input sospetto rilevato"
4. Controlla log: python db_utils.py -> Opzione 2
5. Deve esserci MALICIOUS_INPUT_SQL_INJECTION
```

**3. Test Brute Force:**
```
1. Prova login fallito 5+ volte con password errata
2. Vai su /logs (come admin)
3. Controlla alert "Tentativi di brute force"
4. Deve mostrare il tuo IP con numero tentativi
```

**4. Test Grafici:**
```
1. Crea vari log (registrazione, login, logout, pagine)
2. Vai su /logs
3. Controlla:
   - Grafico a torta: distribuzione tipi
   - Grafico a barre: top IP
   - Grafico a linee: attività per ora
```

### 7.2 Debug con Flask

```python
# app.py
if __name__ == '__main__':
    app.run(debug=True)  # Abilita debug mode
```

**Debug mode:**
- Auto-reload: riavvia server quando modifichi file
- Traceback dettagliati: mostra errori completi nel browser
- Console interattiva: puoi eseguire codice Python negli errori

**Print Debugging:**
```python
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    print(f"DEBUG: Login attempt - username={username}")  # Console output
    
    validation = InputValidator.validate_sql_only(username)
    print(f"DEBUG: Validation result - {validation}")
    
    # ...
```

### 7.3 SQL Debug

```python
# Vedi query SQL generate da SQLAlchemy
app.config['SQLALCHEMY_ECHO'] = True

# Output nella console:
# SELECT users.id, users.username, ... FROM users WHERE users.username = ?
# ['admin']
```

### 7.4 Comandi Utili

```bash
# Ricrea database da zero
python recreate_db.py

# Utility interattiva DB
python db_utils.py

# Verifica struttura DB (con SQLite CLI)
sqlite3 instance/users.db
> .schema users
> .schema logs
> SELECT * FROM users;
> .quit

# Verifica dipendenze
pip freeze

# Installa dipendenze
pip install -r requirements.txt
```

---

## 📝 PROSSIMI PASSI PER LO STUDIO

### Livello 1: Comprensione Base
- [ ] Leggi tutto questo file
- [ ] Analizza struttura progetto (file e cartelle)
- [ ] Studia modelli User e Log
- [ ] Comprendi flusso login/register

### Livello 2: Approfondimento
- [ ] Studia validazione input (regex patterns)
- [ ] Analizza funzionamento bcrypt
- [ ] Comprendi query SQLAlchemy
- [ ] Studia Flask-Login e sessioni

### Livello 3: Avanzato
- [ ] Analizza SecurityAnalyzer (aggregazioni SQL)
- [ ] Studia Chart.js e JavaScript
- [ ] Comprendi Jinja2 templating
- [ ] Analizza CSS dark theme

### Livello 4: Testing Pratico
- [ ] Esegui tutti i test sopra descritti
- [ ] Modifica codice e osserva effetti
- [ ] Crea nuovi log types personalizzati
- [ ] Aggiungi nuovi grafici

---

## 🎓 RISORSE AGGIUNTIVE

- **Flask Docs**: https://flask.palletsprojects.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Bcrypt Explained**: https://en.wikipedia.org/wiki/Bcrypt
- **Regex Tutorial**: https://regexr.com/
- **Chart.js Docs**: https://www.chartjs.org/docs/

---

## ❓ DOMANDE DA PORSI DURANTE LO STUDIO

1. **Perché usiamo bcrypt invece di SHA256?**
2. **Come funziona la relazione User-Log in SQLAlchemy?**
3. **Perché validate_sql_only è più leggero di validate?**
4. **Come previene Flask-Login attacchi session hijacking?**
5. **Perché usiamo db.session.commit() dopo ogni modifica?**
6. **Come funziona il @login_required decorator?**
7. **Cosa succede se due utenti si registrano con stesso username?**
8. **Come Chart.js riceve i dati da Flask?**

---

**Buono studio! 🚀**
