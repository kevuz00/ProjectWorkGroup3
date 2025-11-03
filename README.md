# 🔒 SIEM Flask Application

Sistema di **Security Information and Event Management** (SIEM) base sviluppato con Flask.

## 📋 Descrizione

Applicazione web Python che implementa:
- Sistema di autenticazione (login/registrazione)
- Logging automatico degli eventi di sicurezza
- Dashboard per visualizzazione e analisi dei log
- Database SQLite per utenti e log

---

## 🏗️ Struttura del Progetto

```
ProjectWorkGroup3/
├── app.py                      # Applicazione Flask principale
├── recreate_db.py              # Script per ricreare il database
│
├── model/                      # Modelli del database
│   ├── __init__.py            # Inizializzazione db e bcrypt
│   ├── user.py                # Modello User + CRUD operations
│   └── log.py                 # Modello Log + CRUD operations
│
├── templates/                  # Template HTML (Jinja2)
│   ├── login.html             # Pagina di login
│   ├── register.html          # Pagina di registrazione
│   ├── home.html              # Pagina home (protetta)
│   └── logs.html              # Dashboard log di sicurezza
│
├── static/                     # File statici
│   └── style.css              # Stili CSS
│
├── instance/                   # Database (generato automaticamente)
│   └── users.db               # SQLite database
│
└── .venv/                      # Virtual environment Python
```

---

## 📦 Dipendenze

```
Flask==3.0.0
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
Flask-Bcrypt==1.0.1
```

---

## 🚀 Installazione e Avvio

### 1. Clona il repository (o scarica il progetto)
```bash
git clone https://github.com/kevuz00/ProjectWorkGroup3.git
cd ProjectWorkGroup3
```

### 2. Crea e attiva l'ambiente virtuale
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installa le dipendenze
```bash
pip install -r requirements.txt
```

### 4. Avvia l'applicazione
```bash
python app.py
```
> **Nota:** Il database viene creato automaticamente al primo avvio, insieme all'account admin!

### 5. Accedi all'app
Apri il browser su: **http://127.0.0.1:5000**

### 6. Login
**Account Admin predefinito:**
- Username: `admin`
- Password: `Admin123!`

**Oppure registra un nuovo account** dalla pagina `/register`

---

## 📊 Database

### Tabella `users`
| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id | Integer | Primary Key |
| username | String(80) | Username univoco |
| password | String(200) | Password hashata (bcrypt) |
| is_admin | Boolean | Flag amministratore |
| created_at | DateTime | Data registrazione |

### Tabella `logs`
| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id | Integer | Primary Key |
| ip | String(45) | Indirizzo IP (IPv4/IPv6) |
| type | String(50) | Tipo evento (LOGIN_SUCCESS, ecc.) |
| timestamp | DateTime | Momento dell'evento |
| is_error | Boolean | Flag errore |
| user_id | Integer | Foreign Key → users.id |

---

## 📝 Eventi Loggati

L'applicazione logga automaticamente:

| Evento | Tipo Log | is_error |
|--------|----------|----------|
| Login riuscito | `LOGIN_SUCCESS` | ❌ False |
| Login fallito | `LOGIN_FAILED` | ✅ True |
| Registrazione | `REGISTER_SUCCESS` | ❌ False |
| Logout | `LOGOUT` | ❌ False |
| Cambio password OK | `PASSWORD_CHANGE_SUCCESS` | ❌ False |
| Cambio password KO | `PASSWORD_CHANGE_FAILED` | ✅ True |
| Account eliminato | `ACCOUNT_DELETED` | ❌ False |
| Eliminazione KO | `ACCOUNT_DELETE_FAILED` | ✅ True |
| Accesso home | `PAGE_ACCESS` | ❌ False |
| Accesso logs | `PAGE_ACCESS_LOGS` | ❌ False |
| Form contatto | `CONTACT_FORM_SUCCESS` | ❌ False |
| SQL Injection | `MALICIOUS_INPUT_SQL_INJECTION` | ✅ True |
| XSS | `MALICIOUS_INPUT_XSS` | ✅ True |
| Command Injection | `MALICIOUS_INPUT_COMMAND_INJECTION` | ✅ True |
| Path Traversal | `MALICIOUS_INPUT_PATH_TRAVERSAL` | ✅ True |

---

## 🎯 Funzionalità Principali

