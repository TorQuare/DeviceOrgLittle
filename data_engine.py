import json


class BaseReader:

    backup_directory_name = "Backups"

    def __init__(self):
        self.library_file_name = "data.json"
        self.config_file_name = "config.json"

    def load_json(self, file_name: str):
        """
        Loads JSON file and returns dict.
        :param str file_name: JSON file name to load
        :return: dict from json
        """
        try:
            with open(file_name, "r", encoding="utf-8") as data_file:
                loaded_file = json.load(data_file)
            return loaded_file
        except json.JSONDecodeError:
            backup_version = self.__load_backup_file_name(file_name)
            print(f"File {file_name} is broken, load backup version {backup_version}")
            return self.load_json(backup_version)

    @classmethod
    def __load_backup_file_name(cls, file_name: str):
        from os import listdir
        names_list = []
        for file in listdir(cls.backup_directory_name):
            if file_name in file:
                names_list.append(file)
        names_list.sort()
        return cls.backup_directory_name + "/" + names_list[len(names_list) - 1]

    @staticmethod
    def __check_exists(file_name):
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
        file = base_reader.load_json(base_reader.config_file_name)
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
        self.file = base_reader.load_json(base_reader.config_file_name)

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
        self.file = base_reader.load_json(base_reader.library_file_name)
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

    __item_section_str = "Items"
    __item_struct = {
        "name": str,
        "time": str,
        "work_materials": dict,
        "materials": dict,
        "material_cost": float,
        "sell_cost": float,
        "production_steps": dict,
        "ad_info": str
    }
    __material_section_str = "materials"
    __materials_struct = {
        "id": int,
        "material": str,
        "size": str,
        "number_of": int,
        "time_for": int
    }
    __work_materials_section_str = "work_materials"
    __work_materials_struct = {
        "id": int,
        "material": str,
        "size": str,
        "number_of": int,
        "cost": float
    }
    __steps_section_str = "production_steps"
    __steps_struct = {
        "id": int,
        "step": str,
        "time": int
    }
    __default_int = 0
    __default_str = "N/A"
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

    def clean_dicts(self,
                    item_bool: bool = True,
                    materials_bool: bool = True,
                    work_materials_bool: bool = True,
                    steps_bool: bool = True):
        """
        Cleans all dicts
        :param item_bool: disables clean method
        :param materials_bool: disables clean method
        :param work_materials_bool: disables clean method
        :param steps_bool: disables clean method
        :return: Nothing
        """
        if item_bool:
            self.__loaded_item.clear()
        if materials_bool:
            self.__materials_dict.clear()
        if work_materials_bool:
            self.__work_materials_dict.clear()
        if steps_bool:
            self.__steps_dict.clear()

    def load_item(self, json_id: int):
        """
        Start up func. Loads json item to class variables.
        :param json_id: json ID
        :return: Nothing
        """
        self.__load_json_item(self.__render_json_id(json_id))

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
        new_id = self.__render_json_id(int(self.last_id) + 1)
        if not ad_info:
            ad_info = self.__check_default(str)
        data = self.__render_temp_dict(
            self.__prepare_data_list(
                name,
                time,
                self.__work_materials_dict,
                self.__materials_dict,
                material_cost,
                sell_cost,
                self.__steps_dict,
                ad_info
            ),
            self.__item_struct
        )
        self.json_update.update_json(new_id, data)
        self.clean_dicts()

    def update_item(self,
                    json_id: int,
                    name: str = None,
                    time: str = None,
                    material_cost: float = None,
                    sell_cost: float = None,
                    ad_info: str = None):
        self.load_item(json_id)
        work_materials = self.__work_materials_dict \
            if len(self.__work_materials_dict) > 0 \
            else self.__loaded_item["work_materials"]
        materials = self.__materials_dict if len(self.__materials_dict) > 0 else self.__loaded_item["materials"]
        production_steps = self.__steps_dict if len(self.__steps_dict) > 0 else self.__loaded_item["production_steps"]
        data = self.__render_temp_dict(
            self.__prepare_data_list(
                name if name else self.__loaded_item["name"],
                time if time else self.__loaded_item["time"],
                work_materials,
                materials,
                material_cost if material_cost else self.__loaded_item["material_cost"],
                sell_cost if sell_cost else self.__loaded_item["sell_cost"],
                production_steps,
                ad_info if ad_info else self.__loaded_item["ad_info"]
            ),
            self.__item_struct
        )
        self.json_update.update_json(self.__render_json_id(json_id), data)
        self.clean_dicts()

    def delete_item(self, json_id: int):
        """
        Deletes given item from json file.
        :param json_id: json ID
        :return: Nothing
        """
        self.json_update.delete_from_json(self.__render_json_id(json_id))

    # region Materials

    def add_materials(self, *data: list):
        """
        Adds all materials data from list to dict.
        :param list data: lists with material data
        :return: Nothing
        """
        for item in data:
            self.add_work_material(
                item[0],
                item[1],
                item[2],
                item[3]
            )

    def add_material(self, material: str, size: str, time_for: int, number_of: int = None):
        """
        Adds simple material to dict.
        :param str material: material name
        :param str size: material size
        :param int number_of: number of material
        :param int time_for: time spend on material
        :return: Nothing
        """
        self.__update_materials_dict(
            len(self.__materials_dict),
            self.__render_temp_dict(
                self.__prepare_data_list(
                    len(self.__materials_dict),
                    material,
                    size,
                    number_of if number_of else self.__check_default(int),
                    time_for
                ),
                self.__materials_struct)
        )

    def update_material(self,
                        json_id: int,
                        material: str = None,
                        size: str = None,
                        time_for: int = None,
                        number_of: int = None):
        """
        Updates given json id in materials dict
        :param json_id: json ID
        :param material: material name
        :param size: material size
        :param time_for: time for work with material
        :param number_of: number of materials
        :return: Nothing
        """
        material_dict = self.__load_json_section(materials_bool=True)[json_id]
        self.__update_materials_dict(
            json_id,
            self.__render_temp_dict(
                self.__prepare_data_list(
                    json_id,
                    material if material else material_dict["material"],
                    size if size else material_dict["size"],
                    time_for if time_for else material_dict["time_for"],
                    number_of if number_of else material_dict["number_of"]
                ),
                self.__materials_struct
            )
        )

    def delete_material(self, json_id: int):
        """
        Deletes given id from materials
        :param json_id: json ID
        :return: Nothing
        """
        self.__materials_dict = self.__load_json_section(materials_bool=True)
        self.__materials_dict.pop(json_id)

    # endregion
    # region Work Materials

    def add_work_materials(self, *data: list):
        """
        Adds all materials data from list to dict.
        :param list data: lists with material data
        :return: Nothing
        """
        for item in data:
            self.add_work_material(
                item[0],
                item[1],
                item[2],
                item[3]
            )

    def add_work_material(self, material: str, size: str, number_of: int = None, cost: float = None):
        """
        Adds simple material to dict.
        :param str material: material name
        :param str size: material size
        :param int number_of: number of material
        :param float cost: time spend on material
        :return: Nothing
        """
        self.__update_work_materials_dict(
            len(self.__work_materials_dict),
            self.__render_temp_dict(
                self.__prepare_data_list(
                    len(self.__work_materials_dict),
                    material,
                    size,
                    number_of if number_of else self.__check_default(int),
                    cost if cost else self.__check_default(float)
                ),
                self.__work_materials_struct)
        )

    def update_work_material(self,
                             json_id,
                             material: str = None,
                             size: str = None,
                             number_of: int = None,
                             cost: float = None):
        """
        Updates given json id in materials dict
        :param json_id: json ID
        :param material: material name
        :param size: material size
        :param cost: material cost
        :param number_of: number of materials
        :return: Nothing
        """
        work_material_dict = self.__load_json_section(work_materials_bool=True)[json_id]
        self.__update_work_materials_dict(
            json_id,
            self.__render_temp_dict(
                    self.__prepare_data_list(
                        json_id,
                        material if material else work_material_dict["material"],
                        size if size else work_material_dict["size"],
                        cost if cost else work_material_dict["cost"],
                        number_of if number_of else work_material_dict["number_of"]
                    ),
                    self.__work_materials_struct
                )
        )

    def delete_work_material(self, json_id: int):
        """
        Deletes given id from work materials
        :param json_id: json ID
        :return: Nothing
        """
        self.__work_materials_dict = self.__load_json_section(work_materials_bool=True)
        self.__work_materials_dict.pop(json_id)

    # endregion
    # region Steps

    def add_steps(self, *data: list):
        """
        Adds all materials data from list to dict.
        :param list data: lists with material data
        :return: Nothing
        """
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
        self.__update_steps_dict(
            len(self.__steps_dict),
            self.__render_temp_dict(
                self.__prepare_data_list(
                    len(self.__steps_dict),
                    step,
                    time
                ),
                self.__steps_struct)
        )

    def update_step(self, json_id, step: str = None, time: int = None):
        """
        Updates given json id in steps dict
        :param json_id: json ID
        :param step: step
        :param time: time for step
        :return: Nothing
        """
        step_dict = self.__load_json_section(steps_bool=True)[json_id]
        self.__update_steps_dict(
            json_id,
            self.__render_temp_dict(
                self.__prepare_data_list(
                    json_id,
                    step if step else step_dict["step"],
                    time if time else step_dict["time"]
                ),
                self.__steps_struct
            )
        )

    def delete_step(self, json_id: int):
        """
        Deletes given id from steps
        :param json_id: json ID
        :return: Nothing
        """
        self.__steps_dict = self.__load_json_section(steps_bool=True)
        self.__steps_dict.pop(json_id)

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

    @classmethod
    def __check_default(cls, variable):
        """
        Returns an default value for given var type.
        :param variable: variable type
        :return: default value
        """
        if variable == str:
            return cls.__default_str
        if variable == int:
            return cls.__default_int
        if variable == float:
            return cls.__default_int

    def __load_json_item(self, json_id: str):
        """
        Loads given item into class variable
        :param str json_id: item id
        :return: Nothing
        """
        base = BaseReader()
        file = base.load_json(base.library_file_name)
        self.__loaded_item = file[self.__item_section_str][json_id]

    def __load_json_section(self,
                            materials_bool: bool = False,
                            work_materials_bool: bool = False,
                            steps_bool: bool = False):
        """
        Returns loaded section from json dict.
        :param materials_bool: section selector
        :param work_materials_bool: section selector
        :param steps_bool: section selector
        :return:
        """
        section = str
        if materials_bool:
            section = self.__material_section_str
        if work_materials_bool:
            section = self.__work_materials_section_str
        if steps_bool:
            section = self.__steps_section_str
        return self.__loaded_item[section]

    @staticmethod
    def __render_json_id(json_id: int):
        """
        Generates item id writen like in json file
        :param int json_id: int value of json id
        :return: str json id
        """
        return "id_" + str(json_id)


    @staticmethod
    def __prepare_data_list(*args):
        """
        Creates list form given args
        :param args: item to add
        :return: list of given items
        """
        temp_list = []
        for item in args:
            temp_list.append(item)
        return temp_list

    # endregion


