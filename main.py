import main_window, data_engine

#data = data_engine.DataReader(True)
#print("Main: ", data.return_all_data())

#test2 = main_window.MainWindow()
#test2.start_window()

test_write = data_engine.ItemsWriter()
"""
test_write.add_material("Drewno", "15 cm", 3, 5)
test_write.add_materials(["dr2", "55 cm", 4, 9], ["ite", "90 m", 10, 55])
test_write.add_work_material("Drewno", "15 cm", 3, 5)
test_write.add_work_materials(["dr2", "55 cm", 4, 9], ["ite", "90 m", 10, 55])
test_write.add_step("cięcie drewna", 30)
#test_write.add_steps(["ĆD", 10], ["żywica", 50])
test_write.add_new_item(
    "test",
    "3 dni",
    350,
    667.5
)
"""
#test_write.update_item(json_id=1, name="correct")
backup_test = data_engine.BackupJson(True)
print(backup_test.create_backup())
