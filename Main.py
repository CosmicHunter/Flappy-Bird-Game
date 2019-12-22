import pygame
import  random
import sys
from pygame.locals import *


fps = 30
screen_width = 289
screen_height = 511

game_window = pygame.display.set_mode((screen_width,screen_height))

land_y = screen_height *0.8
images_for_game = {}
sounds_for_game = {}

chidia_img = 'gallery/sprites/bird.png'
background_img = 'gallery/sprites/background.png'
pipe_img = 'gallery/sprites/pipe.png'

def init_screen():
      chidia_x = int(screen_width/5)
      chidia_y = int((screen_height-images_for_game['chidia'].get_height())/2)
      msg_x = int((screen_width - images_for_game['msg'].get_height())/2)
      msg_y = int(screen_height * 0.14)
      land_x = 0
      while True:
          for evt in pygame.event.get():
              if evt.type == QUIT or (evt.type==KEYDOWN and evt.key ==K_ESCAPE):
                  pygame.quit()
                  sys.exit()
              elif evt.type == KEYDOWN and (evt.key == K_SPACE or evt.key == K_UP):
                  return
              else:
                   game_window.blit(images_for_game['bckg'],(0,0))
                   game_window.blit(images_for_game['chidia'], (chidia_x,chidia_y))
                  # game_window.blit(images_for_game['msg'], (msg_x,msg_y))
                   game_window.blit(images_for_game['land'], (land_x,land_y))
                   pygame.display.update()
                   game_clock.tick(fps)


def mainGame():
    game_score = 0
    chidia_x = int(screen_width/5)
    chidia_y = int(screen_width/5)

    # random obstacle generation ## in this case pipes
    pipe_obstacle1 = generate_random_obstacle()
    pipe_obstacle2 = generate_random_obstacle()

    #collection of upper pipes
    upperpipes = [
        {'x':screen_width + 200 ,'y':pipe_obstacle1[0]['y']},
        {'x': screen_width + 200 + int(screen_width/2), 'y': pipe_obstacle2[0]['y']}
        ]
    # collection of lower pipes
    lowerpipes = [
        {'x':screen_width + 200 ,'y':pipe_obstacle1[1]['y']},
        {'x': screen_width + 200 + int(screen_width/2), 'y': pipe_obstacle2[1]['y']}
        ]

    speed_obstacle_x = -4
    chidia_vy = -9
    chidia_maxvy = 10
    chidia_minvy = -8
    chidia_ay = 1

    velocity_while_flapping= -8
    is_chidia_flaping = False

    while True:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN and (e.key == K_SPACE or e.key ==K_UP):
                if chidia_y > 0:
                    chidia_vy  = velocity_while_flapping
                    is_chidia_flaping = True
                    sounds_for_game['wing'].play()
        is_chidia_dead = chkCollision(chidia_x,chidia_y,lowerpipes,upperpipes)

        if is_chidia_dead :
            return

        # score
        chidia_mid_pos = chidia_x + images_for_game['chidia'].get_width()/2
        for pipe in upperpipes:
            pipe_mid_pos = pipe['x'] + images_for_game['pipe'][0].get_width()/2
            if pipe_mid_pos <= chidia_mid_pos < pipe_mid_pos+4:
                game_score+=1
                print(f'Score is {game_score}')
                sounds_for_game['point'].play()

        if chidia_vy < chidia_maxvy and  is_chidia_flaping == False:
             chidia_vy += chidia_ay

        if is_chidia_flaping:
            is_chidia_flaping = False

        chidia_height = images_for_game['chidia'].get_height()
        chidia_y = chidia_y + min(chidia_vy,land_y-chidia_y-chidia_height)

        # move pipe to left
        for up,lp in zip(upperpipes,lowerpipes):
            up['x'] += speed_obstacle_x
            lp['x'] += speed_obstacle_x

        # when pipe is about to leave the screen add a new pipe
        if 0<upperpipes[0]['x']<5:
            newpipe = generate_random_obstacle()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

        # remove the pipe that is out of the screen
        if upperpipes[0]['x'] + images_for_game['pipe'][0].get_width() < 0:
            upperpipes.pop(0)
            lowerpipes.pop(0)


        # Blitting the images
        game_window.blit(images_for_game['bckg'],(0,0))
        print("Hoel")
        for pipe1,pipe2 in zip(upperpipes,lowerpipes):
            print("asd")
            game_window.blit(images_for_game['pipe'][0], (pipe1['x'], pipe1['y']))
            game_window.blit(images_for_game['pipe'][1], (pipe2['x'], pipe2['y']))
        game_window.blit(images_for_game['land'],(0,land_y))
        game_window.blit(images_for_game['chidia'],(chidia_x,chidia_y))


        # Displaying Score
        string_of_score = str(game_score)
        list = [int(x) for x in string_of_score]
        totalwidth = 0

        for i in list:
            totalwidth += images_for_game['numbers'][i].get_width()

        xoffest = (screen_width-totalwidth)/2

        for i in list:
            game_window.blit(images_for_game['numbers'][i],(xoffest,screen_height*0.12))
            xoffest += images_for_game['numbers'][i].get_width()
        pygame.display.update()
        game_clock.tick(fps)




