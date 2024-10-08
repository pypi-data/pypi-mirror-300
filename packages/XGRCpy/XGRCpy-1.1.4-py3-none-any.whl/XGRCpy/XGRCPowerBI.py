import requests
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from requests_html import HTMLSession

import pandas as pd
from io import StringIO


def generate_key_with_salt(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def decrypt(encrypted_data, password):
    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    key = generate_key_with_salt(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_data

def decrypt_dataframe(encrypted_base64, password):
    encrypted_data = base64.b64decode(encrypted_base64)
    decrypted_data = decrypt(encrypted_data, password)
    try:
        decrypted_csv = decrypted_data.decode('utf-8')
    except UnicodeDecodeError as e:
        print(f"Error decoding decrypted data: {e}")
        return None
    df = pd.read_csv(StringIO(decrypted_csv))
    return df

def XGRCViewTablePowerBI(Table, API_UserName, API_Password, API_Key):
    url = 'https://awesomeapi.xgrc.cloud/XGRC_TableViewPowerBI?query=Hakware:Allow'
    try:
        session = HTMLSession()
        headers = {
            "username": API_UserName,
            "password": API_Password,
        }
        params = {
            "TableName": Table
        }
        response = session.get(url, headers=headers, params=params)
        if response.status_code == 200:
            encrypted_data_b64 = response.text.strip()

            decrypted_df = decrypt_dataframe(encrypted_data_b64, API_Key)
            return decrypted_df
        else:
            print("Error: Request failed with status code", response.status_code)
            return None
        


    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


def XGRCViewSPPowerBI(SP, API_UserName, API_Password, API_Key):
    url = 'https://awesomeapi.xgrc.cloud/XGRC_SPViewPowerBI?query=Hakware:Allow'
    try:
        session = HTMLSession()
        headers = {
            "username": API_UserName,
            "password": API_Password,
        }
        params = {
            "SPName": SP
        }
        response = session.get(url, headers=headers, params=params)
        if response.status_code == 200:
            encrypted_data_b64 = response.text.strip()

            decrypted_df = decrypt_dataframe(encrypted_data_b64, API_Key)
            return decrypted_df
        else:
            print("Error: Request failed with status code", response.status_code)
            return None
        


    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
