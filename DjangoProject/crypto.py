from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from django.conf import settings
from decimal import Decimal
from datetime import datetime, date

# Encryption key and initialization vector (you should store these securely)
ENCRYPTION_KEY = settings.ENCRYPTION_KEY    # get AES encryption key
IV = settings.IV    # get AES IV encryption key

''' this function encrypt data using AES encryption algorithm '''
def encrypt(data):
    """
    Encrypt data using AES encryption algorithm.
    Supports str, int, decimal.Decimal, and bool data types.

    :param data: Data to be encrypted
    :return: Base64 encoded encrypted string or the original data if it's a bool or None
    """
    if data is None:
        return None

    if isinstance(data, bool):
        return data
    if isinstance(data, int):
        data = str(data)
    if isinstance(data, (int, Decimal)):
        data = str(data)
    if isinstance(data, str):
        data = data.encode()

    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, IV)
    padded_data = pad(data, AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return b64encode(encrypted).decode('utf-8')

''' this function is used to decrypt data '''
def decrypt(encrypted_data):
    """
    Decrypt data using AES decryption algorithm.
    Returns the decrypted string or the original data if it's a bool or None.

    :param encrypted_data: Base64 encoded encrypted string to decrypt
    :return: Decrypted string or the original data if it's a bool or None
    """
    if encrypted_data is None:
        return None
    if isinstance(encrypted_data, bool):
        return encrypted_data

    try:
        cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, IV)
        encrypted = b64decode(encrypted_data.encode('utf-8'))
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        return decrypted.decode('utf-8')
    except (ValueError, KeyError, TypeError, UnicodeDecodeError) as e:
        # Handle specific errors such as padding errors or decoding issues
        print(f"Decryption error: {e}")
        return encrypted_data  # Return the original data if decryption fails