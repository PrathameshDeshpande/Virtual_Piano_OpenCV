import cv2
import numpy as np
import time
import pygame
pygame.init()
w,h = 78,110
x1,y1= 10,10
x2,y2 = 10+w,10
x3,y3 = 10+2*w,10
x4,y4 = 10+3*w,10
x5,y5 = 10+4*w,10
x6,y6 = 10+5*w,10
x7,y7 = 10+6*w,10
x8,y8 =10+7*w,10
def draw_piano(frame):
    cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (255, 255, 255), 1)
    cv2.rectangle(frame, (x2, y2), (x2 + w, y2 + h), (255, 255, 255), 1)
    cv2.rectangle(frame, (x3, y3), (x3 + w, y3 + h), (255, 255, 255), 1)
    cv2.rectangle(frame, (x4, y4), (x4 + w, y4 + h), (255, 255, 255), 1)
    cv2.rectangle(frame, (x5, y5), (x5 + w, y5 + h), (255, 255, 255), 1)
    cv2.rectangle(frame, (x6, y6), (x6 + w, y6 + h), (255, 255, 255), 1)
    cv2.rectangle(frame, (x7, y7), (x7 + w, y7 + h), (255, 255, 255), 1)
    cv2.rectangle(frame, (x8, y8), (x8 + w, y8 + h), (255, 255, 255), 1)
    cv2.rectangle(frame,(x1, y1),(x8 + w, y8 + h),(0,0,0),1)
    cv2.line(frame, (x2, y2), (x2, y2+h) , (0,0,0) ,1)
    cv2.line(frame, (x3, y3), (x3, y3 + h), (0, 0, 0), 1)
    cv2.line(frame, (x4, y4), (x4, y4 + h), (0,0,0), 1)
    cv2.line(frame, (x5, y5), (x5, y5 + h), (0,0,0,), 1)
    cv2.line(frame, (x6, y6), (x6, y6 + h), (0,0,0), 1)
    cv2.line(frame, (x7, y7), (x7, y7 + h), (0,0,0), 1)
    cv2.line(frame, (x8, y8), (x8, y8 + h), (0, 0, 0), 1)
def key_press(frame,x,y,w1,h1):
    if x>x1 and y>y1 and x+w1<(x1 + w) and y+h1<(y1+h):
        pygame.mixer.Sound('wav/a1.wav').play()
        time.sleep(0.08)
        pygame.mixer.Sound('wav/a1.wav').stop()
    elif x>x2 and y>y2 and x+w1<(x2 + w) and y+h1<(y2+h):
        pygame.mixer.Sound('wav/b1.wav').play()
        time.sleep(0.08)
        pygame.mixer.Sound('wav/b1.wav').stop()
    elif x>x3 and y>y3 and x+w1<(x3 + w) and y+h1<(y3+h):
        pygame.mixer.Sound('wav/c1.wav').play()
        time.sleep(0.08)
        pygame.mixer.Sound('wav/c1.wav').stop()
    elif x>x4 and y>y4 and x+w1<(x4 + w) and y+h1<(y4+h):
        pygame.mixer.Sound('wav/c2.wav').play()
        time.sleep(0.08)
        pygame.mixer.Sound('wav/c2.wav').stop()
    elif x>x5 and y>y5 and x+w1<(x5 + w) and y+h1<(y5+h):
        pygame.mixer.Sound('wav/d1.wav').play()
        time.sleep(0.08)
        pygame.mixer.Sound('wav/d1.wav').stop()
    elif x>x6 and y>y6 and x+w1<(x6 + w) and y+h1<(y6+h):
        pygame.mixer.Sound('wav/e1.wav').play()
        time.sleep(0.08)
        pygame.mixer.Sound('wav/e1.wav').stop()
    elif x>x7 and y>y7 and x+w1<(x7 + w) and y+h1<(y7+h):
        pygame.mixer.Sound('wav/f1.wav').play()
        time.sleep(0.08)
        pygame.mixer.Sound('wav/f1.wav').stop()
    elif x>x8 and y>y8 and x+w1<(x8 + w) and y+h1<(y8+h):
        pygame.mixer.Sound('wav/g1.wav').play()
        time.sleep(0.08)
        pygame.mixer.Sound('wav/g1.wav').stop()
cap = cv2.VideoCapture(0)
while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame =cv2.GaussianBlur(frame,(9,9),0)
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    draw_piano(frame)
    lower_red = np.array([132, 90, 120])  # creating the mask for red color
    upper_red = np.array([179, 255, 255])
    mask_1 = cv2.inRange(frame_hsv, lower_red, upper_red)
    lower_red = np.array([0, 110, 100])
    upper_red = np.array([3, 255, 255])
    mask_2 = cv2.inRange(frame_hsv, lower_red, upper_red)
    masked = mask_1 + mask_2
    kernel_1 = np.ones((4,4),np.uint8)
    kernel_2 = np.ones((15,15),np.uint8)
    masked=cv2.erode(masked,kernel_1,iterations = 1)
    masked=cv2.morphologyEx(masked,cv2.MORPH_CLOSE,kernel_2)
    xr, yr, wr, hr = 0, 0, 0, 0
    contours, hierarchy = cv2.findContours(masked, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    try:
        for i in range(0,10):
            xr, yr, wr, hr = cv2.boundingRect(contours[i])
            if wr*hr > 1000:
                break
    except:
        pass
    cv2.rectangle(frame, (xr, yr), (xr + wr, yr + hr), (255, 255, 255), 2)
    key_press(frame, xr, yr, wr, hr)
    frame = cv2.resize(frame, (800, 800))
    cv2.imshow('frame', frame)
    cv2.imshow('mask',masked)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()