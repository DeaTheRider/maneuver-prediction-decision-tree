import pandas as pd
from pathlib import Path
from multiprocessing import Process

import settings

FIRST_DEGREE_TURN = 15
SECOND_DEGREE_TURN = 30


def get_prediction(row):
    heading_change = (row['end_heading']-row['heading'] + 180) % 360 - 180

    if heading_change >= SECOND_DEGREE_TURN:
        return 'turn-right'
    elif -heading_change >= SECOND_DEGREE_TURN:
        return 'turn-left'
    elif FIRST_DEGREE_TURN <= heading_change < SECOND_DEGREE_TURN:
        return 'easy-turn-right'
    elif FIRST_DEGREE_TURN <= -heading_change < SECOND_DEGREE_TURN:
        return 'easy-turn-left'
    else:
        if row['lonVelocity'] < 0.2 and row['end_lonVelocity'] < 0.2:
            return 'still'
        elif (2*row['end_lonVelocity']/(row['lonVelocity']+row['end_lonVelocity'])) > 1.1:
            return 'faster'
        elif (2*row['end_lonVelocity']/(row['lonVelocity']+row['end_lonVelocity'])) < 0.9:
            return 'slower'
        else:
            return 'constant-speed'


def run_once(dataset, filepath):
    class_name = filepath.name[:-4]
    print(f'Starting {dataset["dataset_name"]} {class_name}')
    if Path(f'{settings.LABELED_DATASET_FOLDER}/{dataset["dataset_name"]}/{class_name}.csv').is_file():
        print('Skipping')
        return
    df = pd.read_csv(filepath)
    all_datasets = []
    for (track_id, recording_id), group in df.groupby(['trackId', 'recordingId']):
        temp_columns = ['heading', 'xCenter', 'yCenter', 'lonVelocity']
        for column in temp_columns:
            group[f'end_{column}'] = group[column].shift(-settings.PREDICTION_FORWARD_FRAMES,
                                                         fill_value=group.iloc[-1][column])
        group['prediction'] = group.apply(get_prediction, axis=1)
        group = group.drop(columns=[f'end_{item}' for item in temp_columns])
        all_datasets.append(group)
    df = pd.concat(all_datasets, axis=0, ignore_index=True)
    Path(f'{settings.LABELED_DATASET_FOLDER}/{dataset["dataset_name"]}/').mkdir(parents=True, exist_ok=True)
    df.to_csv(f'{settings.LABELED_DATASET_FOLDER}/{dataset["dataset_name"]}/{class_name}.csv', index=False)
    print(f'Finished {dataset["dataset_name"]} {class_name}')


def run_all():
    for name, dataset in settings.DATASETS.items():
        for filepath in Path(rf'{settings.BY_CLASS_DATASET_FOLDER}/{dataset["dataset_name"]}/').glob('*.csv'):
            run_once(dataset, filepath)
    print('All Done')


def run_all_multiprocessing():
    all_processes = []
    for name, dataset in settings.DATASETS.items():
        for filepath in Path(rf'{settings.BY_CLASS_DATASET_FOLDER}/{dataset["dataset_name"]}/').glob('*.csv'):
            p = Process(target=run_once, args=(dataset, filepath))
            p.start()
            all_processes.append(p)
    for p in all_processes:
        p.join()
    print('All Done')


run_all()
