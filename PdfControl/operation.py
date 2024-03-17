import fitz
import os
import comtypes.client

# 合并文件
def merge(pdf_paths, output_path):
    # 创建 PDF 写入对象
    pdf_writer = fitz.open()
    
    # 遍历 PDF 文件路径列表
    for pdf_path in pdf_paths:
        # 打开当前 PDF 文件
        pdf_reader = fitz.open(pdf_path)
        for page_num in range(pdf_reader.page_count):
            pdf_writer.insert_pdf(pdf_reader, from_page=page_num, to_page=page_num)
        pdf_reader.close()

    # 保存新的 PDF 文档
    pdf_writer.save(output_path)
    pdf_writer.close()

# 删除页面
def delete(pdf_path, output_path, pages):
    # 创建 PDF 写入对象
    pdf_writer = fitz.open()
    
    # 打开当前 PDF 文件
    pdf_reader = fitz.open(pdf_path)

    # 将当前 PDF 文件的页面逐页写入到输出 PDF
    for page_num in range(pdf_reader.page_count):
        if page_num + 1 not in pages[0]:
            pdf_writer.insert_pdf(pdf_reader, from_page=page_num, to_page=page_num)

    # 保存新的 PDF 文档
    pdf_writer.save(output_path + "/delete_" + os.path.basename(pdf_path))

    pdf_writer.close()

    pdf_reader.close()

# 拆分文件
def split(input, output, pages):
    # 打开当前 PDF 文件
    pdf_reader = fitz.open(input)
        
    for i in range(len(pages)):
        # 创建 PDF 写入对象
        pdf_writer = fitz.open()
    
        # 将当前 PDF 文件的页面逐页写入到输出 PDF
        for page_num in pages[i]:
            pdf_writer.insert_pdf(pdf_reader, from_page=page_num-1, to_page=page_num-1)
        # 将合并后的 PDF 写入到输出文件中
        pdf_writer.save(output+"/{}_".format(i)+os.path.basename(input))
        pdf_writer.close()
    
    pdf_reader.close()
            
# PDF转图片
def pdf2image(pdf_path, output_dir, pages):
    # 打开当前 PDF 文件
    pdf_reader = fitz.open(pdf_path)
        
    for page_num in pages[0]:
        page = pdf_reader.load_page(page_num - 1)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        image_path = os.path.join(output_dir, f"page_{page_num}.png")
        pix._writeIMG(image_path, format_='png', jpg_quality=100)
    
    pdf_reader.close()

# 图片转PDF
def image2pdf(image_paths, output_path):
   # 创建一个新的 PDF 文档
    pdf = fitz.open()

    # 遍历每个图片路径
    for image_path in image_paths:
        # 打开图片文件
        img = fitz.open(image_path)

        # 获取图片的尺寸
        width = img[0].mediabox[2]
        height = img[0].mediabox[3]
        rect = fitz.Rect(0, 0, width, height)

        # 创建一个新的 PDF 页面
        pdf_page = pdf.new_page(width=width, height=height)

        # 获取图片的 pixmap
        pixmap = img[0].get_pixmap()

        # 将 pixmap 数据插入到 PDF 页面
        pdf_page.insert_image(rect, pixmap=pixmap)

        # 关闭图片文件
        img.close()

    # 保存 PDF 文档
    pdf.save(output_path)
    pdf.close()

# WORD转PDF
def word2pdf(word_paths, output_path):
    word_app = comtypes.client.CreateObject("Word.Application")
    word_app.Visible = False

    for word_path in word_paths:
        # 打开 Word 文档
        print(word_path)
        doc = word_app.Documents.Open(os.path.normpath(word_path), ReadOnly=True)
        # 保存为 PDF 文件
        pdf_file = os.path.normpath(os.path.join(output_path, os.path.splitext(os.path.basename(word_path))[0] + '.pdf'))
        if os.path.exists(pdf_file):
            os.remove(pdf_file)
        doc.SaveAs(pdf_file, FileFormat = 17)  # 17 表示 PDF 格式  
        
        # 关闭 Word 文档
        doc.Close()

    word_app.Quit()

