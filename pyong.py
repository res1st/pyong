import sys, pygame, random

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if  ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y, score_time
    
    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)
    
    if current_time - score_time < 400:
        number = game_font.render('3', True, light_grey)
    elif current_time - score_time < 800:
        number = game_font.render('2', True, light_grey)
    elif current_time - score_time < 1200:
        number = game_font.render('1', True, light_grey)
    else:
        number = False

    if number:
        screen.blit(number, (screen_width/2 - 10, screen_height/2 + 20))
  
    if current_time-score_time < 1200:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_x = 7*random.choice((1, -1))
        ball_speed_y = 7*random.choice((1, -1))
        score_time = None

pygame.init()

size = screen_width, screen_height = 1280, 960
screen = pygame.display.set_mode(size)
pygame.display.set_caption('pyong')
clock = pygame.time.Clock()

ball = pygame.Rect(screen_width/2-15, screen_height/2-15, 30, 30)
player = pygame.Rect(screen_width-20, screen_height/2-70, 10, 140)
opponent = pygame.Rect(10,  screen_height/2-70, 10, 140)

backgroudn_color = pygame.Color('grey12')
light_grey = (200,200,200)

ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

score_time = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    player_speed = 0

    ball_animation()
    player_animation()
    opponent_animation()

    screen.fill((backgroudn_color))

    player_text = game_font.render(f"{player_score}", True, light_grey)
    screen.blit(player_text, (screen_width/2 + 20, screen_height/2))

    opponent_text = game_font.render(f"{opponent_score}", True, light_grey)
    screen.blit(opponent_text, (screen_width/2 - 20 - 19 , screen_height/2))

    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

    if score_time:
        ball_restart()

    pygame.display.flip()
    clock.tick(60)

