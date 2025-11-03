# 📝 RIASSUNTO SEMPLICE DEL PROGETTO

> Spiegazione base del Security SIEM Project - senza complicazioni!

---

## 🎯 COS'È QUESTO PROGETTO?

Un **sito web di sicurezza** che:
1. Permette a utenti di registrarsi e fare login
2. **Traccia TUTTO** quello che succede (log di sicurezza)
3. **Blocca attacchi** tipo SQL Injection, XSS, ecc.
4. Mostra una **dashboard** con grafici per vedere gli attacchi

**In pratica:** È come un sistema di videosorveglianza, ma per un sito web.

---

## 📁 FILE PRINCIPALI

### **app.py** - Il cervello
- Gestisce tutte le pagine (/, /login, /register, /account, /logs)
- Controlla chi può accedere dove
- Salva log di ogni azione

### **model/** - I dati
- `user.py`: Utenti (username, password hash)
- `log.py`: Log eventi (cosa è successo, quando, da quale IP)
- `validator.py`: Controlla se input è malevolo
- `password_validator.py`: Controlla se password è forte
- `analyzer.py`: Analizza log per trovare attacchi

### **templates/** - Le pagine HTML
- `home.html`: Homepage con prodotti
- `login.html`: Pagina di login
- `register.html`: Registrazione
- `account.html`: Gestione account utente
- `logs.html`: Dashboard admin con grafici (solo per admin)
- `404.html`, `500.html`: Pagine errore

