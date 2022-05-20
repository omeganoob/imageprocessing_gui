import pygame
import pygame_gui
from processor import processing
import cv2.cv2 as cv2
import numpy as np

from scaler import Scaler
from pygame_gui.elements import UIButton, UIImage
from pygame_gui.windows import UIFileDialog
from pygame_gui.core.utility import create_resource_path


class MainApp:
    def __init__(self):
        pygame.init()
        self.scaler_main = None
        self.scaler_sub = None
        self.open_cv_img = None
        # elements size and bounds
        self.button_size_m = (100, 35)
        self.button_size_l = (150, 30)
        # Main layout and theme
        pygame.display.set_caption('Quick Start')
        self.window_surface = pygame.display.set_mode((800, 600))
        self.ui_manager = pygame_gui.UIManager((800, 600), 'data/themes/main.json')

        self.background = pygame.Surface((800, 600))
        self.background.fill(self.ui_manager.ui_theme.get_colour('dark_bg'))

        # UI Elements
            ##windows
        self.original_image_windows = None

        self.load_button = UIButton(relative_rect=pygame.Rect(( -160, -40), self.button_size_l),
                                    text='Load Image',
                                    manager=self.ui_manager,
                                    anchors={'left': 'right',
                                            'right': 'right',
                                            'top': 'bottom',
                                            'bottom': 'bottom'})

        self.reverse_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), self.button_size_m),
                                                        text='Reverse',
                                                        manager=self.ui_manager,
                                                        anchors={
            'left': 'left',
            'right': 'left',
            'top': 'top',
            'bottom': 'top'
        })

        self.logarit_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, self.button_size_m[1] + 10*2), self.button_size_m),
                                                        text='Logarit',
                                                        manager=self.ui_manager,
                                                        anchors={
            'left': 'left',
            'right': 'left',
            'top': 'top',
            'bottom': 'top'
        })

        self.threshold_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 2*self.button_size_m[1] + 10*3), self.button_size_m),
                                                        text='Threshold',
                                                        manager=self.ui_manager,
                                                        anchors={
            'left': 'left',
            'right': 'left',
            'top': 'top',
            'bottom': 'top'
        })

        self.gamma_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 3*self.button_size_m[1] + 10*4), self.button_size_m),
                                                    text='Gamma',
                                                    manager=self.ui_manager,
                                                    anchors={
            'left': 'left',
            'right': 'left',
            'top': 'top',
            'bottom': 'top'
        })

        self.file_dialog = None

        self.max_image_display_dimensions = (500, 500)
        self.display_loaded_image = None

        self.clock = pygame.time.Clock()
        self.is_running = True

    def run(self):

            isReverse = False
            isLog = False
            isThreshold = False
            isGamma = False

            while self.is_running:

                time_delta = self.clock.tick(60)/1000.0

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.is_running = False
                    
                    if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                            event.ui_element == self.load_button):
                        self.file_dialog = UIFileDialog(pygame.Rect(160, 50, 440, 500),
                                                        self.ui_manager,
                                                        window_title='Choose Image...',
                                                        initial_file_path='data/',
                                                        allow_picking_directories=True,
                                                        allow_existing_files_only=True)
                        # self.load_button.disable()

                    if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                        if self.display_loaded_image is not None:
                            self.display_loaded_image.kill()

                        image_path = create_resource_path(event.text)
                        self.open_cv_img = cv2.imread(image_path)
                        original_img = pygame.image.load(image_path).convert_alpha()
                        self.scaler_sub = Scaler(original_img, (200, 200))
                        original_dis = self.scaler_sub.scale()[0]
                        self.original_image_windows = pygame_gui.elements.UIWindow(rect=pygame.Rect((50, 50), (200, 200)),
                                                        manager=self.ui_manager, resizable=True,
                                                        window_display_title='Original Image')
                        self.original_image_windows.set_minimum_dimensions((100, 100))

                        display_original_image = UIImage(relative_rect=pygame.Rect((0,0), (200, 200)),
                                                            image_surface=original_dis,
                                                            container=self.original_image_windows,
                                                            manager=self.ui_manager,
                                                            anchors={
            'left': 'left',
            'right': 'left',
            'top': 'top',
            'bottom': 'top'
        })

                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.reverse_btn:
                            isReverse = True
                            isLog = False
                            isGamma = False
                            isThreshold = False
                        if event.ui_element == self.logarit_btn:
                            isLog = True
                            isReverse = False
                            isGamma = False
                            isThreshold = False
                        if event.ui_element == self.gamma_btn:
                            isGamma = True
                            isReverse = False
                            isLog = False
                            isThreshold = False
                        if event.ui_element == self.threshold_btn:
                            isThreshold = True
                            isGamma = False
                            isReverse = False
                            isLog = False

                    self.ui_manager.process_events(event)
                
                    if isReverse:
                        self.open_cv_img = processing(self.open_cv_img, "reverse")
                    if isLog:
                        self.open_cv_img = processing(self.open_cv_img, "logarit")
                    if isThreshold:
                        self.open_cv_img = processing(self.open_cv_img, "threshold")
                    if isGamma:
                        self.open_cv_img = processing(self.open_cv_img, "gamma")

                if self.open_cv_img is not None:
                    frame = np.rot90(self.open_cv_img)
                    frame = pygame.surfarray.make_surface(frame).convert_alpha()

                    image_rect = frame.get_rect()
                    self.scaler_main = Scaler(frame, self.max_image_display_dimensions)
                    display_image, image_rect = self.scaler_main.scale()
                    self.display_loaded_image = UIImage(relative_rect=image_rect,
                                                            image_surface=display_image,
                                                            manager=self.ui_manager)

                self.ui_manager.update(time_delta)
                self.window_surface.blit(self.background, (0, 0))
                self.ui_manager.draw_ui(self.window_surface)
                pygame.display.update()
