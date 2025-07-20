import yaml
from ultralytics import YOLO
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()  # Required for Windows multiprocessing

    # Load a model
    model = YOLO("Models/yolov8n.pt")  # load a pretrained model (recommended for training)

    # Train the model
    results = model.train(data="/Users/jarvis/Desktop/project copy/datasets/robot/dataset.yaml", epochs=1, device="mps")
    #results = model.train(data=r"C:\Users\fhs\Desktop\Data analysis project\datasets\dataset.yaml", epochs=1, batch=2, device="cuda:0", half=True)
    
