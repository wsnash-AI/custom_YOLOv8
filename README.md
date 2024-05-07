# YOLOv8
All scripts and code I wrote for training, and using a YOLOv8 model
## Files
- `train_yoloV8.py`: Trains a YOLOv8 model of a dataset
- `yolo_model.py`: Using the trained model, on an local image, url of an image, or a video
- `convert_dataset_YOLOv8.py`: Converts the Label-Studio YOLO format to YOLOv8 format
- `fix_SRGB.sh`: (NEEDS image magick install) Fixes werid SRGB warning for pngs

# Guide
[How To Train YoloV8](https://blog.roboflow.com/how-to-train-yolov8-on-a-custom-dataset/)

# Yolov8 Commands
- Train: `yolo task=detect mode=train model=yolov8s.pt data=datasets/data.yaml epochs=200 imgsz=640`
- Validate: `yolo task=detect mode=val model=runs/detect/train5/weights/best.pt data=datasets/data.yaml`
- Predict: `yolo task=detect mode=predict model=runs/detect/train5/weights/best.pt conf=0.25 source=datasets/test/images/`

## Getting Dataset
1. Using label-studio, label images
2. Export the labels in `YOLO` format
3. Unzip the dataset
4. Run `convert_dataset_YOLOv8.py`
    1. Update `base_path` to be the path of the exported unzipped dataset
5. Move the updated dataset into the datasets folder


## Train on the Dataset
1. Python Virtual Envirnoment
    1. New Venv
        1. Run `python -m venv venv`
        2. Run `source venv/Scripts/activate`
    2. Existing
        1. Run `source venv/Scripts/activate`
2. Install requirements
    1. `pip install -r requirements.txt`
3. In `train_yolov8.py`. Update `data` to be the location of the new dataset
4. Run `python train_yoloV8.py`
    - If getting warning about SRGB, run `./fix_SRGB.sh`
5. In the `dataset/runs` there should be a new train folder, with te best.pt being the model


## Using the New Model
1. In `if __name__ == '__main__':` Change the model to be the path to the previously trained model
2. Methods
    - `.image()`: Provide a path to an image to get results shown (Does not save the detections photo)
    - `.image_url()`: Provide a url to an image (Does not save the detections photo)
    - `.video()`: Provide a video for the detection to be applied (Will save to a different file)
