import fitz
import os
from datetime import datetime
from PIL import Image

# 获取PDF文件信息
def pdfinfo(path):
    if path:
        file = fitz.open(path)
        file_name = os.path.basename(file.name)
        last_modified_timestamp = os.path.getmtime(file.name)
        last_modified_time = datetime.fromtimestamp(last_modified_timestamp)
        num_pages = file.page_count
        file_position = path.replace(file_name, "")
        return(file_name, num_pages, file_position, last_modified_time.strftime("%Y-%m-%d %H:%M:%S"))
    
# 获取图片文件信息
def imageinfo(path):
    if path:
        file_name = os.path.basename(path)
        last_modified_timestamp = os.path.getmtime(path)
        last_modified_time = datetime.fromtimestamp(last_modified_timestamp)
        file_position = path.replace(file_name, "")
        # 获取图像的宽度和高度
        image_width, image_height = get_image_dimensions(path)
        return (file_name, image_width, image_height, file_position, last_modified_time.strftime("%Y-%m-%d %H:%M:%S"))

def get_image_dimensions(path):
    # 通过 PIL 库获取图像的宽度和高度
    with Image.open(path) as img:
        return img.size
    
def convert_bytes(size_bytes):
    # 1 KB = 1024 bytes
    KB = 1024.0
    MB = KB * KB
    GB = MB * KB
    TB = GB * KB

    if size_bytes >= TB:
        return "%.2f TB" % (size_bytes / TB)
    elif size_bytes >= GB:
        return "%.2f GB" % (size_bytes / GB)
    elif size_bytes >= MB:
        return "%.2f MB" % (size_bytes / MB)
    elif size_bytes >= KB:
        return "%.2f KB" % (size_bytes / KB)
    else:
        return "%d Bytes" % size_bytes

# 获取WORD文件信息
def wordinfo(path):
    if path:
        file_name = os.path.basename(path)
        last_modified_timestamp = os.path.getmtime(path)
        last_modified_time = datetime.fromtimestamp(last_modified_timestamp)
        file_position = path.replace(file_name, "")
        size = os.path.getsize(path)
        file_size = convert_bytes(size)  
        return (file_name, file_size, file_position, last_modified_time.strftime("%Y-%m-%d %H:%M:%S"))
    
def rule_check(rule):
    for char in rule:
        # 如果字符不是数字也不是逗号，则返回False
        if not (char.isdigit() or char == ',' or char == ';' or char == '-'):
            return False
    # 如果所有字符都是数字或逗号，则返回True
    return True

# 解析拆分、导出规则
def parse(rule):
    pages0 = rule.split(";")
    pages = []
    for i in range(len(pages0)):
        p_pages0 = pages0[i].split(",")
        p_pages = []
        for page in p_pages0:
            if "-" in page:
                start, end = page.split("-")
                for j in range(int(start), int(end)+1):
                    p_pages.append(j)
            else:
                p_pages.append(int(page))
        pages.append(sorted(p_pages))
    return(pages)