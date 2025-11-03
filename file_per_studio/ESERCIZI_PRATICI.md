# 🎯 ESERCIZI PRATICI - Security SIEM Project

## Obiettivo
Questi esercizi ti aiuteranno a **imparare facendo**. Completa ogni esercizio nell'ordine suggerito.

---

## 📚 LIVELLO 1: FONDAMENTI

### Esercizio 1.1: Esplora il Database
**Obiettivo**: Capire la struttura del database

**Passi:**
1. Avvia l'applicazione: `python app.py`
2. Registra 3 utenti diversi
3. Esegui: `python db_utils.py` -> Opzione 1
4. Osserva gli hash delle password (tutti diversi!)
5. Esegui: `python db_utils.py` -> Opzione 2
6. Conta quanti log di tipo REGISTER_SUCCESS ci sono

**Domanda**: Perché 3 password uguali hanno hash diversi?
**Risposta da trovare**: Studia il concetto di SALT in bcrypt

---

### Esercizio 1.2: Analizza un Log
**Obiettivo**: Comprendere struttura modello Log

**Passi:**
1. Apri `model/log.py`
2. Identifica tutti i campi della tabella
3. Trova la relazione con User
4. Apri Python interattivo:
```python
from app import app, db
from model.log import Log

with app.app_context():
    log = Log.query.first()
    print(f"ID: {log.id}")
    print(f"IP: {log.ip}")
    print(f"Type: {log.type}")
    print(f"User: {log.user.username if log.user else 'Anonimo'}")
    print(f"Timestamp: {log.timestamp}")
```

**Domanda**: Cosa stampa se `log.user` è None?

---

### Esercizio 1.3: Testa Validazione Password
**Obiettivo**: Capire requisiti password sicura

**Passi:**
1. Apri `model/password_validator.py`
2. Trova i 5 requisiti principali
3. Testa queste password (vai su /register):
   - `abc123` -> Errori?
   - `ABCabc123` -> Errori?
   - `ABCabc123!` -> Errori?
   - `test` -> Errori?
   - `MySecurePass123!` -> Errori?

**Task**: Scrivi 3 password che PASSANO la validazione

---

## 📚 LIVELLO 2: SQL INJECTION

### Esercizio 2.1: Riconosci Pattern SQL Injection
**Obiettivo**: Identificare tentativi di attacco

**Passi:**
1. Apri `model/validator.py`
2. Studia i `SQL_PATTERNS`
3. Per OGNI pattern, scrivi un esempio di input che lo triggera

**Esempio:**
```
Pattern: r"UNION\s+SELECT"
Input malevolo: "1 UNION SELECT * FROM users"
```

**Task**: Completa per tutti i 13 pattern SQL

---

### Esercizio 2.2: Testa SQL Injection sul Login
**Obiettivo**: Verificare che la protezione funzioni

**Passi:**
1. Vai su http://127.0.0.1:5000/login
2. Prova questi username:
   ```
   admin' OR '1'='1
   ' OR 1=1--
   admin'--
   ' UNION SELECT * FROM users--
   ```
3. Per ognuno, verifica:
   - Viene bloccato? (flash message)
   - Si crea log MALICIOUS_INPUT_SQL_INJECTION?
   - Quale pattern regex ha fatto match?

**Task**: Esegui `python db_utils.py` e conta quanti attacchi SQL hai generato

---

### Esercizio 2.3: Analizza Funzione validate()
**Obiettivo**: Comprendere il flusso di validazione

**Passi:**
1. Apri `model/validator.py`
2. Trova il metodo `validate()`
3. Aggiungi print per debug:
```python
@staticmethod
def validate(input_string, field_name="input"):
    print(f"[DEBUG] Validating: {input_string}")
    
    # Check SQL Injection
    for pattern in InputValidator.SQL_PATTERNS:
        if re.search(pattern, input_upper, re.IGNORECASE):
            print(f"[DEBUG] SQL INJECTION DETECTED! Pattern: {pattern}")
            return {...}
```
4. Riavvia app e prova un attacco SQL
5. Osserva output console

**Domanda**: Perché usiamo `re.IGNORECASE`?

---

## 📚 LIVELLO 3: XSS E ALTRI ATTACCHI

### Esercizio 3.1: Identifica Pattern XSS
**Obiettivo**: Riconoscere Cross-Site Scripting

