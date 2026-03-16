import torch
import torch.nn as nn
from torchvision import models


def get_model(num_classes):
    """
    Loads pretrained ResNet50 and modifies final layer
    """

    model = models.resnet50(pretrained=True)

    # Replace final fully connected layer
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    return model