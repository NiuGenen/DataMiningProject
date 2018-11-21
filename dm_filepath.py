import os
import dm_source_data as sd

pp1_train_data_name = "pp1_train_data_old.csv"
pp1_test_data_name = "pp1_test_data_old.csv"
pp1_train_data_path = os.path.join(sd.source_data_dir, pp1_train_data_name )
pp1_test_data_path = os.path.join(sd.source_data_dir, pp1_test_data_name )

pp2_direction_map_name = "pp2_direction_map.csv"
pp2_linkid_map_name = "pp2_linkid_map.csv"
pp2_direction_map_path = os.path.join(sd.source_data_dir, pp2_direction_map_name)
pp2_linkid_map_path = os.path.join(sd.source_data_dir, pp2_linkid_map_name )

pp2_train_data_name = "pp2_train_data_new.csv"
pp2_test_data_name = "pp2_test_data_new.csv"
pp2_train_data_path = os.path.join(sd.source_data_dir, pp2_train_data_name )
pp2_test_data_path = os.path.join(sd.source_data_dir, pp2_test_data_name )
