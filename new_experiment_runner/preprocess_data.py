"""
:Date: 2022-02-28
:Author: Quin Adam
:Description: Extracts features from a frame
"""
import os

import cv2
import pandas as pd
import numpy as np
from tensorflow import keras
import tensorflow as tf

from feature_extractors_config import MovenetExtractor
import datasets_config

FEATURE_EXTRACTOR = MovenetExtractor()
DATASET = datasets_config.UCF()

# [label], [video,frame, x, y, channel]
# [video, label], [video, frames, features]]


# extract features from videos
def prepare_all_videos():
    # TODO: make docstring
    """
    description ...

    :parm p1: parameter description
    :type p1: parameter type
    :return: return description
    :rtype: return type
    """

    # pass frame_features into model
    frame_features = pd.DataFrame()

    # # For each video, get features
    for idx, (label, video) in enumerate(DATASET.get_video_information()):
        # Gather all its frames and add a batch dimension.
        frames = video['frames']

        temp_frame_features = pd.DataFrame()
        # display progress
        # TODO: uncomment
        # print(f'Extracting features of video: {idx}/{DATASET.num_videos}, {100 * idx / DATASET.num_videos:.2f}% done')

        # Extract features from the frames of the current video.
        video_length = len(frames)
        for frame in frames:
            extracted_features = FEATURE_EXTRACTOR.pre_process_features(frame[None, ...])
            features_df = pd.DataFrame(data=tf.keras.layers.Flatten()(extracted_features).numpy())
            temp_frame_features = pd.concat((temp_frame_features, features_df), ignore_index=True)

        temp_frame_features = pd.DataFrame(
            data={'video': video['name'], 'label': label, 'frame': range(video_length), **temp_frame_features})
        frame_features = pd.concat((frame_features, temp_frame_features))

    return frame_features


# TODO: uncomment
# def save_data(extracted_frame_pd):
#     extracted_frame_pd.to_csv(datasets.save_file_path, index=False)

if __name__ == '__main__':
    print('Preparing Data')
    # prepare data
    features = prepare_all_videos()

    # TODO: uncomment
    # # save data
    # save_data(features)
