import time
import os

from IPython.display import clear_output

import numpy as np
import torch
from torch import nn, optim, cuda
from torchvision import transforms, datasets, models
from torch.utils.data import DataLoader
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt


BS = 32
RESIZE = 224
device = 'cpu'
if cuda.is_available():
    device_name = cuda.get_device_name(0)
    memory = cuda.get_device_properties(0).total_memory / (1024 ** 3)
    print(f"Device {device_name} has {memory} GB of memory")
    device = torch.device('cuda')
else:
    raise Exception("Cuda isn't available")
device
runs_dir = "runs"
os.makedirs(runs_dir, exist_ok=True)
existing_runs = [d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))]


if existing_runs:
    max_index = max([int(d.split("run")[1]) for d in existing_runs])
    new_run_index = max_index + 1
else:
    new_run_index = 1

current_run_dir = os.path.join(runs_dir, f"run{new_run_index}")
os.makedirs(current_run_dir, exist_ok=True)

train_stats_file = os.path.join(current_run_dir, "train_stats.txt")
test_stats_file = os.path.join(current_run_dir, "test_stats.txt")
best_model_weights_file = os.path.join(current_run_dir, "best.pth")
plot_file = os.path.join(current_run_dir, "plot.png")
def build_figures_with_same_x(figures, x_vals):
    n = len(figures)
    fig, axs = plt.subplots(n, 1)
    for idx, (fig_key, fig_value) in enumerate(figures.items()):
        for (plot_key, plot_value) in fig_value.items():
            # print(f"X and Y shape: {x_vals}\n{plot_value}")
            axs[idx].plot(x_vals, plot_value, label=plot_key)
        axs[idx].legend()
        axs[idx].grid(True)
        axs[idx].set_xticks(x_vals[::5])
        axs[idx].set_xticklabels(x_vals[::5], rotation=90)
        axs[idx].set_title(fig_key)

    plt.tight_layout()
    plt.show()
    plt.savefig(plot_file)
