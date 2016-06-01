# coding:utf-8
import Image
import numpy
from svmutil import *


# 將圖片轉換成libsvm可處理的格式
def image2Standard(imgObject, savedFileName, label):
    """
    :param imgObject: Image.open返回的圖片對象
    :param savedFileName: 將imgObject處理成libsvm可處理的形式,保存到文件savedFileName中
    :param label: 對所有的pixel,加上label的標籤
    :return: None
    """
    # 讀取圖像文件,保存到數組中
    # im = numpy.array(Image.open(imageName))
    im = numpy.array(imgObject)
    # 打開文本文件,往該文件中寫
    f = open(savedFileName, 'w')
    # 對所有的pixel,寫入文件
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            # 處理成libsvm要求的格式
            f.write("%s 1:%d 2:%d 3:%d\n" % (label, im[i][j][0], im[i][j][1], im[i][j][2]))


def standard2Image(filename, shape):
    """
    將libsvm格式的文檔轉換成圖像,並返回
    :param filename: libsvm格式之文件名
    :param shape: 傳入圖像的shape
    :return: 返回圖像
    """
    # 打開txt文檔
    f = open(filename)
    # 用來保存將libsvm格式之文檔轉換成的array
    saved = numpy.zeros(shape, dtype=numpy.uint8)
    # 對每一個pixel, 根據libsvm分類後的label,設置saved的響應RGB值
    for rows in range(shape[0]):
        for columns in range(shape[1]):
            # 讀取一行
            line = f.readline()
            # 獲取label
            if line.split()[0] == '-1':
                saved[rows][columns] = [255, 255, 255]
            else:
                saved[rows][columns] = [0, 0, 0]
                # for i in range(3):
                # 從txt文件中獲得RGB值
                # [1 1:53 2:194 3:90]這樣子的
                # saved[rows][columns][i] = (line.split()[i + 1].split(':')[1])
    # 將saved數組轉化成image
    img = Image.fromarray(saved, 'RGB')
    # 返回圖像
    return img


# 对图片的某一部分截取, 将其转换成训练数据并保存
def getTrainData(imageName, coordinate, savedFileName, label):
    # 打开图片
    img = Image.open(imageName)
    # 获取截取的图片部分
    croped = img.crop(coordinate)
    # 将图片转化成数组
    arr = numpy.array(croped)
    # 将数组转化成libsvm可处理的格式,并保存,标签为label
    image2Standard(croped, savedFileName, label)


def getDetailedTrainData():
    # 小狗的位置在这里
    cropDog = (75, 75, 150, 200)
    # 獲得小狗的訓練數據
    getTrainData(nameOfImage, cropDog, fileNameOfTrainData_1, '-1')
    # 背景的位置在这里
    cropBackground = (0, 0, 75, 75)
    # 獲得背景的訓練數據
    getTrainData(nameOfImage, cropBackground, fileNameOfTrainData_2, '1')
    # 合併兩個訓練數據爲1個
    filenames = [fileNameOfTrainData_1, fileNameOfTrainData_2]
    with open(fileNameOfTrainData, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                outfile.write(infile.read())


# 打開一張圖片, 產生libsvm格式的txt文件,該文件爲測試文件
def getTestData(imageName, savedFileName, label):
    img = Image.open(imageName)
    image2Standard(img, savedFileName, '1')


nameOfImage = 'dog.jpg'
fileNameOfTrainData_1 = 'trainData1.txt'
fileNameOfTrainData_2 = 'trainData2.txt'
fileNameOfTrainData = 'trainData.txt'
fileNameOfTestData = "testData.txt"
fileNameOfResult = 'result.txt'
# 獲取測試數據
getTestData(nameOfImage, fileNameOfTestData, '1')
# 分別獲取訓練數據,得到trainData1.txt和trainData2.txt
getDetailedTrainData()

y, x = svm_read_problem(fileNameOfTrainData)  # 读入训练数据
yt, xt = svm_read_problem(fileNameOfTestData)  # 训练测试数据
m = svm_train(y, x)  # 训练
p_label, p_acc, p_val = svm_predict(yt, xt, m)  # 测试

# 構造libsvm分類後的libsvm格式文件
file = open(fileNameOfResult, 'r+b')
i = 0
for item in p_label:
    file.write("%d 1:%d 2:%d 3:%d\n" % (int(item), int(xt[i][1]), int(xt[i][2]), int(xt[i][3])))
    i += 1

arr = numpy.array(Image.open(nameOfImage, 'r'))
# 將分類後的文件轉換成圖像
im = standard2Image('result.txt', arr.shape)
im.show()

