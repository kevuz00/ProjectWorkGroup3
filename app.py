from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'chiave-segreta-da-cambiare-in-produzione'  # Cambia questo in produzione!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Configurazione Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Devi effettuare il login per accedere a questa pagina.'

# Modello User con SQLAlchemy
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login effettuato con successo!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('home'))
        else:
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
        
        # Validazione
        if not username or not password:
            flash('Tutti i campi sono obbligatori.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Le password non corrispondono.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('La password deve essere di almeno 6 caratteri.', 'error')
            return render_template('register.html')
        
        # Controlla se username esiste già
        if User.query.filter_by(username=username).first():
            flash('Username già esistente.', 'error')
            return render_template('register.html')
        
        # Crea nuovo utente
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registrazione completata! Ora puoi effettuare il login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html', username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout effettuato con successo!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea il database se non esiste
    app.run(debug=True)
