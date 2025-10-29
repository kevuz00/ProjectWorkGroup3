"""
Demo INTERATTIVA del sistema di protezione input malevoli
Prova tu stesso a inserire input e vedere se vengono bloccati!
"""
from model.validator import InputValidator

def demo_interactive():
    print("\n" + "="*70)
    print("🛡️  DEMO INTERATTIVA - SISTEMA DI PROTEZIONE INPUT MALEVOLI")
    print("="*70)
    
    print("\n💡 ISTRUZIONI:")
    print("   - Inserisci vari tipi di input per testarli")
    print("   - Il sistema ti dirà se l'input è sicuro o malevolo")
    print("   - Prova SQL injection, XSS, comandi shell, ecc.")
    print("   - Scrivi 'esempi' per vedere input malevoli da provare")
    print("   - Scrivi 'quit' per uscire\n")
    
    while True:
        print("-" * 70)
        user_input = input("\n📝 Inserisci un input da testare (o 'esempi'/'quit'): ").strip()
        
        if user_input.lower() == 'quit':
            print("\n👋 Chiusura demo. Grazie!\n")
            break
        
        if user_input.lower() == 'esempi':
            print("\n📚 ESEMPI DI INPUT MALEVOLI DA PROVARE:\n")
            print("   SQL Injection:")
            print("   - admin' OR '1'='1")
            print("   - ' UNION SELECT * FROM users--")
            print("   - admin'--")
            print()
            print("   XSS:")
            print("   - <script>alert('XSS')</script>")
            print("   - <img src=x onerror=alert(1)>")
            print("   - javascript:alert(1)")
            print()
            print("   Command Injection:")
            print("   - ; rm -rf /")
            print("   - | cat /etc/passwd")
            print("   - && format c:")
            print()
            print("   Path Traversal:")
            print("   - ../../etc/passwd")
            print("   - ../../../windows/system32")
            print("   - c:\\windows\\system32\\config\\sam")
            print()
            continue
        
        if not user_input:
            print("⚠️  Input vuoto, riprova!")
            continue
        
        # VALIDAZIONE
        result = InputValidator.validate(user_input, 'test_field')
        
        print(f"\n🔍 ANALISI INPUT: '{user_input}'")
        print("-" * 70)
        
        if result['is_safe']:
            print("✅ INPUT SICURO")
            print("   ➜ Questo input passerebbe la validazione")
            print("   ➜ L'operazione verrebbe eseguita normalmente")
        else:
            print("🚨 INPUT MALEVOLO RILEVATO!")
            print(f"   ➜ Tipo di attacco: {result['attack_type']}")
            print(f"   ➜ Pattern rilevato: {result['pattern_matched']}")
            print("   ➜ Azione: INPUT BLOCCATO")
            print("   ➜ Log: Tentativo salvato nel database")
            print("   ➜ Utente vede: '⚠️ Input sospetto rilevato'")
        
        print()

if __name__ == '__main__':
    demo_interactive()
