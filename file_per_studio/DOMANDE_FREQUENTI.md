# ❓ DOMANDE FREQUENTI (FAQ) - Security SIEM Project

## 🔍 Indice per Categoria
1. [Database e SQLAlchemy](#database-e-sqlalchemy)
2. [Sicurezza e Validazione](#sicurezza-e-validazione)
3. [Flask e Routing](#flask-e-routing)
4. [Frontend e JavaScript](#frontend-e-javascript)
5. [Debugging e Errori](#debugging-e-errori)

---

## DATABASE E SQLALCHEMY

### Q1: Perché due password uguali hanno hash diversi?
**A:** Bcrypt aggiunge un **SALT casuale** prima di fare l'hash. Il salt è una stringa random che viene combinata con la password.

**Esempio:**
```
Password: "MyPass123!"
Salt utente 1: "aB3xK9pQ..."
Hash utente 1: "$2b$12$aB3xK9pQ...hashedpassword1"

Password: "MyPass123!"  (stessa!)
Salt utente 2: "zY7wL2mN..."  (diverso!)
Hash utente 2: "$2b$12$zY7wL2mN...hashedpassword2"  (diverso!)
```

**Perché è importante?**
- Se due utenti hanno password uguale, un attaccante non può saperlo
- Se il database viene rubato, attaccante deve craccare OGNI hash separatamente
- Rainbow table attack diventa inutile

---

### Q2: Cosa significa `db.session.commit()`?
**A:** SQLAlchemy usa **transazioni**. Le modifiche al database non sono permanenti finché non fai commit.

**Flusso:**
```python
# 1. Crea oggetto (solo in memoria)
user = User(username='test', password='hash...')

# 2. Aggiungi alla sessione (preparato per DB)
db.session.add(user)

# 3. COMMIT = salva definitivamente nel DB
db.session.commit()  # <-- Adesso è nel database!

# Se qualcosa va male prima del commit:
db.session.rollback()  # Annulla tutto
```

**Analogia:** 
- `db.session.add()` = metti prodotti nel carrello
- `db.session.commit()` = paghi alla cassa (definitivo!)
- `db.session.rollback()` = svuoti il carrello

---

### Q3: Differenza tra `.first()` e `.all()`?
**A:**
- `.first()` → ritorna **1 oggetto** (o None se non trova)
- `.all()` → ritorna **lista di oggetti** (anche vuota [])

**Esempi:**
```python
# first() - Ritorna User object o None
user = User.query.filter_by(username='admin').first()
if user:
    print(user.username)  # OK
else:
    print("Non trovato")

# all() - Ritorna lista (anche se vuota)
users = User.query.filter_by(is_admin=True).all()
print(len(users))  # 0, 1, 2, 3...
for user in users:
    print(user.username)
```

**Quando usare cosa:**
- `.first()` quando cerchi **1 elemento specifico** (es: login)
- `.all()` quando vuoi **lista completa** (es: tutti i log)

---

### Q4: Come funziona la relazione User-Log?
**A:** È una relazione **One-to-Many** (1 utente → molti log)

**Definizione in Log:**
```python
class Log:
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='logs')
```

**Cosa fa:**
- `user_id`: Colonna FK che punta a users.id
- `user`: Proprietà Python per accedere all'oggetto User
- `backref='logs'`: Aggiunge automaticamente `user.logs` in User

**Uso:**
```python
# Da Log a User (forward)
log = Log.query.first()
print(log.user.username)  # 'admin'

# Da User a Log (backref)
user = User.query.first()
print(len(user.logs))  # 150
for log in user.logs:
    print(log.type)
```

**In SQL equivalente:**
```sql
-- Forward: Log -> User
SELECT users.username 
FROM logs 
JOIN users ON logs.user_id = users.id 
WHERE logs.id = 1;

-- Backref: User -> Logs
SELECT logs.* 
FROM logs 
WHERE logs.user_id = 1;
```

---

### Q5: Perché `nullable=True` in user_id del Log?
**A:** Perché **alcuni eventi non hanno utente associato**.

**Esempi:**
- `LOGIN_FAILED`: Utente non esiste ancora → `user_id = None`
- `PAGE_NOT_FOUND`: Potrebbe essere visitatore anonimo → `user_id = None`
- `LOGIN_SUCCESS`: Utente autenticato → `user_id = 5`

```python
# Log senza utente (anonimo)
create_log(ip='192.168.1.1', log_type='PAGE_NOT_FOUND', user=None)

# Log con utente
create_log(ip='192.168.1.1', log_type='LOGOUT', user=current_user)
```

---

## SICUREZZA E VALIDAZIONE

### Q6: Perché usiamo regex per validazione invece di librerie?
**A:** Controllo granulare + comprensione profonda degli attacchi.

**Pro regex custom:**
- Impari ESATTAMENTE cosa stai bloccando
- Controllo totale sui pattern
- Nessuna dipendenza esterna
- Performance migliori (meno overhead)

**Con regex:**
```python
r"(\bOR\b|\bAND\b)\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?"
# Blocca: OR 1=1, AND 1=1, OR '1'='1', AND "1"="1"
```

**Libreria generica:**
```python
# Potrebbe bloccare troppo (falsi positivi)
# Oppure troppo poco (falsi negativi)
```

---

### Q7: Cosa significa `re.IGNORECASE`?
**A:** Ignora maiuscole/minuscole nel match regex.

**Senza IGNORECASE:**
```python
re.search(r"SELECT", "select * from users")  # NO MATCH
re.search(r"SELECT", "SELECT * from users")  # MATCH
```

**Con IGNORECASE:**
```python
re.search(r"SELECT", "select * from users", re.IGNORECASE)  # MATCH
re.search(r"SELECT", "SeLeCt * from users", re.IGNORECASE)  # MATCH
re.search(r"SELECT", "SELECT * from users", re.IGNORECASE)  # MATCH
```

**Perché serve:**
Attaccanti usano trucchi:
- `SeLeCt` invece di `SELECT`
- `uNiOn` invece di `UNION`
- `oR` invece di `OR`

---

### Q8: Differenza tra validate() e validate_sql_only()?
**A:** 
- `validate()`: Controlla **TUTTI** gli attacchi (SQL, XSS, CMD, PATH)
- `validate_sql_only()`: Solo **SQL Injection** (più veloce)

**Quando usare validate_sql_only():**
```python
# Login/Register: solo SQL Injection possibile
username = request.form.get('username')
validation = InputValidator.validate_sql_only(username, 'username')
```

**Quando usare validate():**
```python
# Form contatto: possibile XSS, CMD, PATH
messaggio = request.form.get('messaggio')
validation = InputValidator.validate(messaggio, 'messaggio')
```

**Performance:**
- `validate()`: controlla ~45 pattern
- `validate_sql_only()`: controlla ~13 pattern
- **3x più veloce** per login/register

---

### Q9: Perché bcrypt è migliore di SHA256?
**A:** Bcrypt è **lento by design**, SHA256 è velocissimo.

**Confronto:**

| Algoritmo | Hash/secondo | Brute Force | Salt |
|-----------|-------------|-------------|------|
| SHA256    | 1 miliardo  | Facile      | Manuale |
| bcrypt    | 10.000      | Impossibile | Automatico |

**Esempio attacco:**
```
Password da craccare: "password123"

Con SHA256:
- Attaccante prova 1 miliardo password/sec
- Trova "password123" in ~1 secondo

Con bcrypt:
- Attaccante prova 10.000 password/sec
- Trova "password123" in ~3 ore
- Password complessa (16 char)? ANNI
```

**Bcrypt ha "cost factor":**
```python
bcrypt.generate_password_hash(password, rounds=12)
# rounds=12 -> 2^12 = 4096 iterazioni
# rounds=14 -> 2^14 = 16384 iterazioni (più lento ma più sicuro)
```

---

### Q10: Un attaccante può bypassare la validazione?
**A:** Difficile ma non impossibile. Nessun sistema è 100% sicuro.

**Difese multiple (Defense in Depth):**
1. **Validazione input** (prima linea)
2. **Prepared statements** SQLAlchemy (previene SQL injection)
3. **Escaping HTML** Jinja2 (previene XSS)
4. **HTTPS** (previene sniffing)
5. **Rate limiting** (previene brute force)

**Esempio:**
```python
# Anche se validazione fallisce (bug regex)...
username = "admin' OR '1'='1"  # Passa validazione (ipotesi)

# ...SQLAlchemy usa prepared statements:
User.query.filter_by(username=username).first()
# SQL generato:
# SELECT * FROM users WHERE username = ?
# Parametri: ["admin' OR '1'='1"]
# -> Cerca letteralmente utente "admin' OR '1'='1" (non esiste)
# -> Nessun danno!
```

---

## FLASK E ROUTING

### Q11: Come funziona @login_required?
**A:** È un **decorator** che controlla se utente è autenticato.

**Senza decorator:**
```python
@app.route('/account')
def account():
    if not current_user.is_authenticated:
        return redirect('/login')
    # ... resto del codice
```

**Con decorator:**
```python
@app.route('/account')
@login_required  # Fa controllo automaticamente
def account():
    # Codice eseguito SOLO se autenticato
    return render_template('account.html')
```

**Cosa fa internamente:**
```python
# Semplificazione di come funziona
def login_required(func):
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)  # Esegui funzione
        else:
            flash('Devi fare login', 'error')
            return redirect('/login')
    return wrapper
```

---

### Q12: Differenza tra request.form e request.args?
**A:**
- `request.form`: Dati da **POST** (form submission)
- `request.args`: Dati da **GET** (URL query string)

**Esempi:**

```html
<!-- POST (request.form) -->
<form method="POST" action="/login">
    <input name="username" value="admin">
    <input name="password" value="123">
</form>

<!-- Python -->
username = request.form.get('username')  # 'admin'
password = request.form.get('password')  # '123'
```

```html
<!-- GET (request.args) -->
<a href="/logs?type=LOGIN_SUCCESS&ip=192.168.1.1">Filtra</a>

<!-- Python -->
log_type = request.args.get('type')  # 'LOGIN_SUCCESS'
ip = request.args.get('ip')          # '192.168.1.1'
```

**Sicurezza:**
- POST: Dati NON visibili in URL (meglio per password)
- GET: Dati visibili in URL (OK per filtri, ricerche)

---

### Q13: Come Flask sa quale template renderizzare?
**A:** Usa convenzione **templates/** folder.

**Struttura:**
```
ProjectWorkGroup3/
├── app.py
└── templates/
    ├── home.html
    └── login.html
```

**In app.py:**
```python
from flask import render_template

@app.route('/')
def home():
    return render_template('home.html')  # Cerca in templates/home.html
```

**Con subfolder:**
```
templates/
├── auth/
│   ├── login.html
│   └── register.html
└── admin/
    └── logs.html
```

```python
render_template('auth/login.html')    # templates/auth/login.html
render_template('admin/logs.html')    # templates/admin/logs.html
```

---

### Q14: Cosa fa flash() e come funziona?
**A:** Mostra messaggi temporanei all'utente (salvati in sessione).

**In route Python:**
```python
@app.route('/login', methods=['POST'])
def login():
    if password_sbagliata:
        flash('Password errata!', 'error')  # Categoria: error
        return redirect('/login')
    
    flash('Login riuscito!', 'success')  # Categoria: success
    return redirect('/account')
```

**In template HTML:**
```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
        <div class="alert alert-{{ category }}">
            {{ message }}
        </div>
    {% endfor %}
{% endwith %}
```

**Rendering:**
```html
<!-- Se login fallito -->
<div class="alert alert-error">Password errata!</div>

<!-- Se login riuscito -->
<div class="alert alert-success">Login riuscito!</div>
```

**Importante:** Flash message viene **rimosso dopo la prima visualizzazione** (una sola volta).

---

### Q15: Perché abort(403) invece di return redirect()?
**A:** 
- `abort(403)`: Errore **HTTP Forbidden** (blocco duro)
- `redirect()`: Reindirizzamento (soft)

**Esempio:**
```python
@app.route('/logs')
@login_required
def logs():
    # Utente loggato ma NON admin
    if not current_user.is_admin:
        abort(403)  # STOP! Forbidden
        # Non esegue codice sotto
    
    # Questo codice SOLO se admin
    logs = Log.query.all()
    return render_template('logs.html', logs=logs)
```

**Con redirect invece:**
```python
if not current_user.is_admin:
    flash('Accesso negato', 'error')
    return redirect('/account')  # Reindirizza a pagina sicura
```

**Quale usare:**
- `abort(403)`: Per errori di **autorizzazione** (non hai permesso)
- `redirect()`: Per flussi **normali** (es: dopo login vai a /account)

---

## FRONTEND E JAVASCRIPT

### Q16: Come funziona {{ logs_json | tojson }}?
**A:** Jinja2 converte oggetti Python in JSON per JavaScript.

**In Python (app.py):**
```python
logs_json = [
    {'id': 1, 'type': 'LOGIN_SUCCESS', 'ip': '192.168.1.1'},
    {'id': 2, 'type': 'LOGOUT', 'ip': '192.168.1.2'}
]
return render_template('logs.html', logs_json=logs_json)
```

**In Template (logs.html):**
```html
<script>
    const logs = {{ logs_json | tojson }};
    console.log(logs);
</script>
```

**HTML generato (view source):**
```html
<script>
    const logs = [
        {"id": 1, "type": "LOGIN_SUCCESS", "ip": "192.168.1.1"},
        {"id": 2, "type": "LOGOUT", "ip": "192.168.1.2"}
    ];
    console.log(logs);
</script>
```

**Senza `| tojson`:** Error! (oggetto Python non valido in JavaScript)

---

### Q17: Come Chart.js riceve i dati?
**A:** Da array JavaScript (che viene da Flask tramite tojson).

**Flusso completo:**
```
1. Flask (Python)
   logs = Log.query.all()  # Query DB
   ↓
2. Serializzazione
   logs_json = [log.to_dict() for log in logs]
   ↓
3. Template rendering
   {{ logs_json | tojson }}
   ↓
4. JavaScript riceve
   const logs = [...];  // Array JavaScript
   ↓
5. Chart.js processa
   const logTypes = logs.map(log => log.type);
   const counts = {...};
   ↓
6. Crea grafico
   new Chart(ctx, { data: { labels: ..., datasets: [...] } });
```

---

### Q18: Cosa fa .reduce() in JavaScript?
**A:** **Riduce** array a singolo valore (accumula).

**Esempio conta occorrenze:**
```javascript
const logs = [
    {type: 'LOGIN_SUCCESS'},
    {type: 'LOGOUT'},
    {type: 'LOGIN_SUCCESS'},
    {type: 'LOGIN_FAILED'}
];

const counts = logs.reduce((acc, log) => {
    acc[log.type] = (acc[log.type] || 0) + 1;
    return acc;
}, {});

// Risultato:
// {
//     'LOGIN_SUCCESS': 2,
//     'LOGOUT': 1,
//     'LOGIN_FAILED': 1
// }
```

**Step by step:**
```
Iterazione 1:
  acc = {}
  log.type = 'LOGIN_SUCCESS'
  acc['LOGIN_SUCCESS'] = (undefined || 0) + 1 = 1
  acc = {'LOGIN_SUCCESS': 1}

Iterazione 2:
  acc = {'LOGIN_SUCCESS': 1}
  log.type = 'LOGOUT'
  acc['LOGOUT'] = (undefined || 0) + 1 = 1
  acc = {'LOGIN_SUCCESS': 1, 'LOGOUT': 1}

Iterazione 3:
  acc = {'LOGIN_SUCCESS': 1, 'LOGOUT': 1}
  log.type = 'LOGIN_SUCCESS'
  acc['LOGIN_SUCCESS'] = (1 || 0) + 1 = 2
  acc = {'LOGIN_SUCCESS': 2, 'LOGOUT': 1}

Iterazione 4:
  acc = {'LOGIN_SUCCESS': 2, 'LOGOUT': 1}
  log.type = 'LOGIN_FAILED'
  acc['LOGIN_FAILED'] = (undefined || 0) + 1 = 1
  acc = {'LOGIN_SUCCESS': 2, 'LOGOUT': 1, 'LOGIN_FAILED': 1}
```

---

## DEBUGGING E ERRORI

### Q19: "OperationalError: no such table: users" - Come risolvere?
**A:** Database non creato o non inizializzato.

**Soluzione:**
```bash
# 1. Ricrea database
python recreate_db.py

# 2. Oppure usa Python interattivo
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
...     print("Database creato!")

# 3. Verifica
sqlite3 instance/users.db
> .tables  # Deve mostrare: users, logs
> .quit
```

---

### Q20: "TypeError: Object of type datetime is not JSON serializable"
**A:** Devi convertire datetime in stringa prima di passarlo a JSON.

**Errore:**
```python
log = Log.query.first()
return jsonify(log)  # ERROR!
```

**Soluzione:**
```python
log = Log.query.first()
log_dict = {
    'id': log.id,
    'timestamp': log.timestamp.isoformat(),  # datetime -> string
    'type': log.type,
    'ip': log.ip
}
return jsonify(log_dict)  # OK!
```

**Per lista:**
```python
logs = Log.query.all()
logs_json = [{
    'id': log.id,
    'timestamp': log.timestamp.isoformat(),
    'type': log.type
} for log in logs]
return jsonify(logs_json)
```

---

### Q21: Pagina bianca senza errori - Come debuggare?
**A:** 

**1. Controlla console browser (F12):**
```
- Errori JavaScript?
- Richieste fallite (404, 500)?
```

**2. Controlla console Flask:**
```
- Errori Python?
- Traceback?
```

**3. Aggiungi debug print:**
```python
@app.route('/logs')
def logs():
    print("DEBUG: Route /logs chiamata")
    logs = Log.query.all()
    print(f"DEBUG: Trovati {len(logs)} log")
    return render_template('logs.html', logs=logs)
```

**4. Abilita debug mode:**
```python
if __name__ == '__main__':
    app.run(debug=True)  # Mostra errori dettagliati
```

---

### Q22: "werkzeug.routing.exceptions.BuildError" - Perché?
**A:** Route o file static non trovato.

**Errore comune:**
```python
# Template
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">

# Ma file si chiama styles.css (non style.css)
```

**Verifica:**
```bash
ls static/
# Output: styles.css  <- nome corretto

# Fix in template:
<link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
```

---

**Hai altre domande? Aggiungi qui! 💡**
