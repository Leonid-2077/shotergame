import pygame
import random
import os

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 700, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Проверяем рабочую директорию
print("Текущая рабочая директория:", os.getcwd())


# Функция для безопасной загрузки файлов
def load_file(filename):
    if not os.path.exists(filename):
        print(f"Ошибка: файл '{filename}' не найден!")
        exit()
    return filename


# Загрузка фоновой музыки
pygame.mixer.init()
pygame.mixer.music.load(load_file("space.ogg"))
pygame.mixer.music.play(-1)

fire_sound = pygame.mixer.Sound(load_file("fire.ogg"))

# Загрузка фона
background = pygame.image.load(load_file("background.jpg"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


# Класс GameSprite (универсальный спрайт)
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, speed, width, height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(load_file(image_path)), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.speed = speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Класс игрока
class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width - 5:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx - 5, self.rect.top, 10, 10, 20)
        bullets.add(bullet)
        fire_sound.play()


# Класс врагов
class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = -50
            self.rect.x = random.randint(50, WIDTH - 50)
            missed += 1


# Класс пули
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


# Создание объектов
player = Player("player.png", WIDTH // 2, HEIGHT - 80, 5, 50, 60)
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Создание врагов
for _ in range(5):
    enemy = Enemy("enemy.png", random.randint(50, WIDTH - 50), random.randint(-100, -40), random.randint(1, 1), 50, 50)
    enemies.add(enemy)

# Шрифты
font = pygame.font.Font(None, 36)

# Переменные для счёта
missed, score = 0, 0
clock = pygame.time.Clock()
running = True

# Игровой цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()

    # Обновление объектов
    player.update()
    enemies.update()
    bullets.update()

    # Проверка столкновений (пули и врагов)
    for bullet in bullets:
        hits = pygame.sprite.spritecollide(bullet, enemies, True)
        for _ in hits:
            score += 1
            bullet.kill()
            enemy = Enemy("enemy.png", random.randint(50, WIDTH - 50), random.randint(-100, -40), random.randint(1, 1 ),
                          50, 50)
            enemies.add(enemy)

    # Проверка проигрыша
    if pygame.sprite.spritecollide(player, enemies, False) or missed >= 3:
         running = False

    # Проверка выигрыша
    if score >= 10:
        running = False

    # Отрисовка объектов
    window.blit(background, (0, 0))
    player.draw(window)
    enemies.draw(window)
    bullets.draw(window)

    # Статистика игры
    score_text = font.render(f"Сбито: {score}", True, (255, 255, 255))
    missed_text = font.render(f"Пропущено: {missed}", True, (255, 0, 0))
    window.blit(score_text, (10, 10))
    window.blit(missed_text, (10, 40))

    pygame.display.update()
    clock.tick(60)

pygame.quit()

