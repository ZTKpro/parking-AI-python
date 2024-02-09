
import cv2 

img = cv2.imread('example_image.png')
width, height = 107, 48

while True:
    cv2.rectangle(img, (50,192), (157,240), (255,0,255),2)
    cv2.imshow("image",img)
    cv2.waitKey(1)