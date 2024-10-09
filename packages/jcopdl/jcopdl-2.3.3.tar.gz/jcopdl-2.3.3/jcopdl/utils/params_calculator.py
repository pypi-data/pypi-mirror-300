def count_differentiable_parameters(pytorch_model):
    n_params = sum(p.numel() for p in pytorch_model.parameters() if p.requires_grad)
    return f"This model has {n_params:_} differentiable parameters"
