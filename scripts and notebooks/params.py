from datetime import datetime

#  Download directories for Haiti and Trinidad respectively 
DOWNLOAD_DIR_HT = 'datasets/Planet/GPHT/'
DOWNLOAD_DIR_TT = 'datasets/Planet/CRTT/'

# Shapefiles
HT_SHP = 'datasets/Shapefiles/gpbay.shp'
TT_SHP = 'datasets/Shapefiles/caroniswamp.shp'

TRAINING_LABELS_SHP = 'datasets/Shapefiles/ground_truth_test.shp'

# Image search parameters
TIME_RANGE_BEGINNING = datetime(month=1, day=1, year=2023)
TIME_RANGE_END = datetime(month=1, day=10, year=2023)

CLEAR_PERCENT = 100
VISIBLE_PERCENT = 100

# Date naming convention
PATTERN_REGEX = r'.*(\d{2}-\d{2}-\d{4}).*'

# Model Dump and Load Path
CLASSIFIER_PATH = 'models/hgb_classifier.joblib'