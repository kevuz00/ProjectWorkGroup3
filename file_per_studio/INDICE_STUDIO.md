# 🎓 INDICE MATERIALI DI STUDIO

> **Percorso completo per padroneggiare il Security SIEM Project**

---

## 📚 MATERIALI DISPONIBILI

### 1. 📖 **GUIDA_STUDIO_COMPLETA.md** ⭐ INIZIA DA QUI
**Cosa contiene:**
- Architettura completa del progetto
- Flusso di esecuzione step-by-step
- Spiegazione dettagliata di ogni componente
- Database, modelli, sicurezza, routing
- Frontend (Chart.js, CSS, JavaScript)
- Testing e debugging

**Quando usarla:**
- Prima lettura per comprendere TUTTO il progetto
- Riferimento durante sviluppo
- Ripasso concetti generali

**Tempo stimato:** 2-3 ore di lettura

---

### 2. 🎯 **ESERCIZI_PRATICI.md** ⭐ LEARNING BY DOING
**Cosa contiene:**
- 8 livelli progressivi di esercizi (fondamenti → avanzato)
- 25+ esercizi pratici con soluzioni guidate
- Sfide di programmazione
- Checklist completamento

**Livelli:**
1. **Fondamenti** - Database, log, password validation
2. **SQL Injection** - Pattern, testing, analisi
3. **XSS e Attacchi** - Cross-site scripting, command injection
4. **Database** - Query SQLAlchemy, aggregazioni, JOIN
5. **Security Analyzer** - Brute force, analisi log
6. **Frontend** - Chart.js, JavaScript, CSS
7. **Sfide Avanzate** - LDAP injection, export CSV, real-time
8. **Security Hardening** - Rate limiting, CSRF, password strength

**Quando usarla:**
- Dopo aver letto GUIDA_STUDIO_COMPLETA
- Per mettere in pratica concetti teorici
- Per verificare comprensione

**Tempo stimato:** 5-10 ore totali

---

### 3. ❓ **DOMANDE_FREQUENTI.md** ⭐ RISOLVI DUBBI
**Cosa contiene:**
- 22+ domande con risposte dettagliate
- Spiegazioni approfondite di concetti complessi
- Esempi pratici ed errori comuni

**Sezioni:**
1. **Database e SQLAlchemy** (Q1-Q5)
   - Bcrypt, commit(), first() vs all(), relazioni, nullable
2. **Sicurezza e Validazione** (Q6-Q10)
   - Regex, IGNORECASE, validate(), bcrypt vs SHA256, bypass
3. **Flask e Routing** (Q11-Q15)
   - @login_required, request.form vs args, template, flash, abort
4. **Frontend e JavaScript** (Q16-Q18)
   - tojson, Chart.js, reduce()
5. **Debugging e Errori** (Q19-Q22)
   - No such table, JSON serializable, pagina bianca, BuildError

**Quando usarla:**
- Quando hai un dubbio specifico
- Per approfondire concetti particolari
- Durante debugging

**Tempo stimato:** Consultazione rapida (5-10 min per domanda)

---

### 4. 📖 **GLOSSARIO_TECNICO.md** ⭐ DIZIONARIO
**Cosa contiene:**
- Definizioni di 60+ termini tecnici
- Spiegazioni semplici con esempi
- Simboli regex spiegati
- Acronimi comuni

**Organizzazione alfabetica:**
- A-Z: Termini tecnici (API, Bcrypt, CRUD, Flask, ORM, XSS, ...)
- Simboli Regex (\b, \d, \s, +, *, ?, |, ^, $, [])
- Acronimi (API, CRUD, CSRF, SQL, XSS, ...)

**Quando usarlo:**
- Quando incontri termine sconosciuto
- Come riferimento rapido
- Tienilo aperto mentre studi!

**Tempo stimato:** Consultazione rapida (1-2 min per termine)

---

