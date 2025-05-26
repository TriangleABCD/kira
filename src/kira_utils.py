from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os


def read_from_file(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()


def write_to_file(file_path: str, content: bytes):
    with open(file_path, "wb") as f:
        f.write(content)


def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt_data(data: str, key: bytes) -> bytes:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()
    return iv + encrypted_data


def decrypt_data(encrypted_data: bytes, key: bytes) -> str:
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_data.decode()


def get_encrypted_api_key(api_path, key_path):
    password = 'asoulbella'
    key_content = read_from_file(key_path)

    salt = key_content[:16]
    key = generate_key(password, salt)

    encrypted_content = read_from_file(api_path)

    return decrypt_data(encrypted_content, key)


def get_api_key(path):
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    return content.strip()


def multi_line_input():
    lines = []
    while True:
        line = input()
        if line.strip() == "" or line.strip() == "EOF":
            break
        if line.strip() == "exit" or line.strip() == "quit" or line.strip() == "q":
            return "exit"
        lines.append(line)
    return "\n".join(lines)
