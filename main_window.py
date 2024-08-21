import tkinter
import tkinter.ttk
from tkinter import *
import data_engine


class MainWindowMainloopDetailSettings:

    # Struct columns, column_settings, json_data, treeview_values_to_read
    __work_material_settings = __material_settings = __steps_settings = []

    def __init__(self, item_type, item_id):
        reader = data_engine.TreeviewConfigReader()
        self.reader = reader.read_items_data()
        self.item_id = item_id
        self.item_type = item_type
        self.work_material_data = reader.return_work_material_treeview()
        self.material_data = reader.return_material_treeview()
        self.steps_data = reader.return_steps_treeview()

    def return_work_material_treeview_settings(self):
        return self.__prepare_treeview_settings(self.work_material_data, "work_materials")

    def return_material_treeview_settings(self):
        return self.__prepare_treeview_settings(self.material_data, "materials")

    def return_steps_treeview_settings(self):
        return self.__prepare_treeview_settings(self.steps_data, "production_steps")

    def __prepare_treeview_settings(self, data, data_type: str):
        """
        Prepares settings for treeview in mainloop.
        :param data: Given treeview array.
        :param data_type: name of section from JSON
        :return: arr with treeview settings
        """
        temp_arr = []
        temp_arr.clear()
        temp_arr.append(data[0])
        temp_arr.append(data[1])
        temp_arr.append(self.__read_data()[data_type])
        temp_arr.append(self.__fill_up_treeview_values(self.__read_data()[data_type], data[2]))
        return temp_arr

    @staticmethod
    def __fill_up_treeview_values(read_data, treeview_data):
        """
        Generates 2-D array with values form JSON
        :param dict read_data: data read from JSON
        :param treeview_data: Given treeview array.
        :return: 2-D array with values from JSON
        """
        result = []
        for json_id, data in read_data.items():
            temp_arr = []
            for key in treeview_data:
                temp_arr.append(data[key])
            result.append(temp_arr)
        return result

    def __read_data(self):
        """
        Fill up class task dict.
        :return: Nothing
        """
        data = data_engine.DataReader(self.item_type)
        return data.return_data_dict(self.item_id)


class MainWindowMainloopTISettings:

    # Struct columns, column_settings, json_data, treeview_values_to_read
    __settings = []

    def __init__(self, item_type: bool):
        reader = data_engine.TreeviewConfigReader()
        self.item_type = item_type
        if item_type:
            reader.read_items_data()
        if not item_type:
            reader.read_tasks_data()
        self.columns = reader.return_ti_treeview()[0]
        self.column_settings = reader.return_ti_treeview()[1]
        self.treeview_values_to_read = reader.return_ti_treeview()[2]

    def return_treeview_settings(self):
        """
        Startup func.
        :return: arr with treeview settings
        """
        self.__prepare_treeview_settings()
        return self.__settings

    def __prepare_treeview_settings(self):
        """
        Prepares settings for treeview in mainloop.
        :return: Nothing
        """
        self.__settings.clear()
        self.__settings.append(self.columns)
        self.__settings.append(self.column_settings)
        self.__settings.append(self.__read_data())
        self.__settings.append(self.__fill_up_treeview_values(self.__read_data()))

    def __fill_up_treeview_values(self, read_data):
        """
        Generates 2-D array with values form JSON
        :param dict read_data: data read from JSON
        :return: 2-D array with values from JSON
        """
        result = []
        for json_id, data in read_data.items():
            temp_arr = []
            temp_arr.append(json_id)
            for key in self.treeview_values_to_read:
                temp_arr.append(data[key])
            result.append(temp_arr)
        return result

    def __read_data(self):
        """
        Fill up class task dict.
        :return: Nothing
        """
        data = data_engine.DataReader(self.item_type)
        return data.return_all_data()


class ItemsEngine:

    def __init__(self):
        self.editor = data_engine.ItemsWriter()

    def del_methods(self,
                    json_id: int,
                    inner_id: int = None,
                    item_bool: bool = False,
                    material_bool: bool = False,
                    work_material_bool: bool = False,
                    step_bool: bool = False):
        if not json_id:
            return None
        if item_bool:
            self.editor.delete_item(json_id)
        else:
            self.editor.load_item(json_id)
        if material_bool:
            self.editor.delete_material(inner_id)
        if work_material_bool:
            self.editor.delete_work_material(inner_id)
        if step_bool:
            self.editor.delete_step(inner_id)


