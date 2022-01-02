import torch 
import cv2
import torchvision.transforms as transforms
import numpy as np
from PIL import Image

def converFace(model, image):
    transform = transforms.Compose([
        transforms.Resize((256, 256), Image.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    data = {"A_paths":"", "B_paths": ""}

    data['A'] = torch.unsqueeze(transform(image), 0)
    data['B'] = torch.unsqueeze(transform(image), 0)
    model.set_input(data)  # unpack data from data loader
    model.test()           # run inference
    visuals = model.get_current_visuals()  # get image results
    fake = visuals['fake_B'].squeeze(0).cpu().numpy()
    fake = np.swapaxes(fake,0,1)
    fake = np.swapaxes(fake,1,2)
    return fake
