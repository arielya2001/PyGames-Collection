import pygame, sys , random


def Open_my_screen(X):
    pygame.mixer.pre_init(frequency=44100, size= -16 , channels= 2 , buffer= 4020)
    pygame.init()
    Game_font = pygame.font.Font("AtariClassicChunky-PxXP.ttf",40)
    Opening_screen = pygame.display.set_mode((1440,675))
    background_image = pygame.image.load("assets/Background.png").convert()
    clock = pygame.time.Clock()

    def font_display():
        font_surface = Game_font.render("ENTER YOUR GAME NUMBER: ",True,(21,24,38))
        font_rec = font_surface.get_rect(center = (720,75))
        background_image.blit(font_surface,font_rec)

    actual_sound = pygame.mixer.Sound("sound/mixkit-european-spring-forest-ambience-1219.wav")

    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        Opening_screen.blit(background_image,(0,0))
        actual_sound.play()

        pygame.display.update()
        clock.tick(120)
        font_display()

def flappy_bird():
    def draw_floor():
        screen.blit(floor_surface, (floor_x_pos, 540))
        screen.blit(floor_surface, (floor_x_pos + 376, 540))

    def create_pipe():
        random_pipe_pos = random.choice(pipe_height)
        bottom_pipe = pipe_surface.get_rect(midtop = (400,random_pipe_pos))
        top_pipe = pipe_surface.get_rect(midbottom = (400,random_pipe_pos - 150))
        return bottom_pipe,top_pipe

    def move_pipes(pipes):
        for pipe in pipes:
            pipe.centerx -= 2.5
        return pipes

    def draw_pipes(pipes):
        for pipe in pipes:
            if pipe.bottom >= 624:
              screen.blit(pipe_surface,pipe)
            else:
              flip_pipe = pygame.transform.flip(pipe_surface,False,True)
              screen.blit(flip_pipe,pipe)

    def check_collision(pipes):
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                death_sound.play()
                return False
        if bird_rect.top<= -100 or bird_rect.bottom >= 540:
            return False

        return True

    def rotate_bird(bird):
        new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
        return new_bird

    def bird_animation():
        new_bird = bird_frames[bird_index]
        new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
        return new_bird,new_bird_rect

    def score_display(game_state):
        if game_state == "main_game":
          score_surface = game_font.render(str(int(score)),True,(255,255,255))
          score_rect = score_surface.get_rect(center = (188, 64))
          screen.blit(score_surface,score_rect)
        if game_state == "game_over":
           score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
           score_rect = score_surface.get_rect(center=(188, 85))
           screen.blit(score_surface, score_rect)

           high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
           high_score_rect = high_score_surface.get_rect(center=(188, 500))
           screen.blit(high_score_surface, high_score_rect)

    def update_score(score,high_score):
        if score > high_score:
            high_score = score
        return high_score


    pygame.init()
    screen = pygame.display.set_mode((376, 624))
    clock = pygame.time.Clock()
    game_font = pygame.font.Font("04B_19__.TTF",25)

    # Variables:
    Gravity = 0.15
    bird_movement = 0
    game_active = True
    score = 0
    high_score = 0


    bg_surface = pygame.image.load("assets/background-day.png").convert()
    bg_surface = pygame.transform.scale2x(bg_surface)

    floor_surface = pygame.image.load("assets/base.png").convert()
    floor_surface = pygame.transform.scale2x(floor_surface)
    floor_x_pos = 0

    bird_downflap = pygame.image.load("assets/bluebird-downflap.png").convert_alpha()
    bird_midflap = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
    bird_upflap = pygame.image.load("assets/bluebird-upflap.png").convert_alpha()
    bird_frames = [bird_downflap,bird_midflap,bird_upflap]
    bird_index = 0
    bird_surface = bird_frames[bird_index]
    bird_rect = bird_surface.get_rect(center = (100,318))

    BIRDFLAP = pygame.USEREVENT + 1
    pygame.time.set_timer(BIRDFLAP,200)

    #bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
    #bird_rect = bird_surface.get_rect(center = (100,318))

    pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
    pipe_list = []
    SPAWNPIPES = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPES,1500)
    pipe_height = [320,400,470]

    game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
    game_over_rect = game_over_surface.get_rect(center = (188,312))

    flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
    death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
    score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
    score_sound_countdown = 100

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and game_active:
                    bird_movement = 0
                    bird_movement-=5
                    flap_sound.play()
                if event.key == pygame.K_w and game_active == False:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100,318)
                    bird_movement = 0
                    score = 0

            if event.type == SPAWNPIPES:
                pipe_list.extend(create_pipe())

            if event.type == BIRDFLAP:
                if bird_index <2:
                  bird_index+=1
                else:
                  bird_index = 0
                bird_surface,bird_rect = bird_animation()

        screen.blit(bg_surface,(0,0))

        if game_active:
          # Bird Stuff:

          bird_movement+=Gravity
          rotated_bird = rotate_bird(bird_surface)
          bird_rect.centery+=bird_movement
          screen.blit(rotated_bird,bird_rect)
          game_active = check_collision(pipe_list)

          # pipes:
          pipe_list = move_pipes(pipe_list)
          draw_pipes(pipe_list)

          score+=0.01
          score_display("main_game")
          score_sound_countdown -= 1
          if score_sound_countdown <= 0:
              score_sound.play()
              score_sound_countdown = 100

        else:
            screen.blit(game_over_surface,game_over_rect)
            high_score = update_score(score,high_score)
            score_display("game_over")


        # floor:
        floor_x_pos-=0.75
        draw_floor()
        if floor_x_pos <= -376:
            floor_x_pos = 0


        pygame.display.update()
        clock.tick(120)

