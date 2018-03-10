import sys
import tkinter as tk
import pickle
from crawler import Crawler

class GUIPart:

    master_window_size = '500x380'  # the window size
    label_left_margin_x = 30    # label margin left
    label_top_margin_y = 30    # label margin top
    __label_list = ['Target URL: ', 'Desired Save Path: ', 'Maximum Size (MB): ']
    entry_var_list = ['input_url', 'input_save_path', 'input_max_size']
    __pickle_var_dict = {'input_url':'', 'input_save_path':'', 'input_max_size':''}
    entry_left_margin_x = 160
    entry_input_width = 35
    entry_top_margin_y = label_top_margin_y
    process_info_box_width = 60
    process_info_box_height = 10
    __last_label_y = label_top_margin_y * (len(__label_list) + 2)

    def __init__(self, master):
        self.master = master
        master.title("4chan / Komica Crawler")
        master.geometry(self.master_window_size)

        self.set_label(master)
        self.set_input_entry(master)
        self.set_submit_btn(master)
        self.set_process_info(master)

    def set_label(self, master):
        for i in range(len(self.__label_list)):
            tk.Label(master, text=self.__label_list[i]).place(x=self.label_left_margin_x, y=self.label_top_margin_y*(i+1))

    def set_input_entry(self, master):
        try:
            with open(self.curr_script_folder() + '/user_ref.pickle', 'rb') as user_ref:
                self.__pickle_var_dict = pickle.load(user_ref)
        except:
            with open(self.curr_script_folder() + '/user_ref.pickle', 'wb') as user_ref:
                pickle.dump(self.__pickle_var_dict, user_ref)

        for i in range(len(self.entry_var_list)):
            self.entry_var_list[i] = tk.StringVar(master, value=self.__pickle_var_dict[self.entry_var_list[i]])    # so unnecessary...
            tk.Entry(master, textvariable=self.entry_var_list[i], width=self.entry_input_width).place(x=self.entry_left_margin_x, y=self.entry_top_margin_y*(i+1))

    def curr_script_folder(self):
        return sys.path[0]

    def set_submit_btn(self, master):
        tk.Button(master, text="Submit", command=self.let_crawler_work).place(x=self.label_left_margin_x, y=self.label_top_margin_y*(len(self.__label_list)+1))

    def set_process_info(self, master):
        self.process_info = tk.Listbox(master, width=self.process_info_box_width, height=self.process_info_box_height, bg='white')
        self.process_info.place(x=self.label_left_margin_x, y=self.__last_label_y)

    def let_crawler_work(self):
        # for i in range(len(self.entry_var_list)):
        # self.user_var_list[i] = self.entry_var_list[i].get()
        self.tar_url = self.entry_var_list[0].get()
        self.save_path = self.entry_var_list[1].get()
        self.max_size = self.entry_var_list[2].get()
        self.__pickle_var_dict['input_save_path'] = self.save_path    # is there any better way?
        self.__pickle_var_dict['input_max_size'] = self.max_size
        with open(self.curr_script_folder() + '/user_ref.pickle', 'wb') as user_file:
            pickle.dump(self.__pickle_var_dict, user_file)

        Crawler(self.master, self.tar_url, self.save_path, self.max_size, self.process_info)
