import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox  # 导入文件对话框和消息框组件

class GameFileManager:
    """游戏文件管理器类，负责处理真实目录和沙盒目录之间的文件操作"""
    
    def __init__(self, sandbox_path, real_path):
        """初始化管理器
        Args:
            sandbox_path: 沙盒目录路径（用于集中存储文件）
            real_path: 真实游戏目录路径
        """
        self.sandbox_path = sandbox_path
        self.real_path = real_path

    def copy_files(self, src, dest, move=False):
        """复制或移动文件/文件夹
        Args:
            src: 源目录路径
            dest: 目标目录路径
            move: 是否移动文件（True为移动，False为复制）
        Returns:
            bool: 操作是否成功
        """
        try:
            # 检查源目录是否存在
            if not os.path.exists(src):
                return False
            
            # 如果目标目录不存在则创建
            if not os.path.exists(dest):
                os.makedirs(dest)
            
            # 遍历源目录中的所有项目
            for item in os.listdir(src):
                src_item = os.path.join(src, item)
                dest_item = os.path.join(dest, item)
                
                # 处理目录
                if os.path.isdir(src_item):
                    # 递归复制目录（允许目标目录已存在）
                    shutil.copytree(src_item, dest_item, dirs_exist_ok=True)
                    # 如果是移动操作，复制后删除源目录
                    if move:
                        shutil.rmtree(src_item)
                # 处理文件
                else:
                    # 复制文件（保留元数据）
                    shutil.copy2(src_item, dest_item)
                    # 如果是移动操作，复制后删除源文件
                    if move:
                        os.remove(src_item)
            return True
        except Exception as e:
            # 显示错误信息
            messagebox.showerror("Error", f"Operation failed: {str(e)}")
            return False

    def concentrate_files(self):
        """集中文件：将真实目录中的文件移动到沙盒目录"""
        if self.copy_files(self.real_path, self.sandbox_path, move=True):
            messagebox.showinfo("Success", "Files concentrated to sandbox.")
        else:
            messagebox.showwarning("Error", "Failed to concentrate files.")

    def restore_to_real(self):
        """恢复文件：将沙盒目录中的文件复制回真实目录"""
        if self.copy_files(self.sandbox_path, self.real_path):
            messagebox.showinfo("Success", "Files restored to real location.")
        else:
            messagebox.showwarning("Error", "Failed to restore files.")

    def re_concentrate(self):
        """重新集中：先清空真实目录，再从沙盒目录移动文件"""
        try:
            # 警告：此操作将永久删除真实目录内容！
            if os.path.exists(self.real_path):
                shutil.rmtree(self.real_path)  # 递归删除目录
                os.makedirs(self.real_path)    # 重新创建空目录
            self.concentrate_files()
        except Exception as e:
            messagebox.showerror("Error", f"Re-concentrate failed: {str(e)}")

def browse_directory(entry):
    """打开目录选择对话框并更新输入框内容
    Args:
        entry: tkinter输入框对象
    """
    directory = filedialog.askdirectory()
    if directory:
        entry.delete(0, tk.END)     # 清空输入框
        entry.insert(0, directory)  # 插入新路径

def start_manager():
    """启动文件管理器主功能"""
    real_path = real_entry.get()
    sandbox_path = sandbox_entry.get()
    
    # 验证路径是否已选择
    if not real_path or not sandbox_path:
        messagebox.showwarning("Error", "Please select both paths.")
        return
    
    # 创建文件管理器实例
    manager = GameFileManager(sandbox_path, real_path)
    
    # 创建操作窗口
    action_window = tk.Toplevel(root)
    action_window.title("Game File Actions")
    action_window.geometry("300x200")  # 设置窗口尺寸
    
    # 添加操作按钮
    tk.Button(action_window, text="Concentrate Files", 
              command=manager.concentrate_files).pack(pady=10)
    tk.Button(action_window, text="Restore to Real", 
              command=manager.restore_to_real).pack(pady=10)
    tk.Button(action_window, text="Re-Concentrate", 
              command=manager.re_concentrate).pack(pady=10)

# 创建主GUI窗口
root = tk.Tk()
root.title("Game File Manager Setup")
root.geometry("600x200")  # 设置主窗口尺寸

# 真实游戏路径选择组件
tk.Label(root, text="Real Game Path:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
real_entry = tk.Entry(root, width=50)
real_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", 
          command=lambda: browse_directory(real_entry)).grid(row=0, column=2, padx=10, pady=10)

# 沙盒路径选择组件
tk.Label(root, text="Sandbox Path:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
sandbox_entry = tk.Entry(root, width=50)
sandbox_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", 
          command=lambda: browse_directory(sandbox_entry)).grid(row=1, column=2, padx=10, pady=10)

# 启动管理器按钮
tk.Button(root, text="Start Manager", command=start_manager).grid(row=2, column=0, columnspan=3, pady=20)

# 启动GUI主循环
root.mainloop()