# coding: utf-8
import numpy
import os
import Image
from svmutil import *


class Knn:
    def __init__(self, nameOfImage, objCoor, bgCoor,
                 nameOfTrainData='train.txt', nameOfTestData="test.txt"):
        self.nameOfImage = nameOfImage
        self.nameOfTrainData = nameOfTrainData
        self.nameOfTestData = nameOfTestData
        self.img = Image.open(nameOfImage)
        self.imgArr = numpy.array(self.img)
        self.imgShape = self.imgArr.shape
        # -1 stand for object's coordinate
        self.objCoor = objCoor
        # -1 stand for background's coordinate
        self.bgCoor = bgCoor

    def getDataset(self):
        # generate training data
        crop1 = self.img.crop(knn.bgCoor)
        crop2 = self.img.crop(knn.objCoor)
        self.image2Txt(crop1, 't1.txt', '1')
        self.image2Txt(crop2, 't2.txt', '-1')
        self.mergeFiles('t1.txt', 't2.txt')
        # delete temporary files t1.txt and t2.txt
        os.remove('t1.txt')
        os.remove('t2.txt')
        # generate testing data
        self.image2Txt(self.img, self.nameOfTestData, '1')

    def getDistance(self, pixel, group):
        # for each pixel in image, save the distance from this pixel's (R, G, B)
        # to training pixel's (R, G, B) in dist
        dist = numpy.zeros(len(group))
        for i in range(len(group)):
            dist[i] = (group[i][1] - pixel[0]) ** 2 + (group[i][2] - pixel[1]) ** 2 + (group[i][3] - pixel[2]) ** 2
        return dist

    def getKnnLabel(self, dist, k):
        # get the labels of minimum k distance's
        return self.label[dist.argsort()][:k]

    def belongTo(self, list):
        count = [0, 0]
        for i in list:
            if i < 0:
                count[0] += 1
            else:
                count[1] += 1
        if count[0] > count[1]:
            return -1
        else:
            return 1

    def getDist(self, pixel, group):
        dist = numpy.zeros(len(group))
        for i in range(len(group)):
            dist[i] = (group[i][1] - pixel[0]) ** 2 + (group[i][2] - pixel[1]) ** 2 + (group[i][3] - pixel[2]) ** 2
        return dist

    def getKnnLabel(self, dist, label, k):
        return label[dist.argsort()][:k]

    def startTraining(self, k):
        # generate train data and test data
        self.getDataset()
        label, group = svm_read_problem(self.nameOfTrainData)
        label = numpy.array(label)
        nothing, pixel = svm_read_problem(self.nameOfTestData)
        dist = numpy.zeros(len(group))

        file = open('predict_knn.txt', 'w')
        # calculate distance for each pixel

        count = 0
        for i in range(self.imgArr.shape[0]):
            for j in range(self.imgArr.shape[1]):
                print count
                count += 1
                dist = self.getDist(self.imgArr[i][j], group)
                # knn.getKnnDist(dist, 3)
                list = self.getKnnLabel(dist, label, 3)
                file.write("%d 1:%d 2:%d 3:%d\n" % (
                    int(self.belongTo(list)), int(self.imgArr[i][j][0]), int(self.imgArr[i][j][1]),
                    int(self.imgArr[i][j][2])))

    def belongTo(self, list):
        count = [0, 0]
        for i in list:
            if i < 0:
                count[0] += 1
            else:
                count[1] += 1
        if count[0] > count[1]:
            return -1
        else:
            return 1

    def txt2Image(self, filename_txt, shape):
        f = open(filename_txt)
        saved = numpy.zeros(shape, dtype=numpy.uint8)  # 對每一個pixel, 根據libsvm分類後的label,設置saved的響應RGB值
        for rows in range(shape[0]):
            for columns in range(shape[1]):
                # 讀取一行
                line = f.readline()
                # 獲取label
                if line.split()[0] == '-1':
                    saved[rows][columns] = [255, 255, 255]
                else:
                    saved[rows][columns] = [0, 0, 0]
        img = Image.fromarray(saved, 'RGB')
        return img

    def image2Txt(self, img, savedFileName, label):
        f = open(savedFileName, 'w')
        # 對所有的pixel,寫入文件
        imgArr = numpy.array(img)
        for i in range(imgArr.shape[0]):
            for j in range(imgArr.shape[1]):
                f.write("%s 1:%d 2:%d 3:%d\n" % (label, imgArr[i][j][0], imgArr[i][j][1], imgArr[i][j][2]))

    def mergeFiles(self, file1, file2):
        """
        merge two txt files to one txt file
        :param file1:
        :param file2:
        :return:
        """
        filenames = [file1, file2]
        with open(self.nameOfTrainData, 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    outfile.write(infile.read())


class Svm:
    def __init__(self, nameOfImage, objCoor, bgCoor,
                 nameOfTrainData='train.txt', nameOfTestData="test.txt"):
        self.nameOfImage = nameOfImage
        self.nameOfTrainData = nameOfTrainData
        self.nameOfTestData = nameOfTestData
        self.img = Image.open(nameOfImage)
        self.imgArr = numpy.array(self.img)
        self.imgShape = self.imgArr.shape
        # -1 stand for object's coordinate
        self.objCoor = objCoor
        # -1 stand for background's coordinate
        self.bgCoor = bgCoor

    def startTraining(self, arg):
        y, x = svm_read_problem(self.nameOfTrainData)  # 读入训练数据
        yt, xt = svm_read_problem('test.txt')  # 训练测试数据
        m = svm_train(y, x, arg)  # 训练
        p_label, p_acc, p_val = svm_predict(yt, xt, m)  # 测试
        file = open('predict_svm.txt', 'r+b')
        i = 0
        for item in p_label:
            file.write("%d 1:%d 2:%d 3:%d\n" % (int(item), int(xt[i][1]), int(xt[i][2]), int(xt[i][3])))
            i += 1

    def image2Txt(self, img, savedFileName, label):
        f = open(savedFileName, 'w')
        # 對所有的pixel,寫入文件
        imgArr = numpy.array(img)
        for i in range(imgArr.shape[0]):
            for j in range(imgArr.shape[1]):
                f.write("%s 1:%d 2:%d 3:%d\n" % (label, imgArr[i][j][0], imgArr[i][j][1], imgArr[i][j][2]))

    def txt2Image(self, filename_txt, shape):
        f = open(filename_txt)
        saved = numpy.zeros(shape, dtype=numpy.uint8)  # 對每一個pixel, 根據libsvm分類後的label,設置saved的響應RGB值
        for rows in range(shape[0]):
            for columns in range(shape[1]):
                # 讀取一行
                line = f.readline()
                # 獲取label
                if line.split()[0] == '-1':
                    saved[rows][columns] = [255, 255, 255]
                else:
                    saved[rows][columns] = [0, 0, 0]
        img = Image.fromarray(saved, 'RGB')
        return img


svm = Svm('1.jpg', (0, 0, 40, 40), (41, 38, 68, 42), 'train.txt')
svm.startTraining('-t 1')
img_svm = svm.txt2Image('predict_svm.txt', svm.imgArr.shape)
img_svm.show()

knn = Knn('1.jpg', (0, 0, 40, 40), (41, 38, 68, 42), 'train.txt')
knn.startTraining(3)
img_knn = knn.txt2Image('predict_knn.txt', knn.imgArr.shape)
img_knn.show()