### 5. 📄 **FILE ESISTENTI DEL PROGETTO**

#### **STATO_PROGETTO.md**
- Panoramica funzionalità implementate
- Tecnologie utilizzate
- Stato completamento features

#### **GUIDA_ACCOUNT.md**
- Funzionalità pagina account
- Cambio password, eliminazione account
- Sicurezza implementata

#### **GUIDA_FILTRI.md**
- Sistema filtri dashboard logs
- Tipi di filtro (tipo, IP, data, errori)
- Implementazione JavaScript

#### **PROTEZIONE_INPUT_MALEVOLI.md**
- Dettagli validazione input
- Pattern SQL Injection, XSS, Command Injection, Path Traversal
- Esempi e casi d'uso

#### **OTTIMIZZAZIONE_VALIDATOR.md**
- Performance validazione
- Differenza validate() vs validate_sql_only()
- Best practices

---

## 🗺️ PERCORSO DI STUDIO CONSIGLIATO

### 🟢 **FASE 1: COMPRENSIONE (Settimana 1)**

**Giorno 1-2:**
1. Leggi **GUIDA_STUDIO_COMPLETA.md** (sezioni 1-3)
   - Architettura generale
   - Flusso di esecuzione
   - Database e modelli

**Giorno 3-4:**
2. Continua **GUIDA_STUDIO_COMPLETA.md** (sezioni 4-6)
   - Sistema sicurezza
   - Routing e pagine
   - Frontend

**Giorno 5:**
3. Leggi **STATO_PROGETTO.md** per panoramica features

**Giorno 6-7:**
4. Esplora codice con **GLOSSARIO_TECNICO.md** aperto
   - Analizza `app.py`
   - Studia `model/*.py`
   - Esamina `templates/*.html`

---

### 🟡 **FASE 2: PRATICA (Settimana 2-3)**

**Settimana 2:**
1. **ESERCIZI_PRATICI.md** - Livelli 1-4
   - Fondamenti (Esercizi 1.1-1.3)
   - SQL Injection (Esercizi 2.1-2.3)
   - XSS e Attacchi (Esercizi 3.1-3.3)
   - Database (Esercizi 4.1-4.3)

**Settimana 3:**
2. **ESERCIZI_PRATICI.md** - Livelli 5-8
   - Security Analyzer (Esercizi 5.1-5.3)
   - Frontend (Esercizi 6.1-6.3)
   - Sfide Avanzate (Sfide 7.1-7.3)
   - Security Hardening (Sfide 8.1-8.3)

**Durante pratica:**
- Usa **DOMANDE_FREQUENTI.md** per dubbi
- Consulta **GLOSSARIO_TECNICO.md** per termini
- Testa OGNI esercizio nel progetto vero

---

### 🔴 **FASE 3: APPROFONDIMENTO (Settimana 4)**

**Giorno 1-3:**
1. Studia file specifici:
   - **PROTEZIONE_INPUT_MALEVOLI.md** (validazione dettagliata)
   - **OTTIMIZZAZIONE_VALIDATOR.md** (performance)
   - **GUIDA_FILTRI.md** (dashboard logs)
   - **GUIDA_ACCOUNT.md** (gestione utente)

**Giorno 4-5:**
2. Crea funzionalità personalizzata:
   - Nuovo tipo di log
   - Nuovo grafico Chart.js
   - Nuovo analyzer personalizzato

**Giorno 6-7:**
3. Testing completo:
   - Testa TUTTE le funzionalità
   - Prova attacchi SQL/XSS/CMD
   - Verifica grafici e filtri
   - Debug errori

---

## 📊 CHECKLIST COMPETENZE

Segna [x] quando padroneggi:

### **Database e ORM**
- [ ] So creare modelli SQLAlchemy
- [ ] Capisco relazioni One-to-Many
- [ ] Scrivo query con filter, join, group by
- [ ] Gestisco transazioni (commit, rollback)
- [ ] Uso aggregazioni (count, sum, max)

