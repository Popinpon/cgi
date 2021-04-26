import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1' # 4GPUの場合

import torch
import torch.nn as nn
import torch.optim as optim
import torch.backends.cudnn as cudnn
import torch.nn.functional as F

import numpy as np
import torchvision
from torch.autograd import Variable
from torchvision import models
from torchvision import transforms, utils
from tqdm import tqdm

import time

import matplotlib.pyplot as plt
%matplotlib inline
from PIL import Image

import json

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


vgg = models.vgg16(pretrained=True)