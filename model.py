import constant
import random
import pygame
import _thread
import time
import mthread
import threading
import utils
from pygame.locals import * # 引入pygame中所有的常量
from pygame.sprite import Sprite
from pygame.sprite import Group


class Leaf(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('images/yezi.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, constant.screen_width)
        self.rect.y = random.randint(0, constant.screen_height)
        self.dirction_x = -1
        self.dirction_y = -1
        self.speed = 1

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right < screen_rect.left or self.rect.left > screen_rect.right or self.rect.bottom < screen_rect.top or self.rect.top < screen_rect.bottom:
            return True
        return False

    def update(self):
        if self.dirction_x == -1 and self.dirction_y == -1:
            self.rect.y += self.speed
        else:
            if self.dirction_x != -1:
                self.rect.x += self.dirction_x
            if self.dirction_y != -1:
                self.rect.y += self.dirction_y

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

        for i in range(0,50):
            self.add_leaf()

        self.processing()

    def processing(self):
        # move_thread = mthread.MoveLeavesThread(self.leaf_list)
        # move_thread.start()
        # update_thread = mthread.UpdateUIThread(self)
        # update_thread.start()
        while self.running:
            self.handle_event()
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
        time.sleep(0.001)

    def add_leaf(self):
        leaf = Leaf(self)
        self.leaves.add(leaf)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running == False

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



