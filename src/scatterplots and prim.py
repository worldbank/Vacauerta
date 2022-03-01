#Scatter plots of deep uncertainty

from ema_workbench import (Model, RealParameter,CategoricalParameter, IntegerParameter, TimeSeriesOutcome, ema_logging, perform_experiments)
# from ema_workbench.connectors.excel import ExcelModel
from ema_workbench.em_framework.evaluators import MultiprocessingEvaluator
from ema_workbench.em_framework.outcomes import ArrayOutcome, ScalarOutcome
from ema_workbench.util import ema_exceptions
#from ema_workbench.analysis.plotting import lines
from ema_workbench.analysis import pairs_plotting
from ema_workbench.analysis import prim
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os 
from pandas.core.indexing import convert_missing_indexer, convert_to_index_sliceable
import os 
import warnings
from math import floor

#
indir = "C:\\Users\\wb558960\\OneDrive - WBG\\CCDRs LAC\\Argentina\\DeepDives\\Vaca Muerta\\Python\\outputs\\"
outdir ='C:\\Users\\wb558960\\OneDrive - WBG\\CCDRs LAC\\Argentina\\DeepDives\\Vaca Muerta\\Python\\outputs\\plots\\'

#load summary results from initial 

#scatterplots

#load outcomes and merge
#load experiments and merge

#join outcomes and experiments







try: 
    print('npv unconv gas')
    y = outcomes['gdp_npv_unconv_gas'] < 0.0
    prim_alg = prim.Prim(x, y, threshold=0.1)
    box1 = prim_alg.find_box() 
    box1.show_tradeoff()
    box1.inspect(8)
    box1.inspect(8, style='graph')
    box1.show_pairs_scatter(8)
    plt.savefig(outdir+'prim_npv_unconv_gas.png', bbox_inches="tight")
except: 
    print("no solutions in npv unconventional gas")

try: 
    y = outcomes['gdp_ft_unconv_gas'] < 0.0
    prim_alg = prim.Prim(x, y, threshold=0.1)
    box1 = prim_alg.find_box() 
    box1.show_tradeoff()
    box1.inspect(8)
    box1.inspect(8, style='graph')
    box1.show_pairs_scatter(8)
    plt.savefig(outdir+'prim_ft_unconv_gas.png')
except: 
    print("no solutions in ft unconventional gas")

try: 
    y = outcomes['gdp_npv_unconv_oil'] < 0.0
    prim_alg = prim.Prim(x, y, threshold=0.1)
    box1 = prim_alg.find_box() 
    box1.show_tradeoff()
    box1.inspect(8)
    box1.inspect(8, style='graph')
    box1.show_pairs_scatter(8)
    plt.savefig(outdir+'prim_npv.png', bbox_inches="tight")
except: 
    print("no solutions in npv unconventional oil")

try: 
    y = outcomes['gdp_ft_unconv_oil'] < 0.0
    prim_alg = prim.Prim(x, y, threshold=0.1)
    box1 = prim_alg.find_box() 
    box1.show_tradeoff()
    box1.inspect(8)
    box1.inspect(8, style='graph')
    box1.show_pairs_scatter(8)
    plt.savefig(outdir+'prim_ft_unconv_oil.png')
except: 
    print("no solutions in ft unconventional oil")

try: 
    y = (outcomes['gdp_ft_unconv_gas'] > 0.0) & (outcomes['gdp_npv_unconv_gas'] > 0.0)
    prim_alg = prim.Prim(x, y, threshold=0.1)
    box1 = prim_alg.find_box() 
    box1.show_tradeoff()
    box1.inspect(8)
    box1.inspect(8, style='graph')
    box1.show_pairs_scatter(8)
    plt.savefig(outdir+'prim_ft_npv_unconv_gas.png')
except: 
    print("no solutions in npv & ft unconventional gas")
    
try: 
    y = (outcomes['gdp_ft_unconv_oil'] > 0.0) & (outcomes['gdp_npv_unconv_oil'] > 0.0)
    prim_alg = prim.Prim(x, y, threshold=0.1)
    box1 = prim_alg.find_box() 
    box1.show_tradeoff()
    box1.inspect(8)
    box1.inspect(8, style='graph')
    box1.show_pairs_scatter(8)
    plt.savefig(outdir+'prim_ft_npv_unconv_oil.png')
except: 
    print("no solutions in npv & ft unconventional oil")
    
plt.show()