from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from model import db, bcrypt
from model.user import User, create_user, get_user_by_username, get_user_by_id
from model.log import Log, create_log, get_all_logs, get_error_logs
from model.analyzer import SecurityAnalyzer
from model.validator import InputValidator
from model.password_validator import PasswordValidator
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'chiave-segreta-da-cambiare-in-produzione'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Devi effettuare il login per accedere a questa pagina.'


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


def ensure_admin_user():
    """Crea automaticamente l'utente admin se non esiste"""
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD', 'Admin123!')
    
    admin = get_user_by_username(admin_username)
    if not admin:
        try:
            create_user(admin_username, admin_password, is_admin=True)
            print(f"✅ Utente admin '{admin_username}' creato automaticamente")
        except Exception as e:
            print(f"⚠️  Errore creazione admin: {e}")
    else:
        print(f"ℹ️  Utente admin '{admin_username}' già esistente")


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 🛡️ VALIDAZIONE BASE - Solo SQL Injection (XSS/CMD non servono nel login)
        validation_username = InputValidator.validate_sql_only(username, 'username')
        
        # Se rileva SQL Injection, logga e blocca
        if not validation_username['is_safe']:
            create_log(
                ip=request.remote_addr,
                log_type=f"MALICIOUS_INPUT_{validation_username['attack_type']}",
                user=None,
                is_error=True
            )
            flash('⚠️ Input sospetto rilevato. Tentativo bloccato per motivi di sicurezza.', 'danger')
            return render_template('login.html')

        user = get_user_by_username(username)

        if user and user.check_password(password):
            login_user(user)
            
            # 📝 LOG: Login successo
            create_log(
                ip=request.remote_addr,
                log_type="LOGIN_SUCCESS",
                user=user,
                is_error=False
            )
            
            flash('Login effettuato con successo!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('home'))
        else:
            # 📝 LOG: Login fallito
            create_log(
                ip=request.remote_addr,
                log_type="LOGIN_FAILED",
                user=None,
                is_error=True
            )
            
            flash('Username o password non corretti.', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # 🛡️ VALIDAZIONE BASE - Solo SQL Injection (XSS/CMD non servono nel register)
        validation_username = InputValidator.validate_sql_only(username, 'username')
        
        # Se rileva SQL Injection, logga e blocca
        if not validation_username['is_safe']:
            create_log(
                ip=request.remote_addr,
                log_type=f"MALICIOUS_INPUT_{validation_username['attack_type']}",
                user=None,
                is_error=True
            )
            flash('⚠️ Input sospetto rilevato. Tentativo bloccato per motivi di sicurezza.', 'danger')
            return render_template('register.html')

        # Validation
        if not username or not password:
            flash('Tutti i campi sono obbligatori.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Le password non corrispondono.', 'error')
            return render_template('register.html')

        if get_user_by_username(username):
            flash('Username già esistente.', 'error')
            return render_template('register.html')

        # 🔒 VALIDAZIONE FORZA PASSWORD
        password_validation = PasswordValidator.validate_strength(password, username)
        if not password_validation['is_strong']:
            flash('❌ La password non soddisfa i requisiti di sicurezza.', 'error')
            return render_template('register.html')

        # Create user
        new_user = create_user(username, password)
        
        # 📝 LOG: Registrazione riuscita
        create_log(
            ip=request.remote_addr,
            log_type="REGISTER_SUCCESS",
            user=new_user,
            is_error=False
        )
        
        flash('✅ Registrazione completata! Password sicura accettata.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/home')
@login_required
def home():
    # 📝 LOG: Accesso alla pagina home
    create_log(
        ip=request.remote_addr,
        log_type="PAGE_ACCESS",
        user=current_user,
        is_error=False
    )
    
    return render_template('home.html', username=current_user.username)


@app.route('/logout')
@login_required
def logout():
    # 📝 LOG: Logout (prima di terminare la sessione)
    create_log(
        ip=request.remote_addr,
        log_type="LOGOUT",
        user=current_user,
        is_error=False
    )
    
    logout_user()
    flash('Logout effettuato con successo!', 'success')
    return redirect(url_for('login'))


@app.route('/logs')
@login_required
def logs():
    """Dashboard per visualizzare i log con filtri"""
    # Solo admin può accedere
    if not getattr(current_user, 'is_admin', False):
        flash('Accesso negato: sezione riservata agli amministratori.', 'error')
        return redirect(url_for('home'))
    
    # 📝 LOG: Accesso alla pagina logs (solo se non è un refresh con filtri)
    if not request.args:
        create_log(
            ip=request.remote_addr,
            log_type="PAGE_ACCESS_LOGS",
            user=current_user,
            is_error=False
        )
    
    # 🔍 FILTRI dai parametri URL
    filter_type = request.args.get('type', '')
    filter_ip = request.args.get('ip', '')
    filter_user = request.args.get('user', '')
    filter_error = request.args.get('error', '')
    filter_date = request.args.get('date', '')
    
    # Query base
    query = Log.query
    
    # Applica filtri
    if filter_type:
        query = query.filter(Log.type.like(f'%{filter_type}%'))
    
    if filter_ip:
        query = query.filter(Log.ip.like(f'%{filter_ip}%'))
    
    if filter_user:
        query = query.join(User).filter(User.username.like(f'%{filter_user}%'))
    
    if filter_error == 'true':
        query = query.filter(Log.is_error == True)
    elif filter_error == 'false':
        query = query.filter(Log.is_error == False)
    
    if filter_date:
        from datetime import datetime, timedelta
        try:
            # Filtra per giorno specifico
            target_date = datetime.strptime(filter_date, '%Y-%m-%d')
            next_day = target_date + timedelta(days=1)
            query = query.filter(Log.timestamp >= target_date, Log.timestamp < next_day)
        except ValueError:
            pass  # Data non valida, ignora filtro
    
    # Ordina per timestamp decrescente e limita risultati
    all_logs = query.order_by(Log.timestamp.desc()).limit(200).all()
    
    # 🚨 ANALISI SICUREZZA - Rileva brute force e IP sospetti
    alerts = SecurityAnalyzer.get_all_alerts()
    
    # Statistiche base (sui log filtrati)
    total_logs = len(all_logs)
    error_count = sum(1 for log in all_logs if log.is_error)
    login_success = sum(1 for log in all_logs if log.type == "LOGIN_SUCCESS")
    login_failed = sum(1 for log in all_logs if log.type == "LOGIN_FAILED")
    
    stats = {
        'total': total_logs,
        'errors': error_count,
        'login_success': login_success,
        'login_failed': login_failed
    }
    
    # Ottieni lista tipi di log unici per dropdown
    all_log_types = db.session.query(Log.type).distinct().all()
    log_types = sorted([t[0] for t in all_log_types])
    
    # Ottieni lista IP unici
    all_ips = db.session.query(Log.ip).distinct().limit(50).all()
    unique_ips = sorted([ip[0] for ip in all_ips])
    
    return render_template('logs.html', 
                         logs=all_logs, 
                         stats=stats, 
                         alerts=alerts,
                         log_types=log_types,
                         unique_ips=unique_ips,
                         filters={
                             'type': filter_type,
                             'ip': filter_ip,
                             'user': filter_user,
                             'error': filter_error,
                             'date': filter_date
                         })


@app.route('/account')
@login_required
def account():
    """Pagina gestione account utente"""
    return render_template('account.html')


@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    """Cambia la password dell'utente corrente"""
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # Validazione
    if not current_password or not new_password or not confirm_password:
        flash('Tutti i campi sono obbligatori.', 'error')
        return redirect(url_for('account'))
    
    # Verifica password attuale
    if not current_user.check_password(current_password):
        # 📝 LOG: Tentativo cambio password con password errata
        create_log(
            ip=request.remote_addr,
            log_type="PASSWORD_CHANGE_FAILED",
            user=current_user,
            is_error=True
        )
        flash('Password attuale non corretta.', 'error')
        return redirect(url_for('account'))
    
    # Verifica corrispondenza nuova password
    if new_password != confirm_password:
        flash('Le nuove password non corrispondono.', 'error')
        return redirect(url_for('account'))
    
    # 🔄 PREVENZIONE RIUSO PASSWORD - Verifica che la nuova sia diversa dalla vecchia
    if current_user.check_password(new_password):
        flash('❌ La nuova password deve essere diversa da quella attuale.', 'error')
        return redirect(url_for('account'))
    
    # 🔒 VALIDAZIONE FORZA PASSWORD
    password_validation = PasswordValidator.validate_strength(new_password, current_user.username)
    if not password_validation['is_strong']:
        flash('❌ La nuova password non soddisfa i requisiti di sicurezza.', 'error')
        return redirect(url_for('account'))
    
    # Aggiorna password
    try:
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        
        # 📝 LOG: Cambio password riuscito
        create_log(
            ip=request.remote_addr,
            log_type="PASSWORD_CHANGE_SUCCESS",
            user=current_user,
            is_error=False
        )
        
        flash('✅ Password cambiata con successo! Password sicura accettata.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Errore durante il cambio password.', 'error')
    
    return redirect(url_for('account'))


@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    """Elimina l'account dell'utente corrente"""
    
    # Verifica che NON sia admin
    if current_user.is_admin:
        flash('Gli account amministratore non possono essere eliminati.', 'error')
        return redirect(url_for('account'))
    
    password = request.form.get('password')
    
    # Verifica password
    if not password or not current_user.check_password(password):
        # 📝 LOG: Tentativo eliminazione account con password errata
        create_log(
            ip=request.remote_addr,
            log_type="ACCOUNT_DELETE_FAILED",
            user=current_user,
            is_error=True
        )
        flash('Password non corretta. Eliminazione annullata.', 'error')
        return redirect(url_for('account'))
    
    try:
        # Salva username per il log
        username = current_user.username
        user_id = current_user.id
        
        # 📝 LOG: Account eliminato (prima di eliminare l'utente)
        create_log(
            ip=request.remote_addr,
            log_type="ACCOUNT_DELETED",
            user=current_user,
            is_error=False
        )
        
        # Logout prima di eliminare
        logout_user()
        
        # Elimina l'utente
        from model.user import User
        user_to_delete = User.query.get(user_id)
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
        
        flash(f'Account "{username}" eliminato con successo.', 'success')
        return redirect(url_for('login'))
        
    except Exception as e:
        db.session.rollback()
        flash('Errore durante l\'eliminazione dell\'account.', 'error')
        return redirect(url_for('account'))


if __name__ == '__main__':

    with app.app_context():
        db.create_all()
        ensure_admin_user()  # Crea admin automaticamente
    app.run(debug=True)