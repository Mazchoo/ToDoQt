from cryptography.fernet import Fernet
from pathlib import Path


def save_encryption_key_to_disk(key_file_name: Path, key: bytes):
    if key_file_name.exists():
        key_file_name.unlink()

    with open(str(key_file_name), 'w') as f:
        f.write(str(key))

    if not key_file_name.exists():
        raise FileNotFoundError("Could not write key to disk.")


def load_fernet_key_from_path(key_file_name: Path) -> Fernet:
    key_file_handler = open(str(key_file_name), 'r')

    try:
        fernet_key = eval(key_file_handler.read())
        fernet = Fernet(fernet_key)
    except Exception:
        key_file_handler.close()
        raise ValueError(f"Fernet key {key_file_name} is not valid.")
    else:
        key_file_handler.close()

    return fernet


def fernet_encrypt_string(fernet: Fernet, plain_text: str):
    str_as_bytes = bytes(plain_text, 'utf-8')
    encrypted_bytes = fernet.encrypt(str_as_bytes)
    return str(encrypted_bytes)


def load_fernet_key_if_exists(key_file_name: Path):
    if key_file_name.exists():
        fernet = load_fernet_key_from_path(key_file_name)
    else:
        fernet_key = Fernet.generate_key()
        save_encryption_key_to_disk(key_file_name, fernet_key)
        fernet = Fernet(fernet_key)
    return fernet


def encrypt_dictionary_and_save_key(json_dict: dict, key_file_name: Path, fields: set):
    fernet = load_fernet_key_if_exists(key_file_name)

    output_dict = {}
    for key, value in json_dict.items():
        if key in fields:
            output_dict[key] = fernet_encrypt_string(fernet, value)
        else:
            output_dict[key] = value

    return output_dict


def format_decrypted_string(decrypted_string: str):
    decrypted_string = decrypted_string[2:(len(decrypted_string) - 1)]
    return decrypted_string.replace('\\n', '\n').replace('\\t', '\t')


def fernet_decrypt_string(fernet: Fernet, cipher_text: str):
    byte_cipher = eval(cipher_text)
    if not isinstance(byte_cipher, bytes):
        raise AttributeError(f"Object is not bytes {cipher_text}")

    decrypted_string = str(fernet.decrypt(byte_cipher))
    return format_decrypted_string(decrypted_string)


def decrypt_json_dict(json_dict: dict, key_file_name: Path, fields: set = (), eval_fields: set = ()):

    if not key_file_name.exists():
        raise FileNotFoundError(f"Decryption key {key_file_name} not found")

    fernet = load_fernet_key_from_path(key_file_name)

    output_dict = {}
    for key, value in json_dict.items():
        decrpyted_value = fernet_decrypt_string(fernet, value) if key in fields else value
        output_dict[key] = eval(decrpyted_value) if key in eval_fields else decrpyted_value

    return output_dict
