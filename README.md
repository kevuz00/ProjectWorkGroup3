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

### 1. Attiva l'ambiente virtuale
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 2. Installa le dipendenze (se necessario)
```bash
pip install flask flask-login flask-sqlalchemy flask-bcrypt
```

### 3. Avvia l'applicazione
```bash
python app.py
```

### 4. Accedi all'app
Apri il browser su: **http://127.0.0.1:5000**

---

## 📊 Database

### Tabella `users`
| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id | Integer | Primary Key |
| username | String(80) | Username univoco |
| password | String(200) | Password hashata (bcrypt) |
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
| Accesso pagina home | `PAGE_ACCESS` | ❌ False |
| Accesso pagina logs | `PAGE_ACCESS_LOGS` | ❌ False |

---

## 🎯 Funzionalità Principali

### 1. Autenticazione
- ✅ Registrazione nuovi utenti
- ✅ Login con username e password
- ✅ Password hashate con bcrypt
- ✅ Sessioni gestite con Flask-Login
- ✅ Logout sicuro

### 2. Logging Automatico
- ✅ Ogni evento viene salvato nel database
- ✅ Tracciamento IP address
- ✅ Timestamp preciso
- ✅ Associazione con utente (quando applicabile)

### 3. Dashboard Log
- ✅ Visualizzazione ultimi 100 eventi
- ✅ Statistiche in tempo reale:
  - Totale eventi
  - Login riusciti
  - Login falliti
  - Errori totali
- ✅ Tabella interattiva con filtri visivi

---

## 🔐 Sicurezza

### Implementato:
✅ Password hashate con bcrypt  
✅ Protezione route con `@login_required`  
✅ Validazione form base  
✅ Sessioni sicure Flask-Login  
✅ Logging completo eventi

### Da Implementare (Future):
⚠️ Rate limiting (protezione brute force)  
⚠️ HTTPS in produzione  
⚠️ CSRF protection  
⚠️ Validazione avanzata con Pydantic  
⚠️ Alert automatici su eventi sospetti  
⚠️ Analisi pattern con ML  

---

## 🛠️ Utility Scripts

### Ricreare il Database
```bash
python recreate_db.py
```
⚠️ **ATTENZIONE**: Questo elimina tutti i dati esistenti!

---

## 📚 API / Routes

| Route | Metodi | Descrizione | Autenticazione |
|-------|--------|-------------|----------------|
| `/` | GET | Redirect a login o home | No |
| `/login` | GET, POST | Pagina di login | No |
| `/register` | GET, POST | Registrazione | No |
| `/home` | GET | Pagina principale | ✅ Richiesta |
| `/logout` | GET | Logout | ✅ Richiesta |
| `/logs` | GET | Dashboard log | ✅ Richiesta |

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

- [ ] Implementare Pydantic per validazione
- [ ] Aggiungere campo `severity` ai log (INFO, WARNING, CRITICAL)
- [ ] Creare sistema di alert automatici
- [ ] Implementare analisi brute-force detection
- [ ] Dashboard con grafici temporali
- [ ] Export log in CSV/JSON
- [ ] API REST per integrazione esterna

---

## 👥 Autori

ProjectWorkGroup3

---

## 📄 Licenza

Progetto educativo ITS
