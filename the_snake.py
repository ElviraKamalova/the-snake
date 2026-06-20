from random import choice, randint

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


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
        """Метод для отрисовки объектов."""
        pass


class Apple(GameObject):
    """Дочерний класс игрового объекта-Яблоко."""

    def __init__(self):
        """Метод инициализирует игровой объект."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Метод определяет случайное положение объекта на игровом поле."""
        x = randint(0, (GRID_WIDTH - 1)) * GRID_SIZE
        y = randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Метод для отрисовки объекта."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


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
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Метод возвращает позицию первого сегмента объекта."""
        return self.positions[0]

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод реализует движение змейки."""
        self.update_direction()

        cur_x, cur_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (cur_x + dir_x * GRID_SIZE) % 640
        new_y = (cur_y + dir_y * GRID_SIZE) % 480
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Метод отвечает за отрисовку змейки на игровом поле."""
        # Отрисовка тела змейки
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция описыввает игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Обработка ввода и начало движения змейки
        handle_keys(snake)
        snake.move()

        # Проверка столкновения змейки с собой:
        for element in snake.positions[1:]:
            if snake.get_head_position() == element:
                snake.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)

        # Проверка столкновения змейки с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
