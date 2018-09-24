import numpy as np
from PIL import Image
import argparse

def to_grayscale():
    imggray = img.convert('LA')
    imgmat = np.array(list(imggray.getdata(band=0)), float)
    imgmat.shape = (imggray.size[1], imggray.size[0])
    imgmat = np.matrix(imgmat)
    U, sigma, V = np.linalg.svd(imgmat)
    reconstimg = np.matrix(U[:, :n+1]) * np.diag(sigma[:n+1]) * np.matrix(V[:n+1, :])
    reconstimg.save(path + "_grayscale.jpg")
    
def to_rgb():
    imgrgb = img.convert('RGB')

    imgR = np.empty((imgX, imgY))
    imgG = np.empty((imgX, imgY))
    imgB = np.empty((imgX, imgY))

    for i in range(imgX):
        for j in range(imgY):
            r, g, b = imgrgb.getpixel((i, j))
            imgR[i][j] = r
            imgG[i][j] = g
            imgB[i][j] = b
            
    imgR = np.matrix(imgR)
    imgG = np.matrix(imgG)
    imgB = np.matrix(imgB)

    UR, sigmaR, VR = np.linalg.svd(imgR)
    UG, sigmaG, VG = np.linalg.svd(imgG)
    UB, sigmaB, VB = np.linalg.svd(imgB)

    reconstimgR = np.matrix(UR[:, :2]) * np.diag(sigmaR[:2]) * np.matrix(VR[:2, :])
    reconstimgG = np.matrix(UG[:, :2]) * np.diag(sigmaG[:2]) * np.matrix(VG[:2, :])
    reconstimgB = np.matrix(UB[:, :2]) * np.diag(sigmaB[:2]) * np.matrix(VB[:2, :])

    imgR = Image.fromarray(np.uint8(reconstimgR))
    imgG = Image.fromarray(np.uint8(reconstimgG))
    imgB = Image.fromarray(np.uint8(reconstimgB))

    imgR = imgR.transpose(Image.ROTATE_270)
    imgR = imgR.transpose(Image.FLIP_LEFT_RIGHT)
    imgG = imgG.transpose(Image.ROTATE_270)
    imgG = imgG.transpose(Image.FLIP_LEFT_RIGHT)
    imgB = imgB.transpose(Image.ROTATE_270)
    imgB = imgB.transpose(Image.FLIP_LEFT_RIGHT)

    reconstimgRGB = Image.merge("RGB", (imgR, imgG, imgB))


parser = argparse.ArgumentParser()
parser.add_argument('image', type=str)
parser.add_argument('n', type=int)
parser.add_argument('--grayscale', action='store_true')
args = parser.parse_args()

path = args.image
img = Image.open(args.image)
imgX, imgY = img.size[0], img.size[1]

n = args.n

compression = ((imgX * n) + n + (imgY * n)) / (imgX * imgY)
compression *= 100

if args.grayscale:
    to_grayscale()
else:
    to_rgb()


###
