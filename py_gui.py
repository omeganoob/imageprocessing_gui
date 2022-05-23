import pygame
import pygame_gui
from processor import Processor
import cv2.cv2 as cv2
import numpy as np

from scaler import Scaler
from pygame_gui.elements import UIButton, UIImage
from pygame_gui.windows import UIFileDialog
from pygame_gui.core.utility import create_resource_path
from pygame_gui.elements import UIHorizontalSlider
from pygame_gui.elements import UILabel


class MainApp:
    def __init__(self):
        pygame.init()
        self.scaler_main = None
        self.scaler_sub = None
        self.open_cv_img = None
        self.image_path = None
        self.processor = Processor()
        # elements size and bounds
        self.button_size_m = (100, 35)
        self.button_size_l = (150, 30)
        self.button_square = (35, 35)
        # Main layout and theme
        pygame.display.set_caption('Image Processor')
        self.window_surface = pygame.display.set_mode((800, 600))
        self.ui_manager = pygame_gui.UIManager((800, 600), 'data/themes/main.json')

        self.background = pygame.Surface((800, 600))
        self.background.fill(self.ui_manager.ui_theme.get_colour('dark_bg'))

        # UI Elements
            ##windows
        self.original_image_windows = None

            ##Sliders

        self.slider_threshold = UIHorizontalSlider(pygame.Rect((10, 590 - 25),
                                                          (240, 25)),
                                              255//2,
                                              (0.0, 255.0),
                                              self.ui_manager,
                                              click_increment=5)
        # self.slider_threshold.disable()
        self.label_threshold = UILabel(pygame.Rect((10, 540),
                                                (200, 25)),
                                    'Threshold: ' + str(int(self.slider_threshold.get_current_value())),
                                    self.ui_manager)

        self.slider_c = UIHorizontalSlider(pygame.Rect((260, 590 - 25),
                                                          (240, 25)),
                                              255//2,
                                              (0.0, 255.0),
                                              self.ui_manager,
                                              click_increment=5)
        # self.slider_c.disable()
        self.label_c = UILabel(pygame.Rect((260, 540),
                                                (200, 25)),
                                    'C value: ' + str(int(self.slider_c.get_current_value())),
                                    self.ui_manager)
        
        self.slider_gamma = UIHorizontalSlider(pygame.Rect((510, 590 - 25),
                                                          (240, 25)),
                                              100,
                                              (0.0, 100.0),
                                              self.ui_manager,
                                              click_increment=10)
        # self.slider_gamma.disable()
        self.label_gamma = UILabel(pygame.Rect((510, 540),
                                                (200, 25)),
                                    'Gamma: ' + str(float(self.slider_gamma.get_current_value()/100)),
                                    self.ui_manager)
            ##Buttons
        self.load_button = UIButton(relative_rect=pygame.Rect(( -45, 10), self.button_square),
                                    text="Upload",
                                    manager=self.ui_manager,
                                    anchors={'left': 'right',
                                            'right': 'right',
                                            'top': 'top',
                                            'bottom': 'top'})

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

        self.gaussBlur_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 4*self.button_size_m[1] + 10*5), self.button_size_m),
                                                    text='Gaussian Blur',
                                                    manager=self.ui_manager,
                                                    anchors={
            'left': 'left',
            'right': 'left',
            'top': 'top',
            'bottom': 'top'
        })

        self.hist_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 5*self.button_size_m[1] + 10*6), self.button_size_m),
                                                    text='Histogram E',
                                                    manager=self.ui_manager,
                                                    anchors={
            'left': 'left',
            'right': 'left',
            'top': 'top',
            'bottom': 'top'
        })

        self.adapt_filter_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 6*self.button_size_m[1] + 10*7), self.button_size_m),
                                                    text='Adaptive F',
                                                    manager=self.ui_manager,
                                                    anchors={
            'left': 'left',
            'right': 'left',
            'top': 'top',
            'bottom': 'top'
        })

        self.max_filter_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 7*self.button_size_m[1] + 10*8), self.button_size_m),
                                                    text='Max F',
                                                    manager=self.ui_manager,
                                                    anchors={
            'left': 'left',
            'right': 'left',
            'top': 'top',
            'bottom': 'top'
        })

        self.median_filter_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 8*self.button_size_m[1] + 10*9), self.button_size_m),
                                                    text='Median F',
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
            commands = {
                "isReverse" : False,
                "isLog" : False,
                "isThreshold" : False,
                "isGamma" : False,
                "isGaussian" : False,
                "isHist" : False,
                "isAdaptiveF": False,
                "isMaxF" : False,
                "isMedianF": False
            }

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

                        self.image_path = create_resource_path(event.text)
                        # self.open_cv_img = cv2.imread(self.image_path)
                        # self.open_cv_img = cv2.cvtColor(self.open_cv_img, cv2.COLOR_BGR2RGB)

                        original_img = pygame.image.load(self.image_path).convert_alpha()
                        self.scaler_sub = Scaler(original_img, (200, 200))
                        original_dis = self.scaler_sub.scale()[0]
                        self.original_image_windows = pygame_gui.elements.UIWindow(rect=pygame.Rect((50, 50), (200, 200)),
                                                        manager=self.ui_manager, resizable=True,
                                                        window_display_title='Original Image')
                        self.original_image_windows.set_minimum_dimensions((100, 100))

                        UIImage(relative_rect=pygame.Rect((0,0), (200, 200)),
                                                            image_surface=original_dis,
                                                            container=self.original_image_windows,
                                                            manager=self.ui_manager,
                                                            anchors={
                                                            'left': 'left',
                                                            'right': 'left',
                                                            'top': 'top',
                                                            'bottom': 'top'
                                                        })
                    self.label_threshold.clear_text_surface()
                    self.label_threshold = UILabel(pygame.Rect((10, 540),
                                                (200, 25)),
                                    'Threshold: ' + str(int(self.slider_threshold.get_current_value())),
                                    self.ui_manager)
                    self.label_c.clear_text_surface()
                    self.label_c = UILabel(pygame.Rect((260, 540),
                                                (200, 25)),
                                    'C value: ' + str(int(self.slider_c.get_current_value())),
                                    self.ui_manager)
                    self.label_gamma.clear_text_surface()
                    self.label_gamma = UILabel(pygame.Rect((510, 540),
                                                (200, 25)),
                                    'Gamma: ' + str(float(self.slider_gamma.get_current_value()/100)),
                                    self.ui_manager)
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.reverse_btn:
                            commands = {x : False for x in commands}
                            commands["isReverse"] = True
                        if event.ui_element == self.logarit_btn:
                            commands = {x : False for x in commands}
                            commands["isLog"] = True
                        if event.ui_element == self.gamma_btn:
                            commands = {x : False for x in commands}
                            commands["isGamma"] = True
                        if event.ui_element == self.threshold_btn:
                            commands = {x : False for x in commands}
                            commands["isThreshold"] = True
                        if event.ui_element == self.gaussBlur_btn:
                            commands = {x : False for x in commands}
                            commands["isGaussian"] = True
                        if event.ui_element == self.hist_btn:
                            commands = {x : False for x in commands}
                            commands["isHist"] = True
                        if event.ui_element == self.adapt_filter_btn:
                            commands = {x : False for x in commands}
                            commands["isAdaptiveF"] = True
                        if event.ui_element == self.max_filter_btn:
                            commands = {x : False for x in commands}
                            commands["isMaxF"] = True
                        if event.ui_element == self.median_filter_btn:
                            commands = {x : False for x in commands}
                            commands["isMedianF"] = True

                    self.ui_manager.process_events(event)
                
                if self.image_path is not None:
                    self.open_cv_img = cv2.imread(self.image_path)
                    self.open_cv_img = cv2.cvtColor(self.open_cv_img, cv2.COLOR_BGR2RGB)

                if commands["isReverse"]:
                    self.open_cv_img = self.processor.processing(self.open_cv_img, "reverse")
                if commands["isLog"]:
                    self.open_cv_img = self.processor.processing(self.open_cv_img, "logarit")
                if commands["isThreshold"]:
                    self.open_cv_img = self.processor.processing(self.open_cv_img, "threshold")
                if commands["isGamma"]:
                    self.open_cv_img = self.processor.processing(self.open_cv_img, "gamma")
                if commands["isGaussian"]:
                    self.open_cv_img = self.processor.processing(self.open_cv_img, "gaussian")
                if commands["isHist"]:
                    self.open_cv_img = self.processor.processing(self.open_cv_img, "hist_equalize")
                if commands["isAdaptiveF"]:
                    self.open_cv_img = self.processor.processing(self.open_cv_img, "adaptive_filter")
                if commands["isMaxF"]:
                    self.open_cv_img = self.processor.processing(self.open_cv_img, "max_filter")
                if commands["isMedianF"]:
                    self.open_cv_img = self.processor.processing(self.open_cv_img, "median_filter")

                self.window_surface.blit(self.background, (0, 0))

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
                self.ui_manager.draw_ui(self.window_surface)
                pygame.display.update()
