import torch
from app.data.dataset_loader import create_dataloaders
from app.ml.trainer import train_model


DATASET_PATH = r"C:\Users\ADMIN\Desktop\AgroMind GenAI\app\dataset\train"

BATCH_SIZE = 8
EPOCHS = 8
IMAGE_SIZE = 192
NUM_WORKERS = 2
LEARNING_RATE = 0.0005


def main():

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    train_loader, val_loader, classes = create_dataloaders(
        dataset_path=DATASET_PATH,
        batch_size=BATCH_SIZE,
        image_size=IMAGE_SIZE,
        num_workers=NUM_WORKERS
    )

    train_model(
        train_loader=train_loader,
        val_loader=val_loader,
        classes=classes,
        epochs=EPOCHS,
        learning_rate=LEARNING_RATE,
        device=device
    )


if __name__ == "__main__":
    main()