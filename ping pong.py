import pygame, sys, random


def ball_animation():
	global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	if ball.top <= 0 or ball.bottom >= screen_height:
		pygame.mixer.Sound.play(pong_sound)
		ball_speed_y *= -1
		
	# Player Score
	if ball.left <= 0: 
		pygame.mixer.Sound.play(score_sound)
		score_time = pygame.time.get_ticks()
		player_score += 1
		
	# Opponent Score
	if ball.right >= screen_width:
		pygame.mixer.Sound.play(score_sound)
		score_time = pygame.time.get_ticks()
		opponent_score += 1
		
	if ball.colliderect(player) and ball_speed_x > 0:
		pygame.mixer.Sound.play(pong_sound)
		if abs(ball.right - player.left) < 10:
			ball_speed_x *= -1	
		elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1

	if ball.colliderect(opponent) and ball_speed_x < 0:
		pygame.mixer.Sound.play(pong_sound)
		if abs(ball.left - opponent.right) < 10:
			ball_speed_x *= -1	
		elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1
		

def player_animation():
    player.y += player_speed

    if player.top <= 0:
	    player.top = 0
    if player.bottom >= screen_height:
	    player.bottom = screen_height

def opponent_ai():
	if opponent.top < ball.y:
		opponent.y += opponent_speed
	if opponent.bottom > ball.y:
		opponent.y -= opponent_speed

	if opponent.top <= 0:
		opponent.top = 0
	if opponent.bottom >= screen_height:
		opponent.bottom = screen_height

def ball_start():
	global ball_speed_x, ball_speed_y, ball_moving, score_time

	ball.center = (screen_width/2, screen_height/2)
	current_time = pygame.time.get_ticks()
    
    # Timer
	if current_time - score_time < 700:
		number_three = basic_font.render("3",False,light_grey)
		screen.blit(number_three,(screen_width/2 - 10, screen_height/2 + 20))
	if 700 < current_time - score_time < 1400:
		number_two = basic_font.render("2",False,light_grey)
		screen.blit(number_two,(screen_width/2 - 10, screen_height/2 + 20))
	if 1400 < current_time - score_time < 2100:
		number_one = basic_font.render("1",False,light_grey)
		screen.blit(number_one,(screen_width/2 - 10, screen_height/2 + 20))

	if current_time - score_time < 2100:
		ball_speed_y, ball_speed_x = 0,0
	else:
		ball_speed_x = 7 * random.choice((1,-1))
		ball_speed_y = 7 * random.choice((1,-1))
		score_time = None

# Okay here I am going to add a simple button class that should give you a good idea of what to do if you want to make your own
class Button:
    def __init__(self, pos, text="", rect=(0, 0, 200, 60)):       
        #                 Normal           Hover
        self.colors = ((255,255,51), (255, 255, 255))
        self.hover = False
        self.clicked = False
        self.text = text
        self.center = True

        self.rect = pygame.Rect(rect)
        self.rect.x, self.rect.y = pos
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self.rendText = basic_font.render(self.text, True, (0, 0, 0))
        self.textRect = self.rendText.get_rect()
        if self.center:
            self.textRect.center = pygame.Rect(0, 0, self.rect.width, self.rect.height).center
        else:
            self.textRect.x += 2
            self.textRect.y += 2

    def update(self):
        self.image = pygame.Surface(self.rect.size)
        self.hover = False
        self.clicked = False
        mouseRect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
        if mouseRect.colliderect(self.rect):
            self.hover = True
        
        if self.hover:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
                    # You can add an audio line right here

            self.image.fill(self.colors[1])
        else:
            self.image.fill(self.colors[0])
        
        self.image.blit(self.rendText, self.textRect)
    
    def reset(self):
        self.clicked = False

# General setup
pygame.mixer.pre_init(44100,-16,1, 1024)
pygame.init()
clock = pygame.time.Clock() 



# Main Window
screen_width = 1299
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('MUSTEEYs Pong GAME')



# Colors
black = (0,0,0)
white = (255,255,255)
green = (0,128,0)
red = (255,0,0)
light_grey = (200,200,200)
teal = (0,128,128)
bg_color = pygame.Color('#008080')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 3 -10, screen_height / 2 - 70, 10 +100,140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10,140)

# Game Variables
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7
ball_moving = False
score_time = True

# Score Text
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)

# sound 
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

def render():
    screen.fill(bg_color)
    pygame.draw.rect(screen, black, player)
    pygame.draw.rect(screen, red, opponent)
    pygame.draw.ellipse(screen, white, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height))
    if score_time:
    	ball_start()
    
    player_text = basic_font.render(f'{player_score}',False,black)
    screen.blit(player_text,(660,470))

    opponent_text = basic_font.render(f'{opponent_score}',False,white)
    screen.blit(opponent_text,(600,470))

def refresh():
    pygame.display.flip()
    clock.tick(60)

def quit():
    pygame.quit()
    sys.exit()

def renderMenu():
    # This is how you would render objects
    for i in menuItems:
        screen.blit(i.image, i.rect)

b1 = Button((20, 20), "Start")
b2 = Button((20, 100), "Quit")
menuItems = [b1, b2]
while True:
    for i in menuItems:
        i.update()
    
    if b1.clicked:
        break
    if b2.clicked:
        quit()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    renderMenu()
    refresh()
    
while True:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit() 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed -= 8
            if event.key == pygame.K_DOWN:
                player_speed += 8
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed += 8
            if event.key == pygame.K_DOWN:
                player_speed -= 8
    #Game Logic
    ball_animation()
    player_animation()
    opponent_ai()

    # Visuals
    render()
    refresh()
