# styles.py
COMMON_STYLES = """
QCheckBox { spacing: 15px; font-size: 18px; padding: 5px; }
QCheckBox::indicator { width: 30px; height: 30px; border: 2px solid #555; border-radius: 4px; }
QCheckBox::indicator:unchecked { background-color: transparent; }
QCheckBox::indicator:checked { background-color: #2196F3; }
QPushButton#TextButton { background-color: transparent; border: none; color: #2196F3; text-align: left; padding: 5px; font-size: 14px; text-decoration: underline; }
QPushButton#TextButton:hover { color: #1976D2; }
"""
LIGHT_THEME = COMMON_STYLES + """
QMainWindow, QWidget { background-color: #ffffff; color: #000000; }
QFrame#Sidebar { background-color: #f0f0f0; border-right: 1px solid #cccccc; }
QPushButton#NavButton { text-align: left; padding: 12px; border: none; background-color: transparent; color: #333333; }
QPushButton#NavButton:hover { background-color: #e0e0e0; }
QCheckBox { color: #000000; }
QCheckBox::indicator { border: 2px solid #000000; }
"""
DARK_THEME = COMMON_STYLES + """
QMainWindow, QWidget { background-color: #000000; color: #ffffff; }
QFrame#Sidebar { background-color: #1a1a1a; border-right: 1px solid #333333; }
QPushButton#NavButton { text-align: left; padding: 12px; border: none; background-color: transparent; color: #ffffff; }
QPushButton#NavButton:hover { background-color: #333333; }
QCheckBox { color: #ffffff; }
QCheckBox::indicator { border: 2px solid #ffffff; }
"""