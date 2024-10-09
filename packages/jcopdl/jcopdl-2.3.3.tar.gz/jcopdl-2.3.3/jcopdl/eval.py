import torch
from tqdm.auto import tqdm
from jcopdl.metrics import MiniBatchConfusionMatrix, MiniBatchAccuracy, MiniBatchMisclassified, MiniBatchRMSE, MiniBatchRSquared
from jcopdl.visualization import visualize_prediction_batch

__all__ = [
    "evaluate_confusion_matrix",
    "evaluate_accuracy",
    "evaluate_prediction"
]


@torch.no_grad()
def evaluate_confusion_matrix(dataloader, model, device, desc=""):
    model.eval()
    metric = MiniBatchConfusionMatrix()
    for feature, target in tqdm(dataloader, desc=desc.title(), leave=False):
        feature, target = feature.to(device), target.to(device)
        output = model(feature)
        metric.add_batch(output, target)
    return metric.compute()


@torch.no_grad()
def evaluate_accuracy(dataloader, model, device, desc=""):
    model.eval()
    metric = MiniBatchAccuracy()
    for feature, target in tqdm(dataloader, desc=desc.title(), leave=False):
        feature, target = feature.to(device), target.to(device)
        output = model(feature)
        metric.add_batch(output, target)
    return metric.compute()


@torch.no_grad()
def evaluate_rmse(dataloader, model, device, desc=""):
    model.eval()
    metric = MiniBatchRMSE()
    for feature, target in tqdm(dataloader, desc=desc.title(), leave=False):
        feature, target = feature.to(device), target.to(device)
        output = model(feature)
        metric.add_batch(output, target)
    return metric.compute()


@torch.no_grad()
def evaluate_r2(dataloader, model, device, desc=""):
    model.eval()
    metric = MiniBatchRSquared()
    for feature, target in tqdm(dataloader, desc=desc.title(), leave=False):
        feature, target = feature.to(device), target.to(device)
        output = model(feature)
        metric.add_batch(output, target)
    return metric.compute()


@torch.no_grad()
def evaluate_prediction(dataloader, model, device, viz_transform=None):
    model.eval()
    feature, target = next(iter(dataloader))
    feature, target = feature.to(device), target.to(device)
    output = model(feature)
    
    preds = output.argmax(1)
    classes = dataloader.dataset.classes
    if viz_transform is not None:
        feature = viz_transform(feature)
    image = visualize_prediction_batch(feature, target, preds, classes)
    return image


@torch.no_grad()
def evaluate_misclassified(dataloader, model, device, viz_transform=None, desc=""):
    model.eval()
    metric = MiniBatchMisclassified()
    for feature, target in tqdm(dataloader, desc=desc.title(), leave=False):
        feature, target = feature.to(device), target.to(device)
        output = model(feature)
        metric.add_batch(feature, output, target)
    feature, target, preds = metric.compute()

    if viz_transform is not None:
        feature = viz_transform(feature)
        
    classes = dataloader.dataset.classes
    misclassified = {}
    for i, c in enumerate(classes):
        mask = target == i
        misclassified[c] = visualize_prediction_batch(feature[mask], target[mask], preds[mask], classes)
    return misclassified