train_transform = transforms.Compose([
    transforms.Resize(RESIZE),
    transforms.ToTensor(),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    transforms.RandomAffine(degrees=25, translate=(0.25, 0.25), scale=(0.7, 1.3)),
    transforms.ConvertImageDtype(dtype=torch.float32),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


val_transform = transforms.Compose([
    transforms.Resize(RESIZE),
    transforms.ToTensor(),
    transforms.ConvertImageDtype(dtype=torch.float32),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

train_dataset = datasets.ImageFolder(root='./dataset/tr', transform=train_transform)
val_dataset = datasets.ImageFolder(root='./dataset/val', transform=val_transform)
test_dataset = datasets.ImageFolder(root='./dataset/test', transform=val_transform)

train_loader = DataLoader(train_dataset, batch_size=BS, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BS, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BS, shuffle=True)
# original_train_transform = transforms.Compose([
#     transforms.Resize(RESIZE),
#     transforms.ToTensor(),
#     transforms.ConvertImageDtype(dtype=torch.float32),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
# ])
# original_train_dataset = datasets.ImageFolder(root='./dataset/train_small', transform=original_train_transform)
# train_loader = DataLoader(train_dataset, batch_size=BS, shuffle=False)
# original_train_loader = DataLoader(original_train_dataset, batch_size=BS, shuffle=False)
# def show_original_and_augmented(original_images, augmented_images):
#     fig, axes = plt.subplots(8, 8, figsize=(16, 16))
#     for i in range(8):
#         for j in range(4):
#             axes[i, j*2].imshow(original_images[i*4 + j].permute(1, 2, 0))
#             axes[i, j*2].axis('off')
#             axes[i, j*2+1].imshow(augmented_images[i*4 + j].permute(1, 2, 0))
#             axes[i, j*2+1].axis('off')
#     plt.show()

# original_batch, augmented_batch = next(zip(original_train_loader, train_loader))

# show_original_and_augmented(original_batch[0], augmented_batch[0])

from collections import Counter

train_labels = train_dataset.targets
val_labels = val_dataset.targets
test_labels = test_dataset.targets

class_counts_train = Counter(train_labels)
class_counts_val = Counter(val_labels)
class_counts_test = Counter(test_labels)

print("Train Dataset Class Counts:")
for class_index, count in class_counts_train.items():
    class_name = train_dataset.classes[class_index]
    print(f"{class_name}: {count}")

print("Val Dataset Class Counts:")
for class_index, count in class_counts_val.items():
    class_name = val_dataset.classes[class_index]
    print(f"{class_name}: {count}")

print("Test Dataset Class Counts:")
for class_index, count in class_counts_test.items():
    class_name = test_dataset.classes[class_index]
    print(f"{class_name}: {count}")

try:
  if model:
    model.zero_grad()
    del model
    torch.cuda.empty_cache()
    print('model has been deleted')
except:
  print('model doesnt exist')
class CustomResNet34(nn.Module):
    def __init__(self, num_classes):
        super(CustomResNet34, self).__init__()
        self.resnet34 = models.resnet34(weights=models.ResNet34_Weights.DEFAULT)
        num_features = self.resnet34.fc.in_features
        self.resnet34.fc = nn.Linear(num_features, num_classes)

    def forward(self, x):
        return self.resnet34(x)

model = CustomResNet34(num_classes=2).to(device)
criterion = nn.CrossEntropyLoss()
model
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
num_epochs = 100
len_loader = len(train_loader)
x_vals = []
train_losses = []
val_losses = []
accuracy_list = []
precision_list = []
recall_list = []
f1_list = []

best_val_loss = float('inf')
best_val_accuracy = 0.0
best_epoch = 0
def train_epoch(model, train_loader, optimizer, criterion, device):
    running_loss = 0.0
    i = 0
    for batch_idx, (images, labels) in enumerate(train_loader):
        print(f"\r Train batch {batch_idx}/{len(train_loader)}", end='', flush=True)
        i += 1
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)

        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    return running_loss / len(train_loader)


def val_epoch(model, val_loader, criterion, device):
    model.eval()
    val_running_loss = 0.0
    true_labels = []
    predicted_labels = []
    with torch.no_grad():
        for batch_idx, (images, labels) in enumerate(val_loader):
            print(f"\r Val batch {batch_idx}/{len(val_loader)}", end='', flush=True)
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)
            val_running_loss += loss.item()
            predicted = torch.argmax(outputs, dim=1)

            predicted = torch.argmax(outputs, dim=1)
            true_labels.extend(labels.cpu().numpy())
            predicted_labels.extend(predicted.cpu().numpy())

        epoch_val_loss = val_running_loss / len(val_loader)
        val_losses.append(epoch_val_loss)
        f1 = f1_score(true_labels, predicted_labels)

    return (epoch_val_loss, f1)
start = time.time()
for epoch in range(num_epochs):
    print(f'\rEpoch: {epoch} / {num_epochs}')
    x_vals.append(epoch)


    epoch_train_loss = train_epoch(model, train_loader, optimizer, criterion, device)
    print(f"\nTrain loss: {epoch_train_loss}")
    train_losses.append(epoch_train_loss)


    epoch_val_loss, f1 = val_epoch(model, val_loader, criterion, device)
    f1_list.append(f1)

    if epoch_val_loss < best_val_loss:
        best_val_loss = epoch_val_loss
        best_val_f1 = f1
        best_epoch = epoch
        torch.save(model.state_dict(), best_model_weights_file)
        dur = time.time() - start
        with open(train_stats_file, "a") as f:
            f.write(f"Epoch {epoch + 1} / {num_epochs}: Train Loss: {epoch_train_loss}, Val Loss: {epoch_val_loss}, Val f1: {f1} Dur: {dur} Dur/Epoch: {dur / epoch if epoch != 0 else 0}\n")
    elif epoch > best_epoch + 10:
        print(f"\nTraining has stopped at {epoch} / {num_epochs} cuz val loss didn't decrease for {10} epochs")
        break


    clear_output(wait=True)
    build_figures_with_same_x({'Loss': {'Train loss': train_losses, 'Val loss': val_losses}, 'metrics': {'f1': f1_list}}, x_vals)
    print(train_losses)
    print(val_losses)
    print(f"f1: {f1}")

def denormalize(image):
    """Denormalize the image"""
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    # Ensure mean and std have the same shape as the image
    mean = np.array(mean)[None, :, None, None]
    std = np.array(std)[None, :, None, None]
    image = image * std + mean
    image = np.clip(image, 0, 1)
    return image


def show_8_images(images, labels, predictions, classes):
    fig, axes = plt.subplots(1, 8, figsize=(16, 4))
    for idx, img in enumerate(images):
        img = img[0]
        img = img.transpose((1, 2, 0))
        axes[idx].imshow(img)
        axes[idx].set_title(f"Pred: {classes[predictions[idx]]}\nReal: {classes[labels[idx]]}")
        axes[idx].axis('off')
    plt.show()


def test(model, test_loader, criterion, device):
    model.eval()
    test_running_loss = 0.0
    true_labels = []
    predicted_labels = []

    images_to_display = []
    labels_to_display  = []
    predictions_to_display  = []

    with torch.no_grad():
        for batch_idx, (images, labels) in enumerate(test_loader):
            print(f"\r Test batch {batch_idx}/{len(test_loader)}", end='', flush=True)
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)
            test_running_loss += loss.item()
            predicted = torch.argmax(outputs, dim=1)
            # print(f"\noutputs: {outputs}")
            # print(predicted)

            true_labels.extend(labels.cpu().numpy())
            predicted_labels.extend(predicted.cpu().numpy())

            for img, pred, label in zip(images, predicted, true_labels):
                denormalized_img = denormalize(img.cpu().numpy())
                images_to_display.append(denormalized_img)
                labels_to_display.append(label)
                predictions_to_display.append(pred)

                # print(len(images_to_display))

                if len(images_to_display) == 8:
                    show_8_images(images_to_display, labels_to_display, predictions_to_display, ['hotdog', 'not hotdog'])
                    images_to_display = []
                    labels_to_display = []
                    predictions_to_display = []

        test_loss = test_running_loss / len(test_loader)
        f1 = f1_score(true_labels, predicted_labels)

    return (test_loss, f1)

# best_model_weights_file = r'C:\Users\kuzga\OneDrive\Рабочий стол\sem4\hotdog_nothotdog\runs\run38\best.pth'
# model = CustomResNet34(num_classes=2).to(device)
# model.load_state_dict(torch.load(best_model_weights_file))

test_loss, test_f1 = test(model, test_loader, criterion, device)
res_str = f"Test loss: {test_loss}, test_f1: {test_f1}"
print(res_str)
with open(test_stats_file, "a") as f:
  f.write(res_str)
#10 epochs: Test Loss: 0.2050, Test Accuracy: 0.9193, Test Precision: 0.5031, Test Recall: 0.4503, Test F1-score: 0.4696
#50 epochs: Test Loss: 0.2354, Test Accuracy: 0.9022, Test Precision: 0.5031, Test Recall: 0.4379, Test F1-score: 0.4616



