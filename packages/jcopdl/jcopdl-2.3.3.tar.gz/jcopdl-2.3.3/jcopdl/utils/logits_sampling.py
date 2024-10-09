import torch
import torch.nn.functional as F


def greedy_sampling_from_logits(logits, k, temp=1):
    """
    Sample top K highest probability from logits

    == input == 
    logits: (N, F) or (F,)

    == return ==
    probs: (N, k)
        probability / confidence score from softmax (with temperature)
    
    indexes: (N, k)
        id of the softmax output
    """
    if logits.ndim == 1:
        logits = logits.view(1, -1)
    probs, indexes = F.softmax(logits / temp, dim=1).topk(k)
    return probs, indexes


def multinomial_sampling_from_logits(logits, k, temp=1):
    """
    Sample K item weighted by its probability weighted from logits

    == input == 
    logits: (N, F) or (F,)

    == return ==
    probs: (N, k)
        probability / confidence score from softmax (with temperature)
    
    indexes: (N, k)
        id of the softmax output
    """
    if logits.ndim == 1:
        logits = logits.view(1, -1)
    probs = F.softmax(logits / temp, dim=1)
    indexes = torch.multinomial(probs, k)
    probs = torch.gather(probs, 1, indexes)
    return probs, indexes
