import pandas as pd
import numpy as np
import os
from scipy.spatial.distance import cdist


def distance_all(x, y): # растояние между всеми точками на кадре
    distance_matrix = cdist(x, y, 'euclidean')
    return distance_matrix

def create_dataset(name_dataset):
    for number in range(1, 61):
        print(number)
        num_csv = f"0{number}" if len(str(number)) != 2 else str(number)
        track_csv_path = f"../../lololol/data/datasets/{name_dataset}/data/" + num_csv + "_tracks.csv"
        track_meta_csv_path = f"../../lololol/data/datasets/{name_dataset}/data/" + num_csv + "_tracksMeta.csv"
        track_group = read_tracks_csv(track_csv_path, track_meta_csv_path)
        track = pd.read_csv(track_csv_path)
        column = ['id', 'frame', 'precedingXAcceleration', 'followingXAcceleration', 'followingXVelocity',
                  'leftPrecedingXAcceleration', 'leftPrecedingXVelocity',
                  'leftAlongsideXAcceleration', 'leftAlongsideXVelocity',
                  'leftFollowingXAcceleration', 'leftFollowingXVelocity',
                  'rightPrecedingXAcceleration', 'rightPrecedingXVelocity',
                  'rightAlsongsideXAcceleration', 'rightAlsongsideXVelocity',
                  'rightFollowingXAcceleration', 'rightFollowingXVelocity',
                  'precedingDist', 'followingDist', 'leftPrecedingDist',
                  'leftAlongsideDist', 'leftFollowingDist',
                  'rightPrecedingDist', 'rightAlsongsideDist',
                  'rightFollowingDist',
                  ]
        column_dist = ['precedingDist', 'followingDist', 'leftPrecedingDist', 'leftAlongsideDist', 'leftFollowingDist',
                       'rightPrecedingDist', 'rightAlsongsideDist', 'rightFollowingDist']
        column_check_dist = ['followingId', 'leftPrecedingId', 'leftAlongsideId', 'leftFollowingId', 'rightPrecedingId',
                             'rightAlongsideId', 'rightFollowingId', 'precedingId']
        l = []
        for frame in track_group:
            frame_info = track_group[frame]
            dist_matrix = distance_all(frame_info['bbox'], frame_info['bbox'])
            list_ids = frame_info['id']
            for j, track_id in enumerate(list_ids):
                # idx = np.where(classes == var)
                df = track[(track['id'] == track_id) & (track['frame'] == frame)]
                df = df[column_check_dist]
                followingId = df['followingId'].iloc[0]
                leftPrecedingId = df['leftPrecedingId'].iloc[0]
                leftAlongsideId = df['leftPrecedingId'].iloc[0]
                leftFollowingId = df['leftFollowingId'].iloc[0]
                rightPrecedingId = df['rightPrecedingId'].iloc[0]
                rightAlongsideId = df['rightAlongsideId'].iloc[0]
                rightFollowingId = df['rightFollowingId'].iloc[0]
                precedingId = df['precedingId'].iloc[0]
                if precedingId == 0:
                    precedingXAcceleration = 0
                    precedingDist = 0
                else:
                    idx = np.where(list_ids == precedingId)
                    precedingXAcceleration = frame_info['xAcceleration'][idx][0]
                    precedingDist = dist_matrix[j][idx][0]
                if followingId == 0:
                    followingXAcceleration = 0
                    followingXVelocity = 0
                    followingDist = 0
                else:
                    idx = np.where(list_ids == followingId)
                    followingXAcceleration = frame_info['xAcceleration'][idx][0]
                    followingXVelocity = frame_info['xVelocity'][idx][0]
                    followingDist = dist_matrix[j][idx][0]
                if leftPrecedingId == 0:
                    leftPrecedingXAcceleration = 0
                    leftPrecedingXVelocity = 0
                    leftPrecedingDist = 0
                else:
                    idx = np.where(list_ids == leftPrecedingId)
                    leftPrecedingXAcceleration = frame_info['xAcceleration'][idx][0]
                    leftPrecedingXVelocity = frame_info['xVelocity'][idx][0]
                    leftPrecedingDist = dist_matrix[j][idx][0]
                if leftAlongsideId == 0:
                    leftAlongsideXAcceleration = 0
                    leftAlongsideXVelocity = 0
                    leftAlongsideDist = 0
                else:
                    idx = np.where(list_ids == leftAlongsideId)
                    leftAlongsideXAcceleration = frame_info['xAcceleration'][idx][0]
                    leftAlongsideXVelocity = frame_info['xVelocity'][idx][0]
                    leftAlongsideDist = dist_matrix[j][idx][0]
                if leftFollowingId == 0:
                    leftFollowingXAcceleration = 0
                    leftFollowingXVelocity = 0
                    leftFollowingDist = 0
                else:
                    idx = np.where(list_ids == leftFollowingId)
                    leftFollowingXAcceleration = frame_info['xAcceleration'][idx][0]
                    leftFollowingXVelocity = frame_info['xVelocity'][idx][0]
                    leftFollowingDist = dist_matrix[j][idx][0]

                if rightPrecedingId == 0:
                    rightPrecedingXAcceleration = 0
                    rightPrecedingXVelocity = 0
                    rightPrecedingDist = 0
                else:
                    idx = np.where(list_ids == rightPrecedingId)
                    rightPrecedingXAcceleration = frame_info['xAcceleration'][idx][0]
                    rightPrecedingXVelocity = frame_info['xVelocity'][idx][0]
                    rightPrecedingDist = dist_matrix[j][idx][0]

                if rightAlongsideId == 0:
                    rightAlsongsideXAcceleration = 0
                    rightAlsongsideXVelocity = 0
                    rightAlsongsideDist = 0
                else:
                    idx = np.where(list_ids == rightAlongsideId)
                    rightAlsongsideXAcceleration = frame_info['xAcceleration'][idx][0]
                    rightAlsongsideXVelocity = frame_info['xVelocity'][idx][0]
                    rightAlsongsideDist = dist_matrix[j][idx][0]

                if rightFollowingId == 0:
                    rightFollowingXAcceleration = 0
                    rightFollowingXVelocity = 0
                    rightFollowingDist = 0
                else:
                    idx = np.where(list_ids == rightFollowingId)
                    rightFollowingXAcceleration = frame_info['xAcceleration'][idx][0]
                    rightFollowingXVelocity = frame_info['xVelocity'][idx][0]
                    rightFollowingDist = dist_matrix[j][idx][0]


                frame_distt_info = (track_id, frame, precedingXAcceleration, followingXAcceleration, followingXVelocity,
                                    leftPrecedingXAcceleration, leftPrecedingXVelocity, leftAlongsideXAcceleration,
                                    leftAlongsideXVelocity, leftFollowingXAcceleration, leftFollowingXVelocity,
                                    rightPrecedingXAcceleration, rightPrecedingXVelocity, rightAlsongsideXAcceleration,
                                    rightAlsongsideXVelocity, rightFollowingXAcceleration, rightFollowingXVelocity,
                                    precedingDist, followingDist, leftPrecedingDist, leftAlongsideDist, leftFollowingDist,
                                    rightPrecedingDist, rightAlsongsideDist, rightFollowingDist)

                l.append(frame_distt_info)
        df = pd.DataFrame(data=l, columns=column)
        df.to_csv(f"output2/{name_dataset}_" + num_csv + "_dataset_concat_dist.csv")


def read_tracks_csv(track_csv_path, tracks_meta):
    df = pd.read_csv(track_csv_path)
    tracks_meta_info = pd.read_csv(tracks_meta)
    grouped = df.groupby(['frame'], sort=False)
    tracks = {}
    current_track = 0
    for group_id, rows in grouped:
        bounding_boxes = np.transpose(np.array([rows['x'].values,
                                                rows['y'].values]))

        tracks[np.int64(group_id)] = {
            'id': rows['id'].values,
            'track_id': group_id,
            # 'x': rows['x'].values,
            # 'y': rows['y'].values,
            'bbox': bounding_boxes,
            'xVelocity': rows['xVelocity'].values,
            'yVelocity': rows['yVelocity'].values,
            'xAcceleration': rows['xAcceleration'].values,
            'yAcceleration': rows['yAcceleration'].values,



        }
        current_track = current_track + 1
    return tracks

def run():
    if not os.path.exists("output2"):
        os.makedirs("output2")
    names_dataset = ['highd-dataset-v1.0']
    for i in names_dataset:
        print(i)
        create_dataset(i)

if __name__ == '__main__':
    run()