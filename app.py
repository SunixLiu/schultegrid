"""
Schulte Grid to enhance your ability of attention
"""
import toga
import random
import time
import json
import os
import locale
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class SchulteGrid(toga.App):
    def startup(self):
        # 检测系统语言并设置初始语言
        self.current_language = self.detect_system_language()
        
        # 检测并打印屏幕大小
        self.detect_screen_size()
        
        # 创建翻译字典
        self.translations = {
            'zh': {
                'title': '舒尔特方格',
                'best_record_3x3': '3x3最佳记录: {}',
                'best_record_5x5': '5x5最佳记录: {}',
                'no_record': '暂无记录',
                'seconds': '秒',
                'switch_language': '切换语言',
                'game_over': '游戏结束',
                'congratulations': '恭喜完成！\n用时：{}秒'
            },
            'en': {
                'title': 'Schulte Grid',
                'best_record_3x3': '3x3 Best: {}',
                'best_record_5x5': '5x5 Best: {}',
                'no_record': 'No Record',
                'seconds': 's',
                'switch_language': 'Switch Language',
                'game_over': 'Game Over',
                'congratulations': 'Congratulations!\nTime: {} seconds'
            }
        }
        
        # 设置窗口大小为1080x2340像素
        self.main_window = toga.MainWindow(title=self.translate('title'), size=(1080, 2340))
        self.current_grid_size = 0
        self.numbers = []
        self.current_number = 1
        self.start_time = None
        self.buttons = []
        
        # 添加最好成绩记录并从文件加载
        self.best_times = self.load_best_times()
        
        # 创建主容器，设置为居中对齐，并添加flex属性使内容垂直居中
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10, alignment='center', flex=1))
        
        # 创建一个顶部空白区域来帮助垂直居中
        top_spacer = toga.Box(style=Pack(flex=1))
        
        # 创建顶部工具栏，包含语言切换按钮
        toolbar_box = toga.Box(style=Pack(direction=ROW, padding=5, alignment='right'))
        self.language_button = toga.Button(
            self.translate('switch_language'),
            on_press=self.toggle_language,
            style=Pack(padding=5, font_size=10)
        )
        toolbar_box.add(self.language_button)
        
        # 创建最好成绩显示区域 - 修改为一行显示
        records_box = toga.Box(style=Pack(direction=ROW, padding=5, alignment='center'))
        
        # 格式化显示最佳时间
        time_3x3 = f"{self.best_times[3]}{self.translate('seconds')}" if self.best_times[3] is not None else self.translate('no_record')
        time_5x5 = f"{self.best_times[5]}{self.translate('seconds')}" if self.best_times[5] is not None else self.translate('no_record')
        
        self.record_label_3x3 = toga.Label(self.translate('best_record_3x3').format(time_3x3), style=Pack(padding=(0, 10, 0, 0), font_size=10))
        self.record_label_5x5 = toga.Label(self.translate('best_record_5x5').format(time_5x5), style=Pack(padding=(0, 0, 0, 10), font_size=10))
        
        records_box.add(self.record_label_3x3)
        records_box.add(self.record_label_5x5)
        
        # 创建难度选择按钮，设置为居中对齐
        difficulty_box = toga.Box(style=Pack(direction=ROW, padding=5, alignment='center', flex=1))
        
        # 3x3难度按钮
        btn_3x3 = toga.Button('3x3', 
                             on_press=lambda widget: self.start_game(3),
                             style=Pack(
                                 width=120,
                                 height=100,
                                 padding=10,
                                 font_size=24,
                                 background_color='#2196F3',  # 使用蓝色背景
                                 color='white'  # 白色文字
                             ))
        
        # 添加按钮之间的间距
        spacer = toga.Box(style=Pack(width=30))  # 增加间距
        
        # 5x5难度按钮
        btn_5x5 = toga.Button('5x5', 
                             on_press=lambda widget: self.start_game(5),
                             style=Pack(
                                 width=120,
                                 height=100,
                                 padding=10,
                                 font_size=24,
                                 background_color='#FF4081',  # 使用粉色背景
                                 color='white'  # 白色文字
                             ))
        
        difficulty_box.add(btn_3x3)
        difficulty_box.add(spacer)
        difficulty_box.add(btn_5x5)
        
        # 创建游戏区域容器，设置为居中对齐
        self.game_box = toga.Box(style=Pack(direction=COLUMN, padding=5, alignment='center'))
        
        # 创建一个底部空白区域来帮助垂直居中
        bottom_spacer = toga.Box(style=Pack(flex=1))
        
        # 添加到主容器
        main_box.add(toolbar_box)  # 添加工具栏到顶部
        main_box.add(top_spacer)
        main_box.add(records_box)
        main_box.add(difficulty_box)
        main_box.add(self.game_box)
        main_box.add(bottom_spacer)
        self.main_window.content = main_box
        self.main_window.show()
        
        # 窗口创建后再次打印屏幕大小
        print(f"窗口创建后屏幕大小: {self.main_window.size[0]}x{self.main_window.size[1]}")
        
        # 在Android平台上尝试获取更准确的屏幕大小
        try:
            import platform
            if platform.system() == "Linux":  # 可能是Android
                try:
                    import jnius
                    print("Android平台窗口创建后，再次检测屏幕大小")
                    # 这里可以再次调用Android特定的屏幕大小检测代码
                except ImportError:
                    pass
        except Exception as e:
            print(f"窗口创建后检测Android屏幕大小时出错: {e}")
    def detect_system_language(self):
        """检测系统语言并返回语言代码"""
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale and system_locale.startswith('zh'):
                return 'zh'
            else:
                return 'en'
        except:
            return 'en'  # 默认使用英文
    def detect_screen_size(self):
        """检测屏幕大小并打印到控制台"""
        try:
            # 使用更可靠的方法检测屏幕大小
            import platform
            system = platform.system()
            
            if system == "Windows":
                import ctypes
                user32 = ctypes.windll.user32
                screen_width = user32.GetSystemMetrics(0)
                screen_height = user32.GetSystemMetrics(1)
                print(f"检测到Windows屏幕大小: {screen_width}x{screen_height}")
            elif system == "Linux":
                # 可能是Android平台，Android是基于Linux的
                print("检测到Linux/Android平台，将在窗口创建后获取屏幕大小")
            elif system == "Darwin":  # macOS
                print("检测到macOS平台，将在窗口创建后获取屏幕大小")
            else:
                # 其他平台
                print(f"检测到{system}平台，将在窗口创建后获取屏幕大小")
                
            # 尝试检测是否为Android平台
            try:
                import jnius
                from jnius import autoclass
                # 如果能导入jnius，说明可能在Android环境
                print("检测到可能是Android平台")
                
                # 尝试获取Android屏幕大小
                Activity = autoclass('org.kivy.android.PythonActivity')
                Resources = autoclass('android.content.res.Resources')
                activity = Activity.mActivity
                resources = activity.getResources()
                metrics = resources.getDisplayMetrics()
                screen_width = metrics.widthPixels
                screen_height = metrics.heightPixels
                print(f"检测到Android屏幕大小: {screen_width}x{screen_height}")
            except ImportError:
                # 不是Android平台或jnius未安装
                pass
            except Exception as e:
                print(f"尝试获取Android屏幕大小时出错: {e}")
                
        except Exception as e:
            print(f"检测屏幕大小时出错: {e}")
            print("将在窗口创建后获取屏幕大小")
    def translate(self, key):
        """根据当前语言返回翻译文本"""
        return self.translations.get(self.current_language, {}).get(key, key)
    
    def toggle_language(self, widget):
        """切换语言并更新界面"""
        self.current_language = 'en' if self.current_language == 'zh' else 'zh'
        self.update_ui_language()
    
    def update_ui_language(self):
        """更新界面上的所有文本为当前语言"""
        # 更新窗口标题
        self.main_window.title = self.translate('title')
        
        # 更新语言切换按钮
        self.language_button.text = self.translate('switch_language')
        
        # 更新记录标签
        time_3x3 = f"{self.best_times[3]}{self.translate('seconds')}" if self.best_times[3] is not None else self.translate('no_record')
        time_5x5 = f"{self.best_times[5]}{self.translate('seconds')}" if self.best_times[5] is not None else self.translate('no_record')
        
        self.record_label_3x3.text = self.translate('best_record_3x3').format(time_3x3)
        self.record_label_5x5.text = self.translate('best_record_5x5').format(time_5x5)

    def load_best_times(self):
        """从文件加载最佳时间记录"""
        data_file = os.path.join(self.app_dir, 'best_times.json')
        default_times = {3: None, 5: None}
        
        try:
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    loaded_times = json.load(f)
                    # 确保返回的字典包含所有必需的键
                    return {
                        3: loaded_times.get('3') or loaded_times.get(3),
                        5: loaded_times.get('5') or loaded_times.get(5)
                    }
            return default_times
        except Exception:
            # 如果加载失败，返回默认值
            return default_times
    
    def save_best_times(self):
        """保存最佳时间记录到文件"""
        data_file = os.path.join(self.app_dir, 'best_times.json')
        try:
            with open(data_file, 'w') as f:
                json.dump(self.best_times, f)
        except Exception:
            # 如果保存失败，简单地忽略错误
            pass
    
    @property
    def app_dir(self):
        """获取应用数据目录"""
        app_dir = os.path.join(os.path.expanduser('~'), '.schulte_grid')
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        return app_dir
    
    def start_game(self, size):
        # 清空游戏区域
        self.game_box.clear()
        self.current_grid_size = size
        self.current_number = 1
        self.buttons = []
        
        # 添加调试信息
        # print(f"开始游戏，大小: {size}x{size}")
        
        # 获取屏幕宽度
        screen_width = self.main_window.size[0]
        # print(f"屏幕宽度: {screen_width}")
        
        # 计算网格总宽度为屏幕宽度的80%
        grid_width = screen_width * 0.8
        # 计算每个按钮的宽度（考虑到按钮之间的间距）
        button_width = int(grid_width / size) - 2
        button_height = button_width  # 保持按钮为正方形
        
        # 根据网格大小调整字体大小，5x5网格使用更小的字体
        if size == 3:
            font_size = int(button_width * 0.35)
        else:  # 5x5网格
            font_size = int(button_width * 0.20)  # 减小字体比例
        
        # print(f"按钮宽度: {button_width}, 高度: {button_height}, 字体大小: {font_size}")
        
        # 使用完全不同的方法生成和分配数字
        total_cells = size * size
        numbers_pool = list(range(1, total_cells + 1))
        random.shuffle(numbers_pool)
        
        # print(f"生成的数字池: {numbers_pool}")
        # print(f"数字池长度: {len(numbers_pool)}")
        
        # 创建网格 - 使用一维数组直接分配数字
        button_index = 0
        for i in range(size):
            row_box = toga.Box(style=Pack(direction=ROW))
            for j in range(size):
                if button_index < len(numbers_pool):
                    number = numbers_pool[button_index]
                    # print(f"位置 ({i},{j}) 索引 {button_index} 数字 {number}")
                    button = toga.Button(
                        str(number),
                        on_press=self.handle_button_press,
                        style=Pack(
                            padding=1,
                            width=button_width,
                            height=button_height,
                            font_size=font_size
                        )
                    )
                    row_box.add(button)
                    self.buttons.append(button)
                    button_index += 1
                else:
                    print(f"警告: 位置 ({i},{j}) 索引 {button_index} 超出范围")
            self.game_box.add(row_box)
            # print(f"完成行 {i}, 当前按钮索引: {button_index}")
        
        # print(f"创建的按钮总数: {len(self.buttons)}")
        
        # 开始计时
        self.start_time = time.time()
    
    def handle_button_press(self, button):
        if int(button.text) == self.current_number:
            self.current_number += 1
            button.style.background_color = '#8BC34A'  # 更鲜艳的绿色
            button.style.color = 'white'  # 白色文字，增加对比度
            
            # 检查是否完成游戏
            if self.current_number > self.current_grid_size * self.current_grid_size:
                end_time = time.time()
                elapsed_time = round(end_time - self.start_time, 2)
                # 直接显示对话框
                self.show_result(elapsed_time)
    
    def show_result(self, elapsed_time):
        # 更新最佳成绩
        size = self.current_grid_size
        if self.best_times[size] is None or elapsed_time < self.best_times[size]:
            self.best_times[size] = elapsed_time
            # 更新显示
            if size == 3:
                self.record_label_3x3.text = self.translate('best_record_3x3').format(f"{elapsed_time}{self.translate('seconds')}")
            elif size == 5:
                self.record_label_5x5.text = self.translate('best_record_5x5').format(f"{elapsed_time}{self.translate('seconds')}")
            # 保存最佳时间到文件
            self.save_best_times()
        
        # 创建结果对话框 - 使用同步方式
        self.main_window.info_dialog(
            self.translate('game_over'),
            self.translate('congratulations').format(elapsed_time)
        )
        # Reset game after showing the dialog
        self.reset_game(None)
    
    def reset_game(self, dialog):
        # 重置游戏区域
        self.game_box.clear()
        self.current_number = 1
        self.buttons = []

def main():
    return SchulteGrid('舒尔特方格', 'org.sunix.schulte-grid')

if __name__ == '__main__':
    main().main_loop()