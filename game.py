import pygame
import settings
from random import shuffle


class Game:
    """"Основной класс игрового процесса """

    def __init__(self,obj):
        """"Инцилизируем игру."""

        self.screen = obj.screen
        self.main_class = obj
        self.initialize_game_field()  # Создание игрового поля

        # Шрифт и текст для отображения счета
        self.score_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 40)
        self.score_text = self.score_font.render(f'TOTAL:{self.total_score}', True, settings.SCORE_COLOR)
        self.score_rest = self.score_text.get_rect(center=(settings.SCORE_X, settings.SCORE_Y))

    def update_score_display(self):
        """Обновляет и отображает текущий счет на экране."""
        self.score_text = self.score_font.render(f'TOTAL:{self.total_score}', True, settings.SCORE_COLOR)
        self.screen.blit(self.score_text, self.score_rest)

    def play_game(self):
        """Основной метод игрового процесса."""
        self.screen.fill(settings.MAIN_GAME_BACKGROUND_COLOR)  # Очистка экрана
        self.screen.blit(self.field_surface, self.field_rect)  # Отображение игрового поля
        self.spawn_food()  # Размещение еды
        self.update_score_display()  # Обновление счета

        # Перемещение змейки и проверка на столкновение с едой
        if self.move_snake():
            if (self.cord_food_x,self.cord_food_y) == self.snake_body[-1].get_coord():
                self.snake_length += 1
                self.total_score += 1
                self.food_available = True

            pygame.display.update()
        else:
            self.main_class.total = self.total_score
            self.initialize_game_field()
            self.main_class.status = 'add_result'



    def change_snake_direction(self,event):
        """Обновляет направление змейки в зависимости от нажатой клавиши."""
        if event.type == pygame.KEYDOWN and self.main_class.status == 'game':
            if event.key == pygame.K_RIGHT and not self.snake_direction == 'left':
                self.snake_direction = 'right'

            elif event.key == pygame.K_LEFT and not self.snake_direction == 'right':
                self.snake_direction = 'left'

            elif event.key == pygame.K_DOWN and not self.snake_direction == 'up':
                self.snake_direction = 'down'

            elif event.key == pygame.K_UP and not self.snake_direction == 'down':
                self.snake_direction = 'up'
            return True
        else:
            return False



    def initialize_game_field(self):
        """Создает игровое поле и инициализирует параметры игры."""
        self.total_score = 0  # Счет игры
        self.snake_direction = 'right'  # Направление змейки
        self.food_available = True  # Индикатор наличия еды на поле
        self.snake_head_x = settings.SNAKE_START_X
        self.snake_head_y = settings.SNAKE_START_Y
        self.snake_body = []  # Сегменты змейки
        self.snake_length = 1  # Длина змейки
        self.cell_grid = []  # Сетка клеток игрового поля
        self.available_cells = []  # Доступные клетки для еды

        # Настройка размеров и цветов поля
        field_colors = settings.FIELD_COLOR
        field_width = (settings.GRID_COLS *(settings.CELL_SIZE + settings.GRID_GAP))

        field_height = (settings.GRID_ROWS * (settings.CELL_SIZE + settings.GRID_GAP))
        indent_width = (settings.SCREEN_WIDTH - field_width)/2
        indent_height = (settings.SCREEN_HEIGHT - field_height)/2

        self.field_surface = pygame.Surface((field_width,field_height))

        # Создание сетки клеток
        for col_index in range(settings.GRID_COLS):
            row_cells = []
            for row_index in range(settings.GRID_ROWS):
                cell_surface = pygame.Surface((settings.CELL_SIZE, settings.CELL_SIZE))
                if (col_index + row_index) % 2 == 0:
                    cell_surface.fill(field_colors[0])
                else:
                    cell_surface.fill(field_colors[1])

                cell_x = settings.CELL_SIZE * col_index + settings.GRID_GAP * col_index
                cell_y = settings.CELL_SIZE * row_index + settings.GRID_GAP * row_index

                cell_object = Cell(col_index, row_index, cell_x + indent_width, cell_y + indent_height)
                row_cells.append(cell_object)

                self.field_surface.blit(cell_surface, (cell_x, cell_y))
            self.cell_grid.append(row_cells)

        self.field_rect = self.field_surface.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT  / 2))
        for row in self.cell_grid:
            self.available_cells.extend(row)



    def move_snake(self):
        """Перемещает змейку в текущем направлении и проверяет на столкновения."""
        surface = pygame.Surface((settings.CELL_SIZE, settings.CELL_SIZE))

        # Изменение координат головы змейки
        if self.snake_direction == 'right':
           self.snake_head_x += 1
        elif self.snake_direction == 'left':
            self.snake_head_x -= 1
        elif self.snake_direction == 'down':
            self.snake_head_y += 1
        elif self.snake_direction == 'up':
            self.snake_head_y -= 1

        try:
            object_snake = self.cell_grid[self.snake_head_x][self.snake_head_y]
            self.available_cells.remove(object_snake)
            if self.snake_head_x<0 or self.snake_head_y<0:
                raise IndexError
        except:
            return False

        # Добавление нового сегмента змейки
        self.snake_body.append(object_snake)
        if len(self.snake_body) > self.snake_length:
            self.available_cells.append(self.snake_body.pop(0))

        # Отображение змейки
        for index, obj in enumerate(self.snake_body):
            surface.fill(settings.SNAKE_HEAD_COLOR if index == len(self.snake_body) - 1 else settings.SNAKE_BODY_COLOR)
            self.screen.blit(surface, obj.rect)

        return True




    def spawn_food(self):
        """Размещает еду на поле."""
        if self.food_available:
            while True:
                copy_lst = self.available_cells.copy()
                shuffle(copy_lst)
                self.cord_food_x,self.cord_food_y = copy_lst[0].get_coord()
                if not (self.cord_food_x,self.cord_food_y) == (self.snake_head_x,self.snake_head_y):
                    break


            self.food_available = False

        # Отображение еды
        surface = pygame.Surface((settings.CELL_SIZE, settings.CELL_SIZE))
        surface.fill(settings.FOOD_COLOR)
        self.screen.blit(surface,self.cell_grid[self.cord_food_x][self.cord_food_y].rect)






class Cell:
    def __init__(self, column, row, x_position, y_position):
        """Инициализация клетки игрового поля."""
        self.rect = pygame.Rect(x_position,y_position,settings.CELL_SIZE ,settings.CELL_SIZE)
        self.column = column
        self.row = row

    def get_coord(self):
        """Возвращает координаты клетки (столбец, строка)."""
        return (self.column,self.row)
