import pygame
import settings
class Screensaver:
    def __init__(self,main_instance):
        """"Инициализирует объект заставки."""
        self.screen = main_instance.screen
        self.background = pygame.image.load('images/screensaver_image.png')
        self.remaining_time = settings.SCREENSAVER_REMAINING_TIME
        self.main_instance = main_instance

    def __call__(self):
        """Отображает заставку и переключает статус игры на 'menu' по истечении времени."""
        self.screen.blit(self.background, (0, 0))
        if self.remaining_time > 0:
            self.remaining_time -= 1
        else:
            self.main_instance.status = 'menu'
        pygame.display.update()