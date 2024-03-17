from qfluentwidgets import ToolTipFilter
from qframelesswindow import FramelessWindow

from common.config import cfg
from common.my_logger import my_logger as logger
from common.public import set_stylesheet, show_toast, hide_loading
from common.threads import Worker
from components.custom_titlebar import CustomTitleBar
from view.navigation_interface import NavigationInterface
from view.setting_interface import SettingInterface
from view.ui_main_window import Ui_MainWindow
from view.button_action import buttonaction


class MainWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.settingInterface = None
        self.navigation_interface = None
        self.StateTooltip = None
        logger.debug('init main window')
        # self.setTitleBar(StandardTitleBar(self))
        self.setTitleBar(CustomTitleBar(self))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.worker = Worker()
        self.init_navigation()
        self.init_setting_page()
        self.init_btn_tool_tips()
        self.bind_event()
        set_stylesheet(self, 'main_window')
        cfg.themeChanged.connect(lambda: set_stylesheet(self, 'main_window'))
        # 把窗口放在屏幕中间
        self.move(int((self.screen().size().width() - self.width()) / 2),
                  int((self.screen().size().height() - self.height()) / 2))

    def init_navigation(self):
        logger.debug('init navigation')
        self.navigation_interface = NavigationInterface('张三', parent=self)
        self.ui.main_layout.insertWidget(0, self.navigation_interface)
        self.ui.stackedWidget.currentChanged.connect(self.on_current_interface_changed)
        self.navigation_interface.index_changed.connect(self.ui.stackedWidget.setCurrentIndex)
        self.on_current_interface_changed(0)

    def init_setting_page(self):
        logger.debug('init setting page')
        self.settingInterface = SettingInterface(self)
        self.ui.setting_layout.addWidget(self.settingInterface)
        self.settingInterface.logout.connect(lambda: buttonaction.logout(self))

    def init_btn_tool_tips(self, duration=5000):
        logger.debug('init btn tool tips')
        btn_dict = {'pushButton_2': '测试按钮2'}
        for btn_name, tips in btn_dict.items():
            btn = getattr(self.ui, btn_name)
            btn.setToolTip(tips)
            btn.installEventFilter(ToolTipFilter(btn))
            btn.setToolTipDuration(duration)

    # 绑定按钮与事件
    def bind_event(self):
        logger.debug('bind event')
        self.titleBar.searchSignal.connect(lambda: show_toast(self, '提示', '点击了搜索'))
        # 绑定合并文件事件
        self.ui.pushButton.clicked.connect(lambda: buttonaction.InputFile1(self))
        self.ui.pushButton_4.clicked.connect(lambda: buttonaction.DeleteFile1(self))
        self.ui.pushButton_5.clicked.connect(lambda: buttonaction.OutputChoose1(self))
        self.ui.pushButton_1.clicked.connect(lambda: buttonaction.OutputFile1(self))
        # 绑定拆分文件事件
        self.ui.pushButton_2.clicked.connect(lambda: buttonaction.InputFile2(self))
        self.ui.pushButton_3.clicked.connect(lambda: buttonaction.OutputChoose2(self))
        self.ui.pushButton_7.clicked.connect(lambda: buttonaction.OutputFile2(self))
        # 绑定页面删除事件
        self.ui.pushButton_10.clicked.connect(lambda: buttonaction.InputFile3(self))
        self.ui.pushButton_6.clicked.connect(lambda: buttonaction.OutputChoose3(self))
        self.ui.pushButton_9.clicked.connect(lambda: buttonaction.OutputFile3(self))
        # 绑定PDF转图片事件
        self.ui.pushButton_12.clicked.connect(lambda: buttonaction.InputFile4(self))
        self.ui.pushButton_13.clicked.connect(lambda: buttonaction.OutputChoose4(self))
        self.ui.pushButton_11.clicked.connect(lambda: buttonaction.OutputFile4(self))
        # 绑定图片转PDF事件
        self.ui.pushButton_15.clicked.connect(lambda: buttonaction.InputFile5(self))
        self.ui.pushButton_16.clicked.connect(lambda: buttonaction.DeleteFile5(self))
        self.ui.pushButton_8.clicked.connect(lambda: buttonaction.OutputChoose5(self))
        self.ui.pushButton_14.clicked.connect(lambda: buttonaction.OutputFile5(self))
        # 绑定WORD转PDF事件
        self.ui.pushButton_19.clicked.connect(lambda: buttonaction.InputFile6(self))
        self.ui.pushButton_20.clicked.connect(lambda: buttonaction.DeleteFile6(self))
        self.ui.pushButton_17.clicked.connect(lambda: buttonaction.OutputChoose6(self))
        self.ui.pushButton_18.clicked.connect(lambda: buttonaction.OutputFile6(self))
        # 绑定worker事件
        self.worker.do_something_success.connect(self.on_do_something_success)
        self.worker.do_something_failed.connect(self.on_do_something_failed)

    def on_do_something_success(parent, result):
        logger.debug('do something success')
        show_toast(parent, '提示', result['result'])
        hide_loading(parent, result['result'])

    def on_do_something_failed(parent, msg):
        logger.debug('do something failed')
        show_toast(parent, '提示', msg)
        hide_loading(parent, '加载失败')

    def on_current_interface_changed(parent, index):
        widget = parent.ui.stackedWidget.widget(index)
        parent.navigation_interface.setCurrentItem(widget.objectName())
    
    

