import pathlib
import os
import pandas as pd
import xlrd

def list_valid_files(folder="."):
    data_folder = pathlib.Path(folder)
    fns         = os.listdir(data_folder)
    fns         = list(filter(lambda fn: fn[-5:].lower() == '.xlsx', fns))
    fns         = [data_folder / fn for fn in fns]

    return fns

def merge_label_data(input_fns, output_fn):
    df_list = [pd.read_excel(file) for file in input_fns]

    clean_df_list = []
    for df in df_list:
        df          = df[['Class', 'Sentence']]
        df          = df.dropna()
        df['Class'] = df.Class.apply(lambda x: 0 if x == -1 else x)
        clean_df_list.append(df)

    full_df = pd.concat(clean_df_list)
    full_df.to_csv(output_fn, index = False)

def local_basic_merge(xlsx_folder_name="."):
    input_fns = list_valid_files(xlsx_folder_name)
    output_fn = 'full_dataset.csv'
    merge_label_data(input_fns, output_fn)
