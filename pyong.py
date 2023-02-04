import sys, pygame, random

COUNTDOWN_TIME = 1200

class ImageSprite(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
  
        # We could also create an image on the fly with the code below
        # self.image = pygame.Surface([width, height])
        # self.image.fill(color)
        self.image = pygame.image.load(path)
  
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
    
class Player(ImageSprite):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path,x_pos,y_pos)
        # how fast he moves in general
        self.speed = speed
        # current speed
        self.movement = 0

    def screen_constrain(self):
        """don't move outside of the screen"""
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    
    def update(self,ball_group):
        """moves player and applies the screen siez constaint"""
        self.rect.y += self.movement
        self.screen_constrain()

class Opponent(ImageSprite):
    def __init__(self,path,x_pos,y_pos,speed):
        super().__init__(path,x_pos,y_pos)
        self.speed = speed

    def update(self,ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.constrain()

    def constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height


class Ball(ImageSprite):
    def __init__(self,path,x_pos,y_pos,speed_x,speed_y,paddles):
        super().__init__(path,x_pos,y_pos)
        
        #initial random direction
        self.speed_x = speed_x * random.choice((-1,1))
        self.speed_y = speed_y * random.choice((-1,1))
        
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions() 
        else:
            self.restart_counter()
        
    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self,self.paddles,False):
            collision_paddle = pygame.sprite.spritecollide(self,self.paddles,False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1

    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice((-1,1))
        self.speed_y *= random.choice((-1,1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width/2,screen_height/2)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= COUNTDOWN_TIME*(1/3):
            countdown_number = 3
        if COUNTDOWN_TIME*(1/3) < current_time - self.score_time <= COUNTDOWN_TIME*(2/3):
            countdown_number = 2
        if COUNTDOWN_TIME*(2/3) < current_time - self.score_time <= COUNTDOWN_TIME:
            countdown_number = 1
        if current_time - self.score_time >= COUNTDOWN_TIME:
            self.active = True

        time_counter = game_font.render(str(countdown_number),True,accent_color)
        time_counter_rect = time_counter.get_rect(center = (screen_width/2,screen_height/2 + 50))
        pygame.draw.rect(screen, background_color,time_counter_rect)
        screen.blit(time_counter, time_counter_rect)


class GameManager:
    def __init__(self,ball_group,paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        # Drawing the game objects
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        # Updating the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = game_font.render(str(self.player_score),True,accent_color)
        opponent_score = game_font.render(str(self.opponent_score),True,accent_color)

        player_score_rect = player_score.get_rect(midleft = (screen_width / 2 + 40,screen_height/2))
        opponent_score_rect = opponent_score.get_rect(midright = (screen_width / 2 - 40,screen_height/2))

        screen.blit(player_score,player_score_rect)
        screen.blit(opponent_score,opponent_score_rect)

pygame.init()

size = screen_width, screen_height = 1280, 960
screen = pygame.display.set_mode(size)
pygame.display.set_caption('pyong')
clock = pygame.time.Clock()
game_font = pygame.font.Font("freesansbold.ttf", 30)

# ball = pygame.Rect(screen_width/2-15, screen_height/2-15, 30, 30)
# player = pygame.Rect(screen_width-20, screen_height/2-70, 10, 140)
# opponent = pygame.Rect(10,  screen_height/2-70, 10, 140)

# global variables
# background_color = pygame.Color('grey12')
background_color = pygame.Color('#2F373F')
accent_color = (27,35,43)
# light_grey = (200,200,200)
middle_strip = pygame.Rect(screen_width/2 - 2, 0, 4, screen_height)

# game objects

player = Player('paddle1.png', screen_width - 20, screen_height/2, 5)
opponent = Opponent('paddle1.png', 20, screen_width/2, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('ball1.png', screen_width/2, screen_height/2, 4, 4, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite,paddle_group)

# ball_speed_x = 7 * random.choice((1, -1))
# ball_speed_y = 7 * random.choice((1, -1))
# player_speed = 0
# opponent_speed = 7

# player_score = 0
# opponent_score = 0

# score_time = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # move during key is pressend down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.movement += player.speed
            if event.key == pygame.K_UP:
                player.movement -= player.speed

        # stop moving if key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    player.movement = 0


    screen.fill(background_color)
    pygame.draw.rect(screen, accent_color, middle_strip)

    game_manager.run_game()
    
    pygame.display.flip()
    clock.tick(60)

