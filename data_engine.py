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


class ConfigReader:

    __size_data = {}
    __title = str

    def __init__(self):
        base_reader = BaseReader()
        base_reader.check_exists(base_reader.config_file_name)
        self.data_file = open(base_reader.config_file_name, encoding="utf-8")
        self.file = json.load(self.data_file)

    # region Public methods

    def read_main_window_config(self):
        """
        Startup func.
        :return: Nothing
        """
        section = self.file["MainWindow"]
        self.__read_window_size(section)
        self.__read_window_title(section)

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
