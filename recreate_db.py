"""Script per ricreare il database con tabelle User e Log"""
import os
from app import app, db

# Percorso del database
db_path = 'instance/users.db'

# Elimina il vecchio database se esiste
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"✅ Vecchio database eliminato: {db_path}")
else:
    print(f"ℹ️  Nessun database esistente trovato")

# Crea il nuovo database con la struttura aggiornata
with app.app_context():
    db.create_all()
    print("✅ Nuovo database creato con successo!")
    print("\n📋 Struttura tabella User:")
    print("   - id (Integer, Primary Key)")
    print("   - username (String(80), Unique)")
    print("   - password (String(200), Hashed)")
    print("   - created_at (DateTime)")
    print("\n📋 Struttura tabella Log:")
    print("   - id (Integer, Primary Key)")
    print("   - ip (String(45))")
    print("   - type (String(50))")
    print("   - timestamp (DateTime)")
    print("   - is_error (Boolean)")
    print("   - user_id (Integer, Foreign Key)")
    print("\n🎉 Database pronto! Ora puoi registrare nuovi utenti e verranno loggati tutti gli eventi.")
