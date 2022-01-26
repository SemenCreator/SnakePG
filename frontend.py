import pygame
import random
import sqlite3
# for github


class StartWindow:
    def __init__(self, patch):
        pygame.init()
        pygame.display.set_caption('Змейка')
        self.screen = pygame.display.set_mode((600, 640))
        self.patch = patch
        self.image_on_screen(pygame.image.load("images\\level.png"), ((89, 0)))
        first, second, third = self.define_records()
        self.special()
        self.levels(first, second, third)
        pygame.display.update()

    def define_records(self):
        with sqlite3.connect('bd\\Snake.sqlite') as con:
            cur = con.cursor()
            levels_records = cur.execute(
                """SELECT * FROM records""").fetchone()
            return levels_records

    def image_on_screen(self, image, size):
        self.screen.blit(image, size)

    def special(self):
        if self.patch:
            color = pygame.Color('green')
        else:
            color = pygame.Color('red')
        pygame.draw.polygon(self.screen, color, [
                            (0, 600), (0, 640), (600, 640), (600, 600)])
        font_back = pygame.font.Font(None, 40)
        text = font_back.render("Для 10 IT", True, (0, 0, 0))
        self.screen.blit(text, (230, 610))

    def levels(self, *level_records):
        numbers = [1, 2, 3]
        number = 0
        for x in range(75, 675, 200):
            font = pygame.font.Font(None, 150)
            text = font.render(f"{numbers[number]}", True, (255, 0, 0))
            text_y = 600 // 2 - text.get_height() // 2
            self.screen.blit(text, (x, text_y))
            text_w = text.get_width()
            text_h = text.get_height()
            pygame.draw.rect(self.screen, (255, 0, 0), (x - 10,
                             text_y - 10, text_w + 20, text_h + 20), 1)
            self.image_on_screen(pygame.image.load(
                "images\\record.png"), ((x - 92 + ((text_w + 20) // 2), 362)))
            font_record = pygame.font.Font(None, 75)
            record = font_record.render(
                f"{level_records[number]}", True, (255, 0, 0))
            self.screen.blit(record, (x - (text_w // 2), 462))
            number += 1

    def define_action(self, position):
        x, y = position
        if 65 < x < 142 and 239 < y < 362:
            return self.screen, 'low', self.patch, 7
        elif 265 < x < 342 and 239 < y < 362:
            return self.screen, 'medium', self.patch, 8
        elif 465 < x < 542 and 239 < y < 362:
            return self.screen, 'hard', self.patch, 9
        elif 0 < x < 600 and 600 < y < 640:
            if self.patch:
                self.patch = False
                self.special()
            else:
                self.patch = True
                self.special()
        else:
            pass


class MainSnake(StartWindow):
    def __init__(self, screen, level, width, height, patch, fps):
        self.patch = patch
        if self.patch:
            self.food = "images\\MC.png"
        else:
            self.food = "images\\apple_for_snake.png"
        self.screen = screen
        self.fps = fps
        self.screen.fill('white')
        self.level = level
        self.width = width
        self.height = height
        self.apple_x = 0
        self.apple_y = 0
        self.main_y = 0
        self.amount_apple = 0
        self.snake_color = (0, 255, 0)
        self.snake_coords = [(280, 240), (280, 280), (280, 320)]
        self.obstacle_coords = [(80, 80), (80, 480), (480, 80), (480, 480)]
        self.length = 3
        self.cell_size = 40
        self.render()

    def draw_snake(self):
        for coord in self.snake_coords:
            x, y = coord
            if self.food != 'images\\apple_for_snake.png':
                self.image_on_screen(pygame.image.load(
                    "images\\KE.png"), (x, y))
            else:
                pygame.draw.rect(self.screen, self.snake_color,
                                 (x, y, self.cell_size, self.cell_size))

    def render_cell(self, x, y, color):
        pygame.draw.rect(
            self.screen, color, (x, y, self.cell_size, self.cell_size), 1)

    def render(self):
        self.screen.fill('white')
        self.total_apple(self.amount_apple)
        for h in range(self.height):
            for w in range(self.width):
                x = w * self.cell_size
                y = h * self.cell_size
                self.render_cell(x, y, pygame.Color('black'))
        self.draw_obstacles()
        self.draw_snake()
        self.image_on_screen(pygame.image.load(
            self.food), (self.apple_x, self.apple_y))

    def total_apple(self, amount_apple):
        pygame.draw.polygon(self.screen, pygame.Color('red'), [
                            (0, 600), (0, 640), (600, 640), (600, 600)])
        font_back = pygame.font.Font(None, 40)
        text = font_back.render(
            f"Всего яблок: {amount_apple}", True, (0, 0, 0))
        self.screen.blit(text, (200, 610))

    def draw_obstacles(self):
        if not self.level == 'low':
            self.obstacle_coords.extend(
                [(80, 120), (80, 440), (440, 80), (480, 440)])
            self.obstacle_coords.extend(
                [(120, 80), (120, 480), (480, 120), (440, 480)])
            if self.level == 'hard':
                self.obstacle_coords.extend(
                    [(80, 160), (80, 400), (400, 80), (480, 400)])
                self.obstacle_coords.extend(
                    [(160, 80), (160, 480), (480, 160), (400, 480)])
        for coord in self.obstacle_coords:
            y, x = coord
            pygame.draw.circle(self.screen, pygame.Color(
                'red'), (x + 20, y + 20), 20)

    def random_apple(self):
        apples = []
        for h in range(0, 600, 40):
            for w in range(0, 600, 40):
                if (h, w) not in self.snake_coords:
                    if (h, w) not in self.obstacle_coords:
                        apples.append([h, w])
        w, h = random.choice(apples)
        self.apple_x = w
        self.apple_y = h
        self.image_on_screen(pygame.image.load(
            self.food), (h, w))
        self.amount_apple += 1
        if self.food != 'images\\apple_for_snake.png':
            if self.food == "images\\MC.png":
                self.food = 'images\\KV.png'
            elif self.food == "images\\KV.png":
                self.food = 'images\\AF.png'
            else:
                self.food = 'images\\MC.png'
        if self.amount_apple % 3 == 0:
            self.snake_color = (0, 0, 255)
        elif self.amount_apple % 2 == 0:
            self.snake_color = (0, 255, 0)
        else:
            self.snake_color = (255, 255, 0)
        self.total_apple(self.amount_apple)

    def move_snake(self, x, y):
        new_coord_x = self.snake_coords[0][0] + x
        new_coord_y = self.snake_coords[0][1] + y
        self.snake_coords.insert(0, (new_coord_x, new_coord_y))
        if (self.apple_x, self.apple_y) in self.snake_coords:
            self.length += 1
            self.random_apple()
        elif not 0 <= self.snake_coords[0][0] < 600 or not \
            0 <= self.snake_coords[0][1] < 600 or \
                self.snake_coords[0] in self.obstacle_coords:
            return False
        elif len(self.snake_coords) != len(set(self.snake_coords)):
            if self.snake_coords[0] != self.snake_coords[2]:
                return False
            else:
                del self.snake_coords[0]
        self.snake_coords = self.snake_coords[:self.length]
        return True


class GameOverWindow(MainSnake):
    def __init__(self, screen, amount_apple, level, patch, fps):
        self.fps = fps
        self.patch = patch
        self.level = level
        self.screen = screen
        screen.fill('black')
        self.total_apple(amount_apple)
        self.repeat()
        self.back_on_start_window()
        self.quit()
        self.counting_results(amount_apple, level)

    def back_on_start_window(self):
        pygame.draw.rect(self.screen, pygame.Color(
            'red'), (10, 10, 500, 100), 5)
        font_back = pygame.font.Font(None, 65)
        text = font_back.render("На начальный экран", True, (255, 0, 0))
        self.screen.blit(text, (25, 40))

    def repeat(self):
        pygame.draw.rect(self.screen, pygame.Color(
            'red'), (10, 120, 500, 100), 5)
        font_back = pygame.font.Font(None, 65)
        text = font_back.render("Сыграть Заново", True, (255, 0, 0))
        self.screen.blit(text, (25, 150))

    def quit(self):
        pygame.draw.rect(self.screen, pygame.Color(
            'red'), (10, 230, 500, 100), 5)
        font_back = pygame.font.Font(None, 65)
        text = font_back.render("Выйти из игры", True, (255, 0, 0))
        self.screen.blit(text, (25, 260))

    def last_define_action(self, position):
        x, y = position
        if 10 < x < 510 and 10 < y < 110:
            return self.patch
        elif 10 < x < 510 and 120 < y < 220:
            return self.screen, 'hard', self.patch, self.fps
        elif 10 < x < 510 and 230 < y < 330:
            exit()

    def counting_results(self, amount_apple, level):
        first, second, third = self.define_records()
        with sqlite3.connect('bd\\Snake.sqlite') as con:
            cur = con.cursor()
            if level == 'low':
                if first < amount_apple:
                    cur.execute('''UPDATE records SET low = ?''',
                                (amount_apple,))
            elif level == 'medium':
                if second < amount_apple:
                    cur.execute('''UPDATE records SET medium = ?''',
                                (amount_apple,))
            else:
                if third < amount_apple:
                    cur.execute('''UPDATE records SET hard = ?''',
                                (amount_apple,))


if __name__ == '__main__':
    window = 'StartWindow'
    start_window = StartWindow(False)
    running = True
    main_x = 0
    main_y = 0
    fps = 5
    start = False
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if window == 'StartWindow':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    values = start_window.define_action(
                        event.pos)
                    if values is not None:
                        screen, level, patch, fps = values
                        main_snake = MainSnake(
                            screen, level, 15, 15, patch, fps)
                        window = 'MainWindow'
                        start = False
            elif window == 'MainWindow':
                if event.type == pygame.KEYDOWN:
                    all_keys = pygame.key.get_pressed()
                    if all_keys[pygame.K_RIGHT] or all_keys[pygame.K_d]:
                        main_x = 40
                        main_y = 0
                        start = True
                    elif all_keys[pygame.K_UP] or all_keys[pygame.K_w]:
                        main_x = 0
                        main_y = -40
                        start = True
                    elif all_keys[pygame.K_DOWN] or all_keys[pygame.K_s]:
                        main_x = 0
                        main_y = 40
                        start = True
                    elif all_keys[pygame.K_LEFT] or all_keys[pygame.K_a]:
                        main_x = -40
                        main_y = 0
                        start = True
                    else:
                        pass
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    new_window_values = game_over_window.last_define_action(
                        event.pos)
                    if new_window_values is not None:
                        if not new_window_values:
                            StartWindow(patch)
                            window = 'StartWindow'
                        else:
                            screen, level, patch, fps = values
                            main_snake = MainSnake(
                                screen, level, 15, 15, patch, fps)
                            window = 'MainWindow'
                            start = False
        if start and window == 'MainWindow':
            clock.tick(fps)
            running_game = main_snake.move_snake(main_x, main_y)
            main_snake.render()
            if not running_game:
                game_over_window = GameOverWindow(
                    screen, main_snake.amount_apple, level, patch, fps)
                window = 'GameOverWindow'
        pygame.display.flip()
    pygame.quit()
