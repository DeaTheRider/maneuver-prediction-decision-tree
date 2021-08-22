import pandas as pd
import numpy as np
import os
def all_dataset(name_dataset):
    if name_dataset == "inD-dataset-v1.0":
        count_csv = 33
    else:
        count_csv = 24
    if not os.path.exists("output5"):
        os.makedirs("output5")
    df = pd.DataFrame()
    for i in range(count_csv):
        num_csv = f"0{i}" if len(str(i)) != 2 else str(i)
        path = f"output3/{name_dataset}_2" + num_csv + "concat_dataset.csv"

        df2 = pd.read_csv(path)
        df = pd.concat([df, df2], ignore_index=True)
    df.dropna(axis=0, inplace=True)
    df.to_csv(f'output5/{name_dataset}_all.csv')


def run():
    names_dataset = ["rounD-dataset-v1.0", 'inD-dataset-v1.0']
    for i in names_dataset:
        all_dataset(i)


if __name__ == '__main__':
    run()
