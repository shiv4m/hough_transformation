import cv2
import numpy as np
import math

def saveImage(image, name):
	cv2.imwrite(name+".jpg", image)
	
def showImage(image):
	cv2.imshow('Image', image)
	cv2.waitKey(0)

def calculatePThetaSpace(edgeImage, accumlatorBox): #calculate p,theta space
	z = int(accumlatorBox.shape[0]/2)
	y, x = np.nonzero(edgeImage) #extract all pixel values which are not black
	for i, j in zip(y, x):
		for theta in range(-90, 91, 1): #calculate for all theta values -90 to 90
			p = int(j*np.cos(np.deg2rad(theta)) + i*np.sin(np.deg2rad(theta))) #xcostheta + ysintheta
			accumlatorBox[z + p][theta+90] = accumlatorBox[z + p][theta+90]+1 #voting
	return accumlatorBox
	
def red_lines(pThetaSpace):
	loc = np.where((pThetaSpace > 110) & (pThetaSpace < 250)) #thresholding
	h = loc[0] - 817
	n = -90 + loc[1]
	h = np.asarray(h).tolist()
	n = np.asarray(n).tolist()
	pList, thetaList = [], []
	previous = -1
	for i in range(len(n)):
		if(n[i] > -3 and n[i] < -1): #filter out the theta values
			if(int(h[i]/100) > previous): #filter out p values
				previous = int(h[i]/100)
				thetaList.append(n[i])
				pList.append(h[i])
	print(pList, thetaList)
	img1 = cv2.imread('original_imgs/original_imgs/hough.jpg')
	for i,theta in zip(pList, thetaList):
		a = np.cos(np.deg2rad(theta))
		b = np.sin(np.deg2rad(theta))
		x0 = a*i
		y0 = b*i
		x1 = int(x0 + 1000*(-b)) #coordinates
		y1 = int(y0 + 1000*(a))
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*(a))
		cv2.line(img1,(x1,y1),(x2,y2),(0,0,255),2) #draw line
	saveImage(img1, 'red_line')
	
def blue_lines(pThetaSpace):
	loc = np.where((pThetaSpace > 55) & (pThetaSpace < 170)) #threshold
	h = loc[0] - 817
	n = -90 + loc[1]
	h = np.asarray(h).tolist()
	n = np.asarray(n).tolist()
	pList0, thetaList0 = [], []
	previous = 0
	for i in range(len(n)):
		if(n[i] > -37 and n[i] < -35): #theta values
			if(abs(h[i] - previous) > 71): #p values
				previous = h[i]
				thetaList0.append(n[i])
				pList0.append(h[i])
	print(pList0, thetaList0)
	pList0[1] = pList0[1] + 2
	img1 = cv2.imread('original_imgs/original_imgs/hough.jpg')
	for i,theta in zip(pList0, thetaList0):
		a = np.cos(np.deg2rad(theta))
		b = np.sin(np.deg2rad(theta))
		x0 = a*i
		y0 = b*i
		x1 = int(x0 + 1000*(-b)) #coordinates
		y1 = int(y0 + 1000*(a))
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*(a))
		cv2.line(img1,(x1,y1),(x2,y2),(255,0,0),2) #save image
	saveImage(img1, 'blue_lines')
	#showImage(img1)

def Max(arr):
   max=0
   for i in range(0,len(arr)-1):
       for j in range(0,len(arr)-1):
             if arr[i][j] > max:
                   max=arr[i][j]
   return max;
   
def Flipp(kernel): #flip the kernel for sobel
   for i in range(0,3):
       temp=kernel[0][i]
       kernel[0][i]=kernel[2][i]
       kernel[2][i]=temp
   for i in range(0,3):
       temp=kernel[i][0]
       kernel[i][0]=kernel[i][2]
       kernel[i][2]=temp
   return kernel

def paddingImage(img): #pad image
   return cv2.copyMakeBorder(img, 1,1, 1, 1, cv2.BORDER_CONSTANT,None,0)
 

def sobel_conv(img,sobel_template):
	sumList=[]
	paddedImage=paddingImage(img)
	sobel_template=Flipp(sobel_template) #flip the kernel
	list=[[ 0.0 for x in range(0,img.shape[1])] for y in range(0,img.shape[0])]
	my_arr=np.asarray(list)
	for row in range(1,paddedImage.shape[0]-1):
		for column in range(1,paddedImage.shape[1]-1):
			sum=0
			for i in range(-1,2):
				for j in range(-1,2):			   
					sum=sum+paddedImage[row+i,column+j] * sobel_template[i+1,j+1] #convolute the image portion with kernel
					my_arr[row-1,column-1]=-1*sum
			if sum < 0:
				my_arr[row-1,column-1]=-1*sum
			sumList.append(sum)
	edge=my_arr
	edgeList.append(edge)
	maxPixel=max(sumList)
	edge=edge/maxPixel #normalise
	return edge

img = cv2.imread('original_imgs/original_imgs/hough.jpg', 0)
edgeList=[]
paddedImage=paddingImage(img)
sobel_x=np.asarray([[-1,0,1],[-2,0,2],[-1,0,1]])
sobel_y=np.asarray([[1,2,1],[0,0,0],[-1,-2,-1]])
edge_x=sobel_conv(img,sobel_x)
edge_y=sobel_conv(img,sobel_y)
edge_magnitude=np.sqrt(edge_x**2+edge_y**2) #calculate magnitude
#showImage(edge_magnitude)
edge_magnitude=edge_magnitude/Max(edge_magnitude) #normalize
edge_magnitude = edge_magnitude*255 #scale up to 255
zz = np.max(edge_magnitude)
for i in range(edge_magnitude.shape[0]):
	for j in range(edge_magnitude.shape[1]):
		if(edge_magnitude[i][j] > 35):
			edge_magnitude[i][j] = 255 #darkening the edges
		else:
			edge_magnitude[i][j] = 0
#showImage(edge_magnitude)
diagLength = int(np.sqrt((edge_magnitude.shape[0])**2 + (edge_magnitude.shape[1])**2))
accumlatorBox = np.zeros([diagLength*2, 181])
pThetaSpace = calculatePThetaSpace(edge_magnitude, accumlatorBox) #pthetaspace
print(np.max(pThetaSpace))
red_lines(pThetaSpace) #red lines
blue_lines(pThetaSpace) #blue lines