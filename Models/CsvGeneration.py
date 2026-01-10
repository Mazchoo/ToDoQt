"""Functions to create save csv"""

from typing import Set, Dict
from pathlib import Path

import pandas as pd
from cryptography.fernet import InvalidToken

from Common.GenerateEncryption import encrypt_dictionary_and_save_key


def get_full_hash_path(save_folder: Path, file_name: str) -> str:
    """Get path to hash brown file"""
    return save_folder / "Hashbrowns" / file_name


def turn_loaded_dict_into_df(
    note_data_dict: dict, path: Path, encrypt_fields: set
) -> pd.DataFrame:
    """Converted dict data into encrypted csv data"""
    encrypted_notes = {}
    for file_name, note_data in note_data_dict.items():
        file_path = get_full_hash_path(path, file_name)

        try:
            encrypted_note = encrypt_dictionary_and_save_key(
                note_data, file_path, encrypt_fields
            )
        except InvalidToken as e:
            print(f"Error! Encryption failed {file_name} -> {e}")
        else:
            encrypted_notes[file_name] = encrypted_note

    return pd.DataFrame.from_dict(encrypted_notes, orient="index")


def get_all_new_entries(all_note_data: dict, initial_data: dict) -> Set[str]:
    """Return all new entry keys"""
    all_previous_keys = initial_data.keys()
    all_current_keys = set(all_note_data.keys())
    return all_current_keys.difference(all_previous_keys)


def get_all_edited_entries(all_note_data: dict, initial_data: dict) -> Dict[str, dict]:
    """Get all edited notes"""
    edited_notes = {}
    for key, json_dict in all_note_data.items():
        if key in initial_data and initial_data[key] != json_dict:
            edited_notes[key] = json_dict

    return edited_notes


def get_all_delete_entries(all_note_data: dict, initial_data: dict) -> Set[str]:
    """Return all deleted keys"""
    all_previous_keys = set(initial_data.keys())
    all_current_keys = all_note_data.keys()
    return all_previous_keys.difference(all_current_keys)


def get_new_columns(all_note_data: dict, current_cols: list) -> Set[str]:
    """Get set of all new columns"""
    new_columns = set()
    if all_note_data:
        current_cols_set = set(current_cols)
        first_note = list(all_note_data.values())[0]
        new_columns = current_cols_set.difference(first_note.keys())
    return new_columns


def get_deleted_columns(all_note_data: dict, current_cols: list) -> Set[str]:
    """Get set of all deleted columns"""
    deleted_columns = set()
    if all_note_data:
        first_note_set = set(list(all_note_data.values())[0])
        deleted_columns = first_note_set.difference(current_cols)
    return deleted_columns


def get_rows_from_keys(all_note_data: dict, filter_set: set):
    """Get dict of row from key set"""
    return {k: v for k, v in all_note_data.items() if k in filter_set}


def check_for_duplicate_index(df: pd.DataFrame):
    """If dataframe is re-indexed, drop extra index column and give warning"""
    init_len = len(df)
    df["_index"] = df.index

    df.drop_duplicates(subset="_index", keep="last", inplace=True)
    if len(df) < init_len:
        print("Warning!: Duplicate rows trying to be saved to database!")

    df.drop(columns="_index", inplace=True)


def create_updated_df(
    original_df: pd.DataFrame,
    new_data: dict,
    initial_data: dict,
    path: Path,
    encrypt_fields: set,
) -> pd.DataFrame:
    """Create updated dataframe with minimal changes to encryption"""
    final_df = original_df.copy()

    edited_rows = get_all_edited_entries(new_data, initial_data)
    new_row_set = get_all_new_entries(new_data, initial_data)
    deleted_row_set = get_all_delete_entries(new_data, initial_data)

    new_columns = get_new_columns(new_data, final_df.columns)
    deleted_columns = get_deleted_columns(new_data, final_df.columns)
    new_rows = get_rows_from_keys(new_data, new_row_set)

    edited_rows_df = turn_loaded_dict_into_df(edited_rows, path, encrypt_fields)
    new_rows_df = turn_loaded_dict_into_df(new_rows, path, encrypt_fields)

    # Set value in old data for new columns
    for col in new_columns:
        final_df[col] = None
    final_df.drop(columns=deleted_columns, inplace=True)

    # Update every edited row in the original
    if not edited_rows_df.empty:
        final_df.loc[edited_rows_df.index] = edited_rows_df

    # Remove deleted rows
    final_df.drop(deleted_row_set, inplace=True)
    final_df = pd.concat([final_df, new_rows_df])

    final_df.sort_values(by=["id_number"])
    check_for_duplicate_index(final_df)

    return final_df
