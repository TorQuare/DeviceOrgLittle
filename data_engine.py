import json


class BaseReader:

    def __init__(self):
        self.library_file_name = "data.json"
        self.config_file_name = "config.json"

    @staticmethod
    def check_exists(file_name):
        """
        Checks if file exists.
        :param str file_name:
        :return: True and creates file if not exists
        """
        try:
            check = open(file_name, "x")
            check.close()
        except Exception:
            return True
        return True


class TreeviewConfigReader:

    __ti_treeview = __material_treeview = __work_material_treeview = __steps_treeview = []
    __ti_section = __material_section = __work_material_section = __steps_section = None
    __section_items_str = "Items"
    __section_tasks_str = "Tasks"

    def __init__(self):
        base_reader = BaseReader()
        base_reader.check_exists(base_reader.config_file_name)
        data_file = open(base_reader.config_file_name, encoding="utf-8")
        file = json.load(data_file)
        self.file = file["MainWindowMainloopTreeview"]

    # region Public methods

    def read_tasks_data(self):
        """
        Startup func for tasks list.
        :return: Nothing
        """
        self.__define_sections(self.__section_tasks_str)
        self.__ti_treeview = self.__generate_treeview_data(self.__ti_section)

    def read_items_data(self):
        """
        Startup func for items list.
        :return: Nothing
        """
        self.__define_sections(self.__section_items_str)
        self.__ti_treeview = self.__generate_treeview_data(self.__ti_section)
        self.__material_treeview = self.__generate_treeview_data(self.__material_section)
        self.__work_material_treeview = self.__generate_treeview_data(self.__work_material_section)
        self.__steps_treeview = self.__generate_treeview_data(self.__steps_section)

    def return_ti_treeview(self):
        """
        Returns tasks/items treeview list.
        :return: arr with settings for tasks/items treeview
        """
        return self.__ti_treeview

    def return_material_treeview(self):
        """
        Returns materials treeview list.
        :return: arr with settings for materials treeview
        """
        return self.__material_treeview

    def return_work_material_treeview(self):
        """
        Returns work materials treeview list.
        :return: arr with settings for work materials treeview
        """
        return self.__work_material_treeview

    def return_steps_treeview(self):
        """
        Returns steps treeview list.
        :return: arr with settings for steps treeview
        """
        return self.__steps_treeview

    # endregion

    # region Private methods

    def __generate_treeview_data(self, section):
        """
        Generates arr with data read from JSON.
        :param dict section: dict with data needed to generate treeview.
        :return: arr of values from JSON
        """
        temp_arr = []
        temp_arr.append(self.__create_col_numbers(section["num_of_cols"]))
        temp_arr.append(section["cols"])
        temp_arr.append(section["values_to_read"])
        return temp_arr

    @staticmethod
    def __create_col_numbers(num_of_cols: int):
        """
        Generate list with number of columns.
        :param int num_of_cols: numbers of columns read from JSON
        :return: string arr with numbers of columns
        """
        temp_arr = []
        for iterator in range(num_of_cols):
           temp_arr.append("c" + str(iterator + 1))
        return temp_arr

    def __define_sections(self, section):
        """
        Prepares sections reading from JSON.
        :param str section: name of JSON section to read
        :return: Nothing
        """
        file = self.file[section]
        self.__ti_section = file["ti_treeview"]
        if section == self.__section_items_str:
            self.__material_section = file["material_treeview"]
            self.__work_material_section = file["work_material_treeview"]
            self.__steps_section = file["steps_treeview"]

    # endregion


