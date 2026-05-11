from cryptography.fernet import Fernet
from config import SECRET_KEY

# Ensure the SECRET_KEY in config.py is a valid Fernet key
# You can generate one using Fernet.generate_key()
cipher_suite = Fernet(SECRET_KEY)

def encrypt_file(file_bytes):
    """Encrypts raw bytes and returns encrypted bytes."""
    return cipher_suite.encrypt(file_bytes)

def decrypt_file(file_bytes):
    """Decrypts encrypted bytes and returns original bytes."""
    return cipher_suite.decrypt(file_bytes)