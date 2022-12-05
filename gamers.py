import pygame

pygame.init()

#game window
bottom_panel = 150
screen_width = 900
screen_height = 600 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

#define fonts
font = pygame.font.SysFont('Times New Roman', 26)

#define colors
red = (255, 0, 0)
green = (0, 255, 0)

#load image
#background image
background_img = pygame.image.load('img/background/background.png').convert_alpha()
#panel image
panel_img = pygame.image.load('img/background/panel.png').convert_alpha()

#create function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#function for drawing background
def draw_bg():
    screen.blit(background_img, (0, 0))

#function for drawing panel
def draw_panel():
    #draw panel rectangle
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    #show dullahan stats
    draw_text(f'{dullahan.name} HP: {dullahan.hp}', font, red, 100, screen_height - bottom_panel + 10)
    for count, i in enumerate(goons_list):
        #show name and health
        draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 10) + count * 60)

#fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        img = pygame.image.load(f'img/{self.name}/0.png')
        self.image = pygame.transform.scale(img, (img.get_width() * 7, img.get_height() * 7))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)

class Healthbar():
    def __init__(self, x,  y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        #update with new health
        self.hp = hp
        #calculate health ration
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


dullahan = Fighter(150, 420, 'Dullahan', 30, 10, 3)
goons = Fighter(750, 370, 'Enemy', 30, 10, 1)
goons2 = Fighter(700, 470, 'Enemy', 30, 10, 1)

goons_list = []
goons_list.append(goons)
goons_list.append(goons2)

dullahan_health_bar = Healthbar(100, screen_height - bottom_panel + 40, dullahan.hp, dullahan.max_hp)
goons_health_bar = Healthbar(550, screen_height - bottom_panel + 40, goons.hp, goons.max_hp)
goons2_health_bar = Healthbar(550, screen_height - bottom_panel + 100, goons2.hp, goons2.max_hp)


#testing for HP loss 
#dullahan.hp = 20
#goons.hp = 10
#goons2.hp = 3

run = True
while run:

    #draw background
    draw_bg()

    #draw panel
    draw_panel()
    dullahan_health_bar.draw(dullahan.hp)
    goons_health_bar.draw(goons.hp)
    goons2_health_bar.draw(goons2.hp)

    #draw fighters
    dullahan.draw()
    for goons in goons_list:
        goons.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

