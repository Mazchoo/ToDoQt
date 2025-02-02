''' Encryption helpers that can load and save encrypted files from saved keys '''
from typing import Any, Set
from pathlib import Path
from os import mkdir
import ast

from cryptography.fernet import Fernet


def save_encryption_key_to_disk(key_file_name: Path, key: bytes):
    ''' Save an encryption key (should never be uploaded!) to local disk '''
    if key_file_name.exists():
        key_file_name.unlink()

    with open(str(key_file_name), 'w', encoding='utf-8') as f:
        f.write(str(key))

    if not key_file_name.exists():
        raise FileNotFoundError("Could not write key to disk.")


def load_fernet_key_from_path(key_file_name: Path) -> Fernet:
    ''' Load a fernet key from local disk '''

    with open(str(key_file_name), 'r', encoding='utf-8') as f:
        try:
            fernet_key = ast.literal_eval(f.read())
            fernet = Fernet(fernet_key)
        except Exception as e:
            raise ValueError(f"Fernet key {key_file_name} is not valid.") from e

    return fernet


def fernet_encrypt_string(fernet: Fernet, plain_text: str):
    ''' Encrypt a string in byte form to an encrypted string '''
    str_as_bytes = bytes(plain_text, 'utf-8')
    encrypted_bytes = fernet.encrypt(str_as_bytes)
    return str(encrypted_bytes)


def load_fernet_key_if_exists(key_path: Path):
    ''' Load an encryption key or make a new one if needed '''
    if key_path.exists():
        fernet = load_fernet_key_from_path(key_path)
    else:
        fernet_key = Fernet.generate_key()

        if not key_path.parent.is_dir():
            mkdir(str(key_path.parent))

        save_encryption_key_to_disk(key_path, fernet_key)
        fernet = Fernet(fernet_key)
    return fernet


def encrypt_dictionary_and_save_key(json_dict: dict, key_file_name: Path, fields: set):
    ''' Encrypt every item in a dictionary (treating said item as a string) '''
    fernet = load_fernet_key_if_exists(key_file_name)

    output_dict = {}
    for key, value in json_dict.items():
        if key in fields:
            output_dict[key] = fernet_encrypt_string(fernet, str(value))
        else:
            output_dict[key] = value

    return output_dict


def format_decrypted_string(decrypted_string: str):
    ''' Convert decrypted payload to presentable string '''
    decrypted_string = decrypted_string[2:(len(decrypted_string) - 1)]
    return decrypted_string.replace('\\n', '\n').replace('\\t', '\t')


def fernet_decrypt_string(fernet: Fernet, cipher_text: Any):
    ''' Decrypt contents loaded from a file '''
    if not isinstance(cipher_text, str):
        print("Non encrypted field trying to be decrypted")
        return cipher_text

    byte_cipher = ast.literal_eval(cipher_text)
    if not isinstance(byte_cipher, bytes):
        print("String that is not byte string trying to be decrypted")
        return byte_cipher

    decrypted_string = str(fernet.decrypt(byte_cipher))
    return format_decrypted_string(decrypted_string)


def parse_field(decrpyted_value: str, key: str, eval_fields: set):
    ''' Deserialise object back into utf string or python object for eval_fields '''
    output = ast.literal_eval(decrpyted_value) if key in eval_fields else decrpyted_value
    if isinstance(output, str):
        output = bytes(output, 'utf-8').decode('unicode-escape').encode("latin1").decode("utf-8")
    return output


def decrypt_json_dict(field_value_pairs: dict, key_file_name: Path,
                      decrypt_fields: Set[str], eval_fields: Set[str]):
    '''
        Load contents of loaded file contents, use decryption for decrypt_fields
        and use eval to convert serialized python objects (tuples, list) back into
        Python objects
    '''

    if not key_file_name.exists():
        raise FileNotFoundError(f"Decryption key {key_file_name} not found")

    fernet = load_fernet_key_from_path(key_file_name)

    output_dict = {}
    for key, value in field_value_pairs.items():
        decrpyted_value = fernet_decrypt_string(fernet, value) if key in decrypt_fields else value
        output_dict[key] = parse_field(decrpyted_value, key, eval_fields)

    return output_dict
