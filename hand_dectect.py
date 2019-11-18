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


import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        ret,img = cap.read()
        skinMask = HSVBin(img)
        contours = getContours(skinMask)
        cv2.drawContours(img,contours,-1,(0,255,0),2)
        cv2.imshow('capture',img)
        k = cv2.waitKey(10)
        if k == 27:
            break

def getContours(img):
    kernel = np.ones((5,5),np.uint8)
    closed = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)
    closed = cv2.morphologyEx(closed,cv2.MORPH_CLOSE,kernel)
    contours,h = cv2.findContours(closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    vaildContours = []
    for cont in contours:
        if cv2.contourArea(cont)>9000:
            #x,y,w,h = cv2.boundingRect(cont)
            #if h/w >0.75:
            #filter face failed
            vaildContours.append(cv2.convexHull(cont))
            #rect = cv2.minAreaRect(cont)
            #box = cv2.cv.BoxPoint(rect)
            #vaildContours.append(np.int0(box))
    return  vaildContours

def HSVBin(img):
    hsv = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)

    lower_skin = np.array([100,50,0])
    upper_skin = np.array([125,255,255])

    mask = cv2.inRange(hsv,lower_skin,upper_skin)
    #res = cv2.bitwise_and(img,img,mask=mask)
    return mask

if __name__ =='__main__':
    main()


# import sys
#
# import cv2
#
# hand_model = 'hand.xml'
# out_file = "output.avi"
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
#
#
# main()