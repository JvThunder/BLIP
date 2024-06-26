import argparse
import os
import ruamel.yaml as yaml
import numpy as np
import random
import time
import datetime
import json
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.backends.cudnn as cudnn
import torch.distributed as dist
from torch.utils.data import DataLoader

from data import create_dataset, create_sampler, create_loader
from utils import collate_fn_cirr

def main(args, config):
    device = torch.device(args.device)
    seed = 42

    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    cudnn.benchmark = True

    #### Dataset ####
    print("Creating retrieval dataset")
    train_dataset, val_dataset, test_dataset = create_dataset('cirr', config)

    samplers = [None, None, None]
    train_loader, val_loader, test_loader = create_loader([train_dataset, val_dataset, test_dataset], samplers,
                                                          batch_size=[config['batch_size_train']]+[config['batch_size_test']]*2,
                                                          num_workers=[4, 4, 4],
                                                          is_trains=[True, False, False],
                                                          collate_fns=[collate_fn_cirr, collate_fn_cirr, collate_fn_cirr])

    # in 'relative' mode (for 'classic', separate loaders must be written but we wont use it for now)

    # train loader
    print('train loader')
    for reference_images, target_images, captions in train_loader:
        print(reference_images.size())
        print(target_images.size())
        print(captions)
        break

    # val loader
    print('val loader')
    for batch_reference_names, batch_target_names, captions, batch_group_members in val_loader:
        print(batch_reference_names)
        print(batch_target_names)
        print(captions)
        print(batch_group_members)
        break

    # test loader
    print('test loader')
    for batch_pairs_id, batch_reference_names, captions, batch_group_members in test_loader:
        print(batch_pairs_id)
        print(batch_reference_names)
        print(captions)
        print(batch_group_members)
        break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='./configs/cirr.yaml')
    parser.add_argument('--device', default='cuda')

    args = parser.parse_args()
    config = yaml.load(open(args.config, 'r'), Loader=yaml.Loader)


    main(args, config)