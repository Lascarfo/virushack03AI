import torch

from torchvision import datasets, transforms, models
from torch.utils.data import Dataset, DataLoader, ConcatDataset
from PIL import Image
import torchvision
import os
from torch import nn
from collections import OrderedDict


class BenMalDataset(Dataset):
    def __init__(self, file_list, dir, mode='train', transform=None):
        self.file_list = file_list
        self.dir = dir
        self.mode = mode
        self.transform = transform
        if self.mode == 'train':
            if 'mal' in self.file_list[0]:
                self.label = 1
            else:
                self.label = 0

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        img = Image.open(os.path.join(self.dir, self.file_list[idx]))
        if self.transform:
            img = self.transform(img)
        if self.mode == 'train':
            img = img.numpy()
            return img.astype('float32'), self.label
        else:
            img = img.numpy()
            return img.astype('float32'), self.file_list[idx]


def convertToExpect(fn_list):
    exp_list = []
    for exp in fn_list:
        exp_list.append(1) if (exp[:1] == "m") else exp_list.append(0)
    return exp_list



def check_mole():
    model = models.resnet18(pretrained=True)
    model
    fc = nn.Sequential(OrderedDict([
        ('fc1', nn.Linear(512, 100)),
        ('relu', nn.ReLU()),
        ('fc2', nn.Linear(100, 2)),
        ('output', nn.LogSoftmax(dim=1))
    ]))

    model.fc = fc
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    device = 'cpu'
    test_dir = './test/'
    test_files = os.listdir(test_dir)

    model_load = torch.load("GPU_trained_model1_0.pth", map_location=torch.device('cpu'))
    model.load_state_dict(model_load)
    # model.min_eer_dist = 0.2  # edit this
    test_transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor()
    ])
    testset = BenMalDataset(test_files, test_dir, mode='test', transform=test_transform)
    testloader = DataLoader(testset, batch_size=64, shuffle=False, num_workers=4)
    model.eval()
    fn_list = []
    pred_list = []

    loader = testloader

    for x, fn in loader:
        with torch.no_grad():
            x = x.to(device)
            output = model(x)
            pred = torch.argmax(output, dim=1)
            fn_list += [(n[:1] + n[4:-4]) for n in fn]
            pred_list += [p.item() for p in pred]  # предсказанные значения (массивы содержащие 0 и 1)
            exp_list = convertToExpect(fn_list)  # настоящие значения (0 — нет опухоли, 1 — есть опухоль)




    # precision = precision_score(exp_list, pred_list)
    # recall = recall_score(exp_list, pred_list)
    # roc_auc = roc_auc_score(exp_list, pred_list)

    # return precision, recall, roc_auc
    print(pred_list)
    return pred_list[0]