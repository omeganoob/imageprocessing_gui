from calendar import c
import cv2.cv2 as cv2
import numpy as np
import gaussian_blur
from gaussian_blur import *
from hist_equalizer import hist_equalize
from adaptive_filter import AdaptiveFilter
from max_filter import MaxFilter
from median_filter import MedianFilter
class Processor:
    def __init__(self, app):
        self.app = app

    def processing(self, img, command):

        def histogramEqualize(img):
            image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            image_gray_new = hist_equalize(image_gray)[image_gray.flatten()]
            image_gray_new = np.reshape(image_gray_new, image_gray.shape)
            return image_gray_new

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

        def Gaussian_blur(image):
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            new_img_arr = padding(image_gray)
            kernel = gaussian_kernel(43, 7)
            new_img_arr = gaussian(image, new_img_arr, kernel)
            return new_img_arr

        def adaptive_filter(image):
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return AdaptiveFilter(image, image_gray)
        
        def max_filter(image):
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return MaxFilter(image, image_gray)
        def median_filter(image):
            return MedianFilter(image)

        if command == 'reverse':
            return reverse(img)
        if command == 'logarit':
            return logarit(img, self.app.slider_c.get_current_value())
        if command == 'threshold':
            return threshold(img, self.app.slider_threshold.get_current_value())
        if command == 'gamma':
            return Gamma(img, round(self.app.slider_gamma.get_current_value()/100, 1), self.app.slider_c.get_current_value())
        if command == 'gaussian':
            return Gaussian_blur(img)
        if command == 'hist_equalize':
            return histogramEqualize(img)
        if command == 'adaptive_filter':
            return adaptive_filter(img)
        if command == 'max_filter':
            return max_filter(img)
        if command == 'median_filter':
            return median_filter(img)