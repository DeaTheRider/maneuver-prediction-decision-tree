import pandas as pd
import numpy as np
import os


def add_label(lane_id, lane_id_next, xAcceleration, xAcceleration_next, drivingDirection, x, x_next, y, y_next):

    if lane_id == lane_id_next:
        if x == x_next and y == y_next:
            label = 'still'
        elif xAcceleration == xAcceleration_next:
            label = 'constant-speed'
        elif xAcceleration > xAcceleration_next:
            label = 'slower'
        elif xAcceleration < xAcceleration_next:
            label = 'faster'
    # https://www.highd-dataset.com/format
    elif drivingDirection == 1: #left-to-right
        if lane_id > lane_id_next:
            label = 'lane-change-left'
        elif lane_id < lane_id_next:
            label = 'lane-change-right'
    elif drivingDirection == 2: #right-to-left
        if lane_id > lane_id_next:
            label = 'lane-change-right'
        elif lane_id < lane_id_next:
            label = 'lane-change-left'
    return label


def read_tracks_csv(track_csv_path, tracks_meta):
    df = pd.read_csv(track_csv_path)
    tracks_meta_info = pd.read_csv(tracks_meta)
    grouped = df.groupby(['id'], sort=False)
    tracks = {}
    current_track = 0
    for group_id, rows in grouped:
        class_ = tracks_meta_info[tracks_meta_info['id'] == group_id]['class'].iloc[0]
        bounding_boxes = np.transpose(np.array([rows['x'].values,
                                                rows['y'].values]))
        numLaneChanges = tracks_meta_info[tracks_meta_info['id'] == group_id]['numLaneChanges'].iloc[0]
        drivingDirection = tracks_meta_info[tracks_meta_info['id'] == group_id]['drivingDirection'].iloc[0]
        tracks[np.int64(group_id)] = {
            'frame': rows['frame'].values,
            'x': rows['x'].values,
            'y': rows['y'].values,
            'bbox': bounding_boxes,
            'xVelocity': rows['xVelocity'].values,
            'yVelocity': rows['yVelocity'].values,
            'xAcceleration': rows['xAcceleration'].values,
            'yAcceleration': rows['yAcceleration'].values,
            'class': class_,
            'laneId': rows['laneId'].values,
            'numLaneChanges': numLaneChanges,
            'drivingDirection': drivingDirection


        }
        current_track = current_track + 1
    return tracks


def create_dataset(name_dataset):
    for number in range(1, 61):
        print(number)
        num_csv = f"0{number}" if len(str(number)) != 2 else str(number)
        track_csv_path = f"../../lololol/data/datasets/{name_dataset}/data/" + num_csv + "_tracks.csv"
        track_meta_csv_path = f"../../lololol/data/datasets/{name_dataset}/data/" + num_csv + "_tracksMeta.csv"
        track = read_tracks_csv(track_csv_path, track_meta_csv_path)
        l = []
        name_column = ['id', 'frame', 'class', 'label']
        for track_id in track:
            count_frame = len(track[track_id]['frame'])
            for ind_frame in range(count_frame):
                if ind_frame == count_frame - 1:
                    continue

                else:
                    label = add_label(track[track_id]['laneId'][ind_frame],
                                      track[track_id]['laneId'][ind_frame + 1],
                                      track[track_id]['xAcceleration'][ind_frame],
                                      track[track_id]['xAcceleration'][ind_frame + 1],
                                      track[track_id]['drivingDirection'],
                                      track[track_id]['x'][ind_frame],
                                      track[track_id]['x'][ind_frame + 1],
                                      track[track_id]['y'][ind_frame],
                                      track[track_id]['y'][ind_frame + 1],
                                      )
                    frame_info = (track_id, track[track_id]['frame'][ind_frame], track[track_id]['class'], label)
                    l.append(frame_info)
        df = pd.DataFrame(data=l, columns=name_column)
        df.to_csv(f"output/{name_dataset}_" + num_csv + "_dataset_label.csv")


def run():
    if not os.path.exists("output"):
        os.makedirs("output")
    names_dataset = ['highd-dataset-v1.0']
    for i in names_dataset:
        print(i)
        create_dataset(i)

if __name__ == '__main__':
    run()
