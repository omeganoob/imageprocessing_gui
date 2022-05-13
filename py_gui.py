import pygame
from main import threshold
import pygame_gui
import cv2.cv2 as cv2
import numpy as np

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))

clock = pygame.time.Clock()


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

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if command == 'reverse':
        return reverse(imgRGB)
    if command == 'logarit':
        return logarit(imgRGB, c)
    if command == 'threshold':
        return threshold(imgRGB, th)
    if command == 'gamma':
        return Gamma(imgRGB, gamma, c)


def run():

    button_size = (100, 35)

    reverse_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), button_size),
                                            text='Reverse',
                                            manager=manager)

    logarit_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, button_size[1] + 10*2), button_size),
                                            text='Logarit',
                                            manager=manager)
    
    threshold_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 2*button_size[1] + 10*3), button_size),
                                            text='Threshold',
                                            manager=manager)
    
    gamma_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 3*button_size[1] + 10*4), button_size),
                                            text='Gamma',
                                            manager=manager)

    is_running = True
    isReverse = False
    isLog = False
    isThreshold = False
    isGamma = False

    while is_running:

        time_delta = clock.tick(60)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == reverse_btn:
                    isReverse = True
                if event.ui_element == logarit_btn:
                    isLog = True
                if event.ui_element == gamma_btn:
                    isGamma = True
                if event.ui_element == threshold_btn:
                    isThreshold = True

            manager.process_events(event)

        # keys=pygame.key.get_pressed()

        frame = cv2.imread("flower.jpg")

        if isReverse:
            frame = processing(frame, "reverse")
        if isLog:
            frame = processing(frame, "logarit")
        if isThreshold:
            frame = processing(frame, "threshold")
        if isGamma:
            frame = processing(frame, "gamma")

        manager.update(time_delta)
        window_surface.blit(background, (0, 0))

        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame).convert() 

        window_surface.blit(frame, (120, 10))

        manager.draw_ui(window_surface)

        pygame.display.update()



if __name__ == "__main__":
    run()