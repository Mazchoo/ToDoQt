
import pandas as pd
from pathlib import Path

from Models.NoteFileHelpers import turn_note_data_into_df


def get_all_new_notes(all_note_data: dict, initial_data: dict):
    all_previous_keys = initial_data.keys()
    all_current_keys = set(all_note_data.keys())
    return all_current_keys.difference(all_previous_keys)


def get_all_edited_notes(all_note_data: dict, initial_data: dict):
    edited_notes = {}
    for key, json_dict in all_note_data.items():
        if key in initial_data and initial_data[key] != json_dict:
            edited_notes[key] = json_dict

    return edited_notes


def get_all_delete_notes(all_note_data: dict, initial_data: dict):
    all_previous_keys = set(initial_data.keys())
    all_current_keys = all_note_data.keys()
    return all_previous_keys.difference(all_current_keys)


def get_new_columns(all_note_data: dict, current_cols: list):
    new_columns = {}
    if all_note_data:
        current_cols_set = set(current_cols)
        first_note = list(all_note_data.values())[0]
        new_columns = current_cols_set.difference(first_note.keys())
    return new_columns


def get_deleted_columns(all_note_data: dict, current_cols: list):
    deleted_columns = {}
    if all_note_data:
        first_note_set = set(list(all_note_data.values())[0])
        deleted_columns = first_note_set.difference(current_cols)
    return deleted_columns


def get_new_rows_from_keys(all_note_data: dict, new_row_set: set):
    return {k: v for k, v in all_note_data.items() if k in new_row_set}


def check_for_duplicate_index(df):
    init_len = len(df)
    df["_index"] = df.index

    df.drop_duplicates(subset="_index", keep='last', inplace=True)
    if len(df) < init_len:
        print('Warning!: Duplicate rows trying to be saved to database!')

    df.drop(columns="_index", inplace=True)


def create_updated_df(original_df: pd.DataFrame, all_note_data: dict, initial_data: dict,
                      path: Path, encrypt_fields: set):
    final_df = original_df.copy()

    edited_rows = get_all_edited_notes(all_note_data, initial_data)
    new_row_set = get_all_new_notes(all_note_data, initial_data)
    deleted_row_set = get_all_delete_notes(all_note_data, initial_data)

    new_columns = get_new_columns(all_note_data, final_df.columns)
    deleted_columns = get_deleted_columns(all_note_data, final_df.columns)
    new_rows = get_new_rows_from_keys(all_note_data, new_row_set)

    edited_rows_df = turn_note_data_into_df(edited_rows, path, encrypt_fields)
    new_rows_df = turn_note_data_into_df(new_rows, path, encrypt_fields)

    for col in new_columns:
        final_df[col] = None
    final_df.drop(columns=deleted_columns, inplace=True)

    if not edited_rows_df.empty:
        final_df.loc[edited_rows_df.index] = edited_rows_df
    final_df.drop(deleted_row_set, inplace=True)
    final_df = pd.concat([final_df, new_rows_df])

    final_df.sort_values(by=['id_number'])
    check_for_duplicate_index(final_df)

    return final_df
