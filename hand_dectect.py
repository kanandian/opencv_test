# import cv2
# import numpy as np
#
# vc = cv2.VideoCapture(0)  # 读入视频文件
#
# ret, firstFrame = vc.read()
#
# lower_skin = np.array([100,50,0])
# upper_skin = np.array([125,255,255])
# kernel = np.ones((8, 8), np.uint8)
#
# while True:
#     ret, frame = vc.read()
#     k = cv2.waitKey(1)
#     if k == 27:
#         break
#     if not ret:
#         break
#
#     hsv_frame = cv2.cvtColor(frame,cv2.COLOR_RGB2HSV)
#     mask_frame = cv2.inRange(hsv_frame, lower_skin, upper_skin)
#     open_frame = cv2.morphologyEx(mask_frame, cv2.MORPH_OPEN, kernel)
#     close_frame = cv2.morphologyEx(open_frame, cv2.MORPH_CLOSE, kernel)
#     close_frame = cv2.GaussianBlur(close_frame, (5, 5), 0)
#
#     cv2.imshow('output', close_frame)
# vc.release()
# cv2.destroyAllWindows()


# import cv2
# import numpy as np
#
# def main():
#     cap = cv2.VideoCapture(0)
#     while(cap.isOpened()):
#         ret,img = cap.read()
#         skinMask = HSVBin(img)
#         contours = getContours(skinMask)
#         cv2.drawContours(img,contours,-1,(0,255,0),2)
#         cv2.imshow('capture',img)
#         k = cv2.waitKey(10)
#         if k == 27:
#             break
#
# def getContours(img):
#     kernel = np.ones((5,5),np.uint8)
#     closed = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)
#     closed = cv2.morphologyEx(closed,cv2.MORPH_CLOSE,kernel)
#     contours,h = cv2.findContours(closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#     vaildContours = []
#     for cont in contours:
#         if cv2.contourArea(cont)>9000:
#             #x,y,w,h = cv2.boundingRect(cont)
#             #if h/w >0.75:
#             #filter face failed
#             vaildContours.append(cv2.convexHull(cont))
#             #rect = cv2.minAreaRect(cont)
#             #box = cv2.cv.BoxPoint(rect)
#             #vaildContours.append(np.int0(box))
#     return  vaildContours
#
# def HSVBin(img):
#     hsv = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
#
#     lower_skin = np.array([100,50,0])
#     upper_skin = np.array([125,255,255])
#
#     mask = cv2.inRange(hsv,lower_skin,upper_skin)
#     #res = cv2.bitwise_and(img,img,mask=mask)
#     return mask
#
# if __name__ =='__main__':
#     main()



#使用hand.xml检测
# import cv2
# import time
#
# if __name__ == '__main__':
#
#     capture = cv2.VideoCapture(0)
#     hand_cascade = cv2.CascadeClassifier(r'./resources/hand.xml')
#
#     num = 0;
#     while True:
#         success, img = capture.read()
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         # 探测图片中的人脸
#         hands = hand_cascade.detectMultiScale(
#             gray,
#             scaleFactor=1.15,
#             minNeighbors=5,
#             minSize=(5, 5)
#         )
#         # print("发现{0}个人脸".format(len(faces)))
#         for (x, y, w, h) in hands:
#             # cv2.rectangle(img,(x,y),(x+w,y+w),(0,255,0),2)
#             cv2.circle(img, ((x + x + w) // 2, (y + y + h) // 2), w // 2, (0, 255, 0), 2)
#
#         cv2.imshow("camera", img)
#
#         # 按键处理，注意，焦点应当在摄像头窗口，不是在终端命令行窗口
#         key = cv2.waitKey(10)
#
#         if key == 27:
#             # esc键退出
#             print("esc break...")
#             break
#         if key == ord(' '):
#             # 保存一张图像
#             num = num + 1
#             filename = "frames_%s.jpg" % num
#             cv2.imwrite(filename, img)
#
#     capture.release()


# from imutils.object_detection import non_max_suppression


