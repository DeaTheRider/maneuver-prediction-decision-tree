import pandas as pd
from pathlib import Path

import settings

FIRST_DEGREE_TURN = 15
SECOND_DEGREE_TURN = 30


def get_prediction(row):
    heading_change = (row['end_heading']-row['heading'] + 180) % 360 - 180

    if heading_change >= FIRST_DEGREE_TURN:
        return 'turn-right'
    elif heading_change <= -SECOND_DEGREE_TURN:
        return 'turn-left'
    elif FIRST_DEGREE_TURN <= heading_change < SECOND_DEGREE_TURN:
        return 'easy-turn-right'
    elif -FIRST_DEGREE_TURN >= heading_change > -SECOND_DEGREE_TURN:
        return 'easy-turn-left'
    else:
        if row['xCenter'] == row['end_xCenter'] and row['yCenter'] == row['end_xCenter']:
            return 'still'
        elif row['lonVelocity'] < row['end_lonVelocity']:
            return 'faster'
        elif row['lonVelocity'] > row['end_lonVelocity']:
            return 'slower'
        else:
            return 'constant-speed'


for name, dataset in settings.DATASETS.items():
    print(f'Starting {dataset["dataset_name"]}')
    for filepath in Path(rf'{settings.BY_CLASS_DATASET_FOLDER}/{dataset["dataset_name"]}/').glob('*.csv'):
        class_name = filepath.name[:-4]
        print(f'Starting {class_name}')
        df = pd.read_csv(filepath)
        all_datasets = []
        for (track_id, recording_id), group in df.groupby(['trackId', 'recordingId']):
            temp_columns = ['heading', 'xCenter', 'yCenter', 'lonVelocity']
            for column in temp_columns:
                group[f'end_{column}'] = group[column].shift(-settings.PREDICTION_FORWARD_FRAMES, fill_value=group.iloc[-1][column])
            group['prediction'] = group.apply(get_prediction, axis=1)
            group = group.drop(columns=[f'end_{item}' for item in temp_columns])
            all_datasets.append(group)
        df = pd.concat(all_datasets, axis=0, ignore_index=True)
        Path(f'{settings.LABELED_DATASET_FOLDER}/{dataset["dataset_name"]}/').mkdir(parents=True, exist_ok=True)
        df.to_csv(f'{settings.LABELED_DATASET_FOLDER}/{dataset["dataset_name"]}/{class_name}.csv', index=False)
print('Done')
