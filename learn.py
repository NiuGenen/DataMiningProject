import sklearn.tree as tree
import dm_csv as dmcsv
import pandas as pd
import dm_filepath as dmfp
import os

if os.path.exists( dmfp.result_analysis_path ):
    print(dmfp.result_analysis_path )

if os.path.exists( dmfp.prediction_result_floder_path ):
    print( dmfp.prediction_result_floder_path )