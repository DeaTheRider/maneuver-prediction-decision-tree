from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
import json
from multiprocessing import Process

import settings

SEARCH_PARAMS = {
    'criterion': ['gini', 'entropy'],
    'max_depth': range(1, 10),
    'min_samples_split': range(1, 10),
    'min_samples_leaf': range(1, 5)
}


def run_once(dataset, filepath):
    class_name = filepath.name[:-4]
    print(f'Starting {class_name}')
    df = pd.read_csv(filepath)
    df = df.drop(columns=['recordingId', 'frame', 'trackId', 'class'])
    print(df['prediction'].value_counts())
    x = df.drop('prediction', axis=1)
    y = df['prediction']
    y, prediction_names = pd.factorize(y)
    print(prediction_names)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, stratify=y, random_state=42)
    decision_tree = DecisionTreeClassifier()
    clf = GridSearchCV(decision_tree, param_grid=SEARCH_PARAMS, cv=4, verbose=1, n_jobs=-1)
    clf.fit(x_train, y_train)
    with open(f'{settings.BEST_PARAMETERS_FOLDER}/{dataset["dataset_name"]}/{class_name}.json', 'w') as f:
        json.dump(clf.best_params_, f)
    print(f'Finished {class_name}')


def run_all():
    for name, dataset in settings.DATASETS.items():
        print(f'Starting {dataset["dataset_name"]}')
        for filepath in Path(f'{settings.LABELED_DATASET_FOLDER}/{dataset["dataset_name"]}/').glob('*.csv'):
            run_once(dataset, filepath)


def run_all_multiprocessing():
    all_processes = []
    for name, dataset in settings.DATASETS.items():
        print(f'Starting {dataset["dataset_name"]}')
        for filepath in Path(f'{settings.LABELED_DATASET_FOLDER}/{dataset["dataset_name"]}/').glob('*.csv'):
            p = Process(target=run_once, args=(dataset, filepath))
            p.start()
            p.join()

    for p in all_processes:
        p.join()


run_all()