def  chkCollision(chidia_x,chidia_y,lowerpipes,upperpipes):
    if chidia_y > land_y - images_for_game['chidia'].get_height()-1 or chidia_y < 0:
        sounds_for_game['hit'].play()
        return True
    for p in upperpipes:
        pipe_height = images_for_game['pipe'][0].get_height()
        effective_height_upper_pipe = pipe_height + p['y']
        if( chidia_y < effective_height_upper_pipe and abs(chidia_x - p['x'])<images_for_game['pipe'][0].get_width()):
            sounds_for_game['hit'].play()
            return True

    for p in lowerpipes:
        pipe_height = images_for_game['pipe'][0].get_height()
        if(chidia_y>p['y'] -images_for_game['chidia'].get_height( ) and abs(chidia_x - p['x'])<images_for_game['pipe'][1].get_width()):
            sounds_for_game['hit'].play()
            return True

    return False



def generate_random_obstacle():
    pipe_height = images_for_game['pipe'][0].get_height()
    offset = screen_height/3
    y2 = offset + random.randrange(0,int(screen_height - images_for_game['land'].get_height() -1.2 * offset))

    pipeX = screen_width + 10
    y1 = pipe_height - y2 + 0.9 * offset
    pipe = [
        {'x':pipeX , 'y': -y1}, # for upper pipe obstacle
        {'x': pipeX, 'y': y2}  # for lower pipe obstacle
      ]
    return pipe

x = pygame.init()
print(x)
game_clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird Game")  # convert_alpha optimises images for faster loading
images_for_game['numbers'] = (
     pygame.image.load('gallery/sprites/0.png').convert_alpha(),
     pygame.image.load('gallery/sprites/1.png').convert_alpha(),
     pygame.image.load('gallery/sprites/2.png').convert_alpha(),
     pygame.image.load('gallery/sprites/3.png').convert_alpha(),
     pygame.image.load('gallery/sprites/4.png').convert_alpha(),
     pygame.image.load('gallery/sprites/5.png').convert_alpha(),
     pygame.image.load('gallery/sprites/6.png').convert_alpha(),
     pygame.image.load('gallery/sprites/7.png').convert_alpha(),
     pygame.image.load('gallery/sprites/8.png').convert_alpha(),
     pygame.image.load('gallery/sprites/9.png').convert_alpha(),
)
images_for_game['msg'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
images_for_game['land'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
images_for_game['pipe'] = (
    pygame.transform.rotate(pygame.image.load(pipe_img).convert_alpha(),180),
    pygame.image.load(pipe_img).convert_alpha()
)

#Sounds
sounds_for_game['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
sounds_for_game['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
sounds_for_game['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
sounds_for_game['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
sounds_for_game['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

images_for_game['bckg'] = pygame.image.load(background_img).convert_alpha()
images_for_game['chidia'] = pygame.image.load(chidia_img).convert_alpha()

while True:
    init_screen()
    mainGame()




