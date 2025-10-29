"""
Script di test per il sistema di filtri
Genera log diversificati per testare tutte le combinazioni di filtri
"""
from model import db
from model.log import create_log
from model.user import get_user_by_username, create_user
from app import app
from datetime import datetime, timedelta
import random

def generate_diverse_logs():
    """Genera log di vari tipi per testare i filtri"""
    
    print("\n🧪 GENERAZIONE LOG DIVERSIFICATI PER TEST FILTRI\n")
    print("=" * 70)
    
    with app.app_context():
        # Crea alcuni utenti di test se non esistono
        test_users = ['mario', 'luigi', 'peach']
        for username in test_users:
            if not get_user_by_username(username):
                create_user(username, 'Password123!')
                print(f"✅ Creato utente: {username}")
        
        # IP diversi
        ips = [
            '192.168.1.100',
            '192.168.1.101',
            '10.0.0.50',
            '172.16.0.10',
            '203.0.113.5'
        ]
        
        # Tipi di log
        log_types = [
            ('LOGIN_SUCCESS', False),
            ('LOGIN_FAILED', True),
            ('REGISTER_SUCCESS', False),
            ('LOGOUT', False),
            ('PAGE_ACCESS', False),
            ('PAGE_ACCESS_LOGS', False),
            ('MALICIOUS_INPUT_SQL_INJECTION', True),
            ('MALICIOUS_INPUT_XSS', True),
            ('MALICIOUS_INPUT_COMMAND_INJECTION', True),
            ('MALICIOUS_INPUT_PATH_TRAVERSAL', True),
        ]
        
        print("\n📝 Generazione log...\n")
        
        total = 0
        
        # Genera log distribuiti negli ultimi 3 giorni
        for day_offset in range(3):
            target_date = datetime.now() - timedelta(days=day_offset)
            day_name = ['Oggi', 'Ieri', '2 giorni fa'][day_offset]
            
            print(f"📅 {day_name} ({target_date.strftime('%Y-%m-%d')}):")
            
            # 20 log per giorno
            for i in range(20):
                log_type, is_error = random.choice(log_types)
                ip = random.choice(ips)
                
                # Timestamp casuale durante il giorno
                hour = random.randint(0, 23)
                minute = random.randint(0, 59)
                timestamp = target_date.replace(hour=hour, minute=minute, second=0)
                
                # Crea il log (modificando manualmente il timestamp dopo)
                log = create_log(
                    ip=ip,
                    log_type=log_type,
                    user=None,
                    is_error=is_error
                )
                
                # Modifica timestamp per backdating
                from model.log import Log
                log_entry = Log.query.get(log.id)
                log_entry.timestamp = timestamp
                db.session.commit()
                
                total += 1
                
                if i < 3:  # Mostra solo i primi 3 per giorno
                    print(f"  ✓ {log_type[:30]:30} | {ip:15} | {timestamp.strftime('%H:%M')}")
            
            if day_offset < 2:
                print(f"  ... altri 17 log")
        
        print("\n" + "=" * 70)
        print(f"✅ Creati {total} log diversificati\n")
        
        # Statistiche
        from model.log import Log
        from sqlalchemy import func
        
        print("📊 DISTRIBUZIONE PER TIPO:")
        stats = db.session.query(
            Log.type,
            func.count(Log.id).label('count')
        ).group_by(Log.type).order_by(func.count(Log.id).desc()).all()
        
        for log_type, count in stats:
            print(f"   {log_type[:40]:40} : {count:3} log")
        
        print("\n📊 DISTRIBUZIONE PER IP:")
        ip_stats = db.session.query(
            Log.ip,
            func.count(Log.id).label('count')
        ).group_by(Log.ip).order_by(func.count(Log.id).desc()).limit(10).all()
        
        for ip, count in ip_stats:
            print(f"   {ip:20} : {count:3} log")
        
        print("\n📊 ERRORI vs SUCCESSI:")
        errors = Log.query.filter_by(is_error=True).count()
        success = Log.query.filter_by(is_error=False).count()
        print(f"   ❌ Errori: {errors}")
        print(f"   ✅ Successi: {success}")
        
        print("\n" + "=" * 70)
        print("\n💡 COME TESTARE I FILTRI:\n")
        print("1. Avvia l'app: python app.py")
        print("2. Login come admin: admin/Admin123!")
        print("3. Vai su /logs")
        print("\n🔍 PROVA QUESTI FILTRI:")
        print("   - Tipo: LOGIN_FAILED → Vedi solo login falliti")
        print("   - IP: 192.168 → Vedi tutti i log da rete 192.168")
        print("   - Solo Errori: Solo Errori → Vedi solo errori")
        print("   - Data: (scegli oggi/ieri) → Vedi log del giorno")
        print("   - Quick Filter '🛡️ Attacchi' → Vedi tutti gli attacchi")
        print("\n✅ Ora hai log diversificati per testare TUTTI i filtri!\n")

if __name__ == '__main__':
    generate_diverse_logs()
