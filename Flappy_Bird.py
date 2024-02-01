import pygame
from sys import exit
import random
import bird_player
import comp
import configure
import pops

bp = bird_player.Bird_player()
g = comp.General()
pygame.init()
clock = pygame.time.Clock()
population = pops.Population(100)

# Window
win_height = configure.win_height
win_width = configure.win_width
window = configure.window

# Images
skyline_image = pygame.image.load("assets/background.png")
top_pipe_image = pygame.image.load("assets/pipe_top.png")
bottom_pipe_image = pygame.image.load("assets/pipe_bottom.png")
game_over_image = pygame.image.load("assets/game_over.png")
start_image = pygame.image.load("assets/start.png")

# Game
font = pygame.font.SysFont('Segoe', 26)
game_stopped = True
  
def quit_game():
    # Exit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

# Game Main Method
def manual_play():
    # Instantiate Bird
    bird = pygame.sprite.GroupSingle()
    bird.add(bird_player.Bird_player())
    high_score = 0

    # Setup Pipes
    pipe_timer = 0
    pipes = configure.pipes
    distance = 250
    opening = 90
    speed = 60

    # Instantiate Initial Ground
    x_pos_ground, y_pos_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(comp.Ground(x_pos_ground, y_pos_ground))

    run = True
    while run:
        # Quit
        quit_game()

        # Reset Frame
        window.fill((0, 0, 0))

        # User Input
        user_input = pygame.key.get_pressed()

        # Draw Background
        window.blit(skyline_image, (0, 0)) 

        # Spawn Ground
        if len(ground) <= 2:
            ground.add(comp.Ground(win_width, y_pos_ground))

        # Draw - Pipes, Ground and Bird
        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)

        score_text = font.render('Score: ' + str(comp.g.score), True, pygame.Color(255, 255, 255))
        window.blit(score_text, (20, 20)) 
        high_score_text = font.render('Highest score: ' + str(high_score), True, pygame.Color(255, 255, 255))
        window.blit(high_score_text, (20, 40)) 

        # Update - Pipes, Ground and Bird
        if bird.sprite.alive:
            pipes.update()
            ground.update()
        bird.update(False, user_input)

        # Collision Detection
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        if collision_pipes or collision_ground:
            bird.sprite.alive = False
            if collision_ground:
                window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2,
                                              win_height // 2 - game_over_image.get_height() // 2))
                if user_input[pygame.K_r]:
                    if comp.g.score > high_score:
                        high_score = comp.g.score
                    comp.g.score = 0
                    distance = 250
                    opening = 90
                    speed = 60
                    configure.pipes.empty()
                    break

        # Spawn Pipes
        if pipe_timer <= 0 and bird.sprite.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(opening, 130) + bottom_pipe_image.get_height()
            pipes.add(comp.Pipe(x_top, y_top, top_pipe_image, 'top'))
            pipes.add(comp.Pipe(x_bottom, y_bottom, bottom_pipe_image, 'bottom'))
            pipe_timer = random.randint(180, distance)
        pipe_timer -= 1
        if comp.g.score %5 == 0 and comp.g.score != 0:
            speed += 2
            if distance > 180:
                distance -= 2
            if opening >= 20:
                opening -= 2
            if comp.g.score %10 == 0:
                speed += 2
                if distance > 180:
                    distance -= 2
                if opening >= 20:
                    opening -= 2
            
        clock.tick(speed)
        pygame.display.update()
    
def ai_play():
    population = pops.Population(200)
    # Instantiate Birds using Group
    bird_group = population.generate_birds()
    high_score = 0
    
    # Setup Pipes
    pipe_timer = 0
    pipes = configure.pipes
    distance = 250
    opening = 90
    speed = 60

    # Instantiate Initial Ground
    x_pos_ground, y_pos_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(comp.Ground(x_pos_ground, y_pos_ground))

    while True:
        # Quit
        quit_game()

        generation = population.generation
        bird_group = population.players
        
        # Reset Frame
        window.fill((0, 0, 0))

        # Draw Background
        window.blit(skyline_image, (0, 0))

        # Spawn Ground
        if len(ground) <= 2:
            ground.add(comp.Ground(win_width, y_pos_ground))

        # Draw - Pipes, Ground, and Birds
        pipes.draw(window)
        ground.draw(window)
        bird_group.draw(window)

         # Spawn Pipes
        if pipe_timer <= 0:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(opening, 130) + bottom_pipe_image.get_height()
            pipes.add(comp.Pipe(x_top, y_top, top_pipe_image, 'top'))
            pipes.add(comp.Pipe(x_bottom, y_bottom, bottom_pipe_image, 'bottom'))
            pipe_timer = random.randint(180, distance)
        pipe_timer -= 1
        if comp.g.score %5 == 0 and comp.g.score != 0:
            speed += 2
            if distance > 180:
                distance -= 2
            if opening >= 20:
                opening -= 2
            if comp.g.score %10 == 0:
                speed += 2
                if distance > 180:
                    distance -= 2
                if opening >= 20:
                    opening -= 2

        # Update - Pipes, Ground, and Birds
        alive = sum(b.alive for b in bird_group.sprites())
        score_text = font.render('Score: ' + str(comp.g.score), True, pygame.Color(255, 255, 255))
        window.blit(score_text, (20, 20)) 
        generation_text = font.render('Generation: ' + str(generation), True, pygame.Color(255, 255, 255))
        window.blit(generation_text, (20, 40))
        alive_text = font.render('Alive: ' + str(alive), True, pygame.Color(255, 255, 255))
        window.blit(alive_text, (20, 60))
        high_score_text = font.render('Highest score: ' + str(high_score), True, pygame.Color(255, 255, 255))
        window.blit(high_score_text, (20, 80)) 
        
        if alive >= 1:    
            pipes.update()
            ground.update()
        elif alive == 0:
                configure.pipes.empty()
                ground.empty()
                population.natural_selection()
                if comp.g.score > high_score:
                    high_score = comp.g.score
                comp.g.score = 0
                distance = 250
                opening = 90
                speed = 60
                pipe_timer = 0
                pipes = configure.pipes
                x_pos_ground, y_pos_ground = 0, 520
                ground = pygame.sprite.Group()
                ground.add(comp.Ground(x_pos_ground, y_pos_ground))
        population.update()

        # Collision Detection
        for bird in bird_group:
            collision_pipes = pygame.sprite.spritecollide(bird, pipes, False)
            collision_ground = pygame.sprite.spritecollide(bird, ground, False)
            if collision_pipes or collision_ground or (bird.rect.center[1]<0):
                bird.alive = False
            if collision_ground:
                  bird.image.set_alpha(0 if not bird.alive else 255)

        clock.tick(speed)
        pygame.display.update()

# Menu
def main():
    global game_stopped

    while game_stopped:
        quit_game()

        # Draw Menu
        window.fill((0, 0, 0))
        window.blit(skyline_image, (0, 0))
        window.blit(g.ground_image, comp.Ground(0, 520))
        window.blit(bp.bird_images[0], (100, 250))
        window.blit(start_image, (win_width // 2 - start_image.get_width() // 2,
                                  win_height // 2 - start_image.get_height() // 2))

        # User Input
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            manual_play()
        elif user_input[pygame.K_a]:
            ai_play()
                
        pygame.display.update()

main()
