import os

import cv2
import numpy as np


class DatasetAbstract:
    def load_video(self, path):
        cap = cv2.VideoCapture(path)
        frames = []
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = frame[:, :, [2, 1, 0]]
                frame = frame.astype('float64')
                frames.append(frame)
        finally:
            cap.release()
        return np.array(frames)

    def get_videos(self):
        pass
        # returns labels pd.df[video, label], videos[video, frame, x, y, c]


class UCF(DatasetAbstract):
    def __init__(self):
        self.dataset_name = 'UCF-101'
        self.data_path = os.path.abspath(os.path.join('../datasets', self.dataset_name))
        self.feature_path = os.path.abspath(os.path.join('../features/', self.dataset_name))

    def get_videos(self):
        # get video paths
        video_labels_paths = [(os.path.split(curr_path)[1], files) for curr_path, sub_dirs, files in os.walk(self.data_path)]
        video_labels_paths = [(label_tup[0], vid_path) for label_tup in video_labels_paths[1:] for vid_path in label_tup[1]]

        class VideoIterator:
            def __init__(self_iter, vlp):
                self_iter.video_labels_paths = vlp

            def __iter__(self_iter):
                self_iter.video_index = 0
                return self_iter

            def __next__(self_iter):
                if self_iter.video_index < len(video_labels_paths):
                    x = self_iter.video_labels_paths[self_iter.video_index]
                    self_iter.video_index += 1
                    return x[0], self.load_video(x[1])
                else:
                    raise StopIteration

        return iter(VideoIterator(video_labels_paths))