class MainWindow:

    __item_list_label = "Lista przedmiotów"
    __task_list_label = "Lista zleceń"
    __mainloop_main_treeview_selection = __mainloop_materials_treeview_selection = \
        __mainloop_work_materials_treeview_selection = __mainloop_steps_treeview_selection = None
    main_values = {
        __item_list_label: "1",
        __task_list_label: "2"
    }
    select_list_rad_btn_x_start_pos = 250
    treeview_ti_obj = treeview_materials_obj = treeview_work_materials_obj = treeview_steps_obj = None
    treeview_materials_label = treeview_work_materials_label = treeview_steps_label = None
    add_btn_materials_obj = del_btn_materials_obj = edit_btn_materials_obj = None
    add_btn_work_materials_obj = del_btn_work_materials_obj = edit_btn_work_materials_obj = None
    add_btn_steps_obj = del_btn_steps_obj = edit_btn_steps_obj = None

    def __init__(self):
        # region Construct config
        config = data_engine.WindowConfigReader()
        config.read_main_window_config()
        self.geometry = config.return_geometry()
        self.maxsize = config.return_maxsize()
        self.minsize = config.return_minsize()
        self.title = config.return_title()
        self.ti_list_height = config.return_ti_list_height()
        self.item_material_height = config.return_material_list_height()
        self.item_work_material_height = config.return_work_material_list_height()
        self.steps_height = config.return_steps_list_height()
        if config.return_default_view() == "Items":
            self.select_list_rad_btn_value = 1
        elif config.return_default_view() == "Tasks":
            self.select_list_rad_btn_value = 2
        # endregion
        self.item_engine = ItemsEngine()

    # region Public methods

    def start_window(self):
        """
        Startup func. Creates window.
        :return: Nothing
        """
        window = Tk()
        window.geometry(self.geometry)
        window.title(self.title)

        # region Mainloop methods

        def get_radio_value_mainloop():
            """
            Activate for radio button to change lists.
            :return: Nothing
            """
            self.select_list_rad_btn_value = list_def_value.get()
            generate_ti_view_mainloop()
            generate_details_view_mainloop()

        def generate_ti_view_mainloop():
            """
            Generates tasks/items treeview.
            :return: Nothing
            """
            if self.treeview_ti_obj:
                self.treeview_ti_obj.destroy()
            if self.select_list_rad_btn_value == "1" or self.select_list_rad_btn_value == 1:
                create_treeview_main_mainloop(True)
            if self.select_list_rad_btn_value == "2" or self.select_list_rad_btn_value == 2:
                create_treeview_main_mainloop(False)
            generate_details_view_mainloop()

        def create_treeview_main_mainloop(item_type: bool):
            """
            Creates treeview element in mainloop.
            :return: Nothing
            """
            if item_type:
                self.__create_treeview_main(main_frame, item_type)
                self.treeview_ti_obj.bind('<Button-1>', read_ti_treeview)

        def generate_details_view_mainloop():
            destroy_treeview_details()
            if self.__mainloop_main_treeview_selection:
                selected_id = self.__mainloop_main_treeview_selection
            else:
                selected_id = 0
                self.__mainloop_main_treeview_selection = selected_id
                # TODO: zmienić na 1
            if self.select_list_rad_btn_value == "1" or self.select_list_rad_btn_value == 1:
                self.__generate_item_details_view(main_frame, selected_id)
                self.treeview_materials_obj.bind('<Button-1>',
                                                 lambda event: read_details_treeview(event, materials_treeview=True))
                self.treeview_work_materials_obj.bind('<Button-1>',
                                                      lambda event: read_details_treeview(event,
                                                                                          work_materials_treeview=True
                                                                                          )
                                                      )
                self.treeview_steps_obj.bind('<Button-1>',
                                             lambda event: read_details_treeview(event,
                                                                                 steps_treeview=True
                                                                                 )
                                             )
            if self.select_list_rad_btn_value == "2" or self.select_list_rad_btn_value == 2:
                print("Tasks")

        def read_ti_treeview(event):
            """
            Reads which item is selected form tasks/items treeview
            :param event: binded event
            :return: Nothing
            """
            rowid = self.treeview_ti_obj.identify_row(event.y)
            item = self.treeview_ti_obj.item(rowid)
            if item["text"] == '':
                item = self.treeview_ti_obj.item(self.treeview_ti_obj.focus())["text"]
            else:
                item = item["text"]
            self.__mainloop_main_treeview_selection = item
            generate_details_view_mainloop()

        def read_details_treeview(event,
                                  materials_treeview: bool = False,
                                  work_materials_treeview: bool = False,
                                  steps_treeview: bool = False):
            """
            Reads which item is selected form details treeview
            :param event: binded event
            :param materials_treeview: selector
            :param work_materials_treeview: selector
            :param steps_treeview: selector
            :return: Nothing
            """
            print(self.__mainloop_main_treeview_selection)
            if materials_treeview:
                tree_obj = self.treeview_materials_obj
            if work_materials_treeview:
                tree_obj = self.treeview_work_materials_obj
            if steps_treeview:
                tree_obj = self.treeview_steps_obj
            rowid = tree_obj.identify_row(event.y)
            item = tree_obj.item(rowid)
            if item["text"] == '':
                item = tree_obj.item(tree_obj.focus())["text"]
            else:
                item = item["text"]
            if materials_treeview:
                self.__mainloop_materials_treeview_selection = item
            if work_materials_treeview:
                self.__mainloop_work_materials_treeview_selection = item
            if steps_treeview:
                self.__mainloop_steps_treeview_selection = item

        def destroy_treeview_details():
            """
            Destroys old treeview details form mainloop.
            :return: Nothing
            """
            if self.treeview_materials_obj:
                self.treeview_materials_obj.destroy()
                self.treeview_materials_label.destroy()
            if self.treeview_work_materials_obj:
                self.treeview_work_materials_obj.destroy()
                self.treeview_work_materials_label.destroy()
            if self.treeview_steps_obj:
                self.treeview_steps_obj.destroy()
                self.treeview_steps_label.destroy()

        # endregion

        main_frame = Frame(window)
        main_frame.pack(fill=BOTH, expand=True)
        list_def_value = StringVar(main_frame, str(self.select_list_rad_btn_value))
        for (text, value) in self.main_values.items():
            select_list_rad_btn = Radiobutton(main_frame,
                                              text=text,
                                              value=value,
                                              indicatoron=False,
                                              variable=list_def_value,
                                              command=get_radio_value_mainloop)
            select_list_rad_btn.place(x=self.select_list_rad_btn_x_start_pos, y=10)
            self.select_list_rad_btn_x_start_pos += 110

        add_item_btn = Button(main_frame, text="+", width=2, background="lightgray")
        delete_item_button = Button(main_frame, text="-", width=2, background="lightgray")
        add_item_btn.place(x=625, y=10)
        delete_item_button.place(x=650, y=10)
        generate_ti_view_mainloop()

        window.mainloop()

    # endregion
    # region Private methods

    # region Item view

    def __generate_item_details_view(self, frame, item_id):
        self.__create_treeview_details(frame, item_id)
        self.__create_treeview_labels(frame)
        self.__create_btn_items(frame, item_id)

    def __create_btn_items(self, frame, item_id):
        material_btns_list = self.__create_btn_items_generic(frame,
                                                             item_id,
                                                 [515, 215],
                                                             material_bool=True)
        self.add_btn_materials_obj = material_btns_list[0]
        self.del_btn_materials_obj = material_btns_list[1]
        self.edit_btn_materials_obj = material_btns_list[2]

    def __create_treeview_labels(self, frame):
        # TODO: przeliczyć i dopisać uwzględnienie wysokości treeview
        start_position = 178
        result = []
        label_list = ["Materials", "Work Materials", "Steps list"]
        for label_data in label_list:
            text_var = StringVar()
            text_var.set(label_data)
            label = tkinter.Label(frame, textvariable=text_var)
            label.place(x=20, y=start_position)
            start_position += 150
            result.append(label)
        self.treeview_materials_label = result[0]
        self.treeview_work_materials_label = result[1]
        self.treeview_steps_label = result[2]

    def __create_treeview_details(self, frame, item_id):
        """
        Creates treeview with materials
        :param frame: frame object
        :param int item_id: selected item id
        :return: treeview object
        """
        setting_obj = MainWindowMainloopDetailSettings(True, item_id)
        mainloop_obj_list = []
        details_commands_list = [
            setting_obj.return_material_treeview_settings(),
            setting_obj.return_work_material_treeview_settings(),
            setting_obj.return_steps_treeview_settings()
        ]
        mainloop_obj_heights = [
            self.item_material_height,
            self.item_work_material_height,
            self.steps_height
        ]
        start_position = 200
        for iterator in range(len(details_commands_list)):
            tree = self.__create_treeview_generic(
                frame,
                mainloop_obj_heights[iterator],
                details_commands_list[iterator]
            )
            tree.place(x=15, y=start_position)
            mainloop_obj_list.append(tree)
            start_position += 150

        self.treeview_materials_obj = mainloop_obj_list[0]
        self.treeview_work_materials_obj = mainloop_obj_list[1]
        self.treeview_steps_obj = mainloop_obj_list[2]

    def __create_btn_items_generic(self,
                                   frame,
                                   item_id: int,
                                   btn_position: list,
                                   material_bool: bool = False,
                                   work_material_bool: bool = False,
                                   steps_bool: bool = False):
        name_list = ["Add", "Remove", "Edit"]
        command_list = []
        if material_bool:
            command_list = [self.__add_material,
                            lambda: self.item_engine.del_methods(
                                item_id,
                                inner_id=self.__mainloop_materials_treeview_selection,
                                material_bool=True
                            ),
                            self.__edit_material]
        if work_material_bool:
            command_list = [self.add_work_material, self.del_work_material, self.edit_work_material]
        if steps_bool:
            command_list = [self.add_step, self.del_step, self.edit_step]
        btn_obj_list = []
        command_iterator = 0
        for name in name_list:
            btn = tkinter.ttk.Button(frame,
                                     text=name,
                                     command=command_list[command_iterator])
            btn.place(x=btn_position[0], y=btn_position[1])
            btn_position[1] += 33
            btn_obj_list.append(btn)
            command_iterator += 1
        return btn_obj_list

    # endregion

    def __add_material(self):
        return None

    def __edit_material(self):
        return None

    def __create_treeview_main(self, frame, item_type: bool):
        """
        Creates treeview with tasks/items
        :param frame: frame object
        :return: treeview object
        """
        settings_obj = MainWindowMainloopTISettings(item_type)
        settings = settings_obj.return_treeview_settings()
        tree = self.__create_treeview_generic(frame, self.ti_list_height, settings)
        tree.bind('<Double-1>', self.__treeview_dobule_event)
        tree.place(x=15, y=50)
        self.treeview_ti_obj = tree

    @staticmethod
    def __create_treeview_generic(frame, treeview_height: int, settings):
        """
        Creates treeview object
        :param frame: frame object
        :param int treeview_height: Given treeview height
        :param settings: arr with setting needed to create object
        :return: treeview object
        """
        tree = tkinter.ttk.Treeview(frame,
                                    columns=(settings[0]),
                                    show="headings",
                                    height=treeview_height)
        column_settings = settings[1]
        for index in range(len(column_settings)):
            hash_id = "# " + str(index + 1)
            tree.column(hash_id, anchor=CENTER, stretch=NO, width=int(column_settings[index][1]))
            tree.heading(hash_id, text=column_settings[index][0])

        full_data = settings[2]
        iterator = 0
        for json_id, data in full_data.items():
            tree.insert('',
                        'end',
                        text=json_id,
                        values=(settings[3][iterator]))
            iterator += 1

        return tree

    def __treeview_dobule_event(self, event):
        print("edit window", event)

    # endregion


