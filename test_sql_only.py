"""
Test del nuovo metodo validate_sql_only
Verifica che rilevi solo SQL Injection e ignori XSS/CMD/Path
"""
from model.validator import InputValidator

print("\n🧪 TEST validate_sql_only - Solo SQL Injection\n")
print("=" * 70)

test_cases = [
    # (input, dovrebbe_bloccare, tipo)
    ("admin", False, None),
    ("normaluser123", False, None),
    ("admin' OR '1'='1", True, "SQL_INJECTION"),
    ("' UNION SELECT * FROM users--", True, "SQL_INJECTION"),
    ("<script>alert('XSS')</script>", False, None),  # ← NON deve bloccare
    ("; rm -rf /", False, None),  # ← NON deve bloccare
    ("../../etc/passwd", False, None),  # ← NON deve bloccare
    ("1' OR '1'='1", True, "SQL_INJECTION"),
    ("admin'--", True, "SQL_INJECTION"),
    ("javascript:alert(1)", False, None),  # ← NON deve bloccare
]

print("\n🔍 ESECUZIONE TEST:\n")

passed = 0
failed = 0

for i, (input_text, should_block, expected_type) in enumerate(test_cases, 1):
    result = InputValidator.validate_sql_only(input_text, 'test_field')
    
    # Determina se il test è passato
    test_passed = (not result['is_safe']) == should_block
    if should_block and result['attack_type'] != expected_type:
        test_passed = False
    
    # Status
    status = "✅ PASS" if test_passed else "❌ FAIL"
    
    print(f"{i:2}. {status} | Input: {input_text[:35]:35} | Safe: {str(result['is_safe']):5} | Attack: {result['attack_type'] or 'None'}")
    
    if test_passed:
        passed += 1
    else:
        failed += 1

print("\n" + "=" * 70)
print(f"\n📊 RISULTATI: {passed}/{len(test_cases)} test passati")

if failed == 0:
    print("✅ PERFETTO! validate_sql_only funziona correttamente.\n")
    print("📋 COMPORTAMENTO:")
    print("   ✅ BLOCCA: SQL Injection")
    print("   ❌ IGNORA: XSS, Command Injection, Path Traversal")
    print("\n💡 Questo è corretto per login/register!")
else:
    print(f"⚠️  {failed} test falliti.\n")

print("\n🔧 USO NEL CODICE:")
print("-" * 70)
print("# Login/Register (solo SQL Injection)")
print("validation = InputValidator.validate_sql_only(username, 'username')")
print()
print("# Altri contesti (tutti i controlli)")
print("validation = InputValidator.validate(user_input, 'field_name')")
print()
