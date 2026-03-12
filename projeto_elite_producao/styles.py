COMMON_STYLES = """
QCheckBox { spacing: 15px; font-size: 18px; padding: 5px; }
QCheckBox::indicator { width: 30px; height: 30px; border: 2px solid #555; border-radius: 4px; }
QCheckBox::indicator:checked { background-color: #2196F3; }
QPushButton#TextButton { background: transparent; border: none; color: #2196F3; text-decoration: underline; font-size: 14px; text-align: left; }
QPushButton#NavButton { text-align: left; padding: 12px; border: none; background: transparent; font-size: 14px; }
"""
LIGHT_THEME = COMMON_STYLES + """
QMainWindow, QWidget { background-color: #ffffff; color: #000000; }
QFrame#Sidebar { background-color: #f0f0f0; border-right: 1px solid #cccccc; }
QPushButton#NavButton { color: #333333; }
QPushButton#NavButton:hover { background-color: #e0e0e0; }
"""
DARK_THEME = COMMON_STYLES + """
QMainWindow, QWidget { background-color: #000000; color: #ffffff; }
QFrame#Sidebar { background-color: #1a1a1a; border-right: 1px solid #333333; }
QPushButton#NavButton { color: #ffffff; }
QPushButton#NavButton:hover { background-color: #333333; }
"""