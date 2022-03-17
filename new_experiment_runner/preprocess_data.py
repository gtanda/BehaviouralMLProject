"""
:Date: 2022-02-28
:Author: Quin Adam
:Description: Extracts features from a frame
"""
import multiprocessing as mp
import os

import pandas as pd
from tensorflow import keras
import tensorflow as tf

from feature_extractors_config import MovenetExtractor
import datasets_config

tf.compat.v1.disable_eager_execution()

FILE_NAME = 'test'
FEATURE_EXTRACTOR = MovenetExtractor()
DATASET = datasets_config.UCF()


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
    for idx, video_info in enumerate(DATASET.get_video_information()):
        if idx > 3:
            break

        # Gather all its frames and add a batch dimension.
        frames = video_info['frames']

        temp_frame_features = pd.DataFrame()
        # display progress
        # TODO: uncomment
        # print(f'Extracting features of video: {idx}/{DATASET.num_videos}, {100 * idx / DATASET.num_videos:.2f}% done')
        print(f'Extracting features of video: {idx}')

        # Extract features from the frames of the current video.
        video_length = len(frames)
        for frame in frames:
            extracted_features = FEATURE_EXTRACTOR.pre_process_features(frame[None, ...])
            features_df = pd.DataFrame(data=tf.keras.layers.Flatten()(extracted_features).numpy())
            temp_frame_features = pd.concat((temp_frame_features, features_df), ignore_index=True)

        temp_frame_features = pd.DataFrame(
            data={'video': video_info['name'], 'label': video_info['label'], 'frame': range(video_length), **temp_frame_features})
        frame_features = pd.concat((frame_features, temp_frame_features), copy=False)

    return frame_features


def save_data(extracted_frame_pd):
    dir_path = os.path.join(DATASET.features_save_path, str(type(FEATURE_EXTRACTOR)).split('.')[-1][:-2])
    try:
        os.mkdir(dir_path)
    except:
        pass
    finally:
        extracted_frame_pd.to_csv(os.path.join(dir_path, FILE_NAME+'.zip'), index=False,
                                  compression=dict(method='zip', archive_name=FILE_NAME+'.csv'))


def prepare_all_videos_parallel():
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

    # initiallize multiprocessing pool
    pool = mp.pool.ThreadPool(1)

    with tf.device('/CPU:0'):
        videos_iterator = pool.imap_unordered(prepare_one_video_parallel, DATASET.get_video_information(), chunksize=1)

        for idx, temp_frame_features in enumerate(videos_iterator):
            print('finished video:', idx+1)
            frame_features = pd.concat((frame_features, temp_frame_features), copy=False)

    return frame_features


    # # # For each video, get features
    # for idx, (label, video) in enumerate(DATASET.get_video_information()):
    #     # display progress
    #     # TODO: uncomment
    #     # print(f'Extracting features of video: {idx}/{DATASET.num_videos}, {100 * idx / DATASET.num_videos:.2f}% done')
    #     print(f'Extracting features of video: {idx}')
    #
    #     # Gather frames.
    #     frames = video['frames']
    #     res = prepare_one_batch_parallel(frames)
    #     res = tf.reshape(res, (res.shape[0], -1))
    #     temp_frame_features = pd.DataFrame(data=res.numpy())
    #     print('done')
    #
    #     temp_frame_features = pd.DataFrame(
    #         data={'video': video['name'], 'label': label, 'frame': range(len(frames)), **temp_frame_features})
    #     frame_features = pd.concat((frame_features, temp_frame_features), copy=False)
    #
    # return frame_features


def prepare_one_video_parallel(label_video):
    label = label_video[0]
    video = label_video[1]

    frames = video['frames']
    res = prepare_one_batch_parallel(frames)
    res = tf.reshape(res, (res.shape[0], -1))
    temp_frame_features = pd.DataFrame(data=res.numpy())

    temp_frame_features = pd.DataFrame(
        data={'video': video['name'], 'label': label, 'frame': range(len(frames)), **temp_frame_features})

    return temp_frame_features


@tf.function
def prepare_one_batch_parallel(frames):
    return tf.map_fn(FEATURE_EXTRACTOR.pre_process_features, tf.expand_dims(frames, axis=1),
                     fn_output_signature=tf.TensorSpec((1, 6, 56)),
                     parallel_iterations=2,
                     # swap_memory=True,
                     )


if __name__ == '__main__':
    print('Preparing Data')
    # prepare data
    features = prepare_all_videos_parallel()

    print('Saving Data')
    # save data
    save_data(features)

    # TODO: make more verbose
    print('DONE')