### **Sicurezza**
- [ ] Riconosco SQL Injection
- [ ] Riconosco XSS
- [ ] Riconosco Command Injection
- [ ] Riconosco Path Traversal
- [ ] So come funziona bcrypt
- [ ] Capisco importanza di SALT
- [ ] Implemento validazione input

### **Flask**
- [ ] Creo route GET/POST
- [ ] Uso decorator @login_required
- [ ] Gestisco sessioni
- [ ] Uso flash messages
- [ ] Renderizo template con dati
- [ ] Gestisco errori (404, 500)

### **Frontend**
- [ ] Scrivo template Jinja2
- [ ] Uso variabili {{ }}
- [ ] Uso condizionali {% if %}
- [ ] Uso loop {% for %}
- [ ] Creo grafici Chart.js
- [ ] Scrivo JavaScript base
- [ ] Applico stili CSS

### **Debugging**
- [ ] Uso print() per debug
- [ ] Leggo traceback Python
- [ ] Uso console browser (F12)
- [ ] Risolvo errori database
- [ ] Debug query SQL
- [ ] Fix errori JavaScript

---

## 🎯 OBIETTIVI FINALI

Al termine dello studio, dovresti essere capace di:

1. **Spiegare** ogni riga di codice del progetto
2. **Modificare** funzionalità esistenti
3. **Aggiungere** nuove feature
4. **Riconoscere** vulnerabilità di sicurezza
5. **Debuggare** errori autonomamente
6. **Creare** progetti simili da zero

---

## 💡 SUGGERIMENTI PER LO STUDIO

### ✅ **DA FARE:**
- Leggi codice con **GLOSSARIO** aperto
- Fai **TUTTI** gli esercizi pratici
- **Testa** ogni concetto nel progetto vero
- **Annota** dubbi e cercali nelle FAQ
- **Modifica** codice e osserva effetti
- **Usa** print() per capire flusso
- **Chiedi** se non capisci qualcosa

### ❌ **DA EVITARE:**
- Leggere solo teoria senza praticare
- Saltare esercizi "troppo facili"
- Copiare codice senza capirlo
- Ignorare errori invece di risolverli
- Studiare tutto in un giorno
- Non testare modifiche

---

## 📞 SUPPORTO

### **Hai domande?**
1. Controlla **DOMANDE_FREQUENTI.md**
2. Cerca nel **GLOSSARIO_TECNICO.md**
3. Rileggi sezione in **GUIDA_STUDIO_COMPLETA.md**
4. Prova esercizio in **ESERCIZI_PRATICI.md**
5. Se ancora bloccato: chiedi!

### **Risorse Esterne:**
- Flask Docs: https://flask.palletsprojects.com/
- SQLAlchemy Docs: https://docs.sqlalchemy.org/
- Chart.js Docs: https://www.chartjs.org/
- Regex101 (tester): https://regex101.com/
- Python Docs: https://docs.python.org/3/

---

## 🏆 CERTIFICAZIONE FINALE

**Completa questa sfida per validare la tua competenza:**

### **Progetto Finale**
Crea una nuova funzionalità completa:

1. **Backend:**
   - Nuova route Flask
   - Nuovo modello database (o estendi esistente)
   - Validazione input personalizzata
   - Logging eventi

2. **Frontend:**
   - Nuova pagina HTML
   - Stili CSS custom
   - JavaScript interattivo
   - Grafico Chart.js (opzionale)

3. **Sicurezza:**
   - Protezione contro attacchi
   - Autenticazione richiesta
   - Validazione completa

**Esempio feature:**
- Sistema di commenti ai log (con validazione XSS)
- Export PDF report giornaliero
- API REST per mobile app
- Dashboard statistiche avanzate

---

**Sei pronto? Inizia da GUIDA_STUDIO_COMPLETA.md! 🚀**

**Buono studio!** 📚✨
