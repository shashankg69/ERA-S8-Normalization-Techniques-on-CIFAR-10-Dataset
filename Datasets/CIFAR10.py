import torch
from torchvision import datasets, transforms

from .dataset import DataSet


class CIFAR10(DataSet):
    mean = (0.49139968, 0.48215827, 0.44653124)
    std = (0.24703233, 0.24348505, 0.26158768)
    classes = None

    def get_train_loader(self):
        train_transforms = transforms.Compose([
            transforms.RandomHorizontalFlip(0.5),
            transforms.RandomGrayscale(0.1),
            transforms.RandomRotation((-7.0, 7.0)),
            transforms.RandomPerspective(0.3, 0.5),
            transforms.ToTensor(),
            transforms.Normalize(self.mean, self.std)
        ])
        train_data = datasets.CIFAR10('../data', train=True, download=True, transform=train_transforms)
        if self.classes is None:
            self.classes = {i: c for i, c in enumerate(train_data.classes)}
        self.train_loader = torch.utils.data.DataLoader(train_data, shuffle=True, **self.loader_kwargs)
        return self.train_loader

    def get_test_loader(self):
        test_transforms = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(self.mean, self.std)
        ])
        test_data = datasets.CIFAR10('../data', train=False, download=True, transform=test_transforms)
        self.test_loader = torch.utils.data.DataLoader(test_data, shuffle=True, **self.loader_kwargs)
        return self.test_loader

    def show_transform(self, img):
        return img.permute(1, 2, 0)