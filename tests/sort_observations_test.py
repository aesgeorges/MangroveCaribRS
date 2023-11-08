import pytest
import re, glob
from datetime import datetime

def func(files):    
    date_pattern = r'(\d{2}-\d{2}-\d{4})' #mm-dd-yyy
    dates = [re.search(date_pattern, file).group(1) for file in files]
    dates = [datetime.strptime(date, '%m-%d-%Y') for date in dates]

    return [file for _, file in sorted(zip(dates, files))]

def test_answer():
    files = ['/global/users/timalis/datasets/Planet/GPHT/02-24-2011.tif',
    '/global/scratch/users/timalis/datasets/Planet/GPHT/12-05-2010.tif',
    '/global/scratch/users/timalis/datasets/Planet/GPHT/05-30-2017.tif']
    
    answer = ['/global/scratch/users/timalis/datasets/Planet/GPHT/12-05-2010.tif',
    '/global/users/timalis/datasets/Planet/GPHT/02-24-2011.tif',
    '/global/scratch/users/timalis/datasets/Planet/GPHT/05-30-2017.tif']

    assert func(files) == answer