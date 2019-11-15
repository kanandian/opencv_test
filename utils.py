import cv2

def cv_show2(name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)  #表示按下任意按键
    #cv2.waitKey(1000) #显示1000毫秒
    cv2.destroyAllWindows()

def cv_show1(image):
    cv_show2("image", image)

def cv_show(*args):
    if len(args) == 1:
        cv_show1(args[0])
    elif len(args) == 2:
        cv_show2(args[0]. args[1])