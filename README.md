# SchulteGrid 应用程序

`app.py` 文件包含了一个名为 SchulteGrid 的应用程序，这是一个基于 Toga 框架开发的 Python 应用。舒尔特方格（Schulte Grid）是一种用于提高注意力和视觉搜索能力的训练工具。

## 主要功能

### 多语言支持：

- 自动检测系统语言
- 支持语言切换
- 动态更新界面文本

### 游戏逻辑：

- 生成不同大小的舒尔特方格
- 计时功能
- 记录最佳成绩

### 用户界面：

- 使用 Toga 框架创建跨平台 GUI
- 响应式布局，适应不同屏幕大小

### 数据持久化：

- 保存和加载最佳时间记录

### 系统适配：

- 检测屏幕大小
- 适配不同操作系统的应用数据存储位置

## 核心类和方法

- `SchulteGrid(toga.App)`: 主应用类
- `startup()`: 应用程序入口点
- `start_game(size)`: 开始新游戏
- `handle_button_press(button)`: 处理按钮点击事件
- `show_result(elapsed_time)`: 显示游戏结果
- `reset_game(dialog)`: 重置游戏

## 运行方式

通过执行 `main()` 函数来启动应用程序的主循环。

---

这个应用程序展示了如何使用 Python 和 Toga 框架创建一个功能完整的跨平台 GUI 应用，包括游戏逻辑、用户界面交互、多语言支持和数据持久化等特性。

---

# SchulteGrid Application

The `app.py` file contains an application called SchulteGrid, which is a Python application developed using the Toga framework. The Schulte Grid is a training tool used to improve attention and visual search abilities.

## Main Features

### Multilingual Support:

- Automatic system language detection
- Language switching support
- Dynamic interface text updates

### Game Logic:

- Generate Schulte grids of different sizes
- Timer functionality
- Record best scores

### User Interface:

- Cross-platform GUI created using the Toga framework
- Responsive layout, adapting to different screen sizes

### Data Persistence:

- Save and load best time records

### System Adaptation:

- Screen size detection
- Adapt to different operating systems' application data storage locations

## Core Classes and Methods

- `SchulteGrid(toga.App)`: Main application class
- `startup()`: Application entry point
- `start_game(size)`: Start a new game
- `handle_button_press(button)`: Handle button click events
- `show_result(elapsed_time)`: Display game results
- `reset_game(dialog)`: Reset the game

## Running the Application

The application's main loop is started by executing the `main()` function.

---

This application demonstrates how to create a fully functional cross-platform GUI application using Python and the Toga framework, including game logic, user interface interactions, multilingual support, and data persistence features.