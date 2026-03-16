import torch
import torch.nn as nn
from torchvision.models import efficientnet_b2, EfficientNet_B2_Weights


class MultimodalCropModel(nn.Module):
    def __init__(self, num_classes):
        super().__init__()

        # 🔹 Load pretrained EfficientNet-B2
        weights = EfficientNet_B2_Weights.DEFAULT
        self.backbone = efficientnet_b2(weights=weights)

        # Remove original classifier
        in_features = self.backbone.classifier[1].in_features
        self.backbone.classifier = nn.Identity()

        # 🔹 Weather branch
        self.weather_fc = nn.Sequential(
            nn.Linear(3, 32),
            nn.ReLU(),
            nn.Dropout(0.3)
        )

        # 🔹 Final classifier
        self.classifier = nn.Sequential(
            nn.Linear(in_features + 32, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, image, weather):

        image_features = self.backbone(image)
        weather_features = self.weather_fc(weather)

        combined = torch.cat((image_features, weather_features), dim=1)

        output = self.classifier(combined)
        return output