# import cv2
# import numpy as np
#
# hand_model = './resources/hand.xml'
#
#
# #  Felzenszwalb et al.
# def non_max_suppression_slow(boxes, overlapThresh):
#     # if there are no boxes, return an empty list
#     if len(boxes) == 0:
#         return []
#
#     # initialize the list of picked indexes
#     pick = []
#
#     # grab the coordinates of the bounding boxes
#     x1 = boxes[:, 0]
#     y1 = boxes[:, 1]
#     x2 = boxes[:, 2]
#     y2 = boxes[:, 3]
#
#     # compute the area of the bounding boxes and sort the bounding
#     # boxes by the bottom-right y-coordinate of the bounding box
#     area = (x2 - x1 + 1) * (y2 - y1 + 1)
#     idxs = np.argsort(y2)
#     # keep looping while some indexes still remain in the indexes
#     # list
#     while len(idxs) > 0:
#         # grab the last index in the indexes list, add the index
#         # value to the list of picked indexes, then initialize
#         # the suppression list (i.e. indexes that will be deleted)
#         # using the last index
#         last = len(idxs) - 1
#         i = idxs[last]
#         pick.append(i)
#         suppress = [last]
#         # loop over all indexes in the indexes list
#         for pos in range(0, last):
#             # grab the current index
#             j = idxs[pos]
#
#             # find the largest (x, y) coordinates for the start of
#             # the bounding box and the smallest (x, y) coordinates
#             # for the end of the bounding box
#             xx1 = max(x1[i], x1[j])
#             yy1 = max(y1[i], y1[j])
#             xx2 = min(x2[i], x2[j])
#             yy2 = min(y2[i], y2[j])
#
#             # compute the width and height of the bounding box
#             w = max(0, xx2 - xx1 + 1)
#             h = max(0, yy2 - yy1 + 1)
#
#             # compute the ratio of overlap between the computed
#             # bounding box and the bounding box in the area list
#             overlap = float(w * h) / area[j]
#
#             # if there is sufficient overlap, suppress the
#             # current bounding box
#             if overlap > overlapThresh:
#                 suppress.append(pos)
#
#         # delete all indexes from the index list that are in the
#         # suppression list
#         idxs = np.delete(idxs, suppress)
#
#     # return only the bounding boxes that were picked
#     return boxes[pick]
#
#
# def faceDetect(img, handCascade):
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#
#     # hand
#     hand = handCascade.detectMultiScale(
#         gray,
#         scaleFactor=1.1,
#         minNeighbors=2,
#         minSize=(40, 40)
#     )
#
#     print(hand)
#
#     pick = non_max_suppression_slow(hand, 0.3)
#
#     for (hx, hy, hw, hh) in pick:
#         cv2.rectangle(img, (hx, hy), (hx + hw, hy + hh), (230, 20, 232), 3)
#
#     return img
#
#
# def main():
#     cap = cv2.VideoCapture(0)
#     # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
#     # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
#     # face_cascade = cv2.CascadeClassifier(face_model)
#     # eyeCascade = cv2.CascadeClassifier(eyes_model)
#     # mouth_detector = cv2.CascadeClassifier(mouth_model)
#     handcascade = cv2.CascadeClassifier(hand_model)
#     # fourcc = cv2.VideoWriter_fourcc(*'flv1')  # 'F', 'L', 'V', '1'
#     # video = cv2.VideoWriter(out_file, fourcc, 20.0, (width, height))
#     while (True):
#         ret, frame = cap.read()
#         if ret == True:
#             # frame = faceDetect(frame, face_cascade,eyeCascade,mouth_detector,handcascade)
#             frame = faceDetect(frame, handcascade)
#         cv2.imshow("pose", frame)
#         # video.write(frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     # video.release()
#     cap.release()
#     cv2.destroyAllWindows()


# main()

import cv2
import constant


class HandDectectByHandXML:
    def __init__(self):
        self.hand_cascade = cv2.CascadeClassifier(r'./resources/hand.xml')
        self.init_camera()

    def init_camera(self):
        self.vc = cv2.VideoCapture(0)  # 读入视频文件
        self.vc.set(3, constant.camera_width)  # 设置分辨率
        self.vc.set(4, constant.camera_height)

        rval, firstFrame = self.vc.read()
        # firstFrame = cv2.resize(firstFrame, (640, 360), interpolation=cv2.INTER_CUBIC)
        gray_firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)  # 灰度化
        self.prveFrame = cv2.GaussianBlur(gray_firstFrame, (21, 21), 0)  # 高斯模糊，用于去噪
        self.prveFrame = self.prveFrame.copy()
        # print(firstFrame.shape)

    def get_hand_positions(self, mode):
        if mode == 1:
            return self.get_hand_positions_by_mode1()
        elif mode == 2:
            return self.get_hand_positions_by_mode2()

    def get_hand_positions_by_mode1(self):
        res = []
        # 探测图片中的人脸
        (ret, frame) = self.vc.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hands = self.hand_cascade.detectMultiScale(
            gray_frame,
            scaleFactor=1.15,
            minNeighbors=5,
            minSize=(5, 5)
        )
        for (x, y, w, h) in hands:
            res.append((x+w/2, y+w/2))
            cv2.circle(frame, ((x + x + w) // 2, (y + y + h) // 2), w // 2, (0, 255, 0), 2)

        if constant.show_camera:
            cv2.imshow('frame_with_result', cv2.flip(frame, 1, dst=None))
        return res

    def get_hand_positions_by_mode2(self):
        res = []
        (ret, frame) = self.vc.read()
        if not ret:
            return
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (3, 3), 0)
        # 计算当前帧与上一帧的差别
        frameDiff = cv2.absdiff(self.prveFrame, gray_frame)
        if constant.show_camera:
            cv2.imshow("frameDiff", cv2.flip(frameDiff, 1, dst=None))
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
            if cv2.contourArea(contour) < 1000:  # 面积阈值
                continue
            # 计算最小外接矩形（非旋转）
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            centerx = x + w / 2
            centery = y + h / 2
            centerx *= constant.screen_width / constant.camera_width
            centery *= constant.screen_height / constant.camera_height
            res.append((x, y))
            text = "Occupied!"

        if constant.show_camera:
            cv2.imshow('frame_with_result', cv2.flip(frame, 1, dst=None))

        return res