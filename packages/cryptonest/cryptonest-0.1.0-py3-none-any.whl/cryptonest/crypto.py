import os
from cryptography.hazmat.primitives.asymmetric import rsa # type: ignore
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms # type: ignore
from cryptography.hazmat.primitives import serialization # type: ignore
from cryptography.hazmat.primitives.asymmetric import padding # type: ignore


def generate_rsa_keys():
    """Génère une paire de clés RSA."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_with_chacha20(data, key):
    nonce = os.urandom(12)  # Génération d'un nonce aléatoire pour ChaCha20
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    encryptor = cipher.encryptor()
    encrypted_data = nonce + encryptor.update(data)
    return encrypted_data

def decrypt_with_chacha20(encrypted_data, key):
    nonce = encrypted_data[:12]  # Extraction du nonce
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data[12:])
