import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра на выживание")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Игрок
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - 70
player_speed = 5

# Враги
enemy_size = 50
enemy_speed = 3
enemy_list = []

# Бонусы
bonus_size = 30
bonus_list = []
bonus_duration = 200  # Количество кадров, на которые замедляется скорость врагов
bonus_active = 0

# Таймер для очков
score = 0
font = pygame.font.Font(None, 36)


# Функция создания врага
def create_enemy():
    x = random.randint(0, WIDTH - enemy_size)
    y = 0
    enemy_list.append([x, y])


# Функция создания бонуса
def create_bonus():
    x = random.randint(0, WIDTH - bonus_size)
    y = random.randint(50, HEIGHT - 200)
    bonus_list.append([x, y])


# Основной игровой цикл
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)

    # Закрытие окна
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += player_speed

    # Создание врагов
    if random.randint(1, 40) == 1:
        create_enemy()

    # Создание бонусов
    if random.randint(1, 500) == 1:
        create_bonus()

    # Движение врагов
    for enemy in enemy_list:
        enemy[1] += enemy_speed if bonus_active == 0 else enemy_speed // 2
        enemy[0] += random.choice([-1, 1])  # Немного случайного движения в стороны
        if enemy[1] > HEIGHT:
            enemy_list.remove(enemy)

    # Движение бонусов и проверка на сбор
    for bonus in bonus_list:
        if player_x < bonus[0] < player_x + player_size and player_y < bonus[1] < player_y + player_size:
            bonus_list.remove(bonus)
            bonus_active = bonus_duration  # Активируем бонус (замедляем врагов)

    # Проверка столкновения с врагами
    for enemy in enemy_list:
        if player_x < enemy[0] < player_x + player_size and player_y < enemy[1] < player_y + player_size:
            running = False  # Игра окончена

    # Отрисовка игрока
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))

    # Отрисовка врагов
    for enemy in enemy_list:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))

    # Отрисовка бонусов
    for bonus in bonus_list:
        pygame.draw.rect(screen, BLUE, (bonus[0], bonus[1], bonus_size, bonus_size))

    # Уменьшаем счетчик бонуса, если активен
    if bonus_active > 0:
        bonus_active -= 1

    # Увеличение счета за время выживания
    score += 1
    score_text = font.render(f"Очки: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()