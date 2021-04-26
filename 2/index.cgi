#!/usr/local/anaconda3/bin/python3
import sys
# 日時用モジュールをインポート
from datetime import datetime
# Unixタイムスタンプ用モジュールをインポート
import time


import cv2
import glob
import numpy as np
import os
import base64
import cgi
import cgitb
cgitb.enable()


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
category="business/"
img_src=path+category


def myhist(image,code=None):#3,255,255->4*4*4=64
    ranges=[0,256,0,256,0,256]
    if code!=None:
        image=cv2.cvtColor(image, code)
        if code==cv2.COLOR_BGR2HSV:
            ranges=[0,180,0,256,0,256]
    color_num=4
    hist=cv2.calcHist([image],[0,1,2],None,[color_num]*3,ranges)
    hist=hist.flatten()
    hist=cv2.normalize(hist,hist)
    return hist
def myhist2(image,split_size,code=None):
    imgs=split_imgs(image,split_size)
    hist2=[]
    for img in imgs:
        hist=myhist(img,code)
        hist2.append(hist)
    hist2=np.array(hist2).reshape(-1,1)
    return hist2

def split_imgs(img, split_size):
    h, w = img.shape[:2]
    vsplits=split_size
    hsplits=split_size
    crop_img = img[: h // vsplits * vsplits, : w // hsplits * hsplits]

    return np.array(
        [x for h_img in np.vsplit(crop_img, vsplits) for x in np.hsplit(h_img, hsplits)]
    )
def main():
    
    print(htmlText1st)


    str_imgs=[]
    images=[]
    files = sorted(glob.glob(img_src+"*"))
    for f in files:

        image=cv2.resize(cv2.imread(f),(255,255))

        
        __, img_jpg=cv2.imencode('.jpg', image)
        str_img=base64.b64encode(img_jpg).decode()        
        str_imgs.append(str_img)
        images.append(image)
    print("クエリ")
    print(files[0])
    query_num=0
    query=images[query_num]
    show_size=[225,225]
    __, img_jpg=cv2.imencode('.jpg', query)
    str_img=base64.b64encode(img_jpg).decode()
    img_tag = "<br><img src='data:image/jpeg;base64," + str_img + "' width='"+str(show_size[0])+"' height='"+str(show_size[1])+"'/>"
    print(img_tag)



    for split_size in [2,3]:
        


        
        rgbhists=[]
        hsvhists=[]
        luvhists=[]


        for image in images:
            hist=myhist2(image,split_size)
            rgbhists.append(hist)


            hist=myhist(image,cv2.COLOR_BGR2HSV)
            hsvhists.append(hist)
            
            hist=myhist(image,cv2.COLOR_BGR2LUV)
            luvhists.append(hist)

            
        
        print('<table border="1">')

        q_hist=myhist2(query,split_size)
        print(q_hist.shape)


        results=[]


        for hist in rgbhists:
            d=cv2.compareHist(q_hist,hist,cv2.HISTCMP_INTERSECT)
            results.append(d)
        hists_index =np.argsort(results)[::-1]
        print(cv2.compareHist(q_hist,q_hist,cv2.HISTCMP_INTERSECT))

        top_num=20
        r_num=10
        show_size=[100,100]
        
        print("<th  colspan='"+str(r_num)+"'>64*" + str(split_size) +"^2 RGB上位"+str(top_num)+"</th>")
        for i, index in enumerate(hists_index[0:top_num]):
            if i%r_num==0:
                print('<tr>')

            print('<td>')
            # __, img_jpg=cv2.imencode('.jpg', images[index])
            # str_img=base64.b64encode(img_jpg).decode()
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