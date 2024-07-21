import tkinter.ttk
from tkinter import *
import data_engine


class MainWindow:

    __item_list_label = "Lista przedmiotów"
    __task_list_label = "Lista zleceń"
    main_values = {
        __item_list_label: "1",
        __task_list_label: "2"
    }
    select_list_rad_btn_x_start_pos = 250
    select_list_rad_btn_value = 1
    tree_view_obj = None

    def __init__(self):
        config = data_engine.ConfigReader()
        config.read_main_window_config()
        self.geometry = config.return_geometry()
        self.maxsize = config.return_maxsize()
        self.minsize = config.return_minsize()
        self.title = config.return_title()

    # region Public methods

    def start_window(self):
        """
        Startup func. Creates window.
        :return: Nothing
        """
        window = Tk()
        window.geometry(self.geometry)
        window.title(self.title)

        def get_radio_value():
            """
            Activate for radio button to change lists.
            :return: Nothing
            """
            self.select_list_rad_btn_value = list_def_value.get()
            self.tree_view_obj.destroy()
            self.__create_treeview(main_frame)

        main_frame = Frame(window)
        main_frame.pack(fill=BOTH, expand=True)
        list_def_value = StringVar(main_frame, "1")
        for (text, value) in self.main_values.items():
            select_list_rad_btn = Radiobutton(main_frame,
                                              text=text,
                                              value=value,
                                              indicator=0,
                                              variable=list_def_value,
                                              command=get_radio_value)
            select_list_rad_btn.place(x=self.select_list_rad_btn_x_start_pos, y=10)
            self.select_list_rad_btn_x_start_pos += 110

        self.__create_treeview(main_frame)

        window.mainloop()

    # endregion
    # region Private methods

    # region Treeview

    def __create_treeview(self, frame):
        """
        Creates treeview with tasks/items
        :param frame: frame object
        :return: treeview object
        """
        column_settings = self.__fill_up_columns()
        tree = tkinter.ttk.Treeview(frame,
                                    columns=(column_settings[0]),
                                    show="headings",
                                    height=5)
        column_settings.remove(column_settings[0])
        for index in range(len(column_settings)):
            hash_id = "# " + str(index + 1)
            tree.column(hash_id, anchor=CENTER, stretch=NO, width=column_settings[index][1])
            tree.heading(hash_id, text=column_settings[index][0])

        full_data = self.__fill_up_treeview()
        for json_id, data in full_data["id"]:
            data = full_data["data"]
            tree.insert('',
                        'end',
                        text=json_id,
                        values=(self.__fill_up_values(json_id, data)))

        tree.place(x=15, y=50)
        self.tree_view_obj = tree

    def __fill_up_values(self, json_id, data):
        """
        Reads data from JSDN for given list (tasks or items)
        :param int json_id: ID from JSON
        :param data: data section from JSON
        :return: arr with data from JSON
        """
        if self.select_list_rad_btn_value == "1" or self.select_list_rad_btn_value == 1:
            return [
                json_id,
                data["name"],
                data["time"],
                data["material_cost"],
                data["sell_cost"],
                data["ad_info"]
            ]
        elif self.select_list_rad_btn_value == "2" or self.select_list_rad_btn_value == 2:
            return [
                json_id,
                data["item_name"],
                data["date"],
                data["s/n"],
                data["sell_cost"],
                data["ad_info"]
            ]

    def __fill_up_columns(self):
        """
        Reads selected list and returns column settings.
        :return: arr with column names and width
        """
        if self.select_list_rad_btn_value == "1" or self.select_list_rad_btn_value == 1:
            column_settings = [
                ["c1", "c2", "c3", "c4", "c5", "c6"],
                ["ID", 50],
                ["Name", 120],
                ["Time", 100],
                ["Cost", 100],
                ["Profit", 100],
                ["Ad info", 200]
            ]
        if self.select_list_rad_btn_value == "2" or self.select_list_rad_btn_value == 2:
            column_settings = [
                ["c1", "c2", "c3", "c4", "c5", "c6"],
                ["ID", 50],
                ["Item name", 120],
                ["Date", 100],
                ["S/N", 100],
                ["Profit", 100],
                ["Ad info", 200]
            ]
        return column_settings

    def __fill_up_treeview(self):
        """
        Reads selected list and data from JSON.
        :return: dict with JSON data
        """
        if self.select_list_rad_btn_value == "1" or self.select_list_rad_btn_value == 1:
            return MainWindow.__read_data(True)
        elif self.select_list_rad_btn_value == "2" or self.select_list_rad_btn_value == 2:
            return MainWindow.__read_data(False)

    @staticmethod
    def __read_data(item_type):
        """
        Fill up class task dict.
        :return: Nothing
        """
        data = data_engine.DataReader(item_type)
        return data.return_all_data()

    # endregion

    # endregion
