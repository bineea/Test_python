import numpy as np
from PIL import Image
from os import path
import matplotlib.pyplot as plt
import os
import random

from wordcloud import WordCloud, STOPWORDS


def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)


# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# read the mask image taken from
# http://www.stencilry.org/stencils/movies/star%20wars/storm-trooper.gif
mask = np.array(Image.open(path.join(d, "D:\\Project\\Python\\Test_python\\resource\\1024.png")))

# movie script of "a new hope"
# http://www.imsdb.com/scripts/Star-Wars-A-New-Hope.html
# May the lawyers deem this fair use.
text = open(path.join(d, 'D:\\Project\\Python\\Test_python\\resource\\constitution.txt')).read()

# adding movie script specific stopwords
stopwords = set(STOPWORDS)
stopwords.add("int")
stopwords.add("ext")

wc = WordCloud(
    # 要显示的单词的最大个数
    max_words=10000,
    # 背景图片
    mask=mask,
    # 排除的单词集
    stopwords=stopwords,
    # 单词外边距
    margin=0,
    # 背景颜色
    background_color='white',
    # 配色方案数量
    random_state=50,
    # 最小的字体大小
    min_font_size=1
    # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
    # font_path='C:\Windows\Fonts\STZHONGS.TTF'
    ).generate(text)
# store default colored image
default_colors = wc.to_array()
plt.title("Custom colors")

plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
           interpolation="bilinear")
wc.to_file("1024.png")
plt.axis("off")
plt.figure()
plt.title("Default colors")
plt.imshow(default_colors, interpolation="bilinear")
plt.axis("off")
plt.show()
