import pygame
import settings

class GameOverState:
    """ Класс для управления состоянием "Game Over"""

    def __init__(self,main_instance):
        self.screen = main_instance.screen
        self.main_instance = main_instance
        self.over_screensaver_time = settings.GAME_OVER_SCREENSAVER_TIME

        self.font_title = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 40)
        self.font_text = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 30)

        self.image_game_over = pygame.image.load('images/game_over_image.bmp')
        self.button_yes_off = self.font_text.render('YES', True, settings.COLOR_TEST_OVER)
        self.button_no_off = self.font_text.render('NO', True, settings.COLOR_TEST_OVER)
        self.button_yes_on = self.font_text.render('YES', True, settings.MENU_BACKGROUND_ALT_COLOR)
        self.button_no_on = self.font_text.render('NO', True, settings.MENU_BACKGROUND_ALT_COLOR)


        self.yes_button_rect = self.button_yes_off.get_rect(topleft=(settings.SCREEN_WIDTH / 2 - settings.SCREEN_WIDTH / 4, settings.CHOICE_BUTTON_Y))
        self.no_button_rect  = self.button_no_off.get_rect(topright=(settings.SCREEN_WIDTH / 2 + settings.SCREEN_WIDTH / 4, settings.CHOICE_BUTTON_Y))

        self.play_again_text = self.font_title.render('PLAY AGAIN?', True, settings.COLOR_TEST_OVER)
        self.play_again_text_rect = self.play_again_text.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.PLAY_AGAIN_Y))
        self.is_yes_pressed = False
        self.is_no_pressed = False


    def track_mouse_clicks(self,mouse_rect, mouse_press):
        """Обрабатывает клики мыши на экране вопроса "PLAY AGAIN?"""
        if self.main_instance.status == 'question':
            if self.yes_button_rect.collidepoint(mouse_rect):
                self.is_yes_pressed = True
                if mouse_press[0]:


                    self.main_instance.status = 'game'
            else:
                self.is_yes_pressed = False

            if self.no_button_rect.collidepoint(mouse_rect):
                self.is_no_pressed = True
                if mouse_press[0]:
                    self.main_instance.status = 'menu'
                    self.main_instance.mouse_released = False
            else:
                self.is_no_pressed = False

    def __call__(self):
        """Отображает экран "Game Over" с заставкой."""
        self.screen.fill('Black')
        self.screen.blit(self.image_game_over,(0,200))
        if self.over_screensaver_time > 0:
            self.over_screensaver_time -= 1
        else:
            self.main_instance.status = 'question'
            self.over_screensaver_time = settings.GAME_OVER_SCREENSAVER_TIME

        pygame.display.update()


    def question(self):
        """Отображает экран с вопросом "PLAY AGAIN?"""
        self.screen.fill('Black')
        self.screen.blit(self.play_again_text, self.play_again_text_rect)
        if self.is_yes_pressed:
            self.screen.blit(self.button_yes_on,self.yes_button_rect)
        else:
            self.screen.blit(self.button_yes_off, self.yes_button_rect)
        if self.is_no_pressed:
            self.screen.blit(self.button_no_on,self.no_button_rect)
        else:
            self.screen.blit(self.button_no_off, self.no_button_rect)
        pygame.display.update()