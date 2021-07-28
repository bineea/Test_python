import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom

# Images
img = 'https://ultralytics.com/images/zidane.jpg'  # or PosixPath, PIL, OpenCV, numpy, list

# Inference
results = model(img)

# Results
results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
results.show()



# 配置环境变量“HOMEBREW_GITHUB_API_TOKEN”为github生成的token
# "D:\Program Files\Python\python.exe" D:/project/python/Test_python/Test_yolov5.py
# Downloading: "https://github.com/ultralytics/yolov5/archive/master.zip" to C:\Users\guowenbin9/.cache\torch\hub\master.zip
# YOLOv5  2021-7-28 torch 1.9.0+cu102 CUDA:0 (GeForce MX230, 2048.0MB)
#
# Downloading https://github.com/ultralytics/yolov5/releases/download/v5.0/yolov5s.pt to C:\Users\guowenbin9\.cache\torch\hub\ultralytics_yolov5_master\yolov5s.pt...
# 100%|██████████| 14.1M/14.1M [00:08<00:00, 1.76MB/s]
#
# Fusing layers...
# D:\Program Files\Python\lib\site-packages\torch\nn\functional.py:718: UserWarning: Named tensors and all their associated APIs are an experimental feature and subject to change. Please do not use them for anything important until they are released as stable. (Triggered internally at  ..\c10/core/TensorImpl.h:1156.)
#   return torch.max_pool2d(input, kernel_size, stride, padding, dilation, ceil_mode)
# Model Summary: 224 layers, 7266973 parameters, 0 gradients
# Adding AutoShape...
# image 1/1: 720x1280 2 persons, 2 ties
# Speed: 1209.4ms pre-process, 79.6ms inference, 295.5ms NMS per image at shape (1, 3, 384, 640)
#
# Process finished with exit code 0