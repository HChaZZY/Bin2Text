#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
二进制转换器启动脚本
"""

import sys
import os

def check_requirements():
    """检查是否安装了必要的库"""
    try:
        import tkinter
        return True
    except ImportError:
        print("错误: 未找到tkinter库")
        print("请确保已安装Python的tkinter模块")
        if sys.platform.startswith('win'):
            print("Windows用户: 请重新安装Python，并在安装时勾选'tcl/tk and IDLE'选项")
        elif sys.platform.startswith('linux'):
            print("Linux用户: 请运行'sudo apt-get install python3-tk'(Debian/Ubuntu)或相应的包管理器命令")
        elif sys.platform.startswith('darwin'):
            print("macOS用户: 请使用Homebrew安装'brew install python-tk'")
        return False

def main():
    """主函数"""
    if not check_requirements():
        input("按Enter键退出...")
        return
    
    # 导入主程序
    try:
        from main import main as start_app
        start_app()
    except Exception as e:
        print(f"启动程序时出错: {e}")
        input("按Enter键退出...")

if __name__ == "__main__":
    main()