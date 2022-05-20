import pygame

class Scaler:
    def __init__(self, image, max_image_display_dimensions):
        self.input_image = image
        self.max_image_display_dimensions = max_image_display_dimensions
        self.image_rect = image.get_rect()
        self.aspect_ratio = self.image_rect.width / self.image_rect.height
        self.output_image = None
    def scale(self):
        need_to_scale = False

        try:
            if self.image_rect.width > self.max_image_display_dimensions[0]:
                self.image_rect.width = self.max_image_display_dimensions[0]
                self.image_rect.height = int(self.image_rect.width / self.aspect_ratio)
                need_to_scale = True

            if self.image_rect.height > self.max_image_display_dimensions[1]:
                self.image_rect.height = self.max_image_display_dimensions[1]
                self.image_rect.width = int(self.image_rect.height * self.aspect_ratio)
                need_to_scale = True

            if need_to_scale:
                self.output_image = pygame.transform.smoothscale(self.input_image, self.image_rect.size)
            
            self.image_rect.center = (400, 300)
        except pygame.error:
            pass

        return self.output_image, self.image_rect


