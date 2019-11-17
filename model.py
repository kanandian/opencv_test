import constant
import random
import pygame
import mthread
import threading
from pygame.locals import * # 引入pygame中所有的常量
from pygame.sprite import Sprite
from pygame.sprite import Group
import math


class Leaf(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('images/yezi.png')
        self.rect = self.image.get_rect()
        self.position_x = random.randint(0, constant.screen_width)
        self.position_y = -200
        self.dirction_x = -1
        self.dirction_y = -1
        self.speed = constant.move_speed

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right < screen_rect.left or self.rect.left > screen_rect.right or self.rect.bottom < screen_rect.top or self.rect.top < screen_rect.bottom:
            return True
        return False

    def update(self):
        print(str(self.dirction_x)+'   '+str(self.dirction_y))
        if self.dirction_x == -1 and self.dirction_y == -1:
            self.position_y += self.speed
        else:
            if self.dirction_x != -1:
                self.position_x += self.dirction_x
            if self.dirction_y != -1:
                self.position_y += self.dirction_y
        self.rect.x = int(self.position_x)
        self.rect.y = int(self.position_y)

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Application:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('interation_projection')
        self.screen = pygame.display.set_mode((constant.screen_width, constant.screen_height))
        self.backgound_color = constant.background_color
        self.img_leaf = pygame.image.load('images/yezi.png')
        self.leaves = Group()
        self.lock = threading.Lock()
        self.running = True

        # line_width = 8
        # color = (255, 255, 0)
        # pygame.draw.line(self.screen, color, (100, 100), (500, 400), line_width)
        # pygame.display.update()

        for i in range(0,constant.initial_leaves_num):
            self.add_leaf()

        add_leaf_thread = mthread.AddLeafThread(self)
        add_leaf_thread.start()

        self.processing()

    def processing(self):
        # move_thread = mthread.MoveLeavesThread(self.leaf_list)
        # move_thread.start()
        # update_thread = mthread.UpdateUIThread(self)
        # update_thread.start()
        while self.running:
            self.handle_event()
            # self.add_leaf()
            self.update_leaves()
            self.update_screen()

    def update_leaves(self):
        # self.screen.fill(self.backgound_color)
        #
        # for leaf in self.leaf_list:
        #     leaf.show(self.screen, self.img_leaf)
        #
        # pygame.display.update()
        self.leaves.update()

    def update_screen(self):
        self.screen.fill(constant.background_color)
        self.leaves.draw(self.screen)
        pygame.display.flip()
        # time.sleep(0.001)

    def add_leaf(self):
        leaf = Leaf(self)
        self.leaves.add(leaf)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEMOTION:
                self.sweep_at(event.pos[0], event.pos[1])

    def sweep_at(self, x, y):
        fa = False
        fb = False
        for leaf in self.leaves.sprites():
            dist_x = leaf.rect.centerx-x
            dist_y = leaf.rect.centery-y
            distance = math.sqrt(math.pow(dist_x, 2) + math.pow(dist_y, 2))
            if distance < constant.max_distance:
                if dist_x < 0:
                    fa = True
                if dist_y < 0:
                    fb = True
                if dist_x == 0:
                    leaf.dirction_x = -1
                    leaf.dirction_y = constant.move_speed
                    if fb:
                        leaf.dirction_y *= -1
                else:
                    b = math.fabs(float(dist_y)/float(dist_x))
                    a = leaf.speed/math.sqrt(1+b*b)
                    b *= a
                    if fa:
                        a *= -1
                    if fb:
                        b *= -1
                    leaf.dirction_x = a
                    leaf.dirction_y = b





    # def move_leaves(self):
    #     remove_list = []
    #     self.lock.acquire()
    #     for leaf in self.leaf_list:
    #         if utils.is_out_of_range(leaf):
    #             remove_list.append(leaf)
    #         else:
    #             if leaf.direction_x == -1 and leaf.direction_y == -1:
    #                 leaf.position_y += leaf.speed
    #             else:
    #                 leaf.position_x += leaf.direction_x
    #                 leaf.position_y += leaf.direction_y
    #     for leaf in remove_list:
    #         self.leaf_list.remove(leaf)
    #     self.lock.release()



