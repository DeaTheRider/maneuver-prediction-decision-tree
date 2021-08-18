# https://github.com/RobertKrajewski/highD-dataset

import pandas
import numpy as np

BBOX = "bbox"
FRAMES = "frames"

#Recording Meta Information
RECORDING_ID = "recordingId"
LOCATION_ID = "locationId"
FRAME_RATE = "frameRate"
SPEED_LIMIT = "speedLimit"
WEEKDAY = "weekday"
START_TIME = "startTime"
DURATION = "duration"
NUM_TRACKS = "numTracks"
NUMVEHICLES = "numVehicles"
NUMVRUS = "numVRUs"
LATLOCATION = "latLocation"
LONLACTION = "lonLocation"
XUTMORIGIN = "xUtmOrigin"
YUTMORIGIN = "yUtmOrigin"
ORTHOPXTOMETER = "orthoPxToMeter"

#Meta Information
TRACK_ID = "trackId"
INITIALFRAME = "initialFrame"
FINALFRAME = "finalFrame"
NUMFRAMES = "numFrames"
WIDTH = "width"
LENGHT = "length"
CLASS = "class"

#Tracks
FRAME = "frame"
TRACKLIFETIME = "trackLifetime"
X = "xCenter"
Y = "yCenter"
HEADING = "heading"
X_VELOCITY = "xVelocity"
Y_VELOCITY = "yVelocity"
X_ACCELERATION = "xAcceleration"
Y_ACCELERATION = "yAcceleration"
LONVELOCITY = "lonVelocity"
LATVELOCITY = "latVelocity"
LONACCELERATION = "lonAcceleration"
LATACCELERATION = "latAcceleration"


def read_csv(track_csv_path):
    df = pandas.read_csv(track_csv_path)
    return df

def read_tracks_csv(track_csv_path, tracks_meta, track_meta_recording):
    df = read_csv(track_csv_path)
    tracks_meta_info = read_csv(tracks_meta)
    track_meta_recording_info = read_csv(track_meta_recording)
    frame_rate = track_meta_recording_info[FRAME_RATE].iloc[0]
    grouped = df.groupby([TRACK_ID], sort=False)
    tracks = {}
    current_track = 0
    for group_id, rows in grouped:
        class_ = tracks_meta_info[tracks_meta_info[TRACK_ID] == group_id][CLASS].iloc[0]
        bounding_boxes = np.transpose(np.array([rows[X].values,
                                                rows[Y].values,
                                                rows[WIDTH].values,
                                                rows[LENGHT].values]))
        tracks[np.int64(group_id)] = {
            TRACK_ID: group_id,
            FRAME: rows[FRAME].values,
            X: rows[X].values,
            Y: rows[Y].values,
            BBOX: bounding_boxes,
            X_VELOCITY: rows[X_VELOCITY].values,
            Y_VELOCITY: rows[Y_VELOCITY].values,
            X_ACCELERATION: rows[X_ACCELERATION].values,
            Y_ACCELERATION: rows[Y_ACCELERATION].values,
            TRACKLIFETIME: rows[TRACKLIFETIME].values,
            HEADING: rows[HEADING].values,
            LONVELOCITY: rows[LONVELOCITY].values,
            LATVELOCITY: rows[LATVELOCITY].values,
            LONACCELERATION: rows[LONACCELERATION].values,
            LATACCELERATION: rows[LATACCELERATION].values,
            CLASS: class_,
            FRAME_RATE: frame_rate,



        }
        current_track = current_track + 1
    return tracks


def read2_tracks_csv(track_csv_path, tracks_meta, track_meta_recording):
    df = read_csv(track_csv_path)
    tracks_meta_info = read_csv(tracks_meta)
    track_meta_recording_info = read_csv(track_meta_recording)
    frame_rate = track_meta_recording_info[FRAME_RATE].iloc[0]
    grouped = df.groupby([FRAME], sort=False)
    tracks = {}
    current_track = 0
    for group_id, rows in grouped:
        bounding_boxes = np.transpose(np.array([rows[X].values,
                                                rows[Y].values,
                                                rows[WIDTH].values,
                                                rows[LENGHT].values]))
        tracks[np.int64(group_id)] = {
            TRACK_ID: rows[TRACK_ID].values,
            FRAME: rows[FRAME].values,
            X: rows[X].values,
            Y: rows[Y].values,
            BBOX: bounding_boxes,
            X_VELOCITY: rows[X_VELOCITY].values,
            Y_VELOCITY: rows[Y_VELOCITY].values,
            X_ACCELERATION: rows[X_ACCELERATION].values,
            Y_ACCELERATION: rows[Y_ACCELERATION].values,
            TRACKLIFETIME: rows[TRACKLIFETIME].values,
            HEADING: rows[HEADING].values,
            LONVELOCITY: rows[LONVELOCITY].values,
            LATVELOCITY: rows[LATVELOCITY].values,
            LONACCELERATION: rows[LONACCELERATION].values,
            LATACCELERATION: rows[LATACCELERATION].values,


        }
        current_track = current_track + 1
    return tracks


def read_tracks_meta(tracks_meta_path):
    df = read_csv(tracks_meta_path)
    return df


def read_recording_meta(recording_meta_path):
    df = read_csv(recording_meta_path)
    return df
