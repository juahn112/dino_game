import pygame

pygame.init()
# width, height = 1280, 720 
size = [1280,720]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("신소명 피하기")
clock = pygame.time.Clock()
running = True
FPS = 60
dt = 0

background_img = pygame.image.load("img/upscaling_image.png")
background_img = pygame.transform.scale(background_img, size)

bgm = pygame.mixer.Sound("bgm/bgm.ogg")
bgm.set_volume(0.1)
bgm.play(-1)

player_img = pygame.image.load("img/player.png")
player_img = pygame.transform.scale(player_img, (75, 75))

enemy_img = pygame.image.load("img/enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

player_pos = pygame.Vector2(size[0] // 2, 550)
enemy_pos = pygame.Vector2(100, 100)

while running:
    screen.blit(background_img, (0, 0))
    dt = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False     
    
    #pygame.draw.circle(screen, "blue", player_pos, 15)
    screen.blit(player_img, player_pos)
    screen.blit(enemy_img, enemy_pos)
    
    keys = pygame.key.get_pressed()
    #if keys[pygame.K_UP]:
    #    player_pos.y -= 300 * dt
    #if keys[pygame.K_DOWN]:
    #    player_pos.y += 300 * dt
    if keys[pygame.K_LEFT]:
        player_pos.x -= 300 * dt
        if player_pos.x < 0:
            player_pos.x = 0
    if keys[pygame.K_RIGHT]:
        player_pos.x += 300 * dt
        if player_pos.x > size[0] - 75:
            player_pos.x = size[0] - 75
        
    pygame.display.flip()
pygame.quit()