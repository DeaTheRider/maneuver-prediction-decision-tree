import pandas as pd
from pathlib import Path

import settings


for name, dataset in settings.DATASETS.items():
    all_datasets = []
    for file_num in range(dataset['csv_count']):
        print(f'Reading {dataset["dataset_name"]} {file_num}')
        num_csv = f"0{file_num}"[-2:]
        df = pd.read_csv(f'{settings.PREPARED_DATASET_FOLDER}/{dataset["dataset_name"]}/{num_csv}.csv', index_col=None, header=0)
        all_datasets.append(df)

    df = pd.concat(all_datasets, axis=0, ignore_index=True)
    for class_id, class_group in df.groupby('class'):
        class_group = class_group.drop(columns=['class'])
        print(f'Writing {dataset["dataset_name"]} {class_id}')
        Path(f'{settings.BY_CLASS_DATASET_FOLDER}/{dataset["dataset_name"]}/').mkdir(parents=True, exist_ok=True)
        class_group.to_csv(f'{settings.BY_CLASS_DATASET_FOLDER}/{dataset["dataset_name"]}/{class_id}.csv', index=False)
print('Done')
