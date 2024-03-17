import time

from PyQt5.QtCore import pyqtSignal, QThread

from common.my_logger import my_logger as logger

from PdfControl import operation


# 多线程
class Worker(QThread):
    # 登录成功
    login_success = pyqtSignal()
    # 登录失败
    login_failed = pyqtSignal(str)
    # 操作成功
    do_something_success = pyqtSignal(object)
    # 操作失败
    do_something_failed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # 需要执行的操作
        self.action = None
        # 操作的参数
        self.action_args = None

    # 设置操作和参数
    def set_action(self, action, action_args):
        self.action = action
        self.action_args = action_args

    def run(self):
        # 操作对应的字典函数
        action_dict = {
            'login': self.login,
            'merge': self.merge,
            'split': self.split,
            'delete': self.delete,
            'pdf2image': self.pdf2image,
            'image2pdf': self.image2pdf,
            'word2pdf': self.word2pdf,
        }
        # 执行操作，如果操作不存在则抛出异常
        try:
            action_dict[self.action](self.action_args)
        except KeyError:
            raise Exception('不存在的操作')

    # ============绑定多线程调用============
    # 登录
    def login(self, args):
        try:
            print("登录参数：", args)
            time.sleep(1.5)
            username = args['username']
            password = args['password']
            if username == 'admin' and password == '123456':
                self.login_success.emit()
            else:
                self.login_failed.emit('登录失败，请检查用户信息或验证码！')
        except Exception as e:
            logger.debug(e)
            self.login_failed.emit('登录失败，请检查用户信息或验证码！')

    # 合并
    def merge(self, args):
        try:
            pdf_paths, output_path = args
            time.sleep(0.5)
            operation.merge(pdf_paths, output_path)
            self.do_something_success.emit({'result': '操作成功'})
        except Exception as e:
            logger.debug(e)
            self.do_something_failed.emit('操作失败，请检查导入文件是否出错！')

    # 拆分
    def split(self, args):
        try:
            input, output, rule = args
            time.sleep(0.5)
            operation.split(input, output, rule)
            self.do_something_success.emit({'result': '操作成功'})
        except Exception as e:
            logger.debug(e)
            self.do_something_failed.emit('操作失败，请检查导入文件是否出错！')
    
    # 删除
    def delete(self, args):
        try:
            input, output, pages = args
            time.sleep(0.5)
            operation.delete(input, output, pages)
            self.do_something_success.emit({'result': '操作成功'})
        except Exception as e:
            logger.debug(e)
            self.do_something_failed.emit('操作失败，请检查导入文件页数！')

    # PDF转图片
    def pdf2image(self, args):
        try:
            input, output, pages = args
            time.sleep(0.5)
            operation.pdf2image(input, output, pages)
            self.do_something_success.emit({'result': '操作成功'})
        except Exception as e:
            logger.debug(e)
            self.do_something_failed.emit('操作失败，请检查导入文件页数！')
    
    # 图片转PDF
    def image2pdf(self, args):
        try:
            image_paths, output_path = args
            time.sleep(0.5)
            operation.image2pdf(image_paths, output_path)
            self.do_something_success.emit({'result': '操作成功'})
        except Exception as e:
            logger.debug(e)
            self.do_something_failed.emit('操作失败，请检查导入文件是否出错！')

    # word转PDF    
    def word2pdf(self, args):
        try:
            word_paths, output_path = args
            time.sleep(0.5)
            operation.word2pdf(word_paths, output_path)
            self.do_something_success.emit({'result': '操作成功'})
        except Exception as e:
            logger.debug(e)
            self.do_something_failed.emit('操作失败，请检查导入文件是否出错！')
            