class WindowConfigReader:

    __size_data = {}
    __title = str
    __window_section = __mainloop_section = None

    def __init__(self):
        base_reader = BaseReader()
        base_reader.check_exists(base_reader.config_file_name)
        self.data_file = open(base_reader.config_file_name, encoding="utf-8")
        self.file = json.load(self.data_file)

    # region Public methods

    # region MainWindowMainloop

    def return_ti_list_height(self):
        """
        Returns tasks/item list height
        :return: int height of list
        """
        return self.__mainloop_section["ti_list_height"]

    def return_material_list_height(self):
        """
        Returns material list height
        :return: int height of list
        """
        return self.__mainloop_section["item_material_list_height"]

    def return_work_material_list_height(self):
        """
        Returns work material list height
        :return: int height of list
        """
        return self.__mainloop_section["item_work_material_list_height"]

    def return_steps_list_height(self):
        """
        Returns steps list height
        :return: int height of list
        """
        return self.__mainloop_section["steps_list_height"]

    def return_default_view(self):
        """
        Returns default view setting
        :return: str of default view
        """
        return self.__mainloop_section["default_main_view"]

    # endregion

    # region MainWindow
    def read_main_window_config(self):
        """
        Startup func.
        :return: Nothing
        """
        self.__window_section = self.file["MainWindow"]
        self.__mainloop_section = self.file["MainWindowMainloop"]
        self.__read_window_size(self.__window_section)
        self.__read_window_title(self.__window_section)

    def return_geometry(self):
        """
        Returns window geometry
        :return: str window geometry
        """
        return self.__size_data["geometry"]

    def return_minsize(self):
        """
        Returns window minsize.
        :return: arr window minsize
        """
        temp_arr = []
        temp_arr.append(self.__size_data["minsize_height"])
        temp_arr.append(self.__size_data["minsize_width"])
        return temp_arr

    def return_maxsize(self):
        """
        Returns window maxsize.
        :return: arr window maxsize
        """
        temp_arr = []
        temp_arr.append(self.__size_data["maxsize_height"])
        temp_arr.append(self.__size_data["maxsize_width"])
        return temp_arr

    def return_title(self):
        """
        Returns title.
        :return: str window title
        """
        return self.__title

    # endregion

    # endregion
    # region Private methods

    def __read_window_size(self, data):
        """
        Reads data from JSON and prepared section.
        :param data: prepared section from JSON
        :return: Fill up class variable
        """
        self.__size_data = data["size"]

    def __read_window_title(self, data):
        """
        Reads data from JSON and prepared section.
        :param data: prepared section from JSON
        :return: Fill up class variable
        """
        self.__title = data["title"]

    def __clear_dicts(self):
        """
        Clears class dicts.
        :return: Nothing
        """
        self.__size_data.clear()

    # endregion


class DataReader:

    data_dict = {}
    __id_name = "id"
    __data_name = "data"
    __item_type = "Items"
    __task_type = "Tasks"

    def __init__(self, item_type: bool):
        base_reader = BaseReader()
        base_reader.check_exists(base_reader.library_file_name)
        self.data_file = open(base_reader.library_file_name, encoding="utf-8")
        self.file = json.load(self.data_file)
        if item_type:
            self.__dict = self.file[self.__item_type]
        else:
            self.__dict = self.file[self.__task_type]

    # region Public methods

    def return_all_data(self):
        """
        Startup func.
        :return: dict with all task/items
        """
        self.__sort_via_id()
        return self.data_dict

    def return_data_dict(self, item_id):
        """
        Startup func.
        :param int item_id: task/item id
        :return: dict data for given task/item
        """
        dict_id = "id_" + str(item_id)
        return self.__dict[dict_id]

    # endregion
    # region Private methods

    def __sort_via_id(self):
        """
        Collect all data from JSON sorted by ID.
        :return: Nothing
        """
        self.__clean_dicts()
        for item in self.__dict:
            self.data_dict.update({self.__get_id(item): self.__dict[item]})

    @staticmethod
    def __get_id(json_id: str):
        """
        Changes JSON id data into int.
        :param str json_id:
        :return: int item/task id
        """
        result = json_id.split("_")
        return result[1]

    def __clean_dicts(self):
        """
        Clears class dicts.
        :return: Nothing
        """
        self.data_dict.clear()

    # endregion