### 1. Autenticazione
- ✅ Registrazione nuovi utenti con validazione password
- ✅ Login con username e password
- ✅ Password hashate con bcrypt
- ✅ Sessioni gestite con Flask-Login
- ✅ Logout sicuro
- ✅ Cambio password
- ✅ Eliminazione account

### 2. Logging Automatico
- ✅ Ogni evento viene salvato nel database
- ✅ Tracciamento IP address
- ✅ Timestamp preciso
- ✅ Associazione con utente (quando applicabile)
- ✅ 15+ tipi di eventi diversi

### 3. Dashboard Log (Solo Admin)
- ✅ Visualizzazione ultimi 200 eventi
- ✅ Statistiche in tempo reale:
  - Totale eventi
  - Login riusciti
  - Login falliti
  - Errori totali
- ✅ **3 Grafici interattivi** (Chart.js):
  - Distribuzione tipi di log (torta)
  - Top 10 IP più attivi (barre)
  - Attività per ora del giorno (linee)
- ✅ **Filtri avanzati**:
  - Per tipo evento
  - Per IP address
  - Per username
  - Per data
  - Solo errori/successi
- ✅ **Legenda completa** tipi di log (espandibile)
- ✅ **Sistema di alert automatici**:
  - Brute force detection
  - IP sospetti (troppi errori)
  - Attacchi rilevati (SQL Injection, XSS, ecc.)

### 4. Sicurezza Input
- ✅ Rilevamento SQL Injection
- ✅ Rilevamento XSS (Cross-Site Scripting)
- ✅ Rilevamento Command Injection
- ✅ Rilevamento Path Traversal
- ✅ Tutti i tentativi di attacco vengono loggati

### 5. E-commerce Fake
- ✅ Homepage con 8 prodotti
- ✅ Form contatto
- ✅ Pagine privacy e termini

---

## 🔐 Sicurezza

### Implementato:
✅ Password hashate con bcrypt  
✅ Protezione route con `@login_required`  
✅ Validazione input mallevoli (SQL Injection, XSS, Command Injection, Path Traversal)  
✅ Sessioni sicure Flask-Login  
✅ Logging completo eventi di sicurezza  
✅ Dashboard con grafici (Chart.js)  
✅ Sistema di alert automatici (brute force, IP sospetti)  
✅ Filtri avanzati per log  

### Da Implementare (Future):
⚠️ Rate limiting più aggressivo  
⚠️ HTTPS in produzione  
⚠️ CSRF protection  
⚠️ Export log (CSV/JSON)  
⚠️ Analisi predittiva con ML  

---

## 🛠️ Utility Scripts

### Ricreare il Database (opzionale)
```bash
python recreate_db.py
```
⚠️ **ATTENZIONE**: Questo elimina tutti i dati esistenti e ricrea il database da zero!

> **Nota:** Non necessario al primo avvio - il database viene creato automaticamente da `app.py`

---

## 📚 API / Routes

| Route | Metodi | Descrizione | Autenticazione |
|-------|--------|-------------|----------------|
| `/` | GET | Redirect a login o home | No |
| `/login` | GET, POST | Pagina di login | No |
| `/register` | GET, POST | Registrazione | No |
| `/home` | GET | Pagina principale (e-shop) | No |
| `/contact` | POST | Invio form contatto | No |
| `/account` | GET | Gestione account utente | ✅ Richiesta |
| `/account/change-password` | POST | Cambio password | ✅ Richiesta |
| `/account/delete` | GET | Eliminazione account | ✅ Richiesta |
| `/logout` | GET | Logout | ✅ Richiesta |
| `/logs` | GET | Dashboard log (ADMIN ONLY) | ✅ Richiesta + Admin |
| `/privacy` | GET | Privacy policy | No |
| `/terms` | GET | Termini e condizioni | No |

---

## 🧪 Testing

### Test Manuale
1. Registra un nuovo utente
2. Prova a fare login con password errata (verrà loggato)
3. Fai login corretto
4. Accedi alla dashboard `/logs`
5. Verifica che tutti gli eventi siano registrati

---

## 📈 Prossimi Sviluppi

- [ ] Export log in CSV/JSON
- [ ] API REST per integrazione esterna
- [ ] Implementare CSRF protection
- [ ] Dashboard utente (non-admin) con statistiche personali
- [ ] Sistema di notifiche email per alert critici
- [ ] Analisi predittiva con Machine Learning

---

## 👥 Autori

ProjectWorkGroup3

---

## 📄 Licenza

Progetto educativo ITS
