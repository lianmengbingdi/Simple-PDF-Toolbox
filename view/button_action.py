from qfluentwidgets import qconfig

from common.config import cfg
from common.my_logger import my_logger as logger
from common.public import  show_dialog, show_loading

from PyQt5 import QtWidgets

from PdfControl import base
class buttonaction:

    #==========合并PDF页面按钮事件==========
    # 导入PDF文件
    def InputFile1(parent):
        file_dialog = QtWidgets.QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(parent, "选择PDF文件", "", "PDF Files (*.pdf)")
        if file_paths:
            for file_path in file_paths:
                row = parent.ui.TableWidget.rowCount()
                parent.ui.TableWidget.insertRow(row)
                file_name,num_pages,file_position,time = base.pdfinfo(file_path)
                parent.ui.TableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(file_name))
                parent.ui.TableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(num_pages)))
                parent.ui.TableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(file_position))
                parent.ui.TableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(time))

    # 删除导入的PDF文件
    def DeleteFile1(parent):
        current_row = parent.ui.TableWidget.currentRow()
        if current_row != -1:
            parent.ui.TableWidget.removeRow(current_row)
            parent.ui.TableWidget.setCurrentCell(-1, -1)
        else:
            parent.on_do_something_failed("请选择需要删除的文件")

    # 选择输出路径
    def OutputChoose1(parent):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(parent, "选择输出文件路径", "merge.pdf", "PDF Files (*.pdf)")
        if file_path:
            parent.ui.merge_text.setText(file_path)

    # 输出合并后的文件
    def OutputFile1(parent):
        row = parent.ui.TableWidget.rowCount()
        output_path = parent.ui.merge_text.text()
        if row <= 1:
            parent.on_do_something_failed('请添加需要合并的文件')
            return
        if not output_path:
            parent.on_do_something_failed('请选择合适的路径')
            return
        file_path = []
        for i in range(row):
            file = parent.ui.TableWidget.item(i, 2).text() + parent.ui.TableWidget.item(i, 0).text()
            file_path.append(file)
        logger.debug('导出合并文件')
        if parent.worker.isRunning():
            logger.debug('请等待上一个任务完成')
            return
        args = (file_path, output_path)
        parent.worker.set_action('merge', args)
        show_loading(parent, '正在导出文件', '请稍候')
        parent.worker.start()

    #==========拆分PDF页面按钮事件==========
    # 导入文件
    def InputFile2(parent):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(parent, "选择PDF文件", "", "PDF Files (*.pdf)")
        if file_path:
            parent.ui.LineEdit_3.setText(file_path)
            _,num_pages,_,_ = base.pdfinfo(file_path)    
            parent.ui.BodyLabel_3.setText("文件总页数：{}".format(num_pages))

    # 输出路径
    def OutputChoose2(parent):
        file_dialog = QtWidgets.QFileDialog()
        file_path = file_dialog.getExistingDirectory(parent, "选择文件夹")
        if file_path:
            parent.ui.LineEdit_7.setText(file_path)

    # 导出文件
    def OutputFile2(parent):
        input = parent.ui.LineEdit_3.text()
        output = parent.ui.LineEdit_7.text()
        rule = parent.ui.LineEdit_8.text()
        if input:
            if output:
                if rule:
                    if base.rule_check(rule):
                        try:
                            args = (input, output, base.parse(rule))
                            parent.worker.set_action('split', args)
                            show_loading(parent, '正在导出文件', '请稍候')
                            parent.worker.start()
                        except:
                            parent.on_do_something_failed('请检查规则是否合法')
                    else:
                        parent.on_do_something_failed('拆分规则不合法')
                else:
                    parent.on_do_something_failed('请按要求输入拆分规则')
            else:
                parent.on_do_something_failed('请选择合适的路径')
        else:
            parent.on_do_something_failed('请选择要拆分的文件')

    #==========删除页面事件==========
    # 导入文件
    def InputFile3(parent):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(parent, "选择PDF文件", "", "PDF Files (*.pdf)")
        if file_path:
            parent.ui.LineEdit_5.setText(file_path)
            _,num_pages,_,_ = base.pdfinfo(file_path)    
            parent.ui.BodyLabel_9.setText("文件总页数：{}".format(num_pages))

    # 输出路径
    def OutputChoose3(parent):
        file_dialog = QtWidgets.QFileDialog()
        file_path = file_dialog.getExistingDirectory(parent, "选择文件夹")
        if file_path:
            parent.ui.LineEdit_11.setText(file_path)

    # 导出文件
    def OutputFile3(parent):
        input = parent.ui.LineEdit_5.text()
        output = parent.ui.LineEdit_11.text()
        rule = parent.ui.LineEdit_12.text()
        if input:
            if output:
                if rule:
                    if base.rule_check(rule):
                        try:
                            args = (input, output, base.parse(rule))
                            parent.worker.set_action('delete', args)
                            show_loading(parent, '正在导出文件', '请稍候')
                            parent.worker.start()
                        except:
                            parent.on_do_something_failed('请检查规则是否合法')
                    else:
                        parent.on_do_something_failed('删除规则不合法')
                else:
                    parent.on_do_something_failed('请按要求输入删除规则')
            else:
                parent.on_do_something_failed('请选择合适的路径')
        else:
            parent.on_do_something_failed('请选择要删除的文件')

            
    #==========PDF转图片事件==========
    # 导入文件
    def InputFile4(parent):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(parent, "选择PDF文件", "", "PDF Files (*.pdf)")
        if file_path:
            parent.ui.LineEdit_6.setText(file_path)
            _,num_pages,_,_ = base.pdfinfo(file_path)    
            parent.ui.BodyLabel_10.setText("文件总页数：{}".format(num_pages))

    # 输出路径
    def OutputChoose4(parent):
        file_dialog = QtWidgets.QFileDialog()
        file_path = file_dialog.getExistingDirectory(parent, "选择文件夹")
        if file_path:
            parent.ui.LineEdit_14.setText(file_path)

    # 导出文件
    def OutputFile4(parent):
        input = parent.ui.LineEdit_6.text()
        output = parent.ui.LineEdit_14.text()
        rule = parent.ui.LineEdit_13.text()
        if input:
            if output:
                if rule:
                    if base.rule_check(rule):
                        try:
                            args = (input, output, base.parse(rule))
                            parent.worker.set_action('pdf2image', args)
                            show_loading(parent, '正在导出文件', '请稍候')
                            parent.worker.start()
                        except:
                            parent.on_do_something_failed('请检查规则是否合法')
                    else:
                        parent.on_do_something_failed('导出规则不合法')
                else:
                    parent.on_do_something_failed('请按要求输入导出规则')
            else:
                parent.on_do_something_failed('请选择合适的路径')
        else:
            parent.on_do_something_failed('请选择要导出的文件')
            
    #==========图片转PDF事件==========
    # 导入图片
    def InputFile5(parent):
        file_dialog = QtWidgets.QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(parent, "选择图片文件", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_paths:
            for file_path in file_paths:
                row = parent.ui.TableWidget_2.rowCount()
                parent.ui.TableWidget_2.insertRow(row)
                file_name,width,height,file_position,time = base.imageinfo(file_path)
                parent.ui.TableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(file_name))
                parent.ui.TableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(f"{width}×{height}"))
                parent.ui.TableWidget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(file_position))
                parent.ui.TableWidget_2.setItem(row, 3, QtWidgets.QTableWidgetItem(time))

    # 删除导入的图片
    def DeleteFile5(parent):
        current_row = parent.ui.TableWidget_2.currentRow()
        if current_row != -1:
            parent.ui.TableWidget_2.removeRow(current_row)
            parent.ui.TableWidget_2.setCurrentCell(-1, -1)
        else:
            parent.on_do_something_failed("请选择需要删除的文件")

    # 选择输出路径
    def OutputChoose5(parent):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(parent, "选择输出文件路径", "translate.pdf", "PDF Files (*.pdf)")
        if file_path:
            parent.ui.merge_text_2.setText(file_path)

    # 输出合并后的文件
    def OutputFile5(parent):
        row = parent.ui.TableWidget_2.rowCount()
        output_path = parent.ui.merge_text_2.text()
        if row <= 0:
            parent.on_do_something_failed('请添加需要转换的图片')
            return
        if not output_path:
            parent.on_do_something_failed('请选择合适的路径')
            return
        file_path = []
        for i in range(row):
            file = parent.ui.TableWidget_2.item(i, 2).text() + parent.ui.TableWidget_2.item(i, 0).text()
            file_path.append(file)
        logger.debug('导出PDF文件')
        if parent.worker.isRunning():
            logger.debug('请等待上一个任务完成')
            return
        args = (file_path, output_path)
        parent.worker.set_action('image2pdf', args)
        show_loading(parent, '正在导出文件', '请稍候')
        parent.worker.start()

    #==========WORD转PDF事件==========
    # 导入图片
    def InputFile6(parent):
        file_dialog = QtWidgets.QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(parent, "选择WORD文件", "", "Word Files (*.docx *.doc)")
        if file_paths:
            for file_path in file_paths:
                row = parent.ui.TableWidget_3.rowCount()
                parent.ui.TableWidget_3.insertRow(row)
                file_name,size,file_position,time = base.wordinfo(file_path)
                parent.ui.TableWidget_3.setItem(row, 0, QtWidgets.QTableWidgetItem(file_name))
                parent.ui.TableWidget_3.setItem(row, 1, QtWidgets.QTableWidgetItem(size))
                parent.ui.TableWidget_3.setItem(row, 2, QtWidgets.QTableWidgetItem(file_position))
                parent.ui.TableWidget_3.setItem(row, 3, QtWidgets.QTableWidgetItem(time))

    # 删除导入的图片
    def DeleteFile6(parent):
        current_row = parent.ui.TableWidget_3.currentRow()
        if current_row != -1:
            parent.ui.TableWidget_3.removeRow(current_row)
            parent.ui.TableWidget_3.setCurrentCell(-1, -1)
        else:
            parent.on_do_something_failed("请选择需要删除的文件")

    # 选择输出路径
    def OutputChoose6(parent):
        file_dialog = QtWidgets.QFileDialog()
        file_path= file_path = file_dialog.getExistingDirectory(parent, "选择输出文件夹路径")
        if file_path:
            parent.ui.merge_text_3.setText(file_path)

    # 输出转化后的文件
    def OutputFile6(parent):
        row = parent.ui.TableWidget_3.rowCount()
        output_path = parent.ui.merge_text_3.text()
        if row <= 0:
            parent.on_do_something_failed('请添加需要转换的文件')
            return
        if not output_path:
            parent.on_do_something_failed('请选择合适的路径')
            return
        file_path = []
        for i in range(row):
            file = parent.ui.TableWidget_3.item(i, 2).text() + parent.ui.TableWidget_3.item(i, 0).text()
            file_path.append(file)
        logger.debug('导出PDF文件')
        if parent.worker.isRunning():
            logger.debug('请等待上一个任务完成')
            return
        args = (file_path, output_path)
        parent.worker.set_action('word2pdf', args)
        show_loading(parent, '正在导出文件', '请稍候')
        parent.worker.start()

    #==========退出登录事件==========
    def logout(parent):
        def do_logout():
            qconfig.set(cfg.password, '')
            qconfig.set(cfg.auto_login, False)
            parent.close()

        show_dialog(parent, '退出登录', '提示', do_logout)
    
    