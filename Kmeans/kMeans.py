# coding:utf-8
import numpy
import scipy.spatial
import math
from numpy import dot
from PIL import Image


def getImageInfo(filename):
    """
    獲取圖像的基本信息,包括图像数组，数组行数，数组列数
    :return: 圖像數組，行數，列數
    """
    im = numpy.array(Image.open(filename))
    rows = im.shape[0]
    columns = im.shape[1]
    return im, rows, columns


def getKClusters(n):
    """
    获得n个随机clusters，返回一个list
    e.g.
    n=2,k可能为：[[1,2],[2,66]]
    n=4，k可能为：[[177, 84, 27], [194, 173, 142], [155, 24, 157], [165, 183, 246]]
    :param n: clusters的个数
    :return: 随机的n个分群的列表
    """
    k = []
    for i in range(n):
        k.append([])
    for i in range(n):
        for j in range(3):
            k[i].append(numpy.random.randint(0, 256))
    return k


def updateK(k, now, im):
    """
    # 获得所有属于k1这个cluster的pixel，这些pixel的R，G，B平均更新为新的k1
    # k2，k3同理
    :param now:
    :param clusterImage:
    :return:
    """
    # 产生1×k的行向量
    # 例如如果有2个clusters
    # R = [[0,0]],G = [[0,0]], B=[[0,0]]
    R = numpy.zeros((1, len(k)))
    G = numpy.zeros((1, len(k)))
    B = numpy.zeros((1, len(k)))
    # counter也是1×k的行向量，用来存储属于ki这个cluster的pixel个数
    counter = numpy.zeros((1, len(k)))
    # 对每一个pixel，计算R，G，B的值总和，最后取平均
    for i in range(rows):
        for j in range(columns):
            # now[i][j]可能的值是0,1,2,3有几个clusters，now[i][j]最多就到多少
            # 0表示属于k1这个分群...
            R[0][int(now[i][j])] += im[i][j][0]
            G[0][int(now[i][j])] += im[i][j][1]
            B[0][int(now[i][j])] += im[i][j][2]
            # 计算
            counter[0][now[i][j]] += 1
    # 更新k0~kn
    for i in range(len(k)):
        # 更新Ki这个cluster的R
        if (counter[0][i] != 0):
            k[i][0] = R[0][i] / (counter[0][i])
            # 更新Ki这个cluster的G
            k[i][1] = G[0][i] / (counter[0][i])
            # 更新Ki这个cluster的B
            k[i][2] = B[0][i] / (counter[0][i])
    return k


def getDistance(a, b):
    """
    a和b都是有3个元素的list，3个元素分别是R，G，B值
    例如:[123, 255, 0]
    :param a: a是一个list
    :param b: b是一个list
    :return: 返回a和b的距离
    """
    return math.fabs(math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2))


def getMahalanobisDistance(a, b):
    c = numpy.array([a, b])
    # return scipy.spatial.distance.mahalanobis(c[0],c[1], numpy.linalg.inv(numpy.cov(c)))
    return math.fabs(math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2))


def shoulian(now, last):
    num = 0
    for i in range(rows):
        for j in range(columns):
            if now[i][j] != last[i][j]:
                num += 1
    # 如果不同的数量少于5个，那么认为已经收敛
    print "有%d个点的cluster发生变化" % num
    return num < 5


filename = raw_input("输入文件名：")
im, rows, columns = getImageInfo(filename)
# 复制一个原来图像之数组,用来存放聚类后的图像
a = Image.fromarray(im, 'RGB')
# a.show()
clusteredImage = numpy.copy(im)
# clusteredImage[]
# 存储每个pixel所属的cluster
now = numpy.zeros((rows, columns))
# 存储更新now之前每个pixel所属的cluster
# 用来判断是否收敛，+1是由于让now和last不同，否则一开始就收敛
last = now[:] + 1
# 获取随机cluster的个数
numberOfClusters = int(raw_input("输入Clusters个数:"))
k = getKClusters(numberOfClusters)
flag = raw_input("欧式(e),马氏(m)?:")

time = 1
while (not shoulian(last, now)):
    print ("第%d次") % time
    time += 1
    # 对每一个pixel，将其归为k1，k2，k3三个clusters中的一个,根据距离来归类
    distances = [0 for i in range(numberOfClusters)]
    for i in range(rows):
        for j in range(columns):
            last[i][j] = now[i][j]
    # last = now[:] #这样会让last和now实际上指向同一个地址,why????
    # last = list(now)
    for i in range(rows):
        for j in range(columns):
            # 分别获得clusterImage[i][j]这个pixel到所有clusters的距离
            for t in range(len(k)):
                # distances[t] = getDistance(k[t], im[i][j])
                if (flag == 'e'):
                    distances[t] = getDistance(k[t], im[i][j])
                else:
                    distances[t] = getMahalanobisDistance(k[t], im[i][j])
            # 将clusterImage[i][j]设置为distance中距离最小的
            # clusteredImage[i][j] = sorted(distances)[0]
            clusteredImage[i][j] = k[numpy.array(distances).argsort()[0]]
            # 将distance中距离最小的值的下标赋给now，0表示把这个pixel归为k0,1表示把pixel赋给k1
            now[i][j] = numpy.array(distances).argsort()[0]
    # 更新k个clusters的中心点
    k = updateK(k, now, im)
    img = Image.fromarray(clusteredImage, 'RGB')
    img.show()

img = Image.fromarray(clusteredImage, 'RGB')
img.show()
