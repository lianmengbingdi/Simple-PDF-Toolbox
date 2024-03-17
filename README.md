# 简易PDF工具箱

## 功能简介

- **PDF处理功能**：

  - 将多个PDF文件合并为一个PDF文件。
  - 将一个PDF文件拆分为多个PDF文件。
  - 删除PDF文件中的某些页面。
  - 将PDf转换为图片输出。
  - 将图片合成为PDF。
  - 将WORD文档转化为PDF文档（支持批处理操作）。

  ![image-20240317095256202](show\image-20240317095256202.png)

- **登录功能**：

  - 支持记住密码、自动登录。

    ![image-20240317095516067](show\image-20240317095516067.png)

- **其他功能**：

  - 支持设置外观。
  - 支持自定义主题颜色。![image-20240317095353841](show\image-20240317095353841.png)

  - 支持侧边栏展开。

    ![image-20240317095443956](show\image-20240317095443956.png)

## 文件结构

```shell
Simple-PDF-Toolbox  # 项目名称
│  build.py           # 导出可执行文件
│  config.json        # 配置文件
│  entry.py           # 项目的入口文件
│  pack_resource.py   # 打包资源的脚本文件
│  README.md          # 项目的说明文件
│  requirements.txt   # 包含项目所需的依赖库列表
│  resource_rc.py     # 图片或矢量图等文件打包后的文件
|
├─common            # 基本功能模块
│     aes.py          # AES加密模块
│     config.py       # 配置模块
│     my_logger.py    # 日志模块
│     public.py       # 主题设置以及消息提醒模块
│     threads.py      # 继承 QThread 的多线程处理模块
|
├─components        # 用户界面组件模块
│     custom_titlebar.py      # 自定义标题栏组件模块
│     icon.py                 # 图标组件模块
│     my_stacked_widgets.py   # 切换窗口动态效果模块
|
├─logs              # 日志文件目录
|
├─PdfControl        # PDF操作相关模块
│  │  base.py         # 基础解析模块
│  │  operation.py    # PDF操作模块
│  │
│  ├─test           # 测试相关文件目录
|
├─resource          # 资源文件目录
│  │  resource.qrc  # Qt资源文件
│  │
│  ├─i18n           # 组件中文化支持
│  │
│  ├─images         # 图片文件目录
│  │  │  login_background.png       # 登录背景图片
│  │  │  login_background_dark.png  # 深色登录背景图片
│  │  │  logo.png                   # logo图片
│  │  │
│  │  └─icons       # 图标文件目录
│  │
│  └─qss      # 样式表文件目录
│      ├─dark      # 暗色主题样式表文件目录
│      │      login_window.qss       # 登录窗口暗色主题样式表
│      │      main_window.qss        # 主窗口暗色主题样式表
│      │      setting_interface.qss  # 设置界面暗色主题样式表
│      │
│      └─light     # 亮色主题样式表文件目录
│              login_window.qss       # 登录窗口亮色主题样式表
│              main_window.qss        # 主窗口亮色主题样式表
│              setting_interface.qss  # 设置界面亮色主题样式表

├─ui               # UI文件目录
│     login_window.ui    # 登录窗口UI文件
│     main_window.ui     # 主窗口UI文件

├─view             # 视图相关逻辑模块文件
│     button_action.py         # 按钮动作模块
│     login_window.py          # 登录窗口模块
│     main_window.py           # 主窗口模块
│     navigation_interface.py  # 侧边导航栏模块
│     setting_interface.py     # 设置界面模块
│     ui_login_window.py       # 登录窗口UI逻辑模块
│     ui_main_window.py        # 主窗口UI逻辑模块
```

## 运行

- 环境：

  - **操作系统**：windows

  - **python版本**：python3.8或python3.10

    这两个环境是测试过的，其他环境应该也可以，建议使用python3.8。

    其中，python3.10如果是最高版本，会出现部分库冲突的问题，需要降低python版本。
    
  - **requirements**：
    
    ```shell
    PyQt5  # GUI组件包
    darkdetect  # 用于检测操作系统的当前主题是否为暗色模式。
    loguru     # Python 日志库
    PyMuPDF    # 提供了读取、写入和操作 PDF 文档的功能
    PyQt_Fluent_Widgets     # PyQt5 库的扩展，提供了 Fluent Design 风格的 UI 组件
    PyQt5_Frameless_Window  # PyQt5 库的扩展，用于创建无边框窗口的 GUI 应用程序。
    pycryptodome  # 提供了加密算法
    nuitka        # 将python转换为C，用于打包
    imageio       # 打包时转化logo图标
    comtypes      # 允许 Python 程序调用 COM 对象和接口
    pillow  # 提供图像处理功能
    ```
    
  - 需要安装**WORD应用**。
  
  - **运行指令**：
  
    ```shell
    pip install -r requirements
    python pack_resource.py   # 打包资源文件并转化ui文件
    python entry.py           # 程序入口文件
    ```
    
  - **初始账户**：
  
    用户名：admin
  
    密码：123456

## 打包

**运行指令**：

```shell
python build.py
```

## 相关bug及解决方式

1. 点击导航栏选择页面后，主页面错位，拖动边界复位，再次切换页面再次错位。

   解决方式：是PyQt-Fluent-Widgets版本过旧导致的，需要安装最新版PyQt-Fluent-Widgets。

2. TableWidget组件的表头总是自己隐藏，使用designer设置显示后再保存也没有作用。

   解决方式：手动将ui文件中的horizontalHeaderVisible值改为true。

3. 使用nuitka打包时，fitz.mupdf打包不进去，总是在这里卡住。

   fitz是PyMuPDF的模块。

   解决方式：原因是fitz的部分文件是C语言写的可执行文件，打包时将该库排除，在打包完成后手动将该库文件夹fitz从python环境中的Lib\site-packages复制到打包后的文件夹build\entry.dist中即可。

## 其他

项目UI基于PyQt-Fluent-Widgets模板设计，部分参考[Cheukfung/pyqt-fluent-widgets-template: 配合qt designer使用，基于pyqt-fluent-widgets的模板 (github.com)](https://github.com/Cheukfung/pyqt-fluent-widgets-template)。

