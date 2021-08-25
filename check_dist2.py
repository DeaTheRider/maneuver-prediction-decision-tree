import numpy as np
from read_data import *
import os
import pandas as pd
from scipy.spatial.distance import cdist
import pickle

def distance_all(x, y): # растояние между всеми точками на кадре
    # distance_matrix = cdist(x, y, 'euclidean')
    distance_matrix = cdist(x, y, 'correlation')
    # distance_matrix = cdist(x, y, 'minkowski', p=2.)
    return distance_matrix

def create_distance_matrix(frame):
    """

    dict_keys(['trackId', 'frame', 'xCenter', 'yCenter', 'bbox', 'xVelocity',
     'yVelocity', 'xAcceleration', 'yAcceleration',
     'trackLifetime', 'heading', 'lonVelocity', 'latVelocity', 'lonAcceleration', 'latAcceleration'])
    :param frame:
    :return:
    """
    distance_matrix = distance_all(frame[BBOX], frame[BBOX])

    d = {'id': frame[TRACK_ID], "distance_matrix": distance_matrix, }
    return d

def create_dataset(name_dataset):
    print(name_dataset)
    if name_dataset == "inD-dataset-v1.0":
        count_csv = (27,33)
    else:
        count_csv = (243,)
    for number in range(*count_csv):
        print(number)
        l = []
        num_csv = f"0{number}" if len(str(number)) != 2 else str(number)
        track_csv_path = f"../lololol/data/datasets/{name_dataset}/data/" + num_csv + "_tracks.csv"
        track_meta_csv_path = f"../lololol/data/datasets/{name_dataset}/data/" + num_csv + "_tracksMeta.csv"
        track_meta_recording = f"../lololol/data/datasets/{name_dataset}/data/" + num_csv + "_recordingMeta.csv"
        tracks_csv = read2_tracks_csv(track_csv_path, track_meta_csv_path, track_meta_recording)
        tracks_csv2 = read_csv(track_csv_path)
        tracks_meta = read_csv(track_meta_csv_path)
        recording_meta = read_csv(
            f"../lololol/data/datasets/{name_dataset}/data/" + num_csv + "_recordingMeta.csv")
        for j,i in enumerate(tracks_csv):
            dist = create_distance_matrix(tracks_csv[i])
            d = {FRAME: i, 'dist': dist}
            l.append(d)
        all_frame = []
        for num in range(len(l)):
            frame_id = l[num][FRAME]
            dist = l[num]['dist']

            for i, j in enumerate(dist['id']):
                sort_dist_index = np.argsort(dist['distance_matrix'][i])
                count = len(sort_dist_index)
                d = {'trackId': j,  'frame': frame_id,}

                for k in range(1,4):
                    if k >= count:
                        dict_dist = {f'{k}_yVelocity': 999999,
                                     f'{k}_xVelocity': 999999,
                                     f'{k}_yAcceleration': 999999,
                                     f'{k}_xAcceleration': 999999,
                                     f'{k}_xCenter': 999999,
                                     f'{k}_yCenter': 999999,
                                     f'{k}_distance': 999999}
                    else:
                        index_ = sort_dist_index[k]
                        id_ = dist['id'][index_]
                        df = tracks_csv2[(tracks_csv2['frame'] == frame_id) & (tracks_csv2['trackId'] == id_)]
                        dict_dist = {f'{k}_yVelocity': df['yVelocity'].values[0],
                                     f'{k}_xVelocity': df['xVelocity'].values[0],
                                     f'{k}_yAcceleration': df['yAcceleration'].values[0],
                                     f'{k}_xAcceleration': df['xAcceleration'].values[0],
                                     f'{k}_xCenter': df['xCenter'].values[0],
                                     f'{k}_yCenter': df['yCenter'].values[0],
                                     f'{k}_distance': dist['distance_matrix'][i][index_] ,}
                    d.update(dict_dist)
                all_frame.append(d)
        df_all_frame = pd.DataFrame(all_frame)
        df_all_frame.to_csv(f'check_dist2/{name_dataset}_{num_csv}_dist.csv')




def run():
    if not os.path.exists("check_dist2"):
        os.makedirs("check_dist2")
    names_dataset = ['inD-dataset-v1.0', "rounD-dataset-v1.0"]
    print(type(names_dataset))
    for i in names_dataset:
        if i == 'inD-dataset-v1.0':
            continue
        create_dataset(i)


if __name__ == '__main__':
    run()