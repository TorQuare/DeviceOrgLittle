import json


class BaseReader:

    item_struct = {
        "next_id": {
            "name": "default",
            "time": "default",
            "work_materials": {
                "id": {
                    "id": 0,
                    "material": "default",
                    "size": "0x0",
                    "number_of": 0,
                    "cost": 0
                }
            },
            "materials": {
                "next_id": {
                    "id": 0,
                    "material": "default",
                    "size": "0x0",
                    "number_of": 0,
                    "time_for": 0
                },
            },
            "material_cost": 0,
            "sell_cost": 0,
            "production_steps": {
                "next_id": {
                    "id": 0,
                    "step": "default",
                    "time": 0
                }
            },
            "ad_info": "default"
        }
    }

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

    def return_ids(self):
        """
        Startup func.
        :return: list of ids
        """
        self.__sort_via_id()
        return sorted(self.data_dict.keys())

    def return_last_id(self):
        """
        Startup func.
        :return: int last id
        """
        return self.return_ids()[-1]

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


class ItemsWriter:

    __materials_struct = {
        "id": int,
        "material": str,
        "size": str,
        "number_of": int,
        "time_for": int
    }
    __work_materials_struct = {
        "id": int,
        "material": str,
        "size": str,
        "number_of": int,
        "cost": float
    }
    __steps_struct = {
        "id": int,
        "step": str,
        "time": int
    }
    __loaded_item = {}
    __materials_dict = {}
    __work_materials_dict = {}
    __steps_dict = {}

    def __init__(self):
        read_base = DataReader(True)
        self.json_update = UpdateJson(True)
        self.last_id = read_base.return_last_id()
        self.ids = read_base.return_ids()

    # region Public Methods

    def add_new_item(self,
                     name: str,
                     time: str,
                     material_cost: float,
                     sell_cost: float,
                     ad_info: str = None):
        """
        Adds new item to json file.
        :param str name: name
        :param str time: time
        :param float material_cost: material cost
        :param float sell_cost: prince
        :param str ad_info: additional info
        :return: Nothing
        """
        new_id = "id_" + str(int(self.last_id) + 1)
        if not ad_info:
            ad_info = "N/A"
        data = {
            "name": name,
            "time": time,
            "work_materials": self.__work_materials_dict,
            "materials": self.__materials_dict,
            "material_cost": material_cost,
            "sell_cost": sell_cost,
            "production_steps": self.__steps_dict,
            "ad_info": ad_info
        }
        self.json_update.update_json(new_id, data)

    def update_item(self,
                    json_id: int,
                    name: str = None,
                    time: str = None,
                    work_materials: dict = None,
                    materials: dict = None,
                    material_cost: float = None,
                    sell_cost: float = None,
                    production_steps: dict = None,
                    ad_info: str = None):
        return None

    # region Materials

    def add_materials(self, *data: list):
        """
        Adds all materials data from list to dict.
        :param list data: lists with material data
        :return: Nothing
        """
        for item in data:
            item.insert(0, len(self.__materials_dict))
            self.__render_temp_dict(item, self.__materials_struct)
            self.__update_materials_dict(
                len(self.__materials_dict),
                self.__render_temp_dict(item, self.__materials_struct)
            )

    def add_material(self, material: str, size: str, number_of: int, time_for: int):
        """
        Adds simple material to dict.
        :param str material: material name
        :param str size: material size
        :param int number_of: number of material
        :param int time_for: time spend on material
        :return: Nothing
        """
        temp_list = [
            len(self.__materials_dict),
            material,
            size,
            number_of,
            time_for
        ]
        self.__update_materials_dict(
            len(self.__materials_dict),
            self.__render_temp_dict(temp_list, self.__materials_struct)
        )

    # endregion
    # region Work Materials

    def add_work_materials(self, *data: list):
        """
        Adds all materials data from list to dict.
        :param list data: lists with material data
        :return: Nothing
        """
        for item in data:
            item.insert(0, len(self.__work_materials_dict))
            self.__render_temp_dict(item, self.__work_materials_struct)
            self.__update_work_materials_dict(
                len(self.__work_materials_dict),
                self.__render_temp_dict(item, self.__work_materials_struct)
            )

    def add_work_material(self, material: str, size: str, number_of: int, cost: float):
        """
        Adds simple material to dict.
        :param str material: material name
        :param str size: material size
        :param int number_of: number of material
        :param float cost: time spend on material
        :return: Nothing
        """
        temp_list = [
            len(self.__work_materials_dict),
            material,
            size,
            number_of,
            cost
        ]
        self.__update_work_materials_dict(
            len(self.__work_materials_dict),
            self.__render_temp_dict(temp_list, self.__work_materials_struct)
        )

    # endregion
    # region Steps

    def add_steps(self, *data: list):
        """
        Adds all materials data from list to dict.
        :param list data: lists with material data
        :return: Nothing
        """
        for item in data:
            item.insert(0, len(self.__steps_dict))
            self.__render_temp_dict(item, self.__steps_struct)
            self.__update_steps_dict(
                len(self.__steps_dict),
                self.__render_temp_dict(item, self.__steps_struct)
            )
        for item in data:
            self.add_step(
                item[0],
                item[1]
            )

    def add_step(self, step: str, time: int):
        """
        Adds simple step to dict.
        :param str step: step
        :param int time: time spent on step
        :return: Nothing
        """
        temp_list = [
            len(self.__steps_dict),
            step,
            time
        ]
        self.__update_steps_dict(
            len(self.__steps_dict),
            self.__render_temp_dict(temp_list, self.__steps_struct)
        )

    # endregion
    # endregion

    # region Private Methods

    # region Update dicts

    def __update_materials_dict(self, last_id: int, data: dict):
        """
        Updates materials dict.
        :param int last_id: last material ID
        :param dict data: dict with material data
        :return: Nothing
        """
        self.__materials_dict.update({str(last_id): {}})
        for key, value in data.items():
            self.__materials_dict[str(last_id)].update({key: value})

    def __update_work_materials_dict(self, last_id: int, data: dict):
        """
        Updates materials dict.
        :param int last_id: last material ID
        :param dict data: dict with material data
        :return: Nothing
        """
        self.__work_materials_dict.update({str(last_id): {}})
        for key, value in data.items():
            self.__work_materials_dict[str(last_id)].update({key: value})

    def __update_steps_dict(self, last_id: int, data: dict):
        """
        Updates materials dict.
        :param int last_id: last material ID
        :param dict data: dict with material data
        :return: Nothing
        """
        self.__steps_dict.update({str(last_id): {}})
        for key, value in data.items():
            self.__steps_dict[str(last_id)].update({key: value})

    # endregion

    @staticmethod
    def __render_temp_dict(data: list, struct: dict):
        """
        Renders a temporary dict from given data and for given struct.
        :param list data: list with material data
        :param dict struct: dict struct
        :return: dict with correlated keys and values
        """
        result = struct
        iterator = 0
        for key in struct.keys():
            result[key] = data[iterator]
            iterator += 1
        return result

    # endregion


class UpdateJson:

    __item_section_name = "Items"
    __tasks_section_name = "Tasks"
    __section_dict = dict
    __loaded_file = dict

    def __init__(self, item_type: bool):
        base = BaseReader()
        self.file_name = base.library_file_name
        base.check_exists(self.file_name)
        if item_type:
            self.section = self.__item_section_name
        if not item_type:
            self.section = self.__tasks_section_name

    def update_json(self, json_id: str, data: dict):
        """
        Rewrites json file.
        :param str json_id: new item/task id
        :param dict data: new data to update
        :return: Nothing
        """
        self.__load_json()
        with open(self.file_name, "w", encoding="utf-8") as data_file:
            self.__section_dict.update({json_id: data})
            json.dump(self.__loaded_file, data_file, ensure_ascii=False, indent=4)

    def __load_json(self):
        """
        Loads json file to class variable
        :return: Nothing
        """
        with open(self.file_name, "r", encoding="utf-8") as data_file:
            self.__loaded_file = json.load(data_file)
        self.__section_dict = self.__loaded_file[self.section]
