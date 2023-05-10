import cv2
from PIL import Image
import numpy as np
import argparse

#split
def cut_image(img,n):
    arr = []
    h,w = img.shape[0]//n,img.shape[1]//n
    for i in range(n):
        for j in range(n):
            arr.append(img[h*i:h*(i+1),w*j:w*(j+1),:])
    return arr

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',type=str,required=True,help='image path')
    parser.add_argument('--n',type=int,required=True,help='number of sub')
    args = parser.parse_args()

    img = Image.open(args.path)
    img = np.array(img)
    
    subimgs = cut_image(img,args.n)

    for i,subimg in enumerate(subimgs):
        img = Image.fromarray(subimg)
        img = img.save(f'./sub_images/subimages{i}.png')