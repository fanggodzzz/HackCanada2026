import os
import torch
import torch.nn as nn
import torch.optim as optim

from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split

def remove_empty_classes(dataset_dir):
    """
    Remove class folders that contain no valid images
    """
    valid_ext = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tif', '.tiff')

    for folder in os.listdir(dataset_dir):
        path = os.path.join(dataset_dir, folder)

        if os.path.isdir(path):
            files = [f for f in os.listdir(path) if f.lower().endswith(valid_ext)]

            if len(files) == 0:
                print(f"Removing empty class folder: {folder}")
                os.rmdir(path)


def train_model():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, "dataset")

    if not os.path.exists(dataset_dir):
        print("Dataset folder not found.")
        return

    # Remove empty dataset folders
    remove_empty_classes(dataset_dir)

    # Image preprocessing
    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(20),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485,0.456,0.406],
            std=[0.229,0.224,0.225]
        )
    ])

    # Load dataset
    full_dataset = datasets.ImageFolder(dataset_dir, transform=transform)

    if len(full_dataset) == 0:
        print("No images found in dataset.")
        return

    print("Classes:", full_dataset.classes)
    print("Total images:", len(full_dataset))

    # Split dataset
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size

    train_dataset, val_dataset = random_split(
        full_dataset,
        [train_size, val_size]
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=32,
        shuffle=True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=32
    )

    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    # Load pretrained ResNet18
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(full_dataset.classes))

    model = model.to(device)

    # Loss + optimizer
    criterion = nn.CrossEntropyLoss()

    optimizer = optim.Adam(
        model.parameters(),
        lr=0.001
    )

    epochs = 10

    for epoch in range(epochs):

        model.train()

        train_loss = 0
        correct = 0
        total = 0

        for images, labels in train_loader:

            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(images)

            loss = criterion(outputs, labels)

            loss.backward()

            optimizer.step()

            train_loss += loss.item()

            _, predicted = torch.max(outputs, 1)

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        train_acc = correct / total

        # Validation
        model.eval()

        val_loss = 0
        correct = 0
        total = 0

        with torch.no_grad():

            for images, labels in val_loader:

                images = images.to(device)
                labels = labels.to(device)

                outputs = model(images)

                loss = criterion(outputs, labels)

                val_loss += loss.item()

                _, predicted = torch.max(outputs, 1)

                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        val_acc = correct / total

        print(
            f"Epoch {epoch+1}/{epochs} "
            f"- Train Loss: {train_loss:.4f} "
            f"Acc: {train_acc:.4f} "
            f"| Val Loss: {val_loss:.4f} "
            f"Acc: {val_acc:.4f}"
        )

    # Save model
    model_path = os.path.join(base_dir, "model.pt")

    torch.save(model.state_dict(), model_path)

    print("Model saved to:", model_path)


if __name__ == "__main__":
    train_model()