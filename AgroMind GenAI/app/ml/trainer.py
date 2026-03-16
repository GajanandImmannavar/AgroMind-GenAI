# import torch
# import torch.nn as nn
# import torch.optim as optim

# from sklearn.metrics import (
#     accuracy_score,
#     f1_score,
#     confusion_matrix,
#     classification_report
# )

# from app.models.multimodal_model import MultimodalCropModel


# def train_model(train_loader, val_loader, classes,
#                 epochs, learning_rate, device):

#     num_classes = len(classes)

#     # ✅ CHECK CLASS COUNT
#     print("\nNumber of classes used for training:", num_classes)

#     model = MultimodalCropModel(num_classes).to(device)

#     criterion = nn.CrossEntropyLoss()
#     optimizer = optim.Adam(model.parameters(), lr=learning_rate)

#     best_accuracy = 0
#     patience = 3
#     counter = 0

#     # 🔹 Phase 1: Freeze backbone
#     for param in model.backbone.parameters():
#         param.requires_grad = False

#     print("\n🚀 Training Started\n")

#     for epoch in range(epochs):

#         if epoch == 3:
#             print("🔓 Unfreezing backbone for fine-tuning")
#             for param in model.backbone.parameters():
#                 param.requires_grad = True

#         model.train()
#         train_preds = []
#         train_true = []
#         running_loss = 0.0

#         for images, weather, labels in train_loader:

#             images = images.to(device)
#             weather = weather.to(device)
#             labels = labels.to(device)

#             optimizer.zero_grad()
#             outputs = model(images, weather)
#             loss = criterion(outputs, labels)

#             loss.backward()
#             optimizer.step()

#             running_loss += loss.item() * images.size(0)

#             preds = torch.argmax(outputs, dim=1)
#             train_preds.extend(preds.cpu().numpy())
#             train_true.extend(labels.cpu().numpy())

#         train_loss = running_loss / len(train_loader.dataset)
#         train_accuracy = accuracy_score(train_true, train_preds)

#         model.eval()
#         val_preds = []
#         val_true = []

#         with torch.no_grad():
#             for images, weather, labels in val_loader:

#                 images = images.to(device)
#                 weather = weather.to(device)
#                 labels = labels.to(device)

#                 outputs = model(images, weather)
#                 preds = torch.argmax(outputs, dim=1)

#                 val_preds.extend(preds.cpu().numpy())
#                 val_true.extend(labels.cpu().numpy())

#         accuracy = accuracy_score(val_true, val_preds)
#         f1 = f1_score(val_true, val_preds, average="weighted")

#         cm = confusion_matrix(val_true, val_preds)

#         print(f"\n📘 Epoch [{epoch+1}/{epochs}]")
#         print(f"Train Loss: {train_loss:.4f}")
#         print(f"Train Accuracy: {train_accuracy:.4f}")

#         print(f"\n📊 Validation Accuracy: {accuracy:.4f}")
#         print(f"📊 Validation F1 Score: {f1:.4f}")

#         print("\n📄 Classification Report:")
#         print(classification_report(
#             val_true,
#             val_preds,
#             target_names=classes,
#             zero_division=0
#         ))

#         print("\n📊 Confusion Matrix Shape:", cm.shape)
#         print(cm)
#         print("-" * 60)

#         if accuracy > best_accuracy:
#             best_accuracy = accuracy
#             counter = 0
#             torch.save(model.state_dict(), "app/models/best_agri_model.pth")
#             print("✅ Best model saved")
#         else:
#             counter += 1
#             if counter >= patience:
#                 print("⛔ Early stopping triggered")
#                 break

#     print("\n🎯 Training Complete")



# pause/play 




import torch
import torch.nn as nn
import torch.optim as optim
import os  # ✅ ADDED: Needed to check if checkpoint exists

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from app.models.multimodal_model import MultimodalCropModel


def train_model(train_loader, val_loader, classes,
                epochs, learning_rate, device):

    num_classes = len(classes)

    # ✅ CHECK CLASS COUNT
    print("\nNumber of classes used for training:", num_classes)

    model = MultimodalCropModel(num_classes).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    best_accuracy = 0
    patience = 3
    counter = 0

    # 🔹 Phase 1: Freeze backbone
    for param in model.backbone.parameters():
        param.requires_grad = False

    # ✅ NEW: Check if a resume checkpoint exists
    checkpoint_path = "app/models/resume_checkpoint.pth"
    start_epoch = 0
    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path, map_location=device)
        model.load_state_dict(checkpoint["model_state_dict"])
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        start_epoch = checkpoint["epoch"]
        best_accuracy = checkpoint["best_accuracy"]
        counter = checkpoint["counter"]
        print(f"Resuming training from epoch {start_epoch+1}")

    print("\n Training Started\n")

    # ✅ UPDATED: Loop from start_epoch to handle resume
    for epoch in range(start_epoch, epochs):

        if epoch == 3:
            print(" Unfreezing backbone for fine-tuning")
            for param in model.backbone.parameters():
                param.requires_grad = True

        model.train()
        train_preds = []
        train_true = []
        running_loss = 0.0

        for images, weather, labels in train_loader:

            images = images.to(device)
            weather = weather.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images, weather)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)

            preds = torch.argmax(outputs, dim=1)
            train_preds.extend(preds.cpu().numpy())
            train_true.extend(labels.cpu().numpy())

        train_loss = running_loss / len(train_loader.dataset)
        train_accuracy = accuracy_score(train_true, train_preds)

        model.eval()
        val_preds = []
        val_true = []

        with torch.no_grad():
            for images, weather, labels in val_loader:

                images = images.to(device)
                weather = weather.to(device)
                labels = labels.to(device)

                outputs = model(images, weather)
                preds = torch.argmax(outputs, dim=1)

                val_preds.extend(preds.cpu().numpy())
                val_true.extend(labels.cpu().numpy())

        accuracy = accuracy_score(val_true, val_preds)
        f1 = f1_score(val_true, val_preds, average="weighted")

        cm = confusion_matrix(val_true, val_preds)

        print(f"\n Epoch [{epoch+1}/{epochs}]")
        print(f"Train Loss: {train_loss:.4f}")
        print(f"Train Accuracy: {train_accuracy:.4f}")

        print(f"\n Validation Accuracy: {accuracy:.4f}")
        print(f" Validation F1 Score: {f1:.4f}")

        print("\n Classification Report:")
        print(classification_report(
            val_true,
            val_preds,
            target_names=classes,
            zero_division=0
        ))

        print("\n Confusion Matrix Shape:", cm.shape)
        print(cm)
        print("-" * 60)

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            counter = 0
            torch.save(model.state_dict(), "app/models/best_agri_model.pth")
            print(" Best model saved")
        else:
            counter += 1
            if counter >= patience:
                print(" Early stopping triggered")
                break

        # ✅ NEW: Save checkpoint every epoch to enable pause/resume
        checkpoint = {
            "epoch": epoch + 1,  # next epoch to run
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "best_accuracy": best_accuracy,
            "counter": counter
        }
        torch.save(checkpoint, checkpoint_path)

    print("\n Training Complete")