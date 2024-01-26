import pygame
import time,random,sys
import os
import constants as C
import tools as T
from tools import IMAGES
from pygame.locals import *
pygame.init()
icon = pygame.image.load('assets/sprites/yellow-mid1.png')
pygame.display.set_icon(icon)
SCREEN = pygame.display.set_mode((C.W,C.H))
pygame.display.set_caption("flappy-bird By Wang")
CLOCK = pygame.time.Clock()

def main():
    while True:
        T.MUSIC['swooshing'].play()
        IMAGES['bgpic'] = IMAGES[random.choice(['day','night'])]
        color = random.choice(['red','yellow','blue'])
        IMAGES['birds'] = [IMAGES[color + '-up'],IMAGES[color + '-mid'],IMAGES[color + '-down']]
        pipe = IMAGES[random.choice(['red-pipe','green-pipe'])]
        IMAGES['pipes'] = [pipe,pygame.transform.flip(pipe,False,True)]
        menu_window()
        result = game_window()
        end_window(result)

def menu_window():
    idx = 0
    repeat = 6
    frames = [0]*repeat + [1]*repeat + [2]*repeat + [1]*repeat
    floor_x = 0
    bird_y_vel = 0.5
    bird_y_vel_range = [C.bird_y-8,C.bird_y+8]
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return
        floor_x -= 3
        if floor_x <= -C.floor_gap:
            floor_x = 0
        C.bird_y += bird_y_vel
        if C.bird_y < bird_y_vel_range[0] or C.bird_y > bird_y_vel_range[1]:
            bird_y_vel *= -1
        idx+=1
        idx%=len(frames)
        SCREEN.blit(IMAGES['bgpic'],(0,0))
        SCREEN.blit(IMAGES['floor'],(floor_x,C.floor_y))
        SCREEN.blit(IMAGES['guide'],(C.guide_x,C.guide_y))
        SCREEN.blit(IMAGES['guide1'],(C.guide1_x,C.guide1_y))
        SCREEN.blit(IMAGES['guide2'],(C.guide2_x,C.guide2_y))
        SCREEN.blit(IMAGES['birds'][frames[idx]],(C.bird_x,C.bird_y))
        pygame.display.update()
        CLOCK.tick(C.FPS)

def game_window():
    T.MUSIC['wing'].play()
    floor_x = 0
    bird = Bird(C.W*0.2,C.H*0.3)
    distance = 150
    n_paris = 4
    pipe_group = pygame.sprite.Group()
    pipe_gap = 100

    for i in range(n_paris):
        pipe_y = random.randint(int(C.H*0.4),int(C.H*0.7))
        pipe_up = Pipe(C.W + i*distance,pipe_y,True)
        pipe_down = Pipe(C.W + i*distance,pipe_y - pipe_gap,False)
        pipe_group.add(pipe_up)
        pipe_group.add(pipe_down)
    score = 0
    while True:
        flap = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    flap = True
                    T.MUSIC['wing'].play()
        pygame.display.update()
        floor_x -= 3
        if floor_x <= -C.floor_gap:
            floor_x = 0
        if bird.rect.y > C.floor_y or bird.rect.y < 0 or pygame.sprite.spritecollideany(bird,pipe_group):
            # print(bird.rect.x,bird.rect.y)
            # bird.rect.y = -15
            bird.diying = True
            T.MUSIC['hit'].play()
            T.MUSIC['die'].play()
            result ={'bird':bird,'pipe_group':pipe_group,'score':score}
            return result
        bird.update(flap)     
        first_pipe_up = pipe_group.sprites()[0]
        first_pipe_down = pipe_group.sprites()[1]
        if bird.rect.left+first_pipe_up.x_vel < first_pipe_down.rect.centerx <bird.rect.x:
            T.MUSIC['point'].play()
            score+=1
        if first_pipe_up.rect.right < 0:
            pipe_y = random.randint(int(C.H*0.3),int(C.H*0.7))
            new_pipe_up = Pipe(first_pipe_up.rect.x + n_paris * distance,pipe_y,True)
            new_pipe_down = Pipe(first_pipe_up.rect.x + n_paris * distance,pipe_y - pipe_gap,False)
            pipe_group.add(new_pipe_up)
            pipe_group.add(new_pipe_down)
            first_pipe_down.kill()
            first_pipe_up.kill()
        pipe_group.update()
        SCREEN.blit(IMAGES['bgpic'],(0,0))
        # SCREEN.blit(IMAGES['0'],(150,150))
        pipe_group.draw(SCREEN)
        SCREEN.blit(IMAGES['floor'],(floor_x,C.floor_y))
        show_score(score)
        SCREEN.blit(bird.image,bird.rect)
        CLOCK.tick(C.FPS)

def show_score(score):
    score_str = str(score)
    score_len = len(score_str)
    w = IMAGES['0'].get_width()*1.1
    x = (C.W - w * score_len)/2
    y = C.H * 0.1
    for number in score_str:
        SCREEN.blit(IMAGES[number],(x,y))
        x+=w
