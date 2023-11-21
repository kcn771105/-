# Welcome to GitHub Desktop!

This is your README. READMEs are where you can communicate what your project is and how to use it.

Write your name on line 6, save it, and then head back to GitHub Desktop.
import unittest
from unittest.mock import patch
import tkinter as tk
from tkinter import messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import pachong

class TestPachong(unittest.TestCase):

    def setUp(self):
        self.window = tk.Tk()
        self.window.withdraw()
        self.pachong = pachong

    def tearDown(self):
        self.window.destroy()

    def test_validate_input_with_empty_url(self):
        result = self.pachong.validate_input("", "content", "save_path")
        self.assertFalse(result)
        messagebox.showerror.assert_called_with("错误", "请输入网址！")

    def test_validate_input_with_empty_content(self):
        result = self.pachong.validate_input("url", "", "save_path")
        self.assertFalse(result)
        messagebox.showerror.assert_called_with("错误", "请输入要爬取的内容！")

    def test_validate_input_with_empty_save_path(self):
        result = self.pachong.validate_input("url", "content", "")
        self.assertFalse(result)
        messagebox.showerror.assert_called_with("错误", "请选择保存位置！")

    def test_validate_input_with_valid_input(self):
        result = self.pachong.validate_input("url", "content", "save_path")
        self.assertTrue(result)
        messagebox.showerror.assert_not_called()

    @patch('pachong.requests.get')
    def test_scrape_website_with_valid_input(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.text = "<html><body><div>content1</div><div>content2</div></body></html>"
        mock_response.encoding = 'utf-8'
        mock_response.raise_for_status.return_value = None

        self.pachong.validate_input = lambda url, content, save_path: True
        self.pachong.save_as_text = lambda result, save_path: None

        self.pachong.scrape_website()

        mock_get.assert_called_with("url", timeout=5)
        messagebox.showinfo.assert_called_with("提示", "爬取成功！")

    @patch('pachong.requests.get')
    def test_scrape_website_with_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException()

        self.pachong.validate_input = lambda url, content, save_path: True

        self.pachong.scrape_website()

        messagebox.showerror.assert_called_with("错误", "网络请求异常：")

    @patch('pachong.requests.get')
    def test_scrape_website_with_http_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.HTTPError()

        self.pachong.validate_input = lambda url, content, save_path: True

        self.pachong.scrape_website()

        messagebox.showerror.assert_called_with("错误", "网络请求错误：")

    @patch('pachong.requests.get')
    def test_scrape_website_with_exception(self, mock_get):
        mock_get.side_effect = Exception()

        self.pachong.validate_input = lambda url, content, save_path: True

        self.pachong.scrape_website()

        messagebox.showerror.assert_called_with("错误", "发生异常：")

if __name__ == '__main__':
    unittest.main()