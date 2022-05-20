import cv2.cv2 as cv2
import numpy as np

def processing(img, command):
    c = 100
    th = 255//2
    gamma = 1
    def reverse(img):
        return np.max(img) - img
    
    def logarit(img, c):
        return float(c) * np.log10(1.0 + img)

    def threshold(image, th):
        return (image > th) * 255

    def Gamma(image, gamma, c):
        def nomalize(image):
            return image / (np.amax(image))
        
        return (float(c) * np.exp(np.log(nomalize(image)) * float(gamma))).astype(np.uint8)

    imgRGB = cv2.cvtColor(np.float32(img), cv2.COLOR_BGR2RGB)

    if command == 'reverse':
        return reverse(imgRGB)
    if command == 'logarit':
        return logarit(imgRGB, c)
    if command == 'threshold':
        return threshold(imgRGB, th)
    if command == 'gamma':
        return Gamma(imgRGB, gamma, c)