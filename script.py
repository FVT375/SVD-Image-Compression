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
    reconstimgGS = Image.fromarray(np.uint8(reconstimg))
    reconstimgGS.save(image_name + "_grayscale.jpg")
    print('Done. Compression rate is {0:.2f}%'.format(100 - compression))

    
def to_rgb():
    imgrgb = img.convert('RGB')

    imgR = np.empty((imgY, imgX))
    imgG = np.empty((imgY, imgX))
    imgB = np.empty((imgY, imgX))

    for i in range(imgX):
        for j in range(imgY):
            r, g, b = imgrgb.getpixel((i, j))
            imgR[j][i] = r
            imgG[j][i] = g
            imgB[j][i] = b
            
    imgR = np.matrix(imgR)
    imgG = np.matrix(imgG)
    imgB = np.matrix(imgB)

    UR, sigmaR, VR = np.linalg.svd(imgR)
    UG, sigmaG, VG = np.linalg.svd(imgG)
    UB, sigmaB, VB = np.linalg.svd(imgB)

    reconstimgR = np.matrix(UR[:, :n+1]) * np.diag(sigmaR[:n+1]) * np.matrix(VR[:n+1, :])
    reconstimgG = np.matrix(UG[:, :n+1]) * np.diag(sigmaG[:n+1]) * np.matrix(VG[:n+1, :])
    reconstimgB = np.matrix(UB[:, :n+1]) * np.diag(sigmaB[:n+1]) * np.matrix(VB[:n+1, :])

    imgR = Image.fromarray(np.uint8(reconstimgR))
    imgG = Image.fromarray(np.uint8(reconstimgG))
    imgB = Image.fromarray(np.uint8(reconstimgB))
    reconstimgRGB = Image.merge("RGB", (imgR, imgG, imgB))
    reconstimgRGB.save(image_name + "_rgb.jpg")
    print('Done. Compression rate is {0:.2f}%'.format(100 - compression))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image', type=str)
    parser.add_argument('n', type=int, default=50)
    parser.add_argument('--grayscale', action='store_true')
    args = parser.parse_args()

    path = args.image
    image_name = path.split('.')[0]
    img = Image.open(args.image)
    imgX, imgY = img.size[0], img.size[1]

    n = args.n

    compression = ((imgX * n) + n + (imgY * n)) / (imgX * imgY)
    compression *= 100

    if args.grayscale:
        to_grayscale()
    else:
        to_rgb()
