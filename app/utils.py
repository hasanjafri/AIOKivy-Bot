from Crypto.Cipher import DES
import json
from pathlib import Path
import random
import string

def pad(text):
    while len(text) % 8 != 0:
        text += ' '
    return text

def check_keyfile_exists():
    if not Path('./key.txt').is_file():
        with open('key.txt', 'w') as keyFile:
            allchar = string.ascii_letters + string.digits
            key = "".join(random.choice(allchar) for x in range(8))
            keyFile.write(key)
            return check_keyfile_exists()
    else:
        with open('key.txt', 'r') as f:
            key = f.read()
            return key

def generate_safe_config_file(info):
    key = check_keyfile_exists()
    des = DES.new(key.encode('utf-8'), DES.MODE_ECB)
    padded_dict = pad(json.dumps(info))
    encrypted_dict = des.encrypt(padded_dict.encode('utf-8'))
    return encrypted_dict

def decrypt_config_file(encryptedInfo):
    key = check_keyfile_exists()
    des = DES.new(key.encode('utf-8'), DES.MODE_ECB)
    decrypted_dict = des.decrypt(encryptedInfo)
    decrypted_dict = decrypted_dict.decode('utf-8')
    return json.loads(decrypted_dict)