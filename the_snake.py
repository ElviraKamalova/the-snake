"""Классическая игра Змейка на базе библиотеки Pygame.

Модуль заупскает игорое окно, обрабатывает ввод пользователя и управляет
логикой игры.

Управление в игре:
    - Стрелки (ВВЕРХ, ВНИЗ, ВЛЕВО, ВПРАВО): смена направления змейки.
    - Крестик окна: выход из игры.

Правила:
    - При столкновении змейки с яблоком, змейка растет в длину,
    а яблокот меняет позицию.
    - При выходе за границы игорового окна змейка появляется
    с противополной стороны.
    - При столкновении змейки с своим хвостом игра сбрасывается.
"""

from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Словарь смены направлений:
DIRECTION_KEY = {
    (pg.K_UP, LEFT): UP,
    (pg.K_UP, RIGHT): UP,
    (pg.K_UP, UP): UP,

    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_DOWN, RIGHT): DOWN,
    (pg.K_DOWN, DOWN): DOWN,

    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,
    (pg.K_LEFT, LEFT): LEFT,

    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT,
    (pg.K_RIGHT, RIGHT): RIGHT
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(
            self, body_color=None,
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ):
        """Метод инициализирует игровые объекты."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки объектов.

        Должен быть реализован в дочерних классах.
        """
        raise NotImplementedError(
            f'Метод draw() не реализован к классе {self.__class__.__name__})'
        )

    def _draw_cell(
        self, position=None,
        body_color=None, border_color=BORDER_COLOR
    ):
        """Защищенный метод отрисовки одной ячейки на поле."""
        position = position or self.position
        body_color = body_color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)

        if border_color:
            pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Дочерний класс игрового объекта-Яблоко."""

    def __init__(self, occupied_cells=None):
        """Метод инициализирует игровой объект.

        Принимает набор (set) занятых на игровом поле координат.
        """
        super().__init__(body_color=APPLE_COLOR)
        # Если при старте игры нет занятых клеток, передаем пустое множество:
        occupied_cells = occupied_cells or set()
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells):
        """Метод определяет случайное положение объекта на игровом поле."""
        # Генерируем множество всех возожных координат на поле:
        cells = {
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
        }
        # Вычитаем из всех клеток только те, которые заняты змейкой:
        free_cells = list(cells - set(occupied_cells))

        # Если есть свободные клетки, выбираем случайную позицию:
        if free_cells:
            random_index = randint(0, len(free_cells) - 1)
            self.position = free_cells[random_index]
        else:
            # Если свободных клеток нет, сбрасываем позицию в центр экрана
            self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        """Метод для отрисовки объекта-Яблоко."""
        self._draw_cell()


class Snake(GameObject):
    """Дочерний класс игрового объекта-Змейка."""

    def __init__(self):
        """Метод инициализирует игровой объект."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def reset(self):
        """Метод возвращает объект в исходное состояние."""
        self.length = 1
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [self.position]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.last = None

    def get_head_position(self):
        """Метод возвращает позицию первого сегмента объекта."""
        return self.positions[0]

    def update_direction(self, next_direction):
        """Метод обновления направления после нажатия на кнопку."""
        if next_direction:
            self.direction = next_direction

    def move(self):
        """Метод реализует движение змейки."""
        cur_x, cur_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (cur_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (cur_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        self.last = (
            self.positions.pop()
            if len(self.positions) > self.length
            else None
        )

    def draw(self):
        """Метод отвечает за отрисовку змейки на игровом поле."""
        self._draw_cell(position=self.get_head_position())
        if self.last:
            self._draw_cell(
                position=self.last, body_color=BOARD_BACKGROUND_COLOR,
                border_color=None
            )


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    next_direction = game_object.direction

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit(
                'Игра "Змейка" корректно '
                'завершена через закрытие окна.'
            )
        elif event.type == pg.KEYDOWN:
            next_direction = DIRECTION_KEY.get(
                (event.key, game_object.direction),
                next_direction
            )
    return next_direction


def main():
    """Функция описыввает игровой цикл."""
    # Инициализация PyGame:
    pg.init()
    snake = Snake()
    apple = Apple(occupied_cells=set(snake.positions))
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        # Обработка ввода и начало движения змейки
        next_direction = handle_keys(snake)
        snake.update_direction(next_direction)
        snake.move()

        head_position = snake.get_head_position()

        # Проверка столкновения змейки с яблоком
        if head_position == apple.position:
            snake.length += 1
            apple.randomize_position(occupied_cells=snake.positions)

        # Проверка столкновения змейки с собой:
        for element in snake.positions[1:]:
            if head_position == element:
                snake.reset()
                apple.randomize_position(occupied_cells=snake.positions)
                screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
