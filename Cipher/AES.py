from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import b64encode, b64decode

def encrypt_file(input_file_path, output_file_path, key):
    with open(input_file_path, 'rb') as file:
        plaintext = file.read()

    backend = default_backend()
    iv = b'\0' * 16  # Initialization vector, you may want to generate a random IV for real-world use
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    with open(output_file_path, 'wb') as file:
        file.write(b64encode(iv + ciphertext))

def decrypt_file(input_file_path, output_file_path, key):
    with open(input_file_path, 'rb') as file:
        data = b64decode(file.read())

    backend = default_backend()
    iv = data[:16]  # Extract the IV from the first 16 bytes
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_padded_text = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_text = unpadder.update(decrypted_padded_text) + unpadder.finalize()

    with open(output_file_path, 'wb') as file:
        file.write(decrypted_text)

# Example usage:
encryption_key = b'sfnt3iof2354dwe6'  # Should be a secure random key
input_file = 'input.txt'
encrypted_file = 'encrypted_file.txt'
decrypted_file = 'decrypted_file.txt'

encrypt_file(input_file, encrypted_file, encryption_key)
decrypt_file(encrypted_file, decrypted_file, encryption_key)
