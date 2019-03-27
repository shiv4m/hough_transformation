import numpy as np
import cv2
import math

def detect_circles(edgeImage):
	circleList = []
	sine = []
	cosine = []
	for theta in range(0, 360):
		sine.append(np.sin(theta * np.pi/180))
		cosine.append(np.cos(theta * np.pi/180))
	r = [i for i in range(24, 19, -1)]
	abrSpace = np.zeros([edgeImage.shape[0], edgeImage.shape[1], len(r)])
	
	for radius in range(len(r)):
		for x in range(edgeImage.shape[0]):
			for y in range(edgeImage.shape[1]):
				if(edgeImage[x][y] == 255):
					for angle in range(0, 360):
						a = np.absolute(x - int(r[radius] * cosine[angle]))
						b = np.absolute(y + int(r[radius] * sine[angle]))
						if(a < edgeImage.shape[0] and b < edgeImage.shape[1]):
							abrSpace[int(a)][int(b)][radius] += 1
	print(np.max(abrSpace))
	prev = 0
	for k in range(len(r)):
		for i in range(edgeImage.shape[0]):
			for j in range(edgeImage.shape[1]):
				if(i > 0 and j > 0 and i < edgeImage.shape[0]-1 and j < edgeImage.shape[1]-1 and abrSpace[i][j][k] >= 170):
					
					circleList.append((i, j, r[k]))
	return circleList

img = cv2.imread('original_imgs/original_imgs/hough.jpg', 0)
img_copy = img
blurred_img = cv2.GaussianBlur(img_copy, (5, 5), 0.50)
edgeImage = cv2.Canny(blurred_img, 100, 200)

circleList = detect_circles(edgeImage)
print(circleList)
previous, __ = 0, 0
imgs = cv2.imread('original_imgs/original_imgs/hough.jpg', 1)
for x in circleList:
    if(x[2]== 20 or x[2]==21 or x[2]==22 or x[2]==23 or x[2]==24):
        if(x[0] - previous > 2):
            previous = x[0]
            cv2.circle(imgs, (x[1], x[0]), x[2], (28, 28, 255), 2)
        if(x[2]==21):
            if(x[0] - __ > 8):
                __ = x[0]
                cv2.circle(imgs, (x[1], x[0]), x[2], (28, 28, 255), 2)
cv2.imwrite('coin.jpg', imgs)