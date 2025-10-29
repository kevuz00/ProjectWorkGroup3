"""
Script per generare log di test per verificare il rilevamento brute-force
"""
from app import app, db
from model.log import create_log
from datetime import datetime, timedelta
import random

def generate_brute_force_test():
    """Genera tentativi di brute force fittizi"""
    with app.app_context():
        print("\n🔧 Generazione dati di test per Brute Force Detection\n")
        
        # IP attaccante
        attacker_ip = "192.168.1.100"
        
        # Genera 10 login falliti negli ultimi 3 minuti
        print(f"📝 Creazione 10 login falliti da {attacker_ip}...")
        for i in range(10):
            create_log(
                ip=attacker_ip,
                log_type="LOGIN_FAILED",
                user=None,
                is_error=True
            )
        
        print(f"✅ Creati 10 tentativi falliti da {attacker_ip}")
        
        # Altri IP normali
        normal_ips = ["127.0.0.1", "192.168.1.50", "10.0.0.5"]
        for ip in normal_ips:
            # 2-3 tentativi (sotto la soglia)
            for _ in range(random.randint(2, 3)):
                create_log(
                    ip=ip,
                    log_type="LOGIN_FAILED",
                    user=None,
                    is_error=True
                )
        
        print(f"✅ Creati anche tentativi normali da altri IP")
        
        print("\n🎯 Test completato!")
        print("   Vai su /logs per vedere gli alert di brute-force\n")

if __name__ == '__main__':
    generate_brute_force_test()
