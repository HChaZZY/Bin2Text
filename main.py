#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本与二进制互转GUI程序
支持全Unicode字符集的实时双向转换
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import time

class BinaryConverter:
    """二进制转换器核心类"""
    
    @staticmethod
    def text_to_binary(text):
        """
        将文本转换为二进制字符串
        使用UTF-8编码，每个字节转为8位二进制
        """
        try:
            # 将文本转换为UTF-8编码的字节
            byte_data = text.encode('utf-8')
            # 将每个字节转换为8位二进制字符串（补前导零）
            binary_strings = [f"{byte:08b}" for byte in byte_data]
            # 用空格分隔每8位，方便阅读
            return ' '.join(binary_strings)
        except Exception as e:
            print(f"文本转二进制错误: {e}")
            return ""
    
    @staticmethod
    def binary_to_text(binary):
        """
        将二进制字符串转换为文本
        移除所有非0/1字符，然后按8位分组解码
        """
        try:
            # 移除所有非0/1字符（包括空格）
            clean_binary = ''.join(c for c in binary if c in '01')
            
            # 检查长度是否为8的倍数
            if len(clean_binary) % 8 != 0:
                raise ValueError("二进制长度必须是8的倍数")
            
            # 将二进制字符串按8位分组
            byte_strings = [clean_binary[i:i+8] for i in range(0, len(clean_binary), 8)]
            
            # 将每组二进制转换为整数，然后转换为字节
            byte_data = bytes([int(byte, 2) for byte in byte_strings])
            
            # 将字节解码为UTF-8文本
            return byte_data.decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError("无效的UTF-8编码二进制数据")
        except Exception as e:
            raise ValueError(f"二进制转文本错误: {e}")


class BinaryConverterApp:
    """二进制转换器应用程序"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("二进制双向转换器")
        self.root.geometry("1000x600")
        
        # 标记变量，防止无限循环更新
        self.updating_text = False
        self.updating_binary = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建两个并排的文本框
        text_frame = ttk.LabelFrame(main_frame, text="文本输入区", padding="5")
        text_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        binary_frame = ttk.LabelFrame(main_frame, text="二进制输入区", padding="5")
        binary_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # 配置网格权重，使文本框可以均匀扩展
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # 创建文本输入框
        self.text_input = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=40, height=20)
        self.text_input.pack(fill=tk.BOTH, expand=True)
        
        # 创建二进制输入框
        self.binary_input = scrolledtext.ScrolledText(binary_frame, wrap=tk.WORD, width=40, height=20)
        self.binary_input.pack(fill=tk.BOTH, expand=True)
        
        # 创建状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪 | 文本长度: 0字符 | 二进制长度: 0位")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 绑定事件
        self.text_input.bind("<KeyRelease>", self.on_text_change)
        self.binary_input.bind("<KeyRelease>", self.on_binary_change)
    
    def on_text_change(self, event=None):
        """当文本输入框内容变化时调用"""
        # 防止无限循环更新
        if self.updating_binary:
            return
        
        self.updating_text = True
        
        # 获取文本内容
        text = self.text_input.get("1.0", tk.END).rstrip("\n")
        
        # 测量转换时间
        start_time = time.time()
        
        # 转换为二进制
        binary = BinaryConverter.text_to_binary(text)
        
        # 计算转换时间（毫秒）
        conversion_time = (time.time() - start_time) * 1000
        
        # 更新二进制输入框
        self.binary_input.delete("1.0", tk.END)
        self.binary_input.insert("1.0", binary)
        
        # 更新状态栏
        self.update_status(text, binary, conversion_time)
        
        self.updating_text = False
    
    def on_binary_change(self, event=None):
        """当二进制输入框内容变化时调用"""
        # 防止无限循环更新
        if self.updating_text:
            return
        
        self.updating_binary = True
        
        # 获取二进制内容
        binary = self.binary_input.get("1.0", tk.END).rstrip("\n")
        
        # 测量转换时间
        start_time = time.time()
        
        try:
            # 尝试转换为文本
            text = BinaryConverter.binary_to_text(binary)
            
            # 更新文本输入框
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", text)
            
            # 计算转换时间（毫秒）
            conversion_time = (time.time() - start_time) * 1000
            
            # 更新状态栏
            self.update_status(text, binary, conversion_time)
            
        except ValueError as e:
            # 二进制格式错误，显示错误消息
            self.status_var.set(f"错误: {e} | 保持原文本显示")
        
        self.updating_binary = False
    
    def update_status(self, text, binary, conversion_time):
        """更新状态栏信息"""
        # 计算文本长度（字符数）
        text_length = len(text)
        
        # 计算二进制长度（位数）
        # 移除所有非0/1字符
        clean_binary = ''.join(c for c in binary if c in '01')
        binary_length = len(clean_binary)
        
        # 更新状态栏
        self.status_var.set(
            f"转换耗时: {conversion_time:.2f}ms | "
            f"文本长度: {text_length}字符 | "
            f"二进制长度: {binary_length}位"
        )


def main():
    """主函数"""
    root = tk.Tk()
    app = BinaryConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()