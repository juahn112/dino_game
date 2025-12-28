import os
import sys
import pygame
import random

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#초기화
pygame.init()
size = [1280,720]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("신소명 피하기")
is_playing = False
seconds = 0
alpha = 255
alpha_direction = -5

clock = pygame.time.Clock()
running = True
FPS = 60
game_font = pygame.font.Font(resource_path('font/The Jamsil 4 Medium.ttf'), 36)
start_ticks = pygame.time.get_ticks()

#이미지 설정
background_img = pygame.image.load(resource_path("img/upscaling_image.png"))
background_img = pygame.transform.scale(background_img, size)
player_img = pygame.image.load(resource_path("img/player.png")).convert_alpha()
enemy_img = pygame.image.load(resource_path("img/enemy.png")).convert_alpha()

#SOUND 설정
base_bgm = pygame.mixer.Sound(resource_path("bgm/bgm.ogg"))
base_bgm.set_volume(0.5)

fail_sound = pygame.mixer.Sound(resource_path("bgm/fail_3.mp3"))
fail_sound.set_volume(0.7)

#플레이어 설정
class Player:
    def __init__(self):
        self.img = pygame.transform.scale(player_img, (70, 70))
        self.rect = self.img.get_rect()
        self.rect.center = (size[0] // 2, 591)
        self.player_mask = pygame.mask.from_surface(self.img)
        self.speed = 7
        self.alive = False

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < size[0]:
            self.rect.x += self.speed
    
    def draw(self, screen):
        screen.blit(self.img, self.rect)

#적 설정  
class Enemy:
    def __init__(self):
        self.img = pygame.transform.scale(enemy_img, (50, 50))
        self.rect = self.img.get_rect()
        self.rect.topleft = (random.randint(0, size[0] - 50), -50)
        self.enemy_mask = pygame.mask.from_surface(self.img)
        self.speed = 15

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.img, self.rect)


def start_game():
    global start_ticks, is_playing
    start_ticks = pygame.time.get_ticks()
    enemies.clear()
    player.rect.center = (size[0] // 2, 591)
    base_bgm.play(-1)
    is_playing = True
    player.alive = True


player = Player()
enemy = Enemy()
enemies = []
ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_EVENT, 100)

#게임 루프
while running:
    pygame.display.set_caption(f"신소명 피하기  FPS: {clock.get_fps():.2f}")
    dt = clock.tick(FPS) / 1000
    
    #이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and not is_playing:
                start_game()
        if event.type == ENEMY_EVENT and player.alive and is_playing:
            enemies.append(Enemy())  

    #화면 그리기
    screen.blit(background_img, (0, 0))
    player.draw(screen)
    if is_playing:
        player.handle_keys()
    elif seconds == 0:
        intro_text = game_font.render("스페이스바를 눌러 게임 시작", True, (255, 255, 255))
        intro_text.set_alpha(alpha)
        alpha += alpha_direction
        if alpha <= 0 or alpha >= 255:
            alpha_direction *= -1
        screen.blit(intro_text, (size[0] // 2 - intro_text.get_width() // 2, size[1] // 2 - intro_text.get_height() // 2))
    else:
        over_text = game_font.render(f"게임 오버! 당신은 {seconds}초 동안 버텼습니다.", True, (255, 0, 0))
        retry_text = game_font.render("스페이스바를 눌러 다시 시작", True, (255, 255, 255))
        over_text.set_alpha(alpha)
        retry_text.set_alpha(alpha)
        alpha += alpha_direction
        if alpha <= 0 or alpha >= 255:
            alpha_direction *= -1
        screen.blit(over_text, (size[0] // 2 - over_text.get_width() // 2, size[1] // 2 - over_text.get_height() // 2))
        screen.blit(retry_text, (size[0] // 2 - retry_text.get_width() // 2, size[1] // 2 + 50))

    #적 업데이트 및 충돌 검사
    if is_playing:
        for enm in enemies[:]:
            enm.update()
            enm.draw(screen)
            offset = (enm.rect.x - player.rect.x, enm.rect.y - player.rect.y)

            if player.player_mask.overlap(enm.enemy_mask, offset) and player.alive:
                print("충돌!")
                player.alive = False
                is_playing = False
                base_bgm.stop()
                fail_sound.play()
                pygame.display.set_caption("게임 오버!")
                enemies.clear()
            
            if enm.rect.top > size[1]:
                enemies.remove(enm)

    if player.alive and is_playing:
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000

    else:
        pass
    
    timer_text = game_font.render(f"{seconds}초", True, (255, 255, 255))
    screen.blit(timer_text, (1200, 10))

    pygame.display.update()
pygame.quit()