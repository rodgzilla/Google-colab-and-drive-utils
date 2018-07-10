import pathlib
import os
import pandas as pd
import xlrd
from drive_module import *

def get_all_data_xlsx_files():
    fileList = file_title_list()
    fileList = [f for f in fileList if f.endswith("data.xlsx")]
    print(fileList)
    for f in fileList:
        get_file(f)

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
    
def colab_basic_merge():
    get_all_data_xlsx_files()
    input_fns = list_valid_files()
    output_fn = 'full_dataset.csv'
    merge_label_data(input_fns, output_fn)