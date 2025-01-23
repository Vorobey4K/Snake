import pygame
import settings
import json
import sys
class Menu:
    def __init__(self, main_instance):
        """Инициализация главного меню"""

        # Ссылка на главный объект и экран
        self.main_instance = main_instance
        self.screen = main_instance.screen

        # Настройка шрифтов
        self.menu_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 40)
        self.text_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 20)


        # Фон меню
        self.menu_bg = pygame.image.load('images/menu_decoration_image.jpg')

        # Кнопки меню (основной текст и выделенный текст)
        self.start_game = self.menu_font.render('PLAY', True, settings.MENU_BACKGROUND_COLOR)
        self.scores = self.menu_font.render('HIGH SCORES', True, settings.MENU_BACKGROUND_COLOR)
        self.exit_game = self.menu_font.render('EXIT', True, settings.MENU_BACKGROUND_COLOR)

        self.start_game_hover = self.menu_font.render('PLAY', True, settings.MENU_BACKGROUND_ALT_COLOR)
        self.scores_hover = self.menu_font.render('HIGH SCORES', True, settings.MENU_BACKGROUND_ALT_COLOR)
        self.exit_game_hover = self.menu_font.render('EXIT', True, settings.MENU_BACKGROUND_ALT_COLOR)

        # Прямоугольники кнопок
        self.start_game_rect = self.start_game.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.BUTTON_START_Y))
        self.scores_rect = self.scores.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.BUTTON_SCORES_Y))
        self.exit_game_rect = self.exit_game.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.BUTTON_EXIT_Y))

        # Флаги для отслеживания состояний
        self.is_play_hovered = False
        self.is_scores_hovered  = False
        self.is_exit_hovered  = False
        self.is_name_input_active = False

        # Поле для ввода имени
        self.input_text = ''
        self.base_input_field = pygame.Surface((settings.INPUT_FIELD_WIDTH, settings.INPUT_FIELD_HEIGHT))
        self.base_input_field.fill(settings.INPUT_FIELD_COLOR)
        self.base_input_field_rect = self.base_input_field.get_rect(center=(settings.INPUT_WINDOW_WIDTH/2, settings.INPUT_FIELD_Y))

        # Текст вопроса для ввода имени
        self.input_window_title_text = self.text_font.render('ENTER YOUR NICKNAME', True, settings.MENU_BACKGROUND_COLOR)
        self.input_window_title_rect = self.input_window_title_text.get_rect(center=(settings.INPUT_WINDOW_WIDTH/2, settings.INPUT_WINDOW_TITLE_Y))

        # Кнопка закрытия окна
        self.close_button = self.text_font.render('x', True, 'Black')
        self.close_button_rect = self.close_button.get_rect(center=(settings.CLOSE_BUTTON_X, settings.BUTTON_SCORES_Y))

        # Статус активности меню
        self.is_menu_active = True


    def input_field_events(self, event):
        """Обработка событий для ввода текста в поле имени"""
        if event.type == pygame.KEYDOWN and self.is_name_input_active:
            if event.key == pygame.K_RETURN:  # Подтверждение ввода
                if self.input_text:
                    self.main_instance.name_player = self.input_text
                    self.input_text = ''
                    self.is_name_input_active = False
                    self.is_menu_active = True
                    self.main_instance.status = 'game'

            elif event.key == pygame.K_BACKSPACE:  # Удаление символа
                self.input_text = self.input_text[:-1]

            else:  # Ввод нового символа
                if len(self.input_text ) < 15:
                    self.input_text += event.unicode

    def track_mouse_clicks(self, mouse_rect, mouse_press):
        """Обработка кликов мыши"""
        if self.main_instance.status == 'menu':
            # Закрытие окна ввода имени
            if self.is_name_input_active:
                if self.close_button_rect.collidepoint(mouse_rect) and mouse_press[0]:
                    self.is_name_input_active = False
                    self.is_menu_active = True

            # Кнопка PLAY
            if self.start_game_rect.collidepoint(mouse_rect):
                self.is_play_hovered = True
                if mouse_press[0]:
                    self.is_name_input_active = True
                    self.is_menu_active = False
            else:
                self.is_play_hovered = False

            # Кнопка HIGH SCORES
            if self.scores_rect.collidepoint(mouse_rect) and self.is_menu_active:
                self.is_scores_hovered = True
                if mouse_press[0]:
                    self.main_instance.status = 'record_table'
            else:
                self.is_scores_hovered = False

            # Кнопка EXIT
            if self.exit_game_rect.collidepoint(mouse_rect) and self.is_menu_active:
                self.is_exit_hovered = True
                if mouse_press[0]:
                    pygame.quit()
                    sys.exit()
            else:
                self.is_exit_hovered = False


    def menu(self):
        """Отображение основного меню"""
        self.screen.fill('Black')
        self.screen.blit(self.menu_bg, (0, 0))

        # Кнопки меню
        self.screen.blit(self.start_game_hover if self.is_play_hovered else self.start_game, self.start_game_rect)
        self.screen.blit(self.scores_hover if self.is_scores_hovered else self.scores, self.scores_rect)
        self.screen.blit(self.exit_game_hover if self.is_exit_hovered else self.exit_game, self.exit_game_rect)

        # Поле ввода имени
        if self.is_name_input_active:
            self.draw_name_input_window()

        pygame.display.update()






    def draw_name_input_window(self):
        """Рисует окно для ввода имени"""
        input_box = pygame.Surface((settings.INPUT_WINDOW_WIDTH, settings.INPUT_WINDOW_HEIGHT))
        input_box.fill(settings.MENU_BACKGROUND_ALT_COLOR)

        # Отображение текста пользователя
        name_player = self.text_font.render(self.input_text, True, settings.TEXT_INPUT_COLOR)
        name_player_rect = name_player.get_rect(center=(settings.INPUT_WINDOW_WIDTH/2, settings.INPUT_FIELD_Y))

        # Фон для текста
        dynamic_input_field = pygame.Surface((name_player_rect.width, settings.INPUT_FIELD_HEIGHT))
        dynamic_input_field.fill(settings.INPUT_FIELD_COLOR)
        dynamic_input_field_rect = dynamic_input_field.get_rect(center=(settings.INPUT_WINDOW_WIDTH/2, settings.INPUT_FIELD_Y))

        # Отображение элементов
        input_box.blit(self.base_input_field, self.base_input_field_rect)
        input_box.blit(dynamic_input_field, dynamic_input_field_rect)
        input_box.blit(self.input_window_title_text, self.input_window_title_rect)
        input_box.blit(name_player, name_player_rect)

        # Центрирование окна
        input_box_rect = input_box.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2))

        # Отображение на экране
        self.screen.blit(input_box, input_box_rect)
        self.screen.blit(self.close_button, self.close_button_rect)
