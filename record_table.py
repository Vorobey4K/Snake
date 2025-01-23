import pygame
import settings
import json

class RecordTableScreen:
    def __init__(self,main_instance):
        """Инициализация экрана с таблицей рекордов"""
        self.screen = main_instance.screen
        self.main_instance = main_instance

        self.font_title = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 40)
        self.font_text = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 25)

        self.title_text = self.font_title.render('HIGH SCORES', True, settings.SCOREBOARD_BACKGROUND_COLOR)
        self.button_back_off = self.font_text.render('BACK', True, settings.SCOREBOARD_BACKGROUND_COLOR)
        self.button_back_on = self.font_text.render('BACK', True, settings.SCOREBOARD_BACKGROUND_ALT_COLOR)

        self.title_rect = self.title_text.get_rect(center=(settings.SCOREBOARD_TITLE_X,settings.SCOREBOARD_TITLE_Y))
        self.button_back_rect = self.button_back_on.get_rect(topleft=(settings.BACK_BUTTON_X,settings.BACK_BUTTON_Y))

        self.is_back_pressed = False


    def __call__(self):
        """Основной метод для отображения экрана рекордов"""
        self.screen.fill(settings.MAIN_GAME_BACKGROUND_COLOR)
        self.screen.blit(self.title_text, self.title_rect)
        self.draw_table_scores()
        self.draw_back_button()
        pygame.display.update()


    def track_mouse_clicks(self,mouse_rect,mouse_press):
        """Обработка кликов мыши по кнопке "Назад"""
        if self.button_back_rect.collidepoint(mouse_rect):
            self.is_back_pressed = True
            if mouse_press[0]:
                self.main_instance.status = 'menu'

        else:
            self.is_back_pressed = False


    def draw_table_scores(self):
        """Отображение таблицы с рекордами"""
        leaderboard = self.open_file()
        vertical_position = settings.SCOREBOARD_VERTICAL_POSITION
        for index in range(1, 11):
            player_name, player_score = ('', ''), ('', '')
            if len(leaderboard) >= index:
                player_name, player_score = leaderboard[index - 1].items()
            score_text = self.font_text.render(f'{index}. {player_name[1]}:{player_score[1]}', True,settings.SCOREBOARD_BACKGROUND_COLOR)
            vertical_position += settings.SCOREBOARD_VERTICAL_OFFSET
            text_rect = score_text.get_rect(topleft=(settings.SCOREBOARD_HORIZONTAL_POSITION, vertical_position))
            self.screen.blit(score_text, text_rect)


    def draw_back_button(self):
        """Отображение кнопки "Назад"""
        if self.is_back_pressed:
            self.screen.blit(self.button_back_on, self.button_back_rect)
        else:
            self.screen.blit(self.button_back_off, self.button_back_rect)


    def open_file(self):
        """Открытие и сортировка файла с результатами"""
        with open('scores.json','r',encoding='utf-8') as file:
            data = json.load(file)
        data = sorted(data,key=lambda x:x['score'],reverse=True)
        data = data[:10]
        return data


    def add_result(self):
        """Добавление нового результата в таблицу"""
        data = self.open_file()
        data.append({'name':self.main_instance.name_player,'score':self.main_instance.total})
        with open('scores.json', 'w') as file:
            json.dump(data, file, indent=4)