def show_score1(score,x,y,alpha):
    score_str = str(score)
    score_len = len(score_str)
    w = IMAGES['0'].get_width()
    h = IMAGES['0'].get_height()
    temp = pygame.transform.scale(IMAGES['0'],(int(w*0.6),int(h*0.6)))
    x -= (score_len-1)*temp.get_width()
    # print(temp.get_rect().x)
    but = 0
    for number in score_str:
        if number == '1':
            small = pygame.transform.scale(IMAGES[number],(int(w*0.5),int(h*0.57)))
            # print(1)
            but = w*0.6
        else:
            small = pygame.transform.scale(IMAGES[number],(int(w*0.6),int(h*0.6)))
            but = w*0.7
        # print(IMAGES[number].get_rect().x)
        small.set_alpha(alpha)
        SCREEN.blit(small,(x,y))
        
        # time.sleep(0.1)
        x+=but
def end_window(reslut):
    end = End(C.end_x,C.end_y)
    bird = reslut['bird']
    pipe_group = reslut['pipe_group']
    score = reslut['score']
    timing = time.time()
    b = False
    while True:
        if bird.diying:
            bird.go_die()
        else:
            for event in pygame.event.get():
                    # print(event.type)
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_SPACE:
                    return
        SCREEN.blit(IMAGES['bgpic'],(0,0))
        pipe_group.draw(SCREEN)
        SCREEN.blit(IMAGES['floor'],(0,C.floor_y))
        SCREEN.blit(IMAGES['gameover'],(C.gameover_x,C.gameover_y))
        end.update(score)
        
        SCREEN.blit(end.image,(end.rect.x,end.rect.y))
        SCREEN.blit(bird.image,(bird.rect.x,bird.rect.y))
        show_score1(score,C.W/1.3,C.H/2.18,end.alpha)
        # 显示最佳分数
        # 看看the best文档最佳分数大不大于
        # b = False
        with open("the best.txt",encoding='utf-8') as f:
            best = f.read()
            # print(best)
            if best == "":
                best = 0
            if int(best) > 10000:
                best = 0
            if int(best) < score:
                best = str(score)
                b = True
            # if int(best) == score:
                # best = str(score)
        with open("the best.txt",mode="w",encoding='utf-8') as f:
            f.write(str(best))
        show_score1(int(best),C.W/1.3,C.H/1.85,end.alpha)
        if b:
            # print(1)
            IMAGES['new'].set_alpha(end.alpha)
            SCREEN.blit(IMAGES['new'],(C.new_x,C.new_y))
        SCREEN.blit(IMAGES['start'],(C.start_x,C.start_y))
        IMAGES['birdcoin'].set_alpha(end.alpha)
        SCREEN.blit(IMAGES['birdcoin'],(C.W/5,C.H/2.07))
        pygame.display.update()
        CLOCK.tick(C.FPS)
# 大 -> 👈
class Bird:
    def __init__(self,x,y):
        self.frames = [0]* 6 + [1]*6 + [2]*6 + [1]*6
        self.idx = 0
        self.images = IMAGES['birds']
        self.image = self.images[self.frames[self.idx]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y_vel = -10
        self.max_y_vel = 10
        self.gravity = 1
        self.rotate = 45
        self.min_rotate = -20
        self.rotate_vel = -3
        self.y_vel_after_flap = -10
        self.rotate_after_flap = 45
        self.diying = False
    def update(self,flap=False):
        if flap:
            self.rotate = self.rotate_after_flap
            self.y_vel = self.y_vel_after_flap
        self.y_vel = min(self.y_vel + self.gravity,self.max_y_vel)
        # print(self.y_vel)
        self.rect.y += self.y_vel
        self.rotate = max(self.rotate + self.rotate_vel,self.min_rotate)
        # print(self.rotate)
        self.idx +=1
        self.idx %= len(self.frames)
        self.image = self.images[self.frames[self.idx]]
        self.image = pygame.transform.rotate(self.image,self.rotate)
    def go_die(self):
        if self.rect.y < C.floor_y:
            self.rect.y += self.max_y_vel
            self.rotate = -90
            self.image = self.images[self.frames[self.idx]]
            self.image = pygame.transform.rotate(self.image,self.rotate)
        else:
            self.diying = False

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,upwards=True):
        pygame.sprite.Sprite.__init__(self)
        if upwards:
            self.image = IMAGES['pipes'][0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.top = y
        else:
            self.image = IMAGES['pipes'][1]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = y
        self.x_vel=-4
    def update(self):
        self.rect.x += self.x_vel
class End(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES['end']
        self.alpha = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = C.H/2
    def update(self,score):
        self.image.set_alpha(self.alpha)
        if self.rect.y > C.H*0.4:
            self.rect.y -= 2
        if self.alpha +10 <=255:
            self.alpha += 10
main()
