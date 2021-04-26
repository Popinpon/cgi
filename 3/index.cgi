#!/usr/local/anaconda3/bin/python3
import os
import time

from PIL import Image

import json
import cv2
import glob
import numpy as np
import os
import base64
import cgi
import cgitb
cgitb.enable()



import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
import torch.nn.functional as F


import numpy as np
import torchvision
from torch.autograd import Variable
from torchvision import models
from torchvision import transforms, utils


os.environ['CUDA_VISIBLE_DEVICES'] = '0,1' 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#print("Content-Type: text/plain; charset=utf-8\n")
htmlText1st = '''Content-type: text/html; charset=utf-8

<html>
<head>
  <title>ファイルの読み込みから表示</title>
</head>
<body>
<header class="header">
   <p>CGI表示</p>
</header>
<div class="content">
'''

htmlText2nd = '''

</div>
</body>
</html>
'''
path="../imgdata/cd_8/photos/"
category="location/"
img_src=path+category








def main():

    print(htmlText1st)



    model = models.vgg16()
    model.load_state_dict(torch.load('vgg16.pth'))
    layers = list(model.classifier.children())[:-2]
    model.classifier = nn.Sequential(*layers)

    model=model.to(device)

    str_imgs=[]
    images=[]
    files = sorted(glob.glob(img_src+"*"))
    for f in files:

        image=cv2.resize(cv2.imread(f),(224,224))

        
        __, img_jpg=cv2.imencode('.jpg', image)
        str_img=base64.b64encode(img_jpg).decode()        
        str_imgs.append(str_img)
        images.append(image)
 
    inputs=np.array(images)
    inputs=inputs.transpose(0,3,1,2)
    inputs=torch.from_numpy(inputs.astype(np.float32)).clone()
    inputs=inputs.to(device)
    output=model(inputs)
    output=(output/torch.sum(output,1).unsqueeze(-1))



    print("クエリ")
    print(files[0])
    query_num=0
    query=images[query_num]
    show_size=[224,224]
    __, img_jpg=cv2.imencode('.jpg', query)
    str_img=base64.b64encode(img_jpg).decode()
    img_tag = "<br><img src='data:image/jpeg;base64," + str_img + "' width='"+str(show_size[0])+"' height='"+str(show_size[1])+"'/>"
    print(img_tag)




    
    
    print('<table border="1">')

    results=[]
    output= output.to('cpu').detach().numpy().copy()
    query=output[0]
    print(query.shape)
    for i in range(100):
        minima = np.minimum(output[i], query)
        intersection = np.sum(minima)  
        results.append(intersection)
    hists_index =np.argsort(results)[::-1]
  
    top_num=50
    r_num=10
    show_size=[100,100]
    
    print("<th  colspan='"+str(r_num)+"'>"  +"vgg16による特徴量での上位"+str(top_num)+"</th>")
    for i, index in enumerate(hists_index[0:top_num]):
        if i%r_num==0:
            print('<tr>')

        print('<td>')

        img_tag = "<img src='data:image/jpeg;base64," + str_imgs[index] + "' width='"+str(show_size[0])+"' height='"+str(show_size[1])+"'/>"

        print(img_tag)
        print("<br>")
        print(os.path.basename(files[index]))
        print('</td>')
        if i%r_num==r_num-1:
            print('</tr>')
    print('</tr><br>')



    print(htmlText2nd)
    
if __name__ =="__main__":
    main()