class UpdateJson:

    __item_section_name = "Items"
    __tasks_section_name = "Tasks"
    __section_dict = dict
    __loaded_file = dict

    def __init__(self, item_type: bool):
        self.base = BaseReader()
        self.file_name = self.base.library_file_name
        if item_type:
            self.section = self.__item_section_name
        if not item_type:
            self.section = self.__tasks_section_name

    def update_json(self, json_id: str, data: dict):
        """
        Rewrites json file.
        :param str json_id: item/task id
        :param dict data: new data to update
        :return: Nothing
        """
        self.__load_json()
        self.__create_backup()
        with open(self.file_name, "w", encoding="utf-8") as data_file:
            self.__section_dict.update({json_id: data})
            json.dump(self.__loaded_file, data_file, ensure_ascii=False, indent=4)

    def delete_from_json(self, json_id: str):
        """
        Deletes given json ID and rewrites json file.
        :param json_id: item/task id
        :return: Nothing
        """
        self.__load_json()
        self.__create_backup()
        with open(self.file_name, "w", encoding="utf-8") as data_file:
            self.__section_dict.pop(json_id)
            json.dump(self.__loaded_file, data_file, ensure_ascii=False, indent=4)

    def __load_json(self):
        """
        Loads json file to class variable
        :return: Nothing
        """
        self.__loaded_file = self.base.load_json(self.file_name)
        self.__section_dict = self.__loaded_file[self.section]

    @staticmethod
    def __create_backup():
        """
        Creates object and runs backup func.
        :return: Nothing
        """
        backup = BackupJson(True)
        backup.create_backup()


