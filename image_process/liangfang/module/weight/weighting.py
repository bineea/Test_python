import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def rChannelGray(image):
    height = image.shape[0]
    width = image.shape[1]
    gray = np.zeros((height, width, 1), np.uint8)
    for i in range(height):
        for j in range(width):
            pixel = 0.0 * image[i, j][0] + 0.0 * image[i, j][1] + 1 * image[i, j][2]
            gray[i, j] = pixel
    return gray

## 判断是否有小数点，有则返回True
### 入参：分割出的单一数字图像
def isDot(image):
    # print(image)
    flag = False

    height = image.shape[0]
    width = image.shape[1]
    ph = 0 # 示数最右侧边界到顶端的长度

    for i in range(width - 1, int(width / 2), -1): # 遍历列
        white_num = 0
        for j in range(height - 1): # 遍历行
            if image[j][i] == 255:
                white_num += 1
                if white_num >= 5:
                    # 找到了示数的最右侧边界
                    ph = j
                    break
        
        if white_num >= 5:
            break
        j = 0 # 重置起点
    
    if ph / height >= 0.75:
        flag = True

    return flag

## image相当于分割出的单个数字图像
def TubeIdentification(num, image):    
    tube = 0
    tubo_roi = [
        [image.shape[0] * 0/3, image.shape[0] * 1/3, image.shape[1] * 1/2, image.shape[1] * 1/2],
        [image.shape[0] * 1/3, image.shape[0] * 1/3, image.shape[1] * 2/3, image.shape[1] - 1],
        [image.shape[0] * 2/3, image.shape[0] * 2/3, image.shape[1] * 2/3, image.shape[1] - 1],
        [image.shape[0] * 2/3, image.shape[0] - 1, image.shape[1] * 1/2, image.shape[1] * 1/2],
        [image.shape[0] * 2/3, image.shape[0] * 2/3, image.shape[1] * 0/3, image.shape[1] * 1/3],
        [image.shape[0] * 1/3, image.shape[0] * 1/3, image.shape[1] * 0/3, image.shape[1] * 1/3],
        [image.shape[0] * 1/3, image.shape[0] * 2/3, image.shape[1] * 1/2, image.shape[1] * 1/2]
    ]

    i = 0
    while(i < 7):
        if(Iswhite(image, int(tubo_roi[i][0]), int(tubo_roi[i][1]), int(tubo_roi[i][2]), int(tubo_roi[i][3]))):
            tube = tube + pow(2,i)
            
        cv2.line(image, (int(tubo_roi[i][3]), int(tubo_roi[i][1])), (int(tubo_roi[i][2]), int(tubo_roi[i][0])), (255,0,0), 1)                   
        i += 1
    
    if(tube == 63):
        onenumber = 0
    elif(tube == 6):
        onenumber = 1
    elif(tube == 91):
        onenumber = 2
    elif(tube == 79):
        onenumber = 3
    elif(tube == 102):
        onenumber = 4
    elif(tube == 109):
        onenumber = 5
    elif(tube == 125):    
        onenumber = 6
    elif(tube == 7):
        onenumber = 7
    elif(tube == 127):
        onenumber = 8
    elif(tube == 103):
        onenumber = 9
    else:
        onenumber = -1 

    return onenumber, image      

## 判断是否与数码管    
def Iswhite(image, row_start, row_end, col_start, col_end):
    white_num = 0
    j = row_start
    i = col_start
 
    while(j <= row_end):
        while(i <= col_end):
            if(image[j][i] == 255):                
                white_num += 1
            i += 1
        j += 1
        i = col_start #重置回起点

    # 如果能检测到3个白像素点，则认为该七段线的检测线上有直线
    if(white_num >= 3):
        return True
    else:
        return False
 

### 数字识别
def digitalrec(image_org):

    cv2.resize(image_org, (201, 96))
    height = image_org.shape[0]
    width = image_org.shape[1]

    # 转灰度图
    # image_gray = cv2.cvtColor(image_org, cv2.COLOR_RGB2GRAY) # opencv自带灰度化会抹去示数   
    image_gray = rChannelGray(image_org)   
    
    # 二值化
    meanvalue = image_gray.mean()
    if meanvalue >= 200:                
        hist = cv2.calcHist([image_gray], [0], None, [256], [0,255])  
        min_val, max_val, min_index, max_index = cv2.minMaxLoc(hist)              
        ret, image_bin = cv2.threshold(image_gray, int(max_index[1])-7, 255, cv2.THRESH_BINARY)
    else:                                       
        mean, stddev = cv2.meanStdDev(image_gray)
        ret, image_bin = cv2.threshold(image_gray, meanvalue + 65, 255, cv2.THRESH_BINARY)
                                              
    # 分割数字并识别
    count = 0
    hasWhite = False
    cooList = []

    for i in range(0, width - 1, 3):
        flag = hasWhite
        y = 1
        for j in range(0, height - 1, 3):
            y += 3
            if image_bin[j][i] == 255:
                hasWhite = True
                break
        
        if y < height - 3 and (not flag):
            cooList.append(i) 

        if y < height - 3:
            # break出来
            continue
        elif y >= height - 3 and flag:
            # 遍历完一列
            hasWhite = False
            count += 1
            cooList.append(i)

    if len(cooList) % 2 != 0:
        cooList.append(width - 1)

    num = 0
    result = ''
    ims = []

    for i in range(0, len(cooList), 2):
        roi = image_bin[:, cooList[i] : cooList[i + 1]]

        onenumber, image = TubeIdentification(i, roi)
        ims.append(image)

        if(onenumber == -1):
            result += "0"
        else:
            result += str(onenumber)
            if isDot(roi):
                result += "."
        num += 1
    
    height, width= ims[0].shape
    
    # 创建空白长图
    longImage = Image.new("RGB", (width * len(ims), height))
  
    # 拼接图片
    for i, im in enumerate(ims):
        image = Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
        longImage.paste(image, box=(i * width, 0))

    longImage = np.array(longImage)

    return result, longImage  