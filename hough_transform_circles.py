import cv2
import numpy as np
import math

def distance(x1,y1,x2,y2):
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist 
     
def trackEdge(image, tracked_point, x_start, y_start, r):

    x = tracked_point[0]
    y = tracked_point[1]
    image[y,x] = 254
    for i in range (-1+y,2+y):
        for j in range (-1+x,2+x):
            if (not(i == y and j == x)):
                if (i > 0 and j > 0 and j < image.shape[1] and i < image.shape[0] and image[i,j] == 255):
                    tracked_point[0] = j
                    tracked_point[1] = i
                    
                    if (distance(x_start, y_start, j, i) < r):
                        image[i,j] = 254
                        return trackEdge(image, tracked_point, x_start, y_start, r)
                    else: return tracked_point.copy()
                    
    return tracked_point.copy()
              
def calcEdgeAngle(image, x, y, r):

    point = []
    image[y,x] = 254

    for i in range (-1+y,2+y):
        for j in range (-1+x,2+x):
            if (i > 0 and j > 0 and j < image.shape[1] and i < image.shape[0] and image[i,j] == 255):
                neigh = []
                neigh.append(j)
                neigh.append(i)
                point.append(neigh.copy())
                
    if (len(point) < 2): return None

    point1 = trackEdge(image, point[0], x, y, r)
    point2 = trackEdge(image, point[1], x, y, r)
    
    x_vector = point1[0] - point2[0] 
    y_vector = point1[1] - point2[1]
    
    return math.atan2(y_vector,x_vector)

def drawHoughSpaceForCircle(Image, radius):

    gray = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
    gray = cv2.Canny(gray, 150, 650);
    houghSpace = np.ones((gray.shape[0], gray.shape[1], 1), np.uint8)
    
    for start_y in range (0, gray.shape[0], 2):
        for start_x in range (0, gray.shape[1], 2):
            if (gray[start_y, start_x] == 255):
            
                newImage = gray.copy()
                angle = calcEdgeAngle(newImage, start_x,start_y, 5)

                x = 0
                y = 0

                if (not angle is None):
                    x =  int(start_x + radius * math.cos(angle+3.14/2))
                    y =  int(start_y + radius * math.sin(angle+3.14/2))
                    
                    if (x < gray.shape[1] - 10 and y < gray.shape[0] - 100):
                        for i in range (-2,4):
                            for j in range (-2,4):
                                houghSpace[y+i,x+j] = houghSpace[y+i,x+j] + 1
            
                    x =  int(start_x + radius * math.cos(angle-3.14/2))
                    y =  int(start_y + radius * math.sin(angle-3.14/2))
                    if (x < gray.shape[1] - 10 and y < gray.shape[0] - 100):
                        for i in range (-2,4):
                            for j in range (-2,4):
                                houghSpace[y+i,x+j] = houghSpace[y+i,x+j] + 1
    return houghSpace


#Searching blobs in Hough Space
def getcirclesCenter(houghSpace):

    kernel_size = 20
    kernel = cv2.getStructuringElement(0, ksize=(kernel_size, kernel_size))
    houghSpace = cv2.morphologyEx(houghSpace, 3, kernel)

    kernel_size = 10
    kernel = cv2.getStructuringElement(0, ksize=(kernel_size, kernel_size))
    houghSpace = cv2.morphologyEx(houghSpace, 5, kernel)
    
    pointList = []
    ret,thresh = cv2.threshold(houghSpace,20,255,0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        M = cv2.moments(c)
        
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            
            point = []
            point.append(cX)
            point.append(cY)
            
            pointList.append(point.copy())
    
    return pointList
    
    
file = "blur6.jpg"  
Image = cv2.imread(file)

cv2.imshow("Image", Image)
cv2.waitKey(0)


radius = 30
#Drawing Hough Space for circles where r = 30px
houghSpace = drawHoughSpaceForCircle(Image, radius)

#Searching Blobs in the Hough space
circlesCenter = getcirclesCenter(houghSpace)

# Drawing Circles
for circlePoint in circlesCenter:
    cv2.circle(Image, (circlePoint[0],circlePoint[1]),30, (0,255,0), 2)

cv2.imshow("Image", Image)
cv2.imshow("Image1", houghSpace)
cv2.waitKey(0)


















