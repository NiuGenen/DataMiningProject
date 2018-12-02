import os
import dm_source_data as sd

# preprocessing 1

pp1_train_data_name = "pp1_train_data_old.csv"
pp1_test_data_name = "pp1_test_data_old.csv"
pp1_train_data_path = os.path.join(sd.source_data_dir, pp1_train_data_name )
pp1_test_data_path = os.path.join(sd.source_data_dir, pp1_test_data_name )

# preprocessing 2

pp2_direction_map_name = "pp2_direction_map.csv"
pp2_linkid_map_name = "pp2_linkid_map.csv"
pp2_direction_map_path = os.path.join(sd.source_data_dir, pp2_direction_map_name)
pp2_linkid_map_path = os.path.join(sd.source_data_dir, pp2_linkid_map_name )

pp2_train_data_name = "pp2_train_data_new.csv"
pp2_test_data_name = "pp2_test_data_new.csv"
pp2_train_data_path = os.path.join(sd.source_data_dir, pp2_train_data_name )
pp2_test_data_path = os.path.join(sd.source_data_dir, pp2_test_data_name )

# statistic

sta_unknown_percentage_name = "sta-linkid-unknown-percentage.csv"
sta_unknown_percentage_path = os.path.join(sd.source_data_dir, sta_unknown_percentage_name)

# preprocessing 3

pp3_train_data_folder = os.path.join(sd.source_data_dir, "pp3_train_data_linkid" )
if not os.path.exists( pp3_train_data_folder ):
    os.mkdir( pp3_train_data_folder )

pp3_test_data_folder = os.path.join(sd.source_data_dir, "pp3_test_data_linkid" )
if not os.path.exists( pp3_test_data_folder ):
    os.mkdir( pp3_test_data_folder )

pp3_train_data_name = "pp3_train_data_all.csv"
pp3_train_data_path = os.path.join(sd.source_data_dir, pp3_train_data_name )

# preprocessing 4

pp4_format_train_name = "pp4_format_train_data_all.csv"
pp4_format_train_path = os.path.join(sd.source_data_dir, pp4_format_train_name)

pp4_format_test_name = "pp4_format_test_data_all.csv"
pp4_format_test_path = os.path.join(sd.source_data_dir, pp4_format_test_name)

pp4_format_test_without_label_name = "pp4_format_test_data_without_label_all.csv"
pp4_format_test_without_label_path = os.path.join(sd.source_data_dir, pp4_format_test_without_label_name)

# training

training_module_name = "DecisionTree"
#training_module_config = "default"
#training_module_config = "entropy"
#training_module_config = "minsplitsample10"
#training_module_config = "minsplitsample20"
#training_module_config = "maxdepth30"
#training_module_config = "minsplitsample20maxdepth30"
#training_module_config = "minsamplesleaf10"
#training_module_config = "best1"
#training_module_config = "best1split"
#training_module_config = "best1splitANDtrainwithpredictresult"
training_module_config = "best2"
#raining_module_config = "best3"
training_module_suffix = ".module"

training_modules_floder_name = training_module_name + training_module_config + "Modules"
training_modules_floder_path = os.path.join(sd.source_data_dir, training_modules_floder_name)
if not os.path.exists( training_modules_floder_path ):
    os.mkdir( training_modules_floder_path )

# prediction

prediction_result_floder_name = training_module_name + training_module_config + "Result"
prediction_result_floder_path = os.path.join(sd.source_data_dir, prediction_result_floder_name)
if not os.path.exists( prediction_result_floder_path ):
    os.mkdir( prediction_result_floder_path )

# result analysis

result_real_label_floder_name = "TestDataWithLabel"
result_real_label_floder_path = os.path.join(sd.source_data_dir, result_real_label_floder_name)
if not os.path.exists( result_real_label_floder_path ):
    os.mkdir( result_real_label_floder_path )

result_analysis_name = training_module_name + training_module_config + "ResultAnalysis.csv"
result_analysis_path = os.path.join(sd.source_data_dir, result_analysis_name)
