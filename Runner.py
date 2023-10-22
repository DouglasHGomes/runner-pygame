import pygame
from sys import exit

def display_title_screen():
    
    display_background()
    
    upper_title_surf = font.render("Runner", True, (64, 64, 64))
    upper_title_surf = pygame.transform.rotozoom(upper_title_surf, 0, 2)
    upper_title_rect = upper_title_surf.get_rect(center = (400, 75))
    
    lower_title_surf = font.render("Press Space to begin", False, (64, 64, 64))
    lower_title_rect = lower_title_surf.get_rect(center = (400, 350))
    
    screen.blit(upper_title_surf, upper_title_rect)
    screen.blit(lower_title_surf, lower_title_rect)
    
def display_game_over_screen(score):
    
    game_over_surf = font.render("Game Over", False, (64, 64, 64))
    game_over_rect = game_over_surf.get_rect(midbottom = (400, 50))
    
    game_over_score_surf = font.render("Score: " + str(score), False, (64, 64, 64))
    game_over_score_rect = game_over_score_surf.get_rect(midbottom = (400, 80))
    
    game_restart_surf = font.render("Press Space to restart", False, (64, 64, 64))
    game_restart_rect = game_restart_surf.get_rect(midbottom = (400, 350))
    
    screen.fill((94, 129, 162))

    screen.blit(game_over_surf, game_over_rect)
    screen.blit(game_over_score_surf, game_over_score_rect)
    screen.blit(player_stand_surf, player_stand_rect)
    screen.blit(game_restart_surf, game_restart_rect)    
    
def display_background():
    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0, 275))

def display_score(x, y):
    time_score = int((pygame.time.get_ticks() - start_time)/1000)
    
    score_surf = font.render("Score: " + str(time_score), False, (64, 64, 64))
    score_rect = score_surf.get_rect(midbottom = (x, y))
    
    screen.blit(score_surf, score_rect)
    
    return time_score

# Initial values
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()
font = pygame.font.Font('font\Pixeltype.ttf', 50)
game_state = 'start'
start_time = 0
player_gravity = 0
score = 0

sky_surface = pygame.image.load('graphics\Sky.png').convert()
ground_surface = pygame.image.load('graphics\ground.png').convert()
    
snail_surf = pygame.image.load('graphics\snail\snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (750, 275))
    
player_surf = pygame.image.load('graphics\Player\player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (150, 275))
    
player_stand_surf = pygame.image.load('graphics\Player\player_stand.png').convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)
player_stand_rect = player_stand_surf.get_rect(center = (400, 200))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        match(game_state):
            case 'start':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    snail_rect.right = 750
                    start_time = pygame.time.get_ticks()
                    game_state = 'active'
            case 'active':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player_rect.bottom == 275:
                    player_gravity = -7
            case 'end':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    snail_rect.right = 750
                    start_time = pygame.time.get_ticks()
                    game_state = 'active'

    match(game_state):
        case 'start':
            display_title_screen()
            
        case 'active':
            display_background()
            score = display_score(400, 55)

            screen.blit(snail_surf, snail_rect)
            screen.blit(player_surf, player_rect)

            snail_rect.right -= 4
            if snail_rect.right <= 0: 
                snail_rect.left = 800

            player_rect.bottom += player_gravity

            if player_rect.bottom >= 275:
                player_rect.bottom = 275
            else:
                player_gravity += 0.25
            
            if player_rect.colliderect(snail_rect):
                game_state = 'end'
            
        case 'end':
            display_game_over_screen(score)        

    pygame.display.update()
    clock.tick(60)