import torch
import torch.nn.functional as F
import numpy as np
from scipy.sparse import coo_matrix
from sklearn.metrics import f1_score
from jcopdl.utils.logits_sampling import greedy_sampling_from_logits

class MiniBatchBinaryConfusionMatrix():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F) / (N,)
        batch_targets: (N,)
        """
        if batch_preds.ndim == 2:
            batch_preds = batch_preds.argmax(1)
        
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)

    @torch.no_grad()    
    def compute(self):
        """
         |0_|1_|
        0|__|__|
        1|__|__|
        """
        yp = torch.cat(self.y_pred)
        yt = torch.cat(self.y_true)
        
        fn = ((yt == 1) & (yp == 0)).sum().item()
        tp = ((yt == 1) & (yp == 1)).sum().item()
        fp = ((yt == 0) & (yp == 1)).sum().item()
        tn = ((yt == 0) & (yp == 0)).sum().item()       
        return np.array([[tn, fp], [fn, tp]])
    

class MiniBatchConfusionMatrix():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F) / (N,)
        batch_targets: (N,)
        """
        if batch_preds.ndim == 2:
            batch_preds = batch_preds.argmax(1)
        
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)

    @torch.no_grad()    
    def compute(self):
        """
         |0_|1_|2_|
        0|__|__|__|
        1|__|__|__|
        2|__|__|__|
        """
        yp = torch.cat(self.y_pred).cpu().numpy()
        yt = torch.cat(self.y_true).cpu().numpy()

        sample_weight = np.ones(yt.shape[0], dtype=np.int64)
        cm = coo_matrix((sample_weight, (yt, yp)), dtype=np.int64)
        return cm.toarray()

    
class MiniBatchBinaryF1():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F) / (N,)
        batch_targets: (N,)
        """
        if batch_preds.ndim == 2:
            batch_preds = batch_preds.argmax(1)
        
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)

    @torch.no_grad()    
    def compute(self, pos_label=1):
        yp = torch.cat(self.y_pred)
        yt = torch.cat(self.y_true)
        
        neg_label = 0 if pos_label else 1        
        fn = ((yt == pos_label) & (yp == neg_label)).sum().item()
        tp = ((yt == pos_label) & (yp == pos_label)).sum().item()
        fp = ((yt == neg_label) & (yp == pos_label)).sum().item()
        return tp / (tp + (fp + fn)/2)
    

class MiniBatchF1Macro():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F) / (N,)
        batch_targets: (N,)
        """
        if batch_preds.ndim == 2:
            batch_preds = batch_preds.argmax(1)
        
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)

    @torch.no_grad()    
    def compute(self):
        yp = torch.cat(self.y_pred)
        yt = torch.cat(self.y_true)
        return f1_score(yt, yp, average="macro") 
    

class MiniBatchF1Weighted():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F) / (N,)
        batch_targets: (N,)
        """
        if batch_preds.ndim == 2:
            batch_preds = batch_preds.argmax(1)
        
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)

    @torch.no_grad()    
    def compute(self):
        yp = torch.cat(self.y_pred)
        yt = torch.cat(self.y_true)
        return f1_score(yt, yp, average="weighted")
    

class MiniBatchF1Micro():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F) / (N,)
        batch_targets: (N,)
        """
        if batch_preds.ndim == 2:
            batch_preds = batch_preds.argmax(1)
        
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)

    @torch.no_grad()    
    def compute(self):
        yp = torch.cat(self.y_pred)
        yt = torch.cat(self.y_true)
        return f1_score(yt, yp, average="micro")    


