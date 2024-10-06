from .fira_adamw import AdamW as FiraAdamW
from torch import nn

def divide_params(model = None, target_modules_list = [], rank = 8, update_proj_gap = 200, alpha = 1.0, proj_type = 'std'):
    if model is None:
        return None
    projection_params = []
    for module_name, module in model.named_modules():
        if not isinstance(module, nn.Linear):
            continue

        if not any(target_key in module_name for target_key in target_modules_list):
            continue

        print('enable gradient projection for weights in module: ', module_name)
        projection_params.append(module.weight) 
    id_projection_params = [id(p) for p in projection_params]
    # make parameters without "rank" to another group
    regular_params = [p for p in model.parameters() if id(p) not in id_projection_params]
    # then call fira_adamw
    param_groups = [{'params': regular_params},
                    {'params': projection_params, 'rank': rank, 'update_proj_gap': update_proj_gap,
                     'alpha': alpha, 'proj_type': proj_type}]
    return param_groups

def test():
    return (u'Hello, Fira!')