from ultralytics import YOLO
# import torch

# device = 'cuda' if torch.cuda.is_available() else 'cpu'
# print(f'Using device: {device}')

# Load a new or pre-trained model
model = YOLO("yolov8s.pt")
# model = YOLO('path/to/pretrained_model.pt') # For a pre-trained model

# Train the model
model.train(
    data='datasets/dataset_1/data.yaml',
    epochs=3,
    imgsz=640,
    device='cpu',
)
