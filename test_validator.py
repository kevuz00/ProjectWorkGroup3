"""
Test LIVE del InputValidator - Prova il rilevamento in tempo reale
"""
from model.validator import InputValidator

print("\n🔒 TEST INPUT VALIDATOR - RILEVAMENTO ATTACCHI\n")
print("=" * 70)

# Test cases
test_cases = [
    # (input, campo, dovrebbe_bloccare, tipo_attacco_atteso)
    ("admin", "username", False, None),
    ("password123", "password", False, None),
    ("admin' OR '1'='1", "username", True, "SQL_INJECTION"),
    ("<script>alert('XSS')</script>", "comment", True, "XSS"),
    ("; rm -rf /", "command", True, "COMMAND_INJECTION"),
    ("../../etc/passwd", "filename", True, "PATH_TRAVERSAL"),
    ("mario.rossi@email.com", "email", False, None),
    ("' UNION SELECT password FROM users--", "search", True, "SQL_INJECTION"),
    ("<img src=x onerror=alert(1)>", "bio", True, "XSS"),
    ("normal text 123", "description", False, None),
    ("`cat /etc/shadow`", "input", True, "COMMAND_INJECTION"),
    ("../../../windows/system32", "path", True, "PATH_TRAVERSAL"),
]

print("\n🧪 ESECUZIONE TEST:\n")

passed = 0
failed = 0

for i, (input_text, field, should_block, expected_type) in enumerate(test_cases, 1):
    result = InputValidator.validate(input_text, field)
    
    # Determina se il test è passato
    test_passed = (not result['is_safe']) == should_block
    if should_block and result['attack_type'] != expected_type:
        test_passed = False
    
    # Colore output
    status = "✅ PASS" if test_passed else "❌ FAIL"
    
    print(f"{i:2}. {status} | Campo: {field:15} | Input: {input_text[:40]:40}")
    print(f"     Safe: {result['is_safe']:5} | Attack: {result['attack_type'] or 'None':20}")
    
    if not result['is_safe']:
        print(f"     🚨 BLOCCATO! Pattern: {result['pattern_matched']}")
    
    print()
    
    if test_passed:
        passed += 1
    else:
        failed += 1

print("=" * 70)
print(f"\n📊 RISULTATI: {passed}/{len(test_cases)} test passati")

if failed == 0:
    print("✅ TUTTI I TEST SUPERATI! Il validator funziona correttamente.\n")
else:
    print(f"⚠️  {failed} test falliti. Controlla la configurazione.\n")

# Test avanzato: validazione multipla
print("\n🔬 TEST VALIDAZIONE MULTIPLA (validate_multiple):\n")
print("=" * 70)

form_data = {
    'username': 'admin',
    'password': 'SecurePass123',
    'email': 'user@example.com',
    'comment': 'Questo è un commento normale'
}

result = InputValidator.validate_multiple(form_data)
print("\n✅ Form valido:")
print(f"   {form_data}")
print(f"   Risultato: is_safe={result['is_safe']}, errori={len(result['failed_validations'])}\n")

malicious_form = {
    'username': "admin' OR '1'='1",
    'password': 'password123',
    'email': 'test@example.com',
    'comment': '<script>alert(1)</script>'
}

result = InputValidator.validate_multiple(malicious_form)
print("\n🚨 Form con input malevoli:")
print(f"   {malicious_form}")
print(f"   Risultato: is_safe={result['is_safe']}, errori={len(result['failed_validations'])}")

if not result['is_safe']:
    print("\n   Campi bloccati:")
    for validation in result['failed_validations']:
        print(f"   - {validation['field']}: {validation['attack_type']}")

print("\n" + "=" * 70)
print("\n💡 Il validator è pronto per proteggere l'applicazione!\n")
