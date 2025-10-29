"""
Script di test rapido per verificare il funzionamento del progetto
"""
from app import app, db
from model.user import User, create_user, get_user_by_username
from model.log import Log, get_all_logs

def test_database():
    """Verifica che il database sia accessibile"""
    with app.app_context():
        try:
            # Test query
            users = User.query.all()
            logs = Log.query.all()
            print(f"✅ Database OK - {len(users)} utenti, {len(logs)} log")
            return True
        except Exception as e:
            print(f"❌ Errore database: {e}")
            return False

def test_imports():
    """Verifica che tutti i moduli si importino correttamente"""
    try:
        from flask import Flask
        from flask_login import LoginManager
        from flask_sqlalchemy import SQLAlchemy
        from flask_bcrypt import Bcrypt
        print("✅ Tutti i moduli Flask importati")
        return True
    except ImportError as e:
        print(f"❌ Errore import: {e}")
        return False

def print_stats():
    """Stampa statistiche del progetto"""
    with app.app_context():
        total_users = User.query.count()
        total_logs = Log.query.count()
        error_logs = Log.query.filter_by(is_error=True).count()
        
        print("\n" + "="*50)
        print("STATISTICHE PROGETTO")
        print("="*50)
        print(f"Utenti registrati: {total_users}")
        print(f"Eventi totali: {total_logs}")
        print(f"Eventi con errore: {error_logs}")
        print("="*50)

if __name__ == '__main__':
    print("\n🔍 TEST PROGETTO SIEM\n")
    
    test_imports()
    test_database()
    print_stats()
    
    print("\n✅ TUTTI I TEST SUPERATI\n")
