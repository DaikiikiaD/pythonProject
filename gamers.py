import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panel = 150
screen_width = 900
screen_height = 600 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

#define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 20
clicked = False
game_over = 0

#define fonts
font = pygame.font.SysFont('Impact', 26)

#define colors
red = (230, 230, 250)
green = (0, 255, 0)

#load image
#background image
background_img = pygame.image.load('img/background/background.png').convert_alpha()
#panel image
panel_img = pygame.image.load('img/background/panel.png').convert_alpha()
#button image
potion_img = pygame.image.load('img/assets/potion.png').convert_alpha()
restart_img = pygame.image.load('img/assets/restart.png').convert_alpha()
#load victory and defeat images
victory_img = pygame.image.load('img/assets/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/assets/defeat.png').convert_alpha()
#sword image
sword_img = pygame.image.load('img/assets/fist.png').convert_alpha()
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
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 #0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        #load idle images
        temp_list = []
        for i in range(15):
            img = pygame.image.load(f'img/{self.name}/idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 6, img.get_height() * 6))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load attack images
        temp_list = []
        for i in range(15):
            img = pygame.image.load(f'img/{self.name}/attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 6, img.get_height() * 6))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load hurt images
        temp_list = []
        for i in range(2):
            img = pygame.image.load(f'img/{self.name}/hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 6, img.get_height() * 6))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load dead images
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'img/{self.name}/dead/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 6, img.get_height() * 6))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def idle(self):
        # set variable to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def update(self):
        animation_cooldown = 100
        #handle animation
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out reset back to start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def attack(self, target):
        #deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        #run enemy hurt animation
        target.hurt()
        #check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        #set variable to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        # set variable to hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        # set variable to death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0


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

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        #move damage text up
        self.rect.y -= 1
        #delete the text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


damage_text_group = pygame.sprite.Group()


dullahan = Fighter(150, 450, 'Dullahan', 60, 10, 3)
goons1 = Fighter(800, 420, 'Enemy', 30, 7, 2)
goons2 = Fighter(600, 420, 'Enemy', 30, 7, 2)

goons_list = []
goons_list.append(goons1)
goons_list.append(goons2)

dullahan_health_bar = Healthbar(100, screen_height - bottom_panel + 40, dullahan.hp, dullahan.max_hp)
goons_health_bar = Healthbar(550, screen_height - bottom_panel + 40, goons1.hp, goons1.max_hp)
goons2_health_bar = Healthbar(550, screen_height - bottom_panel + 100, goons2.hp, goons2.max_hp)

#create buttons
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 390, 170, restart_img, 120, 30)

run = True
while run:

    clock.tick(fps)

    #draw background
    draw_bg()

    #draw panel
    draw_panel()
    dullahan_health_bar.draw(dullahan.hp)
    goons_health_bar.draw(goons1.hp)
    goons2_health_bar.draw(goons2.hp)

    #draw fighters
    dullahan.update()
    dullahan.draw()
    for goons in goons_list:
        goons.update()
        goons.draw()

    #draw damage text
    damage_text_group.update()
    damage_text_group.draw(screen)

    #control player actions
    #reset action variables
    attack = False
    potion = False
    target = None
    #make sure mouse is visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, goons in enumerate(goons_list):
        if goons.rect.collidepoint(pos):
            #hide mouse
            pygame.mouse.set_visible(False)
            #show sword in place of mouse cursor
            screen.blit(sword_img, pos)
            if clicked == True and goons.alive == True:
                attack = True
                target = goons_list[count]
    if potion_button.draw():
        potion = True
    draw_text(str(dullahan.potions), font, red, 150, screen_height - bottom_panel + 70)

    if game_over == 0:
        #player action
        if dullahan.alive == True:
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #look for player action
                    #attack
                    if attack == True and target != None:
                        dullahan.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
                    #potion
                    if potion == True:
                        if dullahan.potions > 0:
                            #check if the potion would heal the player beyond max health
                            if dullahan.max_hp - dullahan.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = dullahan.max_hp - dullahan.hp
                            dullahan.hp += heal_amount
                            dullahan.potions -= 1
                            damage_text = DamageText(dullahan.rect.centerx, dullahan.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
        else:
            game_over = -1
        #enemy action
        for count, goons in enumerate(goons_list):
            if current_fighter == 2 + count:
                if goons.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        #check if the enemy needs to heal first
                        if (goons.hp / goons.max_hp) < 0.5 and goons.potions > 0:
                            # check if the potion would heal the enemy beyond max health
                            if goons.max_hp - goons.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = goons.max_hp - goons.hp
                            goons.hp += heal_amount
                            goons.potions -= 1
                            damage_text = DamageText(goons.rect.centerx, goons.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
                        #attack
                        else:
                            goons.attack(dullahan)
                            current_fighter += 1
                            action_cooldown = 0
                else:
                    current_fighter += 1

        #if all fighters have had a turn then reset
        if current_fighter > total_fighters:
            current_fighter = 1

    #check if all enemies are dead
    alive_goons = 0
    for goons in goons_list:
        if goons.alive == True:
            alive_goons += 1
    if alive_goons == 0:
        game_over = 1

    #check if game is over
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (310, 80))
        if game_over == -1:
            screen.blit(defeat_img, (310, 90))
        if restart_button.draw():
            dullahan.reset()
            for goons in goons_list:
                goons.reset()
            current_fighter = 1
            action_cooldown = 0
            game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()

