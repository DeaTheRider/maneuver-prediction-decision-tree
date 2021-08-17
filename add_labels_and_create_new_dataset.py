import numpy as np
from read_data import *
import os


def headingg(heading):
    heading = np.deg2rad(heading)
    heading = np.unwrap([0, heading])[1]
    return heading


def add_label(start_heading,
              end_heading,
              startLONVELOCITY,
              endLONVELOCITY,
              starLONACCELERATION,
              endLONACCELERATION,
              Xstart,
              Xend,
              Ystart,
              Yend):
    start_heading = headingg(start_frame)
    end_heading = headingg(endframe)

    angle_to_goal = np.diff(np.unwrap([start_heading, end_heading]))[0]

    if -np.pi / 8 < angle_to_goal < np.pi / 8:
        a = 'straight-on'
        if Xstart == Xend and Ystart == Yend:
            a = 'still'
        elif startLONVELOCITY > endLONVELOCITY:
            a = 'faster'
        elif startLONVELOCITY < endLONVELOCITY:
            a = 'slower'
        else:
            a = 'constant-speed'
    elif np.pi / 8 <= angle_to_goal < np.pi / 3:
        a = 'easy-turn-right'
    elif np.pi / 3 <= angle_to_goal < np.pi * 3 / 4:
        a = 'turn-right'
    elif -np.pi / 8 >= angle_to_goal > -np.pi / 3:
        a = 'easy-turn-left'
    elif -np.pi / 3 >= angle_to_goal > np.pi * -3 / 4:
        a = 'turn-left'

    return a

def preprocing_label(track):
    count_frames = len(track[HEADING])
    labels = []
    for i, j in enumerate(track[HEADING]):
        if i == count_frames - 1:
            labels.append(labels[-1])
            continue
        label = add_label(
            start_heading=track[HEADING][i],
            end_heading=track[HEADING][i + 1],
            startLONVELOCITY=track[LONVELOCITY][i],
            endLONVELOCITY=track[LONVELOCITY][i + 1],
            starLONACCELERATION=track[LONACCELERATION][i + 1],
            endLONACCELERATION=track[LONACCELERATION][i + 1]
            Xstart=track[X][i],
            Xend=track[X][i + 1],
            Ystart=track[Y][i],
            Yend==track[y][i + 1]

        )
        d = {'label': label, FRAME: track[FRAME][i], CLASS:track[CLASS][0], TRACK_ID: track[TRACK_ID][i}
        labels.append(d)
    return labels


def distance_all(df): # растояние между всеми точками на кадре
    from scipy.spatial.distance import cdist
    distance_matrix = cdist(df.values[:, 0:2], df.values[:, 0:2], 'euclidean')

def run():
    if not os.path.exists("output"):
        os.makedirs("output")
    total_change = 0
    for number in range(1):
        num_csv = f"0{number}" if len(str(number)) != 2 else str(number)
        track_csv_path = "../lololol/data/datasets/rounD-dataset-v1.0/data/" + num_csv + "_tracks.csv"
        track_meta_csv_path = "../lololol/data/datasets/rounD-dataset-v1.0/data/" + num_csv + "_tracksMeta.csv"
        tracks_csv = read_tracks_csv(track_csv_path, track_meta_csv_path)
        tracks_meta = read_csv(track_meta_csv_path)
        recording_meta = read_csv(
            "../lololol/data/datasets/rounD-dataset-v1.0/data/" + num_csv + "_recordingMeta.csv")
        l = []
        for i in tracks_csv:
            labels = preprocing_label(tracks_csv[i])




if __name__ == '__main__':
    run()


"""
speed = v_lon
acceleration = a_lon
"""