class BackupJson:

    from os import listdir, remove, mkdir
    __version_limit = 10
    __directory_name = str
    __path = str
    __file_name = str
    __selector = "__"
    __file = dict
    __data_type_bool = bool

    def __init__(self, data_type: bool):
        self.base = BaseReader()
        self.__file_name = self.base.library_file_name \
            if data_type else \
            self.base.config_file_name
        self.__directory_name = self.base.backup_directory_name
        self.__path = self.__directory_name + "/"
        self.__data_type_bool = data_type

    def create_backup(self):
        """
        Startup func. Creates and deletes backup files.
        :return: Nothing
        """
        self.__load_file()
        self.__check_directory()
        with open(self.__create_file_name(), "w", encoding="utf-8") as file:
            json.dump(self.__file, file, ensure_ascii=False, indent=4)
        if len(self.__check_versions()) >= self.__version_limit:
            self.__delete_last_file(
                self.__create_file_name(
                    self.__return_oldest_version()
                )
            )

    def return_last_version(self):
        """
        Returns last version found in backups folder
        :return: int last version
        """
        self.__load_file()
        all_versions = self.__check_versions()
        if len(all_versions) > 0:
            return all_versions[len(all_versions) - 1]
        else:
            return 0

    def __load_file(self):
        """
        Loads file into class variable
        :return: Nothing
        """
        self.__file = self.base.load_json(self.base.library_file_name) \
            if self.__data_type_bool else \
            self.base.load_json(self.base.config_file_name)

    def __return_oldest_version(self):
        """
        Returns oldest id found in backup folder
        :return: int oldest version
        """
        return self.__check_versions()[0]

    def __delete_last_file(self, file_name: str):
        """
        Deletes given file from directory
        :param str file_name: file name
        :return: Nothing
        """
        self.remove(file_name)

    def __check_versions(self):
        """
        Collects all files from backups
        :return: list with all versions of given file name
        """
        version_list = []
        for file in self.listdir(self.__path):
            try:
                temp_list = file.split(self.__selector)
                if temp_list[1] == self.__file_name:
                    version_list.append(int(temp_list[0]))
            except Exception:
                continue
        version_list.sort()
        return version_list

    def __create_file_name(self, version: int = None):
        """
        Generates new file name with newest version
        :return: new file name
        """
        new_version = int
        if not version:
            new_version = self.return_last_version() + 1
        if version:
            new_version = version
        file_name = str(new_version) + self.__selector + self.__file_name
        return self.__add_path(file_name)

    def __add_path(self, file_name: str):
        """
        Adds file name into path
        :param str file_name: file name
        :return: str file name with path
        """
        return self.__path + file_name

    def __check_directory(self):
        """
        Creates new directory if it doesn't exist
        :return: Nothing
        """
        try:
            self.listdir(self.__path)
        except FileNotFoundError:
            self.mkdir(self.__directory_name)



# TODO: funkcja synchro zmieniająca ID
# TODO: funkcja ładująca ostatni działający plik