### **static/styles.css** - Gli stili
- Dark theme (sfondo nero, testi chiari)
- Colore principale: arancione (#f59e0b)

---

## 🔄 COME FUNZIONA (SEMPLIFICATO)

### **1. Registrazione:**
```
Utente compila form → 
Password viene controllata (forte?) → 
Password viene "hashata" con bcrypt (non salvata in chiaro!) → 
Utente salvato nel database → 
Log: REGISTER_SUCCESS
```

### **2. Login:**
```
Utente inserisce username e password → 
Controlla se c'è SQL Injection → 
Cerca utente nel database → 
Verifica password hash → 
Se OK: login riuscito + Log: LOGIN_SUCCESS → 
Se NO: Log: LOGIN_FAILED
```

### **3. Attacco bloccato:**
```
Attaccante prova: username = "admin' OR '1'='1" → 
validator.py controlla con regex → 
Trova pattern SQL Injection → 
BLOCCA richiesta + Log: MALICIOUS_INPUT_SQL_INJECTION → 
Mostra messaggio: "Input sospetto rilevato"
```

### **4. Dashboard Admin:**
```
Admin va su /logs → 
Vede tutti i log in tabella → 
Filtra per tipo, IP, data → 
Vede grafici:
  - Torta: tipi di eventi
  - Barre: IP più attivi
  - Linee: attività per ora
```

---

## 🛡️ SICUREZZA (3 CONCETTI BASE)

### **1. Hash delle Password (bcrypt)**
```
Password "MyPass123!" 
  ↓ bcrypt aggiunge SALT random
  ↓ fa hash
  ↓ salva: "$2b$12$abc123xyz..."

NON si può tornare indietro! (hash → password impossibile)
```

**Perché:** Se database rubato, attaccante NON vede password in chiaro.

---

### **2. Validazione Input (regex)**
```python
Input: "admin' OR '1'='1"  # Tentativo SQL Injection
  ↓
Validator controlla pattern:
  Pattern: r"'\s*OR\s*'"
  ↓
MATCH TROVATO! → BLOCCA
```

**Tipi di attacchi bloccati:**
- **SQL Injection**: `' OR 1=1--`, `UNION SELECT`
- **XSS**: `<script>alert('XSS')</script>`
- **Command Injection**: `; rm -rf /`
- **Path Traversal**: `../../etc/passwd`

---

### **3. Log di Tutto**
```python
Ogni azione salva un log:
- Timestamp (quando?)
- IP (da dove?)
- Type (cosa? LOGIN_SUCCESS, LOGOUT, ecc.)
- User (chi? se loggato)
- is_error (True se errore)
```

**Esempio log:**
```
2025-11-03 14:30:25 | 192.168.1.100 | LOGIN_FAILED | admin | ERROR
2025-11-03 14:31:10 | 192.168.1.100 | LOGIN_SUCCESS | admin | OK
2025-11-03 14:35:00 | 192.168.1.100 | LOGOUT | admin | OK
```

---

## 📊 DASHBOARD LOGS (GRAFICI)

### **Grafico 1: Torta - Distribuzione Eventi**
```
LOGIN_SUCCESS: 45%
LOGOUT: 20%
PAGE_ACCESS: 25%
LOGIN_FAILED: 10%
```

### **Grafico 2: Barre - Top 10 IP**
```
192.168.1.100 ████████████ 120 eventi
10.0.0.5      ██████████ 100 eventi
172.16.0.20   ████████ 80 eventi
```

### **Grafico 3: Linee - Attività per Ora**
```
Eventi per ora del giorno:
00:00 - 05:00: pochi
09:00 - 18:00: tanti
18:00 - 24:00: medi
```

---

## 🔍 COMPONENTI CHIAVE

### **Flask** - Framework web
```python
@app.route('/login')  # Quando vai su /login
def login():
    return render_template('login.html')  # Mostra pagina login
```

### **SQLAlchemy** - Database
```python
# Cerca utente
user = User.query.filter_by(username='admin').first()

# Crea log
log = Log(ip='192.168.1.1', type='LOGIN_SUCCESS')
db.session.add(log)
db.session.commit()
```

### **Jinja2** - Template HTML
```html
<h1>Benvenuto {{ current_user.username }}!</h1>
<!-- Se username = "admin", diventa: -->
<h1>Benvenuto admin!</h1>
```

### **Chart.js** - Grafici
```javascript
// Dati da Flask
const logs = [
    {type: 'LOGIN_SUCCESS'},
    {type: 'LOGOUT'}
];

// Crea grafico
new Chart(ctx, {
    type: 'pie',
    data: { labels: ['LOGIN', 'LOGOUT'], ... }
});
```

---

## 📋 TIPI DI LOG (15 TOTALI)

### **Autenticazione (4):**
- `LOGIN_SUCCESS` - Login riuscito
- `LOGIN_FAILED` - Login fallito
- `LOGOUT` - Logout
- `REGISTER_SUCCESS` - Registrazione

### **Account (2):**
- `PASSWORD_CHANGE` - Cambio password
- `ACCOUNT_DELETED` - Account eliminato

### **Pagine (7):**
- `PAGE_ACCESS_HOME` - Visita homepage
- `PAGE_ACCESS_LOGIN` - Visita login
- `PAGE_ACCESS_REGISTER` - Visita register
- `PAGE_ACCESS_ACCOUNT` - Visita account
- `PAGE_ACCESS_LOGS` - Visita dashboard
- `PAGE_NOT_FOUND` - 404 errore
- `INTERNAL_SERVER_ERROR` - 500 errore

### **Attacchi (4):**
- `MALICIOUS_INPUT_SQL_INJECTION` - Tentativo SQL Injection
- `MALICIOUS_INPUT_XSS` - Tentativo XSS
- `MALICIOUS_INPUT_COMMAND_INJECTION` - Tentativo Command Injection
- `MALICIOUS_INPUT_PATH_TRAVERSAL` - Tentativo Path Traversal

---

## 🎨 DARK THEME

```css
Colori principali:
- Sfondo: #121212 (nero)
- Card: #1e1e1e (grigio scuro)
- Testo: #e0e0e0 (grigio chiaro)
- Primary: #f59e0b (arancione)
- Bordi: #333 (grigio medio)
- Errore: #ef4444 (rosso)
- Successo: #10b981 (verde)
```

---

## 🗂️ DATABASE

### **Tabella: users**
| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id | Integer | ID univoco |
| username | String | Nome utente (univoco) |
| password | String | Hash bcrypt (60 char) |
| created_at | DateTime | Data creazione |
| is_admin | Boolean | True se admin |

### **Tabella: logs**
| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id | Integer | ID univoco |
| ip | String | Indirizzo IP |
| type | String | Tipo evento |
| timestamp | DateTime | Quando è successo |
| is_error | Boolean | True se errore |
| user_id | Integer | FK a users (opzionale) |

---

## 🚀 COME USARLO

### **1. Avvia applicazione:**
```bash
python app.py
```

### **2. Apri browser:**
```
http://127.0.0.1:5000
```

### **3. Registrati:**
- Vai su /register
- Scegli username e password forte
- Clicca "Registrati"

### **4. Fai login:**
- Vai su /login
- Inserisci credenziali
- Accedi

### **5. Prova attacco (per test):**
- Vai su /login
- Username: `admin' OR '1'='1`
- Vedi messaggio: "Input sospetto rilevato"
- Se sei admin, vai su /logs e vedi log dell'attacco

### **6. Vedi dashboard (solo admin):**
- Vai su /logs
- Filtra per tipo, IP, data
- Vedi grafici interattivi

---

## 💡 CONCETTI IMPORTANTI (5 COSE DA SAPERE)

### **1. Hash ≠ Encryption**
- **Encryption:** Puoi decifrare (reversibile)
- **Hash:** NON puoi tornare indietro (irreversibile)
- Password usa HASH (bcrypt)

### **2. SQL Injection**
```
Vulnerabile:
query = f"SELECT * FROM users WHERE username='{username}'"

Sicuro:
User.query.filter_by(username=username).first()
```

### **3. Flask-Login**
```python
@login_required  # Solo se loggato
def account():
    print(current_user.username)  # Utente loggato
```

### **4. Relazione Database**
```python
# 1 User → Molti Log
user.logs  # Lista di tutti i log dell'utente
log.user   # Utente che ha generato il log
```

### **5. Chart.js riceve dati da Flask**
```python
# Flask (Python)
logs_json = [{'type': 'LOGIN', 'ip': '192.168.1.1'}]
return render_template('logs.html', logs_json=logs_json)

# Template (HTML + JS)
const logs = {{ logs_json | tojson }};
// Ora logs è array JavaScript utilizzabile da Chart.js
```

---

## 🎯 FLUSSO COMPLETO (ESEMPIO LOGIN)

```
1. Browser → GET /login
   ↓
2. Flask → render_template('login.html')
   ↓
3. Browser mostra form login
   ↓
4. Utente compila e clicca "Login"
   ↓
5. Browser → POST /login (username + password)
   ↓
6. Flask → Valida input (SQL Injection?)
   ↓
7. Flask → Cerca user nel DB
   ↓
8. Flask → Verifica password hash
   ↓
9. Se OK:
   - login_user(user) → Crea sessione
   - create_log(ip, 'LOGIN_SUCCESS', user)
   - redirect('/account')
   
   Se NO:
   - create_log(ip, 'LOGIN_FAILED', is_error=True)
   - flash('Credenziali non valide')
   - redirect('/login')
```

---

## 📚 FILE DI STUDIO (SCEGLI IN BASE AL LIVELLO)

### **PRINCIPIANTE (INIZI ORA):**
👉 **Leggi solo questo file** (RIASSUNTO_SEMPLICE.md)

### **INTERMEDIO (HAI CAPITO LE BASI):**
- GUIDA_STUDIO_COMPLETA.md (più dettagliata)
- ESERCIZI_PRATICI.md (livelli 1-4)

### **AVANZATO (VUOI PADRONEGGIARE TUTTO):**
- Tutti i file in INDICE_STUDIO.md
- ESERCIZI_PRATICI.md (livelli 5-8)
- DOMANDE_FREQUENTI.md
- GLOSSARIO_TECNICO.md

---

## ✅ CHECKLIST MINIMA (HAI CAPITO?)

Segna [x] se sai rispondere:

- [ ] Cosa fa app.py?
- [ ] Dove sono salvati gli utenti?
- [ ] Cos'è un hash password?
- [ ] Cosa fa validator.py?
- [ ] Cos'è SQL Injection?
- [ ] Come si fa login?
- [ ] Cosa contiene un log?
- [ ] A cosa serve la dashboard /logs?
- [ ] Chi può vedere /logs? (solo admin)
- [ ] Quanti tipi di log ci sono? (15)

**Se hai risposto SÌ a tutto → Hai capito il progetto! 🎉**

---

## 🔑 IN SINTESI (3 FRASI)

1. **Progetto web** con login/registrazione che **traccia tutto** in log
2. **Blocca attacchi** (SQL Injection, XSS, ecc.) validando input con regex
3. **Dashboard admin** mostra grafici e statistiche di sicurezza

**FINE! Questo è tutto quello che ti serve sapere per iniziare! 🚀**
