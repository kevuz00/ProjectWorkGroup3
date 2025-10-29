from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from model import db, bcrypt
from model.user import User, create_user, get_user_by_username, get_user_by_id
from model.log import Log, create_log, get_all_logs, get_error_logs
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

        # Validation
        if not username or not password:
            flash('Tutti i campi sono obbligatori.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Le password non corrispondono.', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('La password deve essere di almeno 6 caratteri.', 'error')
            return render_template('register.html')

        if get_user_by_username(username):
            flash('Username già esistente.', 'error')
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
        
        flash('Registrazione completata! Ora puoi effettuare il login.', 'success')
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
    """Dashboard per visualizzare i log"""
    # Solo admin può accedere
    if not getattr(current_user, 'is_admin', False):
        flash('Accesso negato: sezione riservata agli amministratori.', 'error')
        return redirect(url_for('home'))
    
    # 📝 LOG: Accesso alla pagina logs
    create_log(
        ip=request.remote_addr,
        log_type="PAGE_ACCESS_LOGS",
        user=current_user,
        is_error=False
    )
    
    # Ottieni tutti i log (limitati agli ultimi 100)
    all_logs = get_all_logs()[:100]
    
    # Statistiche base
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
    
    return render_template('logs.html', logs=all_logs, stats=stats)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        ensure_admin_user()  # Crea admin automaticamente
    app.run(debug=True)