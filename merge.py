import math
import numpy as np
import os
from PIL import Image
import argparse
#merge
def merge(arr):
    n = int(math.sqrt(len(arr)))
    ans = []
    temp = []
    cnt =0 
    for i in range(len(arr)):
        if cnt % n == 0 and i != 0:
            ans.append(np.concatenate(temp,axis=1))
            temp = []
        cnt+=1
        temp.append(arr[i])
    ans.append(np.concatenate(temp,axis=1))
    return np.concatenate(ans)

class RandomVerticalFlip():
    def __init__(self,p=0.5):
        super().__init__()
        self.p = p

    def forward(self,img):
        if np.random.rand(1) < self.p:
            return np.array(img[::-1])
        return np.array(img)       
    
class RandomMirriring():
    def __init__(self,p=0.5):
        super().__init__()
        self.p = p
    def forward(self,img):
        if np.random.rand(1) < self.p:
            temp = []
            for i in img:
                temp.append(i[::-1])
            return np.array(temp)
        return np.array(img)
    
class RandomRotate():
    def __init__(self,p=0.5):
        super().__init__()
        self.p = p
    def forward(self,img):
        if np.random.rand(1) < self.p:
            return np.rot90(img)
        return np.array(img)
    
class Compose():
    def __init__(self):
        super().__init__()
    def forward(self,arr):
        idx = np.random.randint(3)
        return arr[idx]
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',type=str,required=True,help='image path')
    parser.add_argument('--out_path',type=str,required=True,help='output path')
    parser.add_argument('--aug',type=bool,required=True)
    parser.add_argument('--resize',default=256,type=int,required=True,help='Set it on all image size')
    args = parser.parse_args()

    root = args.path
    imgList = [Image.open(os.path.join(root,x)).resize((args.resize,args.resize)) for x in sorted(os.listdir(root))]
    
    augImgs = []
    
    if args.aug:

        for img in imgList:
            
            img = np.array(img)
            aug = Compose()
            m = aug.forward([RandomMirriring(),RandomRotate(),RandomVerticalFlip()])
            augmentated = m.forward(img)
            augImgs.append(augmentated)
            print(augmentated.shape)

    img = merge(augImgs)
    img = Image.fromarray(img)
    img.save(f'{args.out_path}/merge.png')