**Task**: Per ogni pattern XSS, scrivi esempio:
```
Pattern: r"<script[^>]*>"
Input: "<script>alert('XSS')</script>"

Pattern: r"javascript:"
Input: "javascript:alert(document.cookie)"

[... continua per tutti ...]
```

---

### Esercizio 3.2: Testa XSS sul Contact Form
**Obiettivo**: Verificare protezione XSS

**Passi:**
1. Vai su http://127.0.0.1:5000/#contact
2. Nel campo "Messaggio", prova:
   ```
   <script>alert('XSS')</script>
   <img src=x onerror=alert('XSS')>
   javascript:alert(1)
   ```
3. Controlla se vengono bloccati
4. Verifica log con tipo MALICIOUS_INPUT_XSS

**Domanda**: Perché XSS è pericoloso se non bloccato?

---

### Esercizio 3.3: Command Injection
**Obiettivo**: Capire attacchi command injection

**Pattern da studiare:**
```python
r";\s*rm\s+-rf"      # ; rm -rf /
r"&&\s*format"       # && format C:
r"`.*`"              # `whoami`
r"\$\(.*\)"          # $(cat /etc/passwd)
```

**Task**: Scrivi 5 input che triggano questi pattern

---

## 📚 LIVELLO 4: DATABASE E QUERY

### Esercizio 4.1: Query SQLAlchemy Base
**Obiettivo**: Padroneggiare query database

**Apri Python interattivo:**
```python
from app import app, db
from model.user import User
from model.log import Log

with app.app_context():
    # 1. Conta tutti gli utenti
    total_users = User.query.count()
    print(f"Utenti totali: {total_users}")
    
    # 2. Trova utente per username
    admin = User.query.filter_by(username='admin').first()
    print(f"Admin trovato: {admin}")
    
    # 3. Tutti i log di LOGIN_SUCCESS
    logins = Log.query.filter_by(type='LOGIN_SUCCESS').all()
    print(f"Login riusciti: {len(logins)}")
    
    # 4. Log ordinati per data (più recenti)
    recent_logs = Log.query.order_by(Log.timestamp.desc()).limit(5).all()
    for log in recent_logs:
        print(f"{log.timestamp} - {log.type}")
```

**Task**: Scrivi query per:
- Contare log di errore (is_error=True)
- Trovare tutti i log di un utente specifico
- Trovare log delle ultime 24 ore

---

### Esercizio 4.2: Query con Aggregazione
**Obiettivo**: Usare GROUP BY e COUNT

**Query da completare:**
```python
from sqlalchemy import func

with app.app_context():
    # Conta log per tipo
    results = db.session.query(
        Log.type,
        func.count(Log.id).label('total')
    ).group_by(Log.type).all()
    
    for log_type, count in results:
        print(f"{log_type}: {count}")
```

**Task**: Modifica query per:
1. Raggruppa per IP (quali IP hanno più log?)
2. Raggruppa per is_error (quanti errori vs successi?)
3. Raggruppa per user_id (quale utente genera più log?)

---

### Esercizio 4.3: Relazioni e JOIN
**Obiettivo**: Capire relazioni User-Log

**Codice:**
```python
with app.app_context():
    # Trova utente e i suoi log
    user = User.query.filter_by(username='test').first()
    print(f"Utente: {user.username}")
    print(f"Log totali: {len(user.logs)}")
    
    for log in user.logs[:10]:  # Primi 10
        print(f"  - {log.type} @ {log.timestamp}")
```

**Task**: 
- Trova l'utente con più log
- Trova l'utente con più errori
- Stampa ultimo login di ogni utente

---

## 📚 LIVELLO 5: SECURITY ANALYZER

### Esercizio 5.1: Simula Brute Force
**Obiettivo**: Testare rilevamento brute force

**Passi:**
1. Vai su /login
2. Prova login fallito 10 volte consecutive (password errata)
3. Vai su /logs (come admin)
4. Controlla alert "Tentativi di brute force"
5. Verifica il tuo IP nella lista

**Task**: Modifica threshold in `analyzer.py` da 5 a 3 e ri-testa

---

### Esercizio 5.2: Analizza Query Brute Force
**Obiettivo**: Comprendere query complessa

**Apri `model/analyzer.py` -> metodo `detect_brute_force()`**

