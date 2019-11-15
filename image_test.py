import cv2 #opencv读取的格式是BGR(使用其他包进行展示时注意转换)
import matplotlib.pyplot as plt
import numpy as np

def main():
    img = cv2.imread("images/me1.jpeg")

    print(img)
    print(img.size)
    print(img.dtype)
    cv_show("image", img)
    cv2.imwrite('images/me.jpg', img)

def cv_show(name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)  #表示按下任意按键
    #cv2.waitKey(1000) #显示1000毫秒
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()