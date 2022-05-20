import pygame
import cv2.cv2 as cv2
import numpy as np

# video = cv2.VideoCapture(0)
pygame.init()

W = 720
H = 500

window = pygame.display.set_mode((W, H))

pygame.display.set_caption("NqChung")

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

def run():
    isReverse = False
    isLog = False
    isThreshold = False
    isGamma = False

    c = 100
    th = 255//2
    gamma = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            
        keys=pygame.key.get_pressed()

        # ret, frame = video.read()
        
        frame = cv2.imread("flower.jpg")

        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if keys[pygame.K_r]:
            c = 100
            isReverse = True
            isLog = False
            isThreshold = False
            isGamma = False
        if keys[pygame.K_n]:
            isReverse = False
            isLog = False
            isThreshold = False
            isGamma = False
        if keys[pygame.K_l]:
            c = 100
            isLog = True
            isReverse = False
            isThreshold = False
            isGamma = False
        if keys[pygame.K_t]:
            c = 100
            isThreshold = True
            isReverse = False
            isLog = False
            isGamma = False
        if keys[pygame.K_g]:
            c = 255
            isThreshold = False
            isReverse = False
            isLog = False
            isGamma = True
        
        if isReverse:
            imgRGB = reverse(imgRGB)
        if isLog:
            imgRGB = logarit(imgRGB, c)
            if keys[pygame.K_RIGHT]:
                c = c + 1
                print(f"log c: {c}")
            if keys[pygame.K_LEFT]:
                c = c - 1 if c > 1 else 1
                print(f"log c: {c}")
        if isThreshold:
            imgRGB = threshold(imgRGB, th)
        if isGamma:
            imgRGB = Gamma(imgRGB, gamma, c)
            if keys[pygame.K_RIGHT]:
                gamma = gamma + 1
                print(f"gamma: {gamma}")
            if keys[pygame.K_LEFT]:
                gamma = gamma - 0.1 if gamma > 0 else 0
                print(f"gamma: {gamma}")

        imgRGB = np.rot90(imgRGB)
        imgRGB = pygame.surfarray.make_surface(imgRGB).convert() 

        window.fill((84, 160, 255))
        window.blit(imgRGB, ((W - imgRGB.get_size()[0]) // 2, (H - imgRGB.get_size()[1]) // 2))
        pygame.display.update()


if __name__ == "__main__":
    run()