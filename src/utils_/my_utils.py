import torch

def setup_yolo_model(model_name: str, weight_path: str):
    model = torch.hub.load('ultralytics/{}'.format(model_name), 'custom', path = weight_path)
    # Custom config here
    
    # ...
    return model