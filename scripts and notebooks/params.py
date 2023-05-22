from datetime import datetime

mobile = True

#  Download directories for Haiti and Trinidad respectively 
if mobile == True:
    DOWNLOAD_DIR_HT = "E:/Research/Thesis/Chapter 1 - Coastal Dynamics of Grand-Pierre Bay/datasets/Planet/GPHT/Composites/"
else:
    DOWNLOAD_DIR_HT = 'datasets/Planet/GPHT/Composites/'
DOWNLOAD_DIR_TT = 'datasets/Planet/CRTT/'

# Shapefiles
HT_SHP = 'datasets/Shapefiles/gpbay.shp'
TT_SHP = 'datasets/Shapefiles/caroniswamp.shp'

TRAINING_LABELS_SHP = 'datasets/Shapefiles/training_gp_mangrove_v2.shp' #'datasets/Shapefiles/ground_truth_test.shp'

# Image search parameters
TIME_RANGE_BEGINNING = datetime(month=1, day=1, year=2011)
TIME_RANGE_END = datetime(month=1, day=1, year=2012)

CLEAR_PERCENT = 100
CLOUD_COVER = 0 
VISIBLE_PERCENT = 100

SATELLITE_PRODUCT = 'PSScene' # 'REOrthoTile' 
BUNDLE = 'analytic_8b_sr_udm2' # 'analytic_sr' 

# Date naming convention
PATTERN_REGEX = r'.*(\d{2}-\d{2}-\d{4}).*'

# Model Dump and Load Path
CLASSIFIER_PATH = 'models/hgb_gpbay_test2.joblib'#'models/hgb_classifier.joblib'