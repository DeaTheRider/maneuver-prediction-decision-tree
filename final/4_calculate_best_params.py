from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
import json

import settings

SEARCH_PARAMS = {
    'criterion': ['gini', 'entropy'],
    'max_depth': range(1, 10),
    'min_samples_split': range(2, 10),
    'min_samples_leaf': range(1, 5)
}


def run_once(dataset, filepath):
    class_name = filepath.name[:-4]
    print(f'Starting {dataset["dataset_name"]} {class_name}')
    if Path(f'{settings.BEST_PARAMETERS_FOLDER}/{dataset["dataset_name"]}/{class_name}/parameters.json').is_file():
        print(f'Skipping {dataset["dataset_name"]} {class_name}')
        return
    df = pd.read_csv(filepath)
    df = df.drop(columns=['recordingId', 'frame', 'trackId', 'class'])
    print(df['prediction'].value_counts())
    x = df.drop('prediction', axis=1)
    y = df['prediction']
    y, prediction_names = pd.factorize(y)
    Path(f'{settings.BEST_PARAMETERS_FOLDER}/{dataset["dataset_name"]}/{class_name}/').mkdir(parents=True, exist_ok=True)
    with open(f'{settings.BEST_PARAMETERS_FOLDER}/{dataset["dataset_name"]}/{class_name}/prediction_names.json', 'w') as f:
        json.dump({i: item for i, item in enumerate(list(prediction_names))}, f)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, stratify=y, random_state=42)
    decision_tree = DecisionTreeClassifier()
    clf = GridSearchCV(decision_tree, param_grid=SEARCH_PARAMS, cv=4, verbose=1, n_jobs=-1)
    clf.fit(x_train, y_train)
    with open(f'{settings.BEST_PARAMETERS_FOLDER}/{dataset["dataset_name"]}/{class_name}/parameters.json', 'w') as f:
        json.dump(clf.best_params_, f)
    print(f'Finished {dataset["dataset_name"]} {class_name}')


def run_all():
    for name, dataset in settings.DATASETS.items():
        for filepath in Path(f'{settings.LABELED_DATASET_FOLDER}/{dataset["dataset_name"]}/').glob('*.csv'):
            run_once(dataset, filepath)


run_all()