```python
results = db.session.query(
    Log.ip,
    func.count(Log.id).label('attempts'),
    func.max(Log.timestamp).label('last_attempt')
).filter(
    Log.type == 'LOGIN_FAILED',
    Log.timestamp >= time_threshold
).group_by(Log.ip).all()
```

**Domande:**
1. Cosa fa `func.count(Log.id)`?
2. Perché usiamo `group_by(Log.ip)`?
3. Cosa rappresenta `time_threshold`?
4. Come modificare per cercare ultimi 10 minuti invece di 5?

**Task**: Modifica codice e testa

---

### Esercizio 5.3: Crea Nuovo Analyzer
**Obiettivo**: Scrivere funzione di analisi personalizzata

**Task**: Aggiungi a `SecurityAnalyzer`:
```python
@staticmethod
def detect_suspicious_users(threshold=20):
    """
    Trova utenti con troppi errori
    
    Returns:
        Lista di utenti con errori >= threshold
    """
    # TUO CODICE QUI
    # Suggerimento: usa JOIN tra Log e User
    # Filtra is_error=True
    # Raggruppa per user_id
    # Conta errori per utente
```

**Verifica**: Chiama funzione e stampa risultati

---

## 📚 LIVELLO 6: FRONTEND E CHART.JS

### Esercizio 6.1: Analizza Grafico Pie Chart
**Obiettivo**: Comprendere Chart.js

**Apri `templates/logs.html` -> JavaScript Chart.js**

```javascript
// Trova questa sezione
const logTypes = logs.map(log => log.type);
const typeCounts = logTypes.reduce((acc, type) => {
    acc[type] = (acc[type] || 0) + 1;
    return acc;
}, {});
```

**Domande:**
1. Cosa fa `logs.map(log => log.type)`?
2. Come funziona `reduce()`?
3. Cosa contiene `typeCounts` alla fine?

**Task**: Aggiungi `console.log(typeCounts)` e ispeziona browser console

---

### Esercizio 6.2: Modifica Colori Grafico
**Obiettivo**: Personalizzare Chart.js

**Task:**
1. Trova array `backgroundColor` nel grafico a torta
2. Cambia colori con nuovi codici hex:
   ```javascript
   backgroundColor: [
       '#ff6b6b',  // Rosso
       '#4ecdc4',  // Turchese
       '#45b7d1',  // Blu
       '#f9ca24',  // Giallo
       '#6c5ce7'   // Viola
   ]
   ```
3. Ricarica /logs e osserva cambiamento

---

### Esercizio 6.3: Aggiungi Nuovo Grafico
**Obiettivo**: Creare grafico da zero

**Task**: Aggiungi grafico "Errori vs Successi"
```javascript
// Conta errori
const errorCount = logs.filter(log => log.is_error).length;
const successCount = logs.length - errorCount;

// Crea grafico a barre
const ctx = document.getElementById('errorChart').getContext('2d');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Successi', 'Errori'],
        datasets: [{
            label: 'Numero Eventi',
            data: [successCount, errorCount],
            backgroundColor: ['#10b981', '#ef4444']
        }]
    },
    options: {
        responsive: true
    }
});
```

**Non dimenticare**: Aggiungi `<canvas id="errorChart"></canvas>` in HTML!

---

## 📚 LIVELLO 7: SFIDE AVANZATE

### Sfida 7.1: Nuovo Tipo di Attacco
**Obiettivo**: Estendere sistema di validazione

**Task:**
1. Aggiungi nuovo pattern per **LDAP Injection**:
   ```python
   LDAP_PATTERNS = [
       r"\*\)",           # *)
       r"\(\|",           # (|
       r"\)\(",           # )(
   ]
   ```
2. Modifica `validate()` per controllare anche LDAP
3. Testa con input: `admin*)(`
4. Crea log type: `MALICIOUS_INPUT_LDAP_INJECTION`

---

### Sfida 7.2: Esporta Log in CSV
**Obiettivo**: Aggiungere feature export

**Task:**
1. Crea route `/logs/export`
2. Query tutti i log
3. Genera file CSV con campi: id, timestamp, type, ip, username
4. Usa libreria `csv` di Python
5. Return file con `send_file()`

**Bonus**: Aggiungi filtri (export solo errori, solo date range)

---

### Sfida 7.3: Dashboard Real-time
**Obiettivo**: Aggiornamento automatico log

