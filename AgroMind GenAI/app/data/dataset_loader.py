import os
import torch
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader, random_split
from app.data.preprocessing import get_train_transform, get_val_transform


class MultimodalDataset(torch.utils.data.Dataset):
    def __init__(self, dataset_path, transform):
        self.dataset = ImageFolder(dataset_path, transform=transform)

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        image, label = self.dataset[idx]

        # Dummy weather features (replace with real later)
        weather = torch.tensor([30.0, 70.0, 5.0], dtype=torch.float32)

        return image, weather, label


def create_dataloaders(dataset_path, batch_size, image_size, num_workers):

    train_transform = get_train_transform(image_size)
    val_transform = get_val_transform(image_size)

    full_dataset = MultimodalDataset(dataset_path, transform=train_transform)

    # ✅ CHECK CLASSES
    print("\nDetected Classes:", full_dataset.dataset.classes)
    print("Total Classes:", len(full_dataset.dataset.classes))

    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size

    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

    val_dataset.dataset.transform = val_transform

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers
    )

    classes = full_dataset.dataset.classes

    return train_loader, val_loader, classes