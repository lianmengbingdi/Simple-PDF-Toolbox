from PyQt5.QtCore import pyqtSignal
from qfluentwidgets import NavigationInterface as FNavigationInterface, NavigationItemPosition

from components.icon import MyIcon


class NavigationInterface(FNavigationInterface):
    index_changed = pyqtSignal(int)

    def __init__(self, image=None, parent=None):
        super().__init__(parent, True)
        self.image = image
        self.__init_option()

    # 绑定页面与导航栏
    def __init_option(self):
        self.setExpandWidth(280)
        self.addItem(
            routeKey=self.parent().ui.stackedWidget.widget(0).objectName(),
            icon=MyIcon.DICTION,
            text='合并文档',
            tooltip='合并文档',
            onClick=lambda: self.index_changed.emit(0)
        )
        self.addItem(
            routeKey=self.parent().ui.stackedWidget.widget(1).objectName(),
            icon=MyIcon.CLIP,
            text='拆分文档',
            tooltip='拆分文档',
            onClick=lambda: self.index_changed.emit(1)
        )
        self.addItem(
            routeKey=self.parent().ui.stackedWidget.widget(2).objectName(),
            icon=MyIcon.CUT,
            text='删除页面',
            tooltip='删除页面',
            onClick=lambda: self.index_changed.emit(2)
        )
        self.addItem(
            routeKey=self.parent().ui.stackedWidget.widget(3).objectName(),
            icon=MyIcon.PHOTO,
            text='PDf转图片',
            tooltip='PDf转图片',
            onClick=lambda: self.index_changed.emit(3)
        )
        self.addItem(
            routeKey=self.parent().ui.stackedWidget.widget(4).objectName(),
            icon=MyIcon.IMAGE,
            text='图片转PDF',
            tooltip='图片转PDF',
            onClick=lambda: self.index_changed.emit(4)
        )
        self.addItem(
            routeKey=self.parent().ui.stackedWidget.widget(5).objectName(),
            icon=MyIcon.TEXT,
            text='WORD转PDF',
            tooltip='WORD转PDF',
            onClick=lambda: self.index_changed.emit(5)
        )


        self.addItem(
            routeKey=self.parent().ui.stackedWidget.widget(6).objectName(),
            icon=MyIcon.SETTING,
            text='设置',
            onClick=lambda: self.index_changed.emit(6),
            position=NavigationItemPosition.BOTTOM
        )
