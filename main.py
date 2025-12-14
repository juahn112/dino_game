import pygame

pygame.init()
# width, height = 1280, 720 
size = [1280,720]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running = True
FPS = 60
background_color = ["red", "yellow", "darkgray","white"]  
default_color = "black"
dt = 0
sound = pygame.mixer.music.load("bgm.ogg")

player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (75, 75))

enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

player_pos = pygame.Vector2(size[0] // 2, size[1] // 2)

while running:
    screen.fill(default_color)
    
    dt = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False     
    
    #pygame.draw.circle(screen, "blue", player_pos, 15)
    screen.blit(player_img, player_pos)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_DOWN]:
        player_pos.y += 300 * dt
    if keys[pygame.K_LEFT]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_RIGHT]:
        player_pos.x += 300 * dt
        
    pygame.display.flip()
pygame.quit()