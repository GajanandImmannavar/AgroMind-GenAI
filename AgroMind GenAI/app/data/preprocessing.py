from torchvision import transforms


def get_train_transform(image_size):
    return transforms.Compose([

        transforms.RandomResizedCrop(
            image_size,
            scale=(0.6, 1.0),
            ratio=(0.75, 1.33)
        ),

        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.4),
        transforms.RandomRotation(30),

        transforms.RandomPerspective(
            distortion_scale=0.4,
            p=0.3
        ),

        transforms.ColorJitter(
            brightness=0.4,
            contrast=0.4,
            saturation=0.4,
            hue=0.08
        ),

        transforms.RandomApply(
            [transforms.GaussianBlur(kernel_size=3)],
            p=0.2
        ),

        transforms.RandomGrayscale(p=0.1),

        transforms.ToTensor(),

        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])


def get_val_transform(image_size):
    return transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])