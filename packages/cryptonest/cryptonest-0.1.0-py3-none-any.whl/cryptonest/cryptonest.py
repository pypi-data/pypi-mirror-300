import logging
from flask import Flask, request, jsonify  # type: ignore
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet
from datetime import datetime

app = Flask(__name__)

# Configurer le logging pour l'audit trail
logging.basicConfig(filename='audit_trail.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# Générer les clés RSA
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Charger les clés RSA
private_key, public_key = generate_rsa_keys()

def log_audit(action, status, details=""):
    """Journaliser les actions dans l'audit trail."""
    ip = request.remote_addr
    timestamp = datetime.now().isoformat()
    log_message = f"{timestamp} | IP: {ip} | Action: {action} | Status: {status} | Details: {details}"
    logging.info(log_message)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/encrypt', methods=['POST'])
def encrypt_data():
    try:
        data = request.json['data']
        if isinstance(data, dict):  # Vérifiez si 'data' est un dictionnaire
            return jsonify({"error": "Invalid data format. Expected string."}), 400
        
        data = data.encode()  # Encodez les données en bytes

        # Génération de la clé Fernet
        fernet_key = Fernet.generate_key()  
        fernet = Fernet(fernet_key)
        encrypted_data = fernet.encrypt(data)  # Chiffrement des données

        # Chiffrement de la clé Fernet avec RSA
        encrypted_fernet_key = public_key.encrypt(
            fernet_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)  # type: ignore
        )

        # Loguer l'opération de chiffrement réussie
        log_audit(action="Encrypt", status="Success", details="Data encrypted successfully")

        return jsonify({"encrypted_data": encrypted_data.hex(), "encrypted_fernet_key": encrypted_fernet_key.hex()}), 200

    except Exception as e:
        # Loguer l'échec de chiffrement
        log_audit(action="Encrypt", status="Failed", details=str(e))
        return jsonify({"error": "Encryption failed", "details": str(e)}), 500

@app.route('/sensitive', methods=['POST'])
def handle_sensitive_data():
    """Gérer les données sensibles."""
    try:
        sensitive_data = request.json['sensitive_data']
        if isinstance(sensitive_data, dict):  # Vérifiez si 'sensitive_data' est un dictionnaire
            return jsonify({"error": "Invalid data format. Expected string."}), 400

        sensitive_data = sensitive_data.encode()  # Encodez les données en bytes

        # Chiffrement des données sensibles
        encrypted_result = encrypt_data(sensitive_data)

        # Vérifiez si l'encryptage a réussi avant de déchiffrer
        if "error" in encrypted_result:
            return encrypted_result  # Retourne l'erreur si l'encryptage échoue

        # Déchiffrement des données
        decrypted_result = decrypt_data(encrypted_result['encrypted_data'], encrypted_result['encrypted_fernet_key'])

        return jsonify({
            "encrypted": encrypted_result,
            "decrypted": decrypted_result
        }), 200

    except Exception as e:
        log_audit(action="Handle Sensitive Data", status="Failed", details=str(e))
        return jsonify({"error": "Failed to handle sensitive data", "details": str(e)}), 500

# Mettez à jour decrypt_data pour accepter les données en tant qu'arguments
def decrypt_data(encrypted_data_hex, encrypted_fernet_key_hex):
    try:
        encrypted_data = bytes.fromhex(encrypted_data_hex)
        encrypted_fernet_key = bytes.fromhex(encrypted_fernet_key_hex)

        # Déchiffrement de la clé Fernet avec RSA
        fernet_key = private_key.decrypt(
            encrypted_fernet_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)  # type: ignore
        )

        fernet = Fernet(fernet_key)
        decrypted_data = fernet.decrypt(encrypted_data)  # Déchiffrement des données

        # Loguer l'opération de déchiffrement réussie
        log_audit(action="Decrypt", status="Success", details="Data decrypted successfully")

        return decrypted_data.decode()

    except Exception as e:
        # Loguer l'échec de déchiffrement
        log_audit(action="Decrypt", status="Failed", details=str(e))
        return {"error": "Decryption failed", "details": str(e)}

if __name__ == '__main__':
    app.run(port=5000)

