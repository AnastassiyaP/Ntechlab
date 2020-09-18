import json
import os
import sys
import torch
import numpy as np

from torchvision import models, transforms
from torch.nn import Linear
from torch.utils.data import Dataset
from PIL import Image


MODEL_PATH ="models/model.torch"

args = sys.argv
if len(args) == 1:
    print("Usage: python3 process.py /path/to/images")
    exit()

PATH = sys.argv[1]

model = models.resnet18(pretrained=False)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

model.fc = Linear(model.fc.in_features, 2)
model = model.to(device)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()

img_transform=transforms.Compose([
                           transforms.Resize((224, 224)),
                           transforms.ToTensor(),
                           transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
                       ])

class TestMaleFemaleDataset(Dataset):
    def __init__(self, path, transform=None):
        self.path=path
        self.transform = transform
        img_list = []
        length = 0
        for imgname in os.listdir(path):
            if imgname.endswith('jpg'):
                img_list.append(imgname)
                length +=1
        self.length = length
        self.img_list = img_list

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        if torch.is_tensor(index):
            index = index.tolist()
        image_name = self.img_list[index]
        img = Image.open(os.path.join(self.path, image_name))
        if self.transform:
            img = self.transform(img)

        return img, image_name, int(index)


dataset = TestMaleFemaleDataset(PATH, transform=img_transform )
dataloader = torch.utils.data.DataLoader(dataset, batch_size=64)

predictions = np.array([])
names = np.array([])

with torch.no_grad():
    for i, (x, name, _) in enumerate(dataloader):
        image = x.to(device)
        prediction = model(image)
        _, indices = torch.max(prediction, 1)

        names = np.append(names, name)
        predictions = np.append(predictions, indices.tolist())

predictions = ['male' if p==0 else 'female' for p in predictions]
answer = dict(zip(names,predictions))

with open('process_results.json', 'w') as file:
    json.dump(answer, file)


