from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

import settings


for name, dataset in settings.DATASETS.items():
    print(f'Starting {dataset["dataset_name"]}')
    for filepath in Path(f'{settings.LABELED_DATASET_FOLDER}/{dataset["dataset_name"]}/').glob('*.csv'):
        class_name = filepath.name[:-4]
        print(f'Starting {class_name}')
        df = pd.read_csv(filepath)
        print(df['prediction'].value_counts())
