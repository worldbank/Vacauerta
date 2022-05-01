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
outdir = "C:\\Users\\wb558960\\OneDrive - WBG\\CCDRs LAC\\Argentina\\DeepDives\\Vaca Muerta\\Python\\inputs\\"
indir ='C:\\Users\\wb558960\\OneDrive - WBG\\CCDRs LAC\\Argentina\\DeepDives\\Vaca Muerta\\'#

# load: 
ngfs_indices = pd.read_csv(indir+"Python\\inputs\\price_indices_ngfs.csv")
del ngfs_indices ["Variable"]
del ngfs_indices ["Unit"]

#reshape wide to long
ngfs_long=pd.melt(ngfs_indices,id_vars=['Model','Scenario','Region','stage','type'],var_name='year', value_name='values').reset_index()

ngfs_long['col_index'] = ngfs_long['Model']+"_"+ngfs_long['Scenario']+"_"+ngfs_long['Region']+"_"+ngfs_long['stage']+"_"+ngfs_long['type']

ngfs_long = ngfs_long.pivot_table(
        values='values', 
        index=['year'], 
        columns=['col_index'])

ngfs_long['new'] = ngfs_long.index.astype(str).astype(int)

ngfs_long.index = pd.to_datetime(ngfs_long.index, format='%Y')
idx = pd.date_range(ngfs_long.index.min(), ngfs_long.index.max(), freq='Y')
oidx= ngfs_long.index

res = ngfs_long.reindex(oidx.union(idx)).interpolate('linear')
del res["new"]
# print(res.tail())
# res.to_csv(outdir+'annual interpolate tesst.csv')


#now POLES
poles = read_csv(indir+'Python\\inputs\\POLES Scenarios Combined.csv')
#reshape long
poles = poles.loc[poles['Category']=="Prices"]
poles_long=pd.melt(poles,id_vars=['Indicator','Sector','Category','Units','Subcategory','Scenario',"ID"],var_name='year', value_name='values')
poles_long['year'] = poles_long['year'].astype(str).astype(int)
poles_long = poles_long.loc[poles_long['year']>=2015]
del poles_long["Sector"]
del poles_long["Subcategory"]
del poles_long["ID"]
del poles_long["Units"]

#index values
poles_long['col_index'] = 'POLES_'+poles_long['Scenario']+'_World_Primary Energy_'+poles_long['Indicator']
index_2020 = poles_long[poles_long['year']==2020]

poles_long = poles_long.pivot_table(
        values='values', 
        index=['year'], 
        columns=['col_index'])

collist = poles_long.columns.values.tolist()

for c in collist:
    poles_long[c] = poles_long[c]/index_2020[index_2020['col_index']==c]['values'].squeeze()

poles_long.to_csv(outdir+"polestest.csv")
poles_long.index = pd.to_datetime(poles_long.index, format='%Y')
idx = pd.date_range(poles_long.index.min(), poles_long.index.max(), freq='Y')
oidx= poles_long.index

# Reindex and interpolate 
poles = poles_long.reindex(oidx.union(idx)).interpolate('linear')

#merge with ngfs and reindex to 2021
indices = pd.merge(res,poles, left_index=True, right_index=True)
indices.to_csv(outdir+"indices.csv")

my_list = indices.columns.values.tolist() 