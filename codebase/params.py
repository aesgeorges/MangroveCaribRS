from datetime import datetime

mobile = False

# Directory roots
DOWNLOAD_DIR_ROOT = '/global/scratch/users/alexandregeorges/datasets/Planet/'
ROOT_SHP = 'datasets/Shapefiles/'

#  Download directories for Haiti and Trinidad respectively 
if mobile == True:
    DOWNLOAD_DIR_HT_COMP = "E:/Research/Thesis/Chapter 1 - Coastal Dynamics of Grand-Pierre Bay/datasets/Planet/GPHT/Composites/"
else:
    DOWNLOAD_DIR_HT_COMP = '/global/scratch/users/alexandregeorges/datasets/Planet/GPHT/Composites/'
DOWNLOAD_DIR_HT = '/global/scratch/users/alexandregeorges/datasets/Planet/GPHT/'
DOWNLOAD_DIR_HT_CARACOL = '/global/scratch/users/alexandregeorges/datasets/Planet/CCHT/'
DOWNLOAD_DIR_TT = '/global/scratch/users/alexandregeorges/datasets/Planet/CRTT/'

# Shapefiles
HT_SHP = '../datasets/Shapefiles/GPHT.shp'
TT_SHP = '../datasets/Shapefiles/CCHT.shp'

TRAINING_LABELS_SHP = 'datasets/Shapefiles/crtt_training.shp' #'datasets/Shapefiles/ground_truth_real.shp' #'datasets/Shapefiles/ground_truth_test.shp'

# Image search parameters
TIME_RANGE_BEGINNING = datetime(month=1, day=1, year=2010)
TIME_RANGE_END = datetime(month=6, day=1, year=2023)

CLEAR_PERCENT = 100
CLOUD_COVER_PERCENT = 5
CLOUD_COVER_RATIO = 5
VISIBLE_PERCENT = 100

SATELLITE_PRODUCT_RE = 'REOrthoTile' #'PSScene' # 
SATELLITE_PRODUCT_PS = 'PSScene'
BUNDLE = 'analytic_8b_sr_udm2' #analytic_sr #'analytic_8b_sr_udm2' # 

# Date naming convention
PATTERN_REGEX = r'.*(\d{2}-\d{2}-\d{4}).*'

# Model Dump and Load Path
CLASSIFIER_PATH = 'outputs/models/hgb_retrained.joblib' #'models/hgb_gpbay_test2.joblib'#'models/hgb_gpbay.joblib'#'models/hgb_classifier.joblib'

# Observation Datacube
OBS_PREFIX = '/global/scratch/users/alexandregeorges/datasets/Processed/'
OBSERVATION_DATA_CUBE = '/global/scratch/users/alexandregeorges/datasets/Processed/GPHT_obs_2010_2020_full.nc'
OBSERVATION_DATA_ALL = '/global/scratch/users/alexandregeorges/datasets/Processed/GPHT_obs_stragglers_1020.nc'

# Classified Datacube
CLASSIFIED_PREFIX = '/global/scratch/users/alexandregeorges/datasets/Processed/'
CLASSIFIED_DATA_CUBE = '/global/scratch/users/alexandregeorges/datasets/Processed/GPHT_classified_2010_2020.nc'
CLASSIFIED_DATA_ALL = '/global/scratch/users/alexandregeorges/datasets/Processed/GPHT_classified_stragglers_1020.nc'

# UVVR and NDVI dataframes
UVVR_DF = '../datasets/Processed/GPHT_uvvr_2010_2020.csv'
NDVI_DF = '../datasets/Processed/GPHT_ndvi_2010_2020.csv'