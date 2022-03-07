#preprocess input prices

import warnings, os, time
import logging.handlers

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from pandas.core.indexing import convert_missing_indexer, convert_to_index_sliceable


from pandas import read_csv
from pandas import datetime

warnings.simplefilter(action='ignore', category=FutureWarning)
# print('hello')

os.chdir('C:\\Users\\wb558960\\OneDrive - WBG\\CCDRs LAC\\Argentina\\DeepDives\\Vaca Muerta\\')
outdir = "C:\\Users\\wb558960\\OneDrive - WBG\\CCDRs LAC\\Argentina\\DeepDives\\Vaca Muerta\\Python\\outputs\\"
indir ='C:\\Users\\wb558960\\OneDrive - WBG\\CCDRs LAC\\Argentina\\DeepDives\\Vaca Muerta\\'#

# load: 
ngfs_indices = pd.read_csv(indir+"Python\\inputs\\price_indices_ngfs.csv")

#reshape wide to long
ngfs_long=pd.melt(ngfs_indices,id_vars=['Model','Scenario','Region','Variable','Unit'],var_name='year', value_name='values')

ngfs_long['col_index'] = ngfs_long['Model']+"_"+ngfs_long['Scenario']+"_"+ngfs_long['Region']+"_"+ngfs_long['Variable']+"_"+ngfs_long['Unit']

ngfs_long = ngfs_long.pivot_table(
        values='values', 
        index=['year'], 
        columns=['Model','Scenario','Region','Variable','Unit'])
ngfs_long['new'] = ngfs_long.index.astype(str).astype(int)

ngfs_long.index = pd.to_datetime(ngfs_long.index, format='%Y')
idx = pd.date_range(ngfs_long.index.min(), ngfs_long.index.max(), freq='Y')
oidx= ngfs_long.indexf

# Reindex and interpolate with cubicspline as an example
res = ngfs_long.reindex(oidx.union(idx)).interpolate('linear')
print(res.tail())
res.to_csv(outdir+'ngfs interpolate test.csv')

poles = read_csv(indir+'Report\\POLES Data Combined\\POLES Scenarios Combined.csv')
#reshape long
poles_long=pd.melt(poles,id_vars=['Indicator','Sector','Category','Units','Subcategory','Scenario'],var_name='year', value_name='values')
print(poles_long.head())
poles_long['col_index'] = poles_long['Indicator']+"_"+poles_long['Sector']+"_"+poles_long['Category']+"_"+poles_long['Units']+"_"+poles_long['Subcategory']+"_"+poles_long['Scenario']

poles_long = poles_long.pivot_table(
        values='values', 
        index=['year'], 
        columns=['Indicator','Sector','Category','Units','Subcategory','Scenario'])
poles_long['new'] = poles_long.index.astype(str).astype(int)

poles_long.index = pd.to_datetime(poles_long.index, format='%Y')
idx = pd.date_range(poles_long.index.min(), poles_long.index.max(), freq='Y')
oidx= poles_long.index

# Reindex and interpolate with cubicspline as an example
res = poles_long.reindex(oidx.union(idx)).interpolate('linear')
print(res.tail())
res.to_csv(outdir+'poles interpolate test.csv')

#
#ngfs_price = 