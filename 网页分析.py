import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import threading
import http.server
import socketserver
import re

def validate_url(url):
    if not url:
        messagebox.showerror("错误", "请输入URL")
        return False
    
    if not re.match(r'^https?://\S+$', url):
        messagebox.showerror("错误", "URL格式不正确")
        return False
    
    return True

def request_and_parse(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("错误", f"请求错误：{str(e)}")
        return None
    
    html_content = response.text
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
    except Exception as e:
        messagebox.showerror("错误", f"解析错误：{str(e)}")
        return None
    
    return soup

def analyze_links(soup):
    links = soup.find_all('a')
    
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "漏洞分析结果：\n")
    for i, link in enumerate(links, start=1):
        href = link.get('href')
        if href:
            result_text.insert(tk.END, f"{i}. 链接：{href}\n")
            if re.match(r'^https?://\S+$', href):
                result_text.insert(tk.END, "   漏洞类型：链接漏洞\n")
            else:
                result_text.insert(tk.END, "   漏洞类型：无效链接\n")
            analyze_vulnerabilities_in_link(href)
        else:
            result_text.insert(tk.END, f"{i}. 这是一个无效链接\n")

def analyze_vulnerabilities_in_link(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        result_text.insert(tk.END, f"   漏洞分析失败：请求错误：{str(e)}\n")
        return
    
    html_content = response.text
    if re.search(r'<\s*script[^>]*>', html_content, re.IGNORECASE):
        result_text.insert(tk.END, "   漏洞类型：XSS攻击\n")
    if re.search(r'\'\s*or\s+\'\d+\s*=\s*\d+\'', html_content, re.IGNORECASE):
        result_text.insert(tk.END, "   漏洞类型：SQL注入\n")
    if re.search(r'(password|passwd|pwd)=', html_content, re.IGNORECASE):
        result_text.insert(tk.END, "   漏洞类型：敏感信息泄露\n")
    if re.search(r'include\s*[\(\"]', html_content, re.IGNORECASE):
        result_text.insert(tk.END, "   漏洞类型：文件包含漏洞\n")

def analyze_vulnerabilities():
    url = url_entry.get()
    if not validate_url(url):
        return
    
    threading.Thread(target=lambda: analyze_links(request_and_parse(url))).start()

def run_http_server():
    PORT = 8000
    if PORT < 1024 or PORT > 65535:
        messagebox.showerror("错误", "端口号不合法")
        return
    
    Handler = http.server.SimpleHTTPRequestHandler

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        messagebox.showerror("错误", f"HTTP服务器启动错误：{str(e)}")

window = tk.Tk()
window.title("网页漏洞分析程序")

url_label = tk.Label(window, text="请输入URL：")
url_label.pack()
url_entry = tk.Entry(window)
url_entry.pack()

analyze_button = tk.Button(window, text="开始分析", command=analyze_vulnerabilities)
analyze_button.pack()

result_text = tk.Text(window, height=10, width=50)
result_text.pack()

http_thread = threading.Thread(target=run_http_server)
http_thread.daemon = True
http_thread.start()

window.mainloop()