class MiniBatchBinaryPrecision():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F) / (N,)
        batch_targets: (N,)
        """
        if batch_preds.ndim == 2:
            batch_preds = batch_preds.argmax(1)
        
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)

    @torch.no_grad()    
    def compute(self, pos_label=1):
        yp = torch.cat(self.y_pred)
        yt = torch.cat(self.y_true)
        
        neg_label = 0 if pos_label else 1        
        tp = ((yt == pos_label) & (yp == pos_label)).sum().item()
        fp = ((yt == neg_label) & (yp == pos_label)).sum().item()
        return tp / (tp + fp)
    
    
class MiniBatchBinaryRecall():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F) / (N,)
        batch_targets: (N,)
        """
        if batch_preds.ndim == 2:
            batch_preds = batch_preds.argmax(1)
        
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)

    @torch.no_grad()    
    def compute(self, pos_label=1):
        yp = torch.cat(self.y_pred)
        yt = torch.cat(self.y_true)
        
        neg_label = 0 if pos_label else 1        
        fn = ((yt == pos_label) & (yp == neg_label)).sum().item()
        tp = ((yt == pos_label) & (yp == pos_label)).sum().item()
        return tp / (tp + fn)
    
    
class MiniBatchAccuracy():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F) / (N,)
        batch_targets: (N,)
        """
        if batch_preds.ndim == 2:
            batch_preds = batch_preds.argmax(1)
        
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)

    @torch.no_grad()    
    def compute(self):
        yp = torch.cat(self.y_pred)
        yt = torch.cat(self.y_true)
        return (yp == yt).sum().item() / yp.size(0)
    
    
class MiniBatchTopKAccuracy():
    def __init__(self, k):
        self.y_true = []
        self.y_pred = []
        self.k = k
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F) / (N,)
        batch_targets: (N,)
        """
        _, indexes = greedy_sampling_from_logits(batch_preds, self.k)
        self.y_pred.append(indexes)
        self.y_true.append(batch_targets)

    @torch.no_grad()    
    def compute(self):
        yp = torch.cat(self.y_pred)
        yt = torch.cat(self.y_true)
        correct = (yp == yt.view(-1, 1)).sum(1) > 0
        return correct.sum().item() / yp.size(0)    
    

class MiniBatchRSquared():
    def __init__(self):
        self.y_true = []
        self.y_pred = []
    
    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, 1)
        batch_targets: (N, 1)
        """
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)

    @torch.no_grad()    
    def compute(self):
        yp = torch.cat(self.y_pred)
        yt = torch.cat(self.y_true)
        r2 = 1 - (yp - yt).pow(2).sum() / (yt - yt.mean()).pow(2).sum()
        return r2.item()


class MiniBatchRMSE():
    def __init__(self):
        self.y_true = []
        self.y_pred = []

    def add_batch(self, batch_preds, batch_targets):
        """
        batch_preds: (N, F)
        batch_targets: (N, F)
        """
        self.y_pred.append(batch_preds)
        self.y_true.append(batch_targets)

    @torch.no_grad()    
    def compute(self):
        yp = torch.cat(self.y_pred)
        yt = torch.cat(self.y_true)
        return F.mse_loss(yp, yt).sqrt().item()


class MiniBatchCost():
    def __init__(self):
        self.cost = 0
        self.total_data = 0

    def add_batch(self, batch_loss, n_data):
        """
        batch_preds: (N, F) / (N,)
        batch_targets: (N,)
        """
        self.cost += batch_loss.item() * n_data
        self.total_data += n_data

    @torch.no_grad()    
    def compute(self):
        return self.cost / self.total_data


class MiniBatchMisclassified():
    def __init__(self):
        self.feature = []        
        self.target = []
        self.preds = []
    
    def add_batch(self, batch_features, batch_preds, batch_targets):
        """
        batch_preds: (N, F) / (N,)
        batch_targets: (N,)
        """
        if batch_preds.ndim == 2:
            batch_preds = batch_preds.argmax(1)
        
        mask = batch_targets != batch_preds
        self.feature.append(batch_features[mask])
        self.preds.append(batch_preds[mask])
        self.target.append(batch_targets[mask])

    @torch.no_grad()    
    def compute(self):
        feature = torch.cat(self.feature)
        target = torch.cat(self.target)        
        preds = torch.cat(self.preds)
        return feature, target, preds
