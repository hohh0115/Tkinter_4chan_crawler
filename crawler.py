
import sys
import os
import time
import requests
from bs4 import BeautifulSoup
import tkinter as tk
import tkinter.messagebox

# from six.moves import queue as Queue
# from threading import Thread

class Crawler:

    is_cancel = False
    __thread_title_class = ''
    __file_href_class = ''
    __too_big_files = []
    __thread_number_input_name = 'resto'
    folder_forbidden_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']    # forbidden characters as a folder name

    def __init__(self, master, tar_url, save_path, max_size, process_info):
        self.__master = master
        self.__tar_url = tar_url
        self.__save_path = save_path
        self.__max_size = max_size
        self.__process_info = process_info
        self.__make_cancel_button()
        self.__input_validate()
        self.__get_started()

    def __get_started(self):
        # get page context
        html = requests.get(self.__tar_url)
        soup = BeautifulSoup(html.text, 'lxml')  # get BeautifulSoup object
        thread_title = self.list_to_string(soup.find_all('span', class_=self.__thread_title_class)[0].contents)
        thread_number = soup.find(attrs={"name": self.__thread_number_input_name}).get('value')
        # thread_number = soup.find('input', {'name': self.__thread_number_input_name})['value']
        if not thread_title:
            thread_title = 'No Title'
        thread_title = thread_number + ' ' + thread_title
        self.__save_path = self.open_dir(thread_title)

        self.insert_message_to_process_info("Sending request for " + self.__tar_url)
        self.insert_message_to_process_info("Save path is " + self.__save_path)

        all_files = soup.find_all('a', class_=self.__file_href_class)
        files_count = len(all_files)
        too_big_files_count = 0

        for i in all_files:
            if not self.is_cancel:
                file_index = all_files.index(i) + 1
                self.insert_message_to_process_info('Downloading ' + str(i['href']) + '(' + str(file_index) + ' / ' + str(files_count) + ')')
                try:
                    i_url = 'https:' + i['href']
                except:
                    self.insert_message_to_process_info('This file couldn\'t be downloaded')
                    continue
                req = requests.get(i_url)  # req.url = url
                result = self.check_file_size(req)
                if result:
                    self.download_file(req)
                else:
                    self.insert_message_to_process_info('File No.' + str(file_index) + ' exceeds maximum file size')
                    too_big_files_count += 1
                    self.__too_big_files.append(i_url)
            else:
                break

        if not self.is_cancel:
            self.insert_message_to_process_info('Download complete!')
        else:
            self.insert_message_to_process_info('Download cancel!')

        self.insert_message_to_process_info(str(too_big_files_count) + ' files exceed maximum file size: ' + '\n '.join(self.__too_big_files))

    def cancel(self):
        self.is_cancel = True

    def __make_cancel_button(self):
        cancel = tk.Button(self.__master, text="Cancel", command=self.cancel)
        cancel.place(relx=0.5, rely=0.95, anchor='s')
        cancel.update()

    def __input_validate(self):
        if not self.__tar_url or not self.__save_path or not self.__max_size:
            self.__show_error_message('No entry should be empty!')
        elif not self.__max_size.isdigit() and not self.__isfloat(self.__max_size):
            self.__show_error_message('Maximum Size Entry ONLY accept numbers')
        else:
            self.__max_size = self.__string_to_number(self.__max_size)
            if not self.__save_path.endswith("/"):
                self.__save_path = self.__save_path + '/'
            # self.__check_save_path()
            self.__check_url_belong()

    def download_file(self, req_obj):
        file_name = req_obj.url
        last_char = file_name[::-1].find("/")
        file_name = file_name[len(file_name) - last_char:]
        save_path_file_name = self.__save_path + "/" + str(file_name)
        with open(save_path_file_name, 'wb') as fh:
            fh.write(req_obj._content)

    def check_file_size(self, req_obj):
        req_file_size = self.bytesto(req_obj.headers['Content-Length'], 'm')
        if req_file_size > self.__max_size:
            return False
        return True

    def bytesto(self, bytes, to, bsize=1024):
        a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}
        r = float(bytes)
        for i in range(a[to]):
            r = r / bsize

        return (r)

    def __check_folder_forbidden_chars(self, name):
        for char in self.folder_forbidden_chars:
            if char in name:
                name = name.replace(char, '')

        return name

    def insert_message_to_process_info(self, info):
        self.__process_info.insert('end', info + '\n')
        self.__process_info.yview('end')    # make it auto scroll
        self.__process_info.update()    # insert info in each iteration

    def open_dir(self, thread_title):
        thread_title = self.__check_folder_forbidden_chars(thread_title)
        try:
            path = self.__save_path + thread_title + ' ' + self.time_string()
            if not os.path.exists(path):
                os.makedirs(path)
                return path
        except Exception as e:
            self.__show_error_message('Path Unavailable!')

    def time_string(self):
        return str(time.strftime("%y%m%d%H%M%S"))

    def __check_save_path(self):
        try:
            if not os.path.isdir(self.__save_path):
                # os.mkdir(save_path)
                os.makedirs(self.__save_path)
        except SystemError:
            self.__show_error_message('Path Unavailable!')

    def list_to_string(self, list):
        str = ''.join(list)
        return str

    def __check_url_belong(self):
        if '4chan' in self.__tar_url:
            self.__thread_title_class = 'subject'
            self.__file_href_class = 'fileThumb'
        elif 'komica' in self.__tar_url:
            self.__thread_title_class = 'title'
            self.__file_href_class = 'file-thumb'
        else:
            self.__show_error_message('Can\'t recognize the url!')

    def __isfloat(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def __string_to_number(self, str):
        try:
            return int(str)
        except ValueError:
            return float(str)

    def __show_error_message(self, message):
        tk.messagebox.showerror('Error', message)

