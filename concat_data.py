import pickle
import pandas as pd
import numpy as np
from read_data import *
import os

column = ['recordingId', 'trackId', 'frame', 'trackLifetime',
          'xCenter', 'yCenter', 'heading', 'width', 'length', 'xVelocity',
          'yVelocity', 'xAcceleration', 'yAcceleration', 'lonVelocity',
          'latVelocity', 'lonAcceleration', 'latAcceleration', 'label', 'class']


column2 = ['1_yVelocity', '1_xVelocity', '1_yAcceleration', '1_xAcceleration', '1_xCenter', '1_yCenter',
           '2_yVelocity', '2_xVelocity', '2_yAcceleration', '2_xAcceleration', '2_xCenter', '2_yCenter',
           '3_yVelocity', '3_xVelocity', '3_yAccelerationv', '3_xAcceleration', '3_xCenter', '3_yCenter']

def concat_dataset(name_dataset):
    print(name_dataset)
    if name_dataset == "inD-dataset-v1.0":
        count_csv = 33
    else:
        count_csv = 24
    for number in range(count_csv):
        print(number)
        l = []
        num_csv = f"0{number}" if len(str(number)) != 2 else str(number)
        track_csv_path = f"../lololol/data/datasets/{name_dataset}/data/" + num_csv + "_tracks.csv"
        print(track_csv_path)
        labels_csv_path = f"output/{name_dataset}_" + num_csv + "_dataset.csv"
        distance_pickle_path = f"output4/{name_dataset}_" + num_csv + "_dataset.pickle"
        tracks_csv = read_csv(track_csv_path)
        labels_csv = read_csv(labels_csv_path)
        merged = tracks_csv.reset_index().merge(labels_csv.reset_index(), on=['frame', 'trackId'])
        merged = merged[column]
        with open(distance_pickle_path, 'rb') as f:
            distance = pickle.load(f)
        frames = tuple(set(merged['frame'].to_list()))
        l = []
        # dict_keys(['id', 'distance_matrix'])
        all_frame = []
        for num in range(len(distance)):
            if num not in frames:
                continue
            frame_id = distance[num][FRAME]
            dist = distance[num]['dist']

            for i, j in enumerate(dist['id']):
                sort_dist_index = np.argsort(dist['distance_matrix'][i])
                count = len(sort_dist_index)
                d = {'trackId': j,  'frame': frame_id,}

                for k in range(4):

                    if k == 0:
                        continue
                    if k >= count:
                        dict_dist = {f'{k}_yVelocity': 999999,
                                     f'{k}_xVelocity': 999999,
                                    f'{k}_yAcceleration': 999999,
                                    f'{k}_xAcceleration': 999999,
                                    f'{k}_xCenter': 999999,
                                    f'{k}_yCenter': 999999,
                                     f'{k}_distance': 999999}
                    else:

                        df = tracks_csv[(tracks_csv['frame'] == frame_id) & (tracks_csv['trackId'] == j)]
                        dict_dist = {f'{k}_yVelocity': df['yVelocity'].values[0],
                                    f'{k}_xVelocity': df['xVelocity'].values[0],
                                    f'{k}_yAcceleration': df['yAcceleration'].values[0],
                                    f'{k}_xAcceleration': df['xAcceleration'].values[0],
                                    f'{k}_xCenter': df['xCenter'].values[0],
                                    f'{k}_yCenter': df['yCenter'].values[0],
                                     f'{k}_distance': dist['distance_matrix'][i][k] ,}
                    d.update(dict_dist)


                all_frame.append(d)


        df2 = pd.DataFrame(all_frame)
        all_dataset = merged.reset_index().merge(df2.reset_index(), on=['frame', 'trackId'], how='left')
        # all_dataset = all_dataset[]
        all_dataset.to_csv(f"output3/{name_dataset}_2" + num_csv + "concat_dataset.csv")


def run():
    if not os.path.exists("output2"):
        os.makedirs("output2")
    if not os.path.exists("output3"):
        os.makedirs("output3")
    names_dataset = ["rounD-dataset-v1.0", 'inD-dataset-v1.0']
    # names_dataset = ["rounD-dataset-v1.0"]

    for i in names_dataset:

        concat_dataset(i)

if __name__ == '__main__':
    run()