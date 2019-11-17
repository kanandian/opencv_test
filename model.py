import constant
import random
import pygame
import mthread
import threading
from pygame.locals import * # 引入pygame中所有的常量
from pygame.sprite import Sprite
from pygame.sprite import Group
import math
import cv2


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

        self.init_camera()
        self.processing()

    def init_camera(self):
        self.vc = cv2.VideoCapture(0)  # 读入视频文件
        self.vc.set(3, constant.camera_width)  # 设置分辨率
        self.vc.set(4, constant.camera_height)

        rval, firstFrame = self.vc.read()
        # firstFrame = cv2.resize(firstFrame, (640, 360), interpolation=cv2.INTER_CUBIC)
        gray_firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)  # 灰度化
        firstFrame = cv2.GaussianBlur(gray_firstFrame, (21, 21), 0)  # 高斯模糊，用于去噪
        self.prveFrame = firstFrame.copy()
        print(firstFrame.shape)

    def capture_and_handle_frame(self):
        (ret, frame) = self.vc.read()

        # 如果没有获取到数据，则结束循环
        if not ret:
            return
        # 对获取到的数据进行预处理
        # frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_CUBIC)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (3, 3), 0)
        # cv2.imshow("current_frame", gray_frame)
        # cv2.imshow("prveFrame", prveFrame)
        # 计算当前帧与上一帧的差别
        frameDiff = cv2.absdiff(self.prveFrame, gray_frame)
        cv2.imshow("frameDiff", frameDiff)
        self.prveFrame = gray_frame.copy()
        # 忽略较小的差别
        retVal, thresh = cv2.threshold(frameDiff, 100, 255, cv2.THRESH_BINARY)
        # 对阈值图像进行填充补洞
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        text = "Unoccupied"
        # 遍历轮廓
        for contour in contours:
            # if contour is too small, just ignore it
            if cv2.contourArea(contour) < 50:  # 面积阈值
                continue
            # 计算最小外接矩形（非旋转）
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            centerx = x + w/2
            centery = y + h/2
            centerx *= constant.screen_width/constant.camera_width
            centery *= constant.screen_height/constant.camera_height
            self.sweep_at(centerx, centery)
            text = "Occupied!"
        # cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # cv2.putText(frame, "F{}".format(frameCount), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('frame_with_result', frame)
        # cv2.imshow('thresh', thresh)
        # cv2.imshow('frameDiff', frameDiff)

    def processing(self):
        # move_thread = mthread.MoveLeavesThread(self.leaf_list)
        # move_thread.start()
        # update_thread = mthread.UpdateUIThread(self)
        # update_thread.start()
        while self.running:
            self.handle_event()
            # self.add_leaf()
            self.capture_and_handle_frame()
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
                self.vc.release()
                cv2.destroyAllWindows()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.vc.release()
                    cv2.destroyAllWindows()
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



