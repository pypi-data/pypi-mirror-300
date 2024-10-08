from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64
import ast

class Security:
    CHARSET_NAME = 'ISO-8859-1'

    def generate_aes_key():
        # Génère une clé de 16 octets (128 bits) pour AES
        print(os.urandom(16))

    def get_aes_key():
        # Récupère la clé AES dans les variables d'environnement
        return ast.literal_eval(os.environ.get("AES_KEY"))

    def generate_aes_iv():
        # Génère un vecteur d'initialisation de 16 octets (128 bits) pour AES
        return os.urandom(16)

    def encrypt_aes(str_value, key):
        # Chiffre le texte en utilisant AES avec CBC
        iv = Security.generate_aes_iv()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(str_value.encode()) + padder.finalize()
        encrypted_str_value = encryptor.update(padded_data) + encryptor.finalize()
        # Concatène l'IV et le texte chiffré et encode en base64
        encrypted_data = base64.b64encode(iv + encrypted_str_value).decode(Security.CHARSET_NAME)
        return encrypted_data

    def decrypt_aes(encrypted_data, key):
        # Déchiffre le texte en utilisant AES avec CBC
        encrypted_data = base64.b64decode(encrypted_data)
        # Extrait la valeur de l'IV
        iv = encrypted_data[:16]
        # Extrait le texte chiffré
        encrypted_data = encrypted_data[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        decrypted_str_value = unpadder.update(padded_data) + unpadder.finalize()
        return decrypted_str_value.decode(Security.CHARSET_NAME)
