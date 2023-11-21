import tkinter as tk  # 导入tkinter模块，用于创建GUI界面
from tkinter import messagebox, filedialog  # 导入messagebox和filedialog模块，用于显示消息框和选择文件对话框
import requests  # 导入requests模块，用于发送HTTP请求
from bs4 import BeautifulSoup  # 导入BeautifulSoup模块，用于解析HTML

def validate_input(url, content, save_path):
    """
    验证输入的网址、内容和保存位置是否为空
    :param url: 网址
    :param content: 要爬取的内容
    :param save_path: 保存位置
    :return: 验证结果，True为验证通过，False为验证失败
    """
    if not url:
        messagebox.showerror("错误", "请输入网址！")  # 显示错误消息框
        return False
    if not content:
        messagebox.showerror("错误", "请输入要爬取的内容！")  # 显示错误消息框
        return False
    if not save_path:
        messagebox.showerror("错误", "请选择保存位置！")  # 显示错误消息框
        return False
    return True

def save_as_text(result, save_path):
    """
    将爬取结果保存为文本文件
    :param result: 爬取结果
    :param save_path: 保存位置
    """
    with open(save_path + "/result.txt", "w", encoding="utf-8") as file:
        for item in result:
            file.write(str(item) + "\n")

def save_as_csv(result, save_path):
    """
    将爬取结果保存为CSV文件
    :param result: 爬取结果
    :param save_path: 保存位置
    """
    with open(save_path + "/result.csv", "w", encoding="utf-8") as file:
        for item in result:
            file.write(str(item) + ",")
        file.write("\n")

def save_as_json(result, save_path):
    """
    将爬取结果保存为JSON文件
    :param result: 爬取结果
    :param save_path: 保存位置
    """
    with open(save_path + "/result.json", "w", encoding="utf-8") as file:
        file.write(str(result))

def scrape_website():
    """
    爬取网页内容并保存
    """
    url = entry_url.get()  # 获取输入的网址
    content = entry_content.get().encode('utf-8')  # 获取输入的要爬取的内容，并转换为UTF-8编码
    save_path = entry_save_path.get()  # 获取输入的保存位置
    format_choice = format_var.get()  # 获取选择的保存格式

    try:
        if not validate_input(url, content, save_path):  # 验证输入的网址、内容和保存位置是否为空
            return

        response = requests.get(url, timeout=5)  # 发送HTTP请求，获取网页内容
        response.encoding = 'utf-8'  # 设置编码为UTF-8
        response.raise_for_status()  # 如果请求失败，抛出异常

        soup = BeautifulSoup(response.text, 'html.parser')  # 使用BeautifulSoup解析HTML
        result = soup.find_all(content)  # 查找所有符合要求的内容

        save_functions = {
            "Text": save_as_text,  # 保存为文本文件的函数
            "CSV": save_as_csv,  # 保存为CSV文件的函数
            "JSON": save_as_json  # 保存为JSON文件的函数
        }

        if format_choice in save_functions:  # 如果选择的保存格式在保存函数字典中
            save_functions[format_choice](result, save_path)  # 调用对应的保存函数
        else:
            messagebox.showerror("错误", "不支持的保存格式！")  # 显示错误消息框
            return

        messagebox.showinfo("提示", "爬取成功！")  # 显示提示消息框
    except requests.exceptions.RequestException as e:
        messagebox.showerror("错误", "网络请求异常：" + str(e))  # 显示错误消息框
    except requests.exceptions.HTTPError as e:
        messagebox.showerror("错误", "网络请求错误：" + str(e))  # 显示错误消息框
    except Exception as e:
        messagebox.showerror("错误", "发生异常：" + str(e))  # 显示错误消息框

window = tk.Tk()  # 创建窗口
window.title("网页爬取工具")  # 设置窗口标题

label_url = tk.Label(window, text="请输入网址：")  # 创建标签，显示提示文本
label_url.pack()  # 将标签添加到窗口

entry_url = tk.Entry(window)  # 创建文本框，用于输入网址
entry_url.pack()  # 将文本框添加到窗口

label_content = tk.Label(window, text="请输入要爬取的内容（例如：div、p、a等）：")  # 创建标签，显示提示文本
label_content.pack()  # 将标签添加到窗口

entry_content = tk.Entry(window)  # 创建文本框，用于输入要爬取的内容
entry_content.pack()  # 将文本框添加到窗口

label_save_path = tk.Label(window, text="请选择保存位置：")  # 创建标签，显示提示文本
label_save_path.pack()  # 将标签添加到窗口

entry_save_path = tk.Entry(window)  # 创建文本框，用于显示保存位置
entry_save_path.pack()  # 将文本框添加到窗口

def select_save_path():
    """
    选择保存位置
    """
    save_path = filedialog.askdirectory()  # 打开选择文件对话框，选择保存位置
    entry_save_path.delete(0, tk.END)  # 清空文本框内容
    entry_save_path.insert(tk.END, save_path)  # 在文本框中插入选择的保存位置

button_select_save_path = tk.Button(window, text="选择", command=select_save_path)  # 创建按钮，用于选择保存位置
button_select_save_path.pack()  # 将按钮添加到窗口

format_var = tk.StringVar()  # 创建变量，用于保存选择的保存格式
format_var.set("Text")  # 设置默认值为Text

label_format = tk.Label(window, text="请选择爬取内容的格式：")  # 创建标签，显示提示文本
label_format.pack()  # 将标签添加到窗口

format_menu = tk.OptionMenu(window, format_var, "Text", "CSV", "JSON", "XML", "Image", "Video")  # 创建下拉菜单，用于选择保存格式
format_menu.pack()  # 将下拉菜单添加到窗口

button_scrape = tk.Button(window, text="开始爬取", command=scrape_website)  # 创建按钮，用于开始爬取
button_scrape.pack()  # 将按钮添加到窗口

window.mainloop()  # 进入主循环，等待用户操作