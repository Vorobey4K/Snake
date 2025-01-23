import pygame
import sys
import settings
from menu import Menu
from game import Game
from screensaver import Screensaver
from record_table import RecordTableScreen
from game_over import GameOverState
class MainClass:
    """Основной класс игры, управляющий состояниями и основным циклом."""

    def __init__(self):
        """Инициализация игры и ее компонентов."""
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.GAME_NAME)
        self.menu = Menu(self)
        self.game = Game(self)
        self.screensaver = Screensaver(self)
        self.record_table = RecordTableScreen(self)
        self.game_over = GameOverState(self)
        self.time = pygame.time.Clock()
        self.status = 'screensaver' # Начальное состояние игры
        self.FPS = settings.FPS_MENU
        self.name_player = None
        self.total = None
    def run_game(self):
        """Запуск основного игрового цикла."""
        while True:
            self.mouse_rect = pygame.mouse.get_pos()
            self.mouse_press = pygame.mouse.get_pressed()
            self.time.tick(self.FPS)
            self._check_events()
            self._execute_game_state()



    def _check_events(self):
        """Обработка событий игры."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.menu.input_field_events(event) # Обработка событий ввода в меню

            if self.game.change_snake_direction(event):  # Изменение направления змейки
                break

        # Проверяем текущее состояние игры и обрабатываем клики мыши соответствующим образом
        if self.status == 'record_table':
            self.record_table.track_mouse_clicks(self.mouse_rect,self.mouse_press)
        elif self.status == 'menu':
            self.menu.track_mouse_clicks(self.mouse_rect,self.mouse_press)
        elif self.status == 'question':
            self.game_over.track_mouse_clicks(self.mouse_rect,self.mouse_press)


    def _execute_game_state(self):
        """Выполнение действий в зависимости от состояния игры."""
        if self.status == 'screensaver':
            self.screensaver()
        elif self.status == 'menu':
            self.FPS = settings.FPS_MENU
            self.menu.menu()
        elif self.status == 'add_result':
            self.record_table.add_result()
            self.status = 'game_over'
        elif self.status == 'game_over':
            self.FPS = settings.FPS_MENU
            self.game_over()
        elif self.status == 'game':
            self.game.play_game()
            self.FPS = settings.FPS_GAME
        elif self.status == 'question':
            self.game_over.question()
        elif self.status == 'record_table':
            self.record_table()




if __name__ == '__main__':
    ai = MainClass()
    ai.run_game()



