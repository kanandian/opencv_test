import cv2 #opencv读取的格式是BGR(使用其他包进行展示时注意转换)
import matplotlib.pyplot as plt
import numpy as np

def main():
    vc = cv2.VideoCapture("videos/test.mov")    #打开视频
    if vc.isOpened():   #判断视频是否打开
        ret, frame = vc.read()  #读取一帧
    else:
        ret = False

    while ret:
        ret, frame = vc.read()
        if frame is None:
            break
        if ret == True:
            #处理逻辑
            grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow("result", grayframe)
            if cv2.waitKey(10) & 0xFF == 27: #每一帧显示100毫秒，按27退出
                break
    vc.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()