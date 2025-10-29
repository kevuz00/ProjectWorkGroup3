"""
Utility per gestione database - Query rapide
"""
from app import app, db
from model.user import User
from model.log import Log
from datetime import datetime

def show_users():
    """Mostra tutti gli utenti"""
    with app.app_context():
        users = User.query.all()
        print("\n" + "="*60)
        print("UTENTI REGISTRATI")
        print("="*60)
        for user in users:
            print(f"ID: {user.id} | Username: {user.username} | Creato: {user.created_at}")
        print("="*60)
        print(f"Totale: {len(users)} utenti\n")

def show_logs(limit=20):
    """Mostra gli ultimi log"""
    with app.app_context():
        logs = Log.query.order_by(Log.timestamp.desc()).limit(limit).all()
        print("\n" + "="*80)
        print(f"ULTIMI {limit} LOG")
        print("="*80)
        for log in logs:
            error_flag = "⚠️" if log.is_error else "✓"
            username = log.user.username if log.user else "N/A"
            print(f"{error_flag} [{log.timestamp.strftime('%d/%m %H:%M:%S')}] {log.type:20} | IP: {log.ip:15} | User: {username}")
        print("="*80)
        print(f"Totale log nel DB: {Log.query.count()}\n")

def show_stats():
    """Mostra statistiche dettagliate"""
    with app.app_context():
        total_logs = Log.query.count()
        login_success = Log.query.filter_by(type="LOGIN_SUCCESS").count()
        login_failed = Log.query.filter_by(type="LOGIN_FAILED").count()
        register = Log.query.filter_by(type="REGISTER_SUCCESS").count()
        logout = Log.query.filter_by(type="LOGOUT").count()
        page_access = Log.query.filter(Log.type.like("PAGE_ACCESS%")).count()
        errors = Log.query.filter_by(is_error=True).count()
        
        print("\n" + "="*60)
        print("STATISTICHE DETTAGLIATE")
        print("="*60)
        print(f"Totale eventi:        {total_logs}")
        print(f"Login riusciti:       {login_success}")
        print(f"Login falliti:        {login_failed}")
        print(f"Registrazioni:        {register}")
        print(f"Logout:               {logout}")
        print(f"Accessi pagine:       {page_access}")
        print(f"Errori totali:        {errors}")
        print("="*60 + "\n")

def clear_logs():
    """Cancella tutti i log (ATTENZIONE!)"""
    with app.app_context():
        count = Log.query.count()
        confirm = input(f"⚠️  Vuoi eliminare {count} log? (si/no): ")
        if confirm.lower() == 'si':
            Log.query.delete()
            db.session.commit()
            print(f"✅ {count} log eliminati\n")
        else:
            print("❌ Operazione annullata\n")

def menu():
    """Menu interattivo"""
    print("\n" + "="*60)
    print("🔧 UTILITY DATABASE SIEM")
    print("="*60)
    print("1. Mostra utenti")
    print("2. Mostra ultimi 20 log")
    print("3. Mostra ultimi 50 log")
    print("4. Mostra statistiche")
    print("5. Cancella tutti i log")
    print("0. Esci")
    print("="*60)
    
    choice = input("\nScelta: ")
    
    if choice == '1':
        show_users()
    elif choice == '2':
        show_logs(20)
    elif choice == '3':
        show_logs(50)
    elif choice == '4':
        show_stats()
    elif choice == '5':
        clear_logs()
    elif choice == '0':
        print("👋 Arrivederci!\n")
        return False
    else:
        print("❌ Scelta non valida\n")
    
    return True

if __name__ == '__main__':
    while menu():
        pass
