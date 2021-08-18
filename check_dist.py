#TODO

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
        count_csv = 33
    else:
        count_csv = 24
    for number in range(count_csv):
        print(number)
        l = []
        num_csv = f"0{number}" if len(str(number)) != 2 else str(number)
        track_csv_path = f"../lololol/data/datasets/{name_dataset}/data/" + num_csv + "_tracks.csv"
        track_meta_csv_path = f"../lololol/data/datasets/{name_dataset}/data/" + num_csv + "_tracksMeta.csv"
        track_meta_recording = f"../lololol/data/datasets/{name_dataset}/data/" + num_csv + "_recordingMeta.csv"
        tracks_csv = read2_tracks_csv(track_csv_path, track_meta_csv_path, track_meta_recording)
        tracks_meta = read_csv(track_meta_csv_path)
        recording_meta = read_csv(
            f"../lololol/data/datasets/{name_dataset}/data/" + num_csv + "_recordingMeta.csv")
        for j,i in enumerate(tracks_csv):
            dist = create_distance_matrix(tracks_csv[i])
            d = {FRAME: tracks_csv[i][FRAME], 'dist': dist}
            l.append(d)
        with open(f"output1/{name_dataset}_" + num_csv + "_dataset.pickle", 'wb') as f:
            pickle.dump(l, f)

        #     l.extend(dist)
        # df = pd.DataFrame(l)
        # df.to_csv(f"output/{name_dataset}_" + num_csv + "_dataset.csv")

def run():
    if not os.path.exists("output1"):
        os.makedirs("output1")
    names_dataset = ['inD-dataset-v1.0', "rounD-dataset-v1.0"]
    print(type(names_dataset))
    for i in names_dataset:
        print(i)
        create_dataset(i)


if __name__ == '__main__':
    run()