**Task:**
1. Aggiungi JavaScript in logs.html:
   ```javascript
   setInterval(() => {
       fetch('/api/logs/latest')
           .then(res => res.json())
           .then(data => {
               // Aggiorna tabella senza ricaricare pagina
           });
   }, 5000);  // Ogni 5 secondi
   ```
2. Crea route `/api/logs/latest` che ritorna JSON
3. Testa aprendo /logs in due tab, genera log in uno, osserva aggiornamento nell'altro

---

## 📚 LIVELLO 8: SECURITY HARDENING

### Sfida 8.1: Implementa Rate Limiting
**Obiettivo**: Previeni spam login

**Task:**
1. Installa: `pip install Flask-Limiter`
2. Aggiungi in app.py:
   ```python
   from flask_limiter import Limiter
   
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   
   @app.route('/login', methods=['POST'])
   @limiter.limit("5 per minute")  # Max 5 tentativi/minuto
   def login():
       # ...
   ```
3. Testa: prova 10 login in 1 minuto
4. Deve bloccare dopo il 5°

---

### Sfida 8.2: CSRF Protection
**Obiettivo**: Protezione Cross-Site Request Forgery

**Task:**
1. Installa: `pip install Flask-WTF`
2. Aggiungi CSRF token ai form:
   ```html
   <form method="POST">
       {{ csrf_token() }}
       <input type="text" name="username">
       <!-- ... -->
   </form>
   ```
3. Configura in app.py:
   ```python
   from flask_wtf.csrf import CSRFProtect
   
   app.config['SECRET_KEY'] = 'your-secret-key'
   csrf = CSRFProtect(app)
   ```

---

### Sfida 8.3: Password Strength Meter
**Obiettivo**: Feedback visivo forza password

**Task:**
1. Aggiungi JavaScript in register.html:
   ```javascript
   const passwordInput = document.getElementById('password');
   const strengthMeter = document.getElementById('strength');
   
   passwordInput.addEventListener('input', (e) => {
       const password = e.target.value;
       let strength = 0;
       
       if (password.length >= 8) strength++;
       if (/[A-Z]/.test(password)) strength++;
       if (/[a-z]/.test(password)) strength++;
       if (/\d/.test(password)) strength++;
       if (/[^A-Za-z0-9]/.test(password)) strength++;
       
       strengthMeter.textContent = ['Molto Debole', 'Debole', 'Media', 'Forte', 'Molto Forte'][strength];
   });
   ```
2. Aggiungi `<div id="strength"></div>` sotto input password
3. Colora con CSS (rosso->verde)

---

## 🎓 CHECKLIST COMPLETAMENTO

Segna con [x] quando completi:

**Livello 1 - Fondamenti:**
- [ ] Esercizio 1.1: Esplora Database
- [ ] Esercizio 1.2: Analizza Log
- [ ] Esercizio 1.3: Validazione Password

**Livello 2 - SQL Injection:**
- [ ] Esercizio 2.1: Pattern SQL
- [ ] Esercizio 2.2: Test SQL Injection
- [ ] Esercizio 2.3: Funzione validate()

**Livello 3 - XSS:**
- [ ] Esercizio 3.1: Pattern XSS
- [ ] Esercizio 3.2: Test XSS
- [ ] Esercizio 3.3: Command Injection

**Livello 4 - Database:**
- [ ] Esercizio 4.1: Query Base
- [ ] Esercizio 4.2: Aggregazione
- [ ] Esercizio 4.3: Relazioni

**Livello 5 - Analyzer:**
- [ ] Esercizio 5.1: Brute Force
- [ ] Esercizio 5.2: Query Analyzer
- [ ] Esercizio 5.3: Nuovo Analyzer

**Livello 6 - Frontend:**
- [ ] Esercizio 6.1: Pie Chart
- [ ] Esercizio 6.2: Colori
- [ ] Esercizio 6.3: Nuovo Grafico

**Livello 7 - Sfide:**
- [ ] Sfida 7.1: LDAP Injection
- [ ] Sfida 7.2: Export CSV
- [ ] Sfida 7.3: Real-time

**Livello 8 - Security:**
- [ ] Sfida 8.1: Rate Limiting
- [ ] Sfida 8.2: CSRF Protection
- [ ] Sfida 8.3: Password Strength

---

**Completato tutto? SEI UN PRO! 🏆**
