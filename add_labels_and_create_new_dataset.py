import numpy as np
from read_data import *
import os
import pandas as pd


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
    start_heading = headingg(start_heading)
    end_heading = headingg(end_heading)

    angle_to_goal = np.diff(np.unwrap([start_heading, end_heading]))[0]
    # first = np.pi / 8
    # second = np.pi / 3
    # third = np.pi * 3 / 4
    #np.pi/8
    third = np.pi / 3
    second = np.pi / 6
    first = np.pi / 12
    if -first < angle_to_goal < first:
        a = 'straight-on'
        if Xstart == Xend and Ystart == Yend:
            a = 'still'
        elif startLONVELOCITY > endLONVELOCITY:
            a = 'faster'
        elif startLONVELOCITY < endLONVELOCITY:
            a = 'slower'
        else:
            a = 'constant-speed'
    elif first <= angle_to_goal < second:
        a = 'easy-turn-right'

    elif second <= angle_to_goal:
        a = 'turn-right'
    elif -first >= angle_to_goal > -second:
        a = 'easy-turn-left'

    elif - second >= angle_to_goal:
        a = 'turn-left'

    return a

def preprocing_label(track):
    count_frames = len(track[HEADING])
    labels = []
    frame_rate = int(track[FRAME_RATE])
    for i in range(0, len(track[HEADING]), int(frame_rate)):

        if len(track[HEADING]) <= frame_rate:
            label = add_label(
                start_heading=track[HEADING][i],
                end_heading=track[HEADING][-1],
                startLONVELOCITY=track[LONVELOCITY][i],
                endLONVELOCITY=track[LONVELOCITY][-1],
                starLONACCELERATION=track[LONACCELERATION][-1],
                endLONACCELERATION=track[LONACCELERATION][-1],
                Xstart=track[X][i],
                Xend=track[X][-1],
                Ystart=track[Y][i],
                Yend=track[Y][-1],)
            d = {'label': label,
                 FRAME: track[FRAME][i],
                 CLASS:track[CLASS],
                 TRACK_ID: track[TRACK_ID]}
            labels.append(d)

            continue

        if i + frame_rate >= len(track[HEADING]):
            # labels.append(labels[-1])
            continue
        label = add_label(
            start_heading=track[HEADING][i],
            end_heading=track[HEADING][i + frame_rate],
            startLONVELOCITY=track[LONVELOCITY][i],
            endLONVELOCITY=track[LONVELOCITY][i + frame_rate],
            starLONACCELERATION=track[LONACCELERATION][i + frame_rate],
            endLONACCELERATION=track[LONACCELERATION][i + frame_rate],
            Xstart=track[X][i],
            Xend=track[X][i + frame_rate],
            Ystart=track[Y][i],
            Yend=track[Y][i + frame_rate],)
        d = {'label': label,
             FRAME: track[FRAME][i],
             CLASS:track[CLASS],
             TRACK_ID: track[TRACK_ID]}
        labels.append(d)
    return labels


def distance_all(df): # растояние между всеми точками на кадре
    from scipy.spatial.distance import cdist
    distance_matrix = cdist(df.values[:, 0:2], df.values[:, 0:2], 'euclidean')

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
        tracks_csv = read_tracks_csv(track_csv_path, track_meta_csv_path, track_meta_recording)
        tracks_meta = read_csv(track_meta_csv_path)
        recording_meta = read_csv(
            f"../lololol/data/datasets/{name_dataset}/data/" + num_csv + "_recordingMeta.csv")
        for j,i in enumerate(tracks_csv):
            print(i)
            labels = preprocing_label(tracks_csv[i])
            l.extend(labels)
        df = pd.DataFrame(l)
        df.to_csv(f"output/{name_dataset}_" + num_csv + "_dataset.csv")

def run():
    if not os.path.exists("output"):
        os.makedirs("output")
    total_change = 0
    #"rounD-dataset-v1.0",
    names_dataset = ['inD-dataset-v1.0', "rounD-dataset-v1.0"]

    print(type(names_dataset))
    for i in names_dataset:
        print(i)
        create_dataset(i)







if __name__ == '__main__':
    run()


"""
speed = v_lon
acceleration = a_lon
"""