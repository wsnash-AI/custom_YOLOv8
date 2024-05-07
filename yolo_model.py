from io import BytesIO
import supervision as sv
import numpy as np
from ultralytics import YOLO
import requests
from PIL import Image


class UseModel:
    """
    YOLOv8 Ojbect Detection Class
    """

    def __init__(self, model):
        self.model = YOLO(model)

    def image_url(self, url):
        """Runs the model on an image from a URL

        :param string url: Url to the image
        """
        resp = requests.get(url, timeout=15)

        if resp.status_code != 200:
            print(f"Failed to download image: {url}")

        image = Image.open(BytesIO(resp.content))

        # original_width, original_height = image.size

        results = self.model.predict(image)
        # Process results list
        for result in results:
            result.show()  # display to screen

    def image(self, file):
        """Runs the model on an image from a local file

        :param string file: path to the image file
        """

        image = Image.open(file)

        # original_width, original_height = image.size

        results = self.model.predict(image)
        # Process results list
        for result in results:
            result.show()  # display to screen

    def __process_frame(self, frame: np.ndarray, _) -> np.ndarray:
        """Runs the model on a frame of a video

        :param np.ndarray frame:
        :return np.ndarray:
        """
        results = self.model(frame, imgsz=1280, verbose=False)[0]

        detections = sv.Detections.from_ultralytics(results)

        box_annotator = sv.BoundingBoxAnnotator(
            thickness=4)

        label_annotator = sv.LabelAnnotator(
            text_thickness=4, text_scale=2)

        labels = [
            self.model.model.names[class_id]
            for class_id
            in detections.class_id
        ]

        frame = box_annotator.annotate(
            scene=frame, detections=detections)

        frame = label_annotator.annotate(
            scene=frame, detections=detections, labels=labels)

        return frame

    def video(self, path):
        """Runs the model on a video

        :param string path: path to the video file
        """
        video_info = sv.VideoInfo.from_video_path(path)
        print(video_info)
        if video_info is None:
            print("Failed to load video")
            return
        sv.process_video(
            source_path=path,
            target_path=f"result.mp4",
            callback=self.__process_frame
        )


if __name__ == '__main__':
    ml = UseModel(model='./best.pt')
