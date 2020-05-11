import pygame
import random
import math
import time
import sys

# view open
pygame.init()

view_width = 800
view_height = 600

view = pygame.display.set_mode((view_width, view_height))
pygame.display.set_caption("Egg War")

# utility functions
def distance(pos_1, pos_2):
   return math.sqrt( (pos_1[0] - pos_2[0]) ** 2 +  (pos_1[1] - pos_2[1]) ** 2 )

def middlePoint(pos_1, pos_2):
   return ( (pos_1[0] + pos_2[0]) / 2, (pos_1[1] + pos_2[1]) / 2 )

def text_obj(text, font, color):
   textSurface = font.render(text, True, color)
   return textSurface, textSurface.get_rect()

def showText(text, pos=(view_width / 2, view_height * 0.1), size=50, color=(0, 0, 0)):
   arial_font = pygame.font.Font("Arial.ttf", size)
   textSurf, textContainer = text_obj(text, arial_font, color)
   textContainer.center = pos
   view.blit(textSurf, textContainer)

# images
player = pygame.image.load("player.png")
egg = pygame.image.load("egg.png")
chicken = pygame.image.load("chicken.png")

# score
score = 0

# music
pygame.mixer.music.load("main-theme.mp3")
pygame.mixer.music.play(-1)

# sound effects
eat_sound = pygame.mixer.Sound("eat.wav")
chicken_sound = pygame.mixer.Sound("chicken.wav")

##### game #####
# player pos data
x_pos = view_width / 2
y_pos = view_height * 0.8

# chicken pos data
chicken_x_pos = view_width * 0.2
chicken_y_pos = view_height / 2

def game_loop():

   # player pos_mod/speed data
   x_mod = 0
   y_mod = 0

   speed = 0.9

   # egg pos data
   egg_x_pos = random.randint(view_width * 0.05, view_width * 0.95)
   egg_y_pos = random.randint(view_height * 0.1, view_height * 0.65)

   # chicken pos/speed data
   chicken_x_mod = 0
   chicken_y_mod = 0

   chicken_speed = 0.14

   # globalization
   global x_pos
   global y_pos
   global chicken_x_pos
   global chicken_y_pos
   global score

   running = True

   while True:

      for event in pygame.event.get():

         if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
               x_mod = -speed
            
            if event.key == pygame.K_RIGHT:
               x_mod = speed

            if event.key == pygame.K_UP:
               y_mod = -speed
            
            if event.key == pygame.K_DOWN:
               y_mod = speed

         if event.type == pygame.KEYUP:
            x_mod = 0
            y_mod = 0

         if distance(middlePoint((x_pos, y_pos), (x_pos + 64, y_pos - 64)), middlePoint((x_pos, y_pos), (egg_x_pos + 64, egg_y_pos - 64))) < 29.5:
            eat_sound.play()
            score += 1
            time.sleep(0.3)
            game_loop()

         if distance(middlePoint((x_pos, y_pos), (x_pos + 64, y_pos - 64)), middlePoint((x_pos, y_pos), (chicken_x_pos + 64, chicken_y_pos - 64))) < 29.5:
            chicken_sound.play()
            score -= 1
            time.sleep(0.01)
            
         # chicken movement algorithm
         if chicken_x_pos > x_pos and chicken_y_pos > y_pos:
            chicken_x_mod = -chicken_speed
            chicken_y_mod = -chicken_speed

         if chicken_x_pos > x_pos and chicken_y_pos < y_pos:
            chicken_x_mod = -chicken_speed
            chicken_y_mod = chicken_speed

         if chicken_x_pos < x_pos and chicken_y_pos > y_pos:
            chicken_x_mod = chicken_speed
            chicken_y_mod = -chicken_speed

         if chicken_x_pos < x_pos and chicken_y_pos < y_pos:
            chicken_x_mod = chicken_speed
            chicken_y_mod = chicken_speed

         # wall collision
         if x_pos >= view_width - 69:
            x_pos = random.randint(view_width * 0.05, view_width * 0.95)
            y_pos = random.randint(view_height * 0.1, view_height * 0.65)

         if x_pos <= -12:
            x_pos = random.randint(view_width * 0.05, view_width * 0.95)
            y_pos = random.randint(view_height * 0.1, view_height * 0.65)

      speed = 0.9

      x_pos += x_mod
      y_pos += y_mod

      chicken_x_pos += chicken_x_mod
      chicken_y_pos += chicken_y_mod

      view.fill((255, 255, 255))
      
      view.blit(egg, (egg_x_pos, egg_y_pos)) 
      view.blit(player, (x_pos, y_pos))
      view.blit(chicken, (chicken_x_pos, chicken_y_pos))

      showText("Score: " + str(score))
      pygame.display.update()

game_loop()
