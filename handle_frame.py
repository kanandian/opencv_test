import cv2
import matplotlib.pyplot as plt
import numpy as np
import utils


def clip_image():
    img = cv2.imread('images/me1.jpeg')
    img_clip = img[200:400, 200:400]    #截取部分图像
    utils.cv_show('cat', img_clip)


def channel_extraction():
    img = cv2.imread('images/me1.jpeg')
    b, g, r = cv2.split(img) #颜色通道提取, 或使用img[:,:,0], img[:,:,1],img[:,:,2]分别表示bgr
    print(b.shape) #二维
    img = cv2.merge((b, g, r))
    #只保留r通道：
    img[:,:,0] = 0    #第一个冒号表示显示前几行
    img[:,:,1] = 1
    utils.cv_show("R通道", img)


#边界填充
def fill_boundary():
    img = cv2.imread('images/me1.jpeg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    top_size, bottom_size, left_size, right_size = (100, 100, 100, 100)
    replicate = cv2.copyMakeBorder(img, top_size, bottom_size, left_size, right_size, borderType=cv2.BORDER_REPLICATE)
    reflect = cv2.copyMakeBorder(img, top_size, bottom_size, left_size, right_size, cv2.BORDER_REFLECT)
    reflect101 = cv2.copyMakeBorder(img, top_size, bottom_size, left_size, right_size, cv2.BORDER_REFLECT_101)
    wrap = cv2.copyMakeBorder(img, top_size, bottom_size, left_size, right_size, cv2.BORDER_WRAP)
    constant = cv2.copyMakeBorder(img, top_size, bottom_size, left_size, right_size, cv2.BORDER_CONSTANT, value=0)

    plt.subplot(231), plt.imshow(img, "gray"), plt.title('ORIGINAL')
    plt.subplot(232), plt.imshow(replicate, "gray"), plt.title('REPLICATE')
    plt.subplot(233), plt.imshow(reflect, "gray"), plt.title('REFLECT')
    plt.subplot(234), plt.imshow(reflect101, "gray"), plt.title('REFLECT_101')
    plt.subplot(235), plt.imshow(wrap, "gray"), plt.title('WRAP')
    plt.subplot(236), plt.imshow(constant, "gray"), plt.title('CONSTANT')
    plt.show()


#数值计算(只有(h,w,c)全部相同才能进行计算, 不相同则使用cv2.resize(img, (width, height))或cv2.resize(img, (0,0), fx={倍数}, fy={倍数})重新定义其中一张图的大小)
#numpy的加法(img1+img2)[:,5:,0]超出255则%256
#cv2.add(img1, img2)若大于255 则取255



#图像融合
def image_merge():
    img = cv2.imread('images/me1.jpeg')
    img1 = cv2.imread('images/me2.jpeg')
    res = cv2.addWeighted(img, 0.4, img1, 0.6, 0) #最后的0表示提升的亮度值
    # plt.imshow(res)
    utils.cv_show('res', res)


#图像阈值
def image_threshold():
    # ret, dst = cv2.threshold(src,  thresh, maxval, type)
    #       输出图             输入图    阈值   最大值   二值化操作的类型有以下5种
    # cv2.THRESH_BINARY 超过阈值部分去maxval，否则取0
    # cv2.THRESH_BINARY_INV 上面那个反过来
    # cv2.THRESH_TRUNC  大于阈值的部分设为阈值，否则不变（截断值）
    # cv2.THRESH_TOZERO 大于阈值部分保持不变，否则为0
    # cv2.THRESH_TOZERO_INV 上面那个反转
    pass

#平滑处理
def smoothing_processing():
    # 均值滤波
    img = cv2.imread('images/me1.jpeg')
    blur = cv2.blur(img, (3, 3))    #(3,3)表示核的大小
    # 方框滤波
    box = cv2.boxFilter(img, -1, (3,3), normalize=True)
    # 高斯滤波
    gaussian = cv2.GaussianBlur(img, (5,5), 1)  #越近的像素点比重更大
    #中值滤波(取几个值的中值)(有噪点时最有效)
    median = cv2.medianBlur(img, 5)

    res = np.hstack((blur, gaussian, median))   #横着拼接
    # res = np.vstack((blur, gaussian, median)) #竖着拼接
    print(res.shape)
    utils.cv_show(res)


#形态学 腐蚀操作（适用于二值数据）
def corrosion_operation():
    img = cv2.imread('images/circle.jpeg')
    kernel = np.ones((30,30), np.uint8)
    erode1 = cv2.erode(img, kernel, iterations=1)
    erode2 = cv2.erode(img, kernel, iterations=2)
    res = np.hstack((img, erode1, erode2))
    utils.cv_show(res)
    pass


#形态学 膨胀操作
def expansion_operation():
    img = cv2.imread('images/circle.jpeg')
    kernel = np.ones((30,30), np.uint8)

    erode = cv2.erode(img, kernel, iterations=1)
    dilate = cv2.dilate(erode, kernel, iterations=1)

    res = np.hstack((img, erode, dilate))

    utils.cv_show(res)


#开运算和闭运算
def open_and_close():
    img = cv2.imread('images/circle.jpeg')
    kernel = np.ones((30, 30), np.uint8)
    # 开运算：先腐蚀，在膨胀
    open = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    utils.cv_show(open)
    # 闭运算：先膨胀，在腐蚀
    close = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    utils.cv_show(close)


#梯度运算(梯度=膨胀-腐蚀)
def gradient_operation():
    img = cv2.imread('images/circle.jpeg')
    kernel = np.ones((30, 30), np.uint8)
    grandient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
    utils.cv_show(grandient)

# 礼帽与黑帽
# 礼帽=原始输入-开运算结果
# 黑帽=闭运算-原始输入
def hothat_and_blackhat():
    img = cv2.imread('images/circle.jpeg')
    kernel = np.ones((10, 10), np.uint8)
    #礼帽
    tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)

    res = np.hstack((tophat, blackhat))

    utils.cv_show(res)

def main():
    hothat_and_blackhat()


if __name__ == '__main__':
    main()



