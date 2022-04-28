# labelme_to_yolo
Convert object detect  json file that labeled by labelme  to yolo format
;
Labelme format: ((x1, y1), (x2, y2))     # 注：矩形框两种情况：1）起始点左上角，终点是右下角； 2）起始点左下角，终点右上角； 计算w,h时，需要使用np.abs();
yolo format: (x_center, y_center, w, h)

# 1.数据准备：使用Labelme标注的目标检测数据集
  JPEGImages:存放原始标注图片
  Annotations:存放labelme生成的json文件，一张图片对应一个json文件  
  
# 2.运行代码：修改代码中的图片、json文件的目录地址、类名、训练集比例
  python labelme_to_yolo.py
  
# 3.转换成yolo格式标注文件
  1）复制图片到   images/train/demo1.jpg
                 images/val/demo2.jpg
  2) 生成txt格式  labels/train/demo1.txt
                 labels/val/demo2.txt
                 

