import os
import xml.etree.ElementTree as ET

# 类别映射表
CLASS_MAPPING = {
    "Repair": 0, #修复
    "D00": 1, #纵向裂纹
    "D10": 2, #横向裂纹
    "D20": 3, #网状裂纹
    "D40": 4 #坑洞
}

def convert_xml_to_yolo(xml_file, output_dir):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 获取图像尺寸
    size = root.find("size")
    img_width = int(size.find("width").text)
    img_height = int(size.find("height").text)

    # YOLO标注内容
    yolo_annotations = []

    # 遍历所有对象
    for obj in root.findall("object"):
        class_name = obj.find("name").text
        if class_name not in CLASS_MAPPING:
            continue  # 跳过未定义的类别

        class_id = CLASS_MAPPING[class_name]
        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        # 转换为YOLO格式
        x_center = (xmin + xmax) / 2 / img_width
        y_center = (ymin + ymax) / 2 / img_height
        width = (xmax - xmin) / img_width
        height = (ymax - ymin) / img_height

        yolo_annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    # 保存为.txt文件
    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(xml_file))[0] + ".txt")
    with open(output_file, "w") as f:
        f.write("\n".join(yolo_annotations))

def batch_convert_xml_to_yolo(xmls_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for xml_file in os.listdir(xmls_dir):
        if xml_file.endswith(".xml"):
            convert_xml_to_yolo(os.path.join(xmls_dir, xml_file), output_dir)

# 使用示例
xmls_dir = "RDD2022_China_MotorBike/China_MotorBike/train/annotations/xmls"
output_dir = "RDD2022_China_MotorBike/China_MotorBike/train/annotations/yolo"
batch_convert_xml_to_yolo(xmls_dir, output_dir)