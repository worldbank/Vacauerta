#comparison graphs-post process
#run after rdm_well_closure'

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

#load phsyical flows
exports_lock = pd.read_csv(indir+"exports_1.5_lock in.csv")
exports_pess = pd.read_csv(indir+"exports_CURR_pessimistic.csv")
exports_1_5 = pd.read_csv(indir+"exports_1.5_optimistic.csv")

#load fiscal data 
fiscal_lock = pd.read_csv(indir+"fiscal_1.5_lock in.csv")
fiscal_lock['import subsidy'] = -1*fiscal_lock['import subsidy'] 
fiscal_lock = fiscal_lock.pivot_table(index="year", 
                    columns=['well_type','product'], 
                    values=['price','ds_capex','opex','domestic revenue','export revenue','production subsidy','import subsidy','royalties','export duties','us_capex','starts','trade balance'])

fiscal_pess = pd.read_csv(indir+"fiscal_CURR_pessimistic.csv")
fiscal_pess['import subsidy'] = -1*fiscal_pess['import subsidy'] 
fiscal_pess = fiscal_pess.pivot_table(index="year", 
                    columns=['well_type','product'], 
                    values=['price','ds_capex','opex','domestic revenue','export revenue','production subsidy','import subsidy','royalties','export duties','us_capex','starts', 'trade balance'])

fiscal_1_5 = pd.read_csv(indir+"fiscal_1.5_optimistic.csv")
fiscal_1_5['import subsidy'] = -1*fiscal_1_5['import subsidy'] 
fiscal_1_5 = fiscal_1_5.pivot_table(index="year", 
                    columns=['well_type','product'], 
                    values=['price','ds_capex','opex','domestic revenue','export revenue','production subsidy','import subsidy','royalties','export duties','us_capex','starts', 'trade balance'])



#df.loc[:, ("bar", "one")]
# df.xs(("one", "bar"), level=("second", "first"), axis=1)

#load physical data and make lineplots of oil and gas production, oil and gas consumption, net exports, net imports, and surplus

#across scenarios
#lineplot for gas production
# create data
def lineplot_comparison(x_axis, pess_sce,opt_sce,lock_sce,title):
    plt.plot(x_axis, pess_sce, label = "Current Policy")
    plt.plot(x_axis, opt_sce, label = "1.5 Degrees")
    plt.plot(x_axis, lock_sce, label = "Lock in Risk")
    plt.title(title)
    plt.legend(loc='upper right')
    plt.savefig(outdir+'{}.png'.format(title))
    plt.show()
    plt.clf()

def lineplot_4_comparison(x_axis, prod,cons,exports,title):
    plt.plot(x_axis, prod, label = "Production", color = 'goldenrod')
    plt.plot(x_axis, cons, label = "Consumption", color = 'magenta')
    plt.plot(x_axis, exports, label = "Net Exports", color = 'darkgreen')
    plt.title(title)
    plt.legend(loc='upper right')
    plt.savefig(outdir+'{}.png'.format(title))
    plt.show()
    plt.clf()

def lineplot_comparison2(x_axis, pess_sce,opt_sce,lock_sce,title):
    plt.plot(x_axis, pess_sce, label = "Royalties and Ex. Duties")
    plt.plot(x_axis, opt_sce, label = "Prod. and Import Subsidies")
    plt.plot(x_axis, lock_sce, label = "Investments")
    plt.title(title)
    plt.legend(loc='upper right')
    plt.savefig(outdir+'{}.png'.format(title))
    plt.show()
    plt.clf()
    

#replica of excel graph: production, consumption, imports,expo
# rts for oil and gas
lineplot_4_comparison(exports_pess["year"], exports_pess["Gas_prod"]/1000,exports_pess["gas_cons"]/1000,exports_pess["im_ex_Oil"]/1000,"Current Policies Gas Production, Consumption, Trade")
lineplot_4_comparison(exports_1_5["year"], exports_1_5["Gas_prod"]/1000,exports_1_5["gas_cons"]/1000,exports_1_5["im_ex_Oil"]/1000,"Coordinated Net Zero Gas Production, Consumption, Trade")
lineplot_4_comparison(exports_lock["year"], exports_lock["Gas_prod"]/1000,exports_lock["gas_cons"]/1000,exports_lock["im_ex_Oil"]/1000,"Lock In Risk Gas Production, Consumption, Trade")

lineplot_4_comparison(exports_pess["year"], exports_pess["Oil_prod"]/1000,exports_pess["oil_cons"]/1000,exports_pess["im_ex_Oil"]/1000,"Current Policies Oil Production, Consumption, Trade")
lineplot_4_comparison(exports_1_5["year"], exports_1_5["Oil_prod"]/1000,exports_1_5["oil_cons"]/1000,exports_1_5["im_ex_Oil"]/1000,"Coordinated Net Zero Oil Production, Consumption, Trade")
lineplot_4_comparison(exports_lock["year"], exports_lock["Oil_prod"]/1000,exports_lock["oil_cons"]/1000,exports_lock["im_ex_Oil"]/1000,"Lock In Risk Oil Production, Consumption, Trade")


#production
lineplot_comparison(exports_pess["year"],exports_pess["Gas_prod"]/1000,exports_1_5["Gas_prod"]/1000,exports_lock["Gas_prod"]/1000,"Gas Production (Ktoe)")
lineplot_comparison(exports_pess["year"],exports_pess["Oil_prod"]/1000,exports_1_5["Oil_prod"]/1000,exports_lock["Oil_prod"]/1000,"Oil Production (Ktoe)")

#consumption
lineplot_comparison(exports_pess["year"],exports_pess["total_cons"]/1000,exports_1_5["total_cons"]/1000,exports_lock["total_cons"]/1000,"Total Consumption (Ktoe)")
lineplot_comparison(exports_pess["year"],exports_pess["gas_cons"]/1000,exports_1_5["gas_cons"]/1000,exports_lock["gas_cons"]/1000,"Gas Consumption (Ktoe)")
lineplot_comparison(exports_pess["year"],exports_pess["oil_cons"]/1000,exports_1_5["oil_cons"]/1000,exports_lock["oil_cons"]/1000,"Oil Consumption (Ktoe)")
lineplot_comparison(exports_pess["year"],exports_pess["electricity_cons"]/1000,exports_1_5["electricity_cons"]/1000,exports_lock["electricity_cons"]/1000,"Electricity Consumption (Ktoe)")

#imports
lineplot_comparison(exports_pess["year"],exports_pess["net_imports_Gas"]/1000,exports_1_5["net_imports_Gas"]/1000,exports_lock["net_imports_Gas"]/1000,"Gas Imports (Ktoe)")
lineplot_comparison(exports_pess["year"],exports_pess["net_imports_Oil"]/1000,exports_1_5["net_imports_Oil"]/1000,exports_lock["net_imports_Oil"]/1000,"Oil Imports (Ktoe)")

#exports
lineplot_comparison(exports_pess["year"],exports_pess["net_exports_Gas"]/1000,exports_1_5["net_exports_Gas"]/1000,exports_lock["net_exports_Gas"]/1000,"Gas Exports (Ktoe)")
lineplot_comparison(exports_pess["year"],exports_pess["net_exports_Oil"]/1000,exports_1_5["net_exports_Oil"]/1000,exports_lock["net_exports_Oil"]/1000,"Oil Exports (Ktoe)")
lineplot_comparison(exports_pess["year"],exports_pess["net_exports_El"]/1000,exports_1_5["net_exports_El"]/1000,exports_lock["net_exports_El"]/1000,"Electricity Exports (Ktoe)")

#surplus
lineplot_comparison(exports_pess["year"],exports_pess["surplus_Gas"]/1000,exports_1_5["surplus_Gas"]/1000,exports_lock["surplus_Gas"]/1000,"Gas Surplus (Ktoe)")
lineplot_comparison(exports_pess["year"],exports_pess["surplus_Oil"]/1000,exports_1_5["surplus_Oil"]/1000,exports_lock["surplus_Oil"]/1000,"Oil Surplus (Ktoe)")

#trade balance -physical flows
net_trade_gas_pess = exports_pess["net_exports_Gas"] + exports_pess["net_imports_Gas"]
net_trade_gas_lock = exports_lock["net_exports_Gas"] + exports_lock["net_imports_Gas"]
net_trade_gas_1_5 = exports_1_5["net_exports_Gas"] + exports_1_5["net_imports_Gas"]
lineplot_comparison(exports_pess["year"],net_trade_gas_pess,net_trade_gas_1_5,net_trade_gas_lock,"Net exports Gas (ktoe)")

net_trade_oil_pess = exports_pess["net_exports_Oil"] + exports_pess["net_imports_Oil"]
net_trade_oil_lock = exports_lock["net_exports_Oil"] + exports_lock["net_imports_Oil"]
net_trade_oil_1_5 = exports_1_5["net_exports_Oil"] + exports_1_5["net_imports_Oil"]
lineplot_comparison(exports_pess["year"],net_trade_oil_pess,net_trade_oil_1_5,net_trade_oil_lock,"Net exports Oil (ktoe)")


#Pessimistic
investments_gas_pess = fiscal_pess.xs(("Gas",'ds_capex'), level=("product",0), axis=1)+fiscal_pess.xs(("Gas",'us_capex'), level=("product",0), axis=1)+fiscal_pess.xs(("Gas",'opex'), level=("product",0), axis=1)
investments_gas_pess = investments_gas_pess.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'investments'})

fiscal_in_gas_pess = fiscal_pess.xs(("Gas",'royalties'), level=("product",0), axis=1)+fiscal_pess.xs(("Gas",'export duties'), level=("product",0), axis=1)
fiscal_in_gas_pess = fiscal_in_gas_pess.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'fiscal_in'})

fiscal_out_gas_pess = fiscal_pess.xs(("Gas",'production subsidy'), level=("product",0), axis=1)+fiscal_pess.xs(("Gas",'import subsidy'), level=("product",0), axis=1)
fiscal_out_gas_pess = fiscal_out_gas_pess.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'fiscal_out'})

trade_bal_gas_pess = fiscal_pess.xs(("Gas",'trade balance'), level=("product",0), axis=1)
trade_bal_gas_pess = trade_bal_gas_pess.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'trade_bal'})

lineplot_comparison2(fiscal_out_gas_pess["year"],fiscal_in_gas_pess["fiscal_in"]/1000000,fiscal_out_gas_pess["fiscal_out"]/1000000,investments_gas_pess["investments"]/1000000,"Fiscal Transfers and Investments Gas Current Policy (MUSD)")

#oil
investments_oil_pess = fiscal_pess.xs(("Oil",'ds_capex'), level=("product",0), axis=1)+fiscal_pess.xs(("Oil",'us_capex'), level=("product",0), axis=1)+fiscal_pess.xs(("Oil",'opex'), level=("product",0), axis=1)
investments_oil_pess = investments_oil_pess.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'investments'})

fiscal_in_oil_pess = fiscal_pess.xs(("Oil",'royalties'), level=("product",0), axis=1)+fiscal_pess.xs(("Oil",'export duties'), level=("product",0), axis=1)
fiscal_in_oil_pess = fiscal_in_oil_pess.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'fiscal_in'})

fiscal_out_oil_pess = fiscal_pess.xs(("Oil",'production subsidy'), level=("product",0), axis=1)+fiscal_pess.xs(("Oil",'import subsidy'), level=("product",0), axis=1)
fiscal_out_oil_pess = fiscal_out_oil_pess.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'fiscal_out'})

trade_bal_oil_pess = fiscal_pess.xs(("Oil",'trade balance'), level=("product",0), axis=1)
trade_bal_oil_pess = trade_bal_oil_pess.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'trade_bal'})

lineplot_comparison2(fiscal_out_oil_pess["year"],fiscal_in_oil_pess["fiscal_in"]/1000,fiscal_out_oil_pess["fiscal_out"]/1000,investments_oil_pess["investments"]/1000,"Fiscal Transfers and Investments Oil Current Policy (MUSD)")

#1.5 degrees
#gas
investments_gas_1_5 = fiscal_1_5.xs(("Gas",'ds_capex'), level=("product",0), axis=1)+fiscal_1_5.xs(("Gas",'us_capex'), level=("product",0), axis=1)+fiscal_1_5.xs(("Gas",'opex'), level=("product",0), axis=1)
investments_gas_1_5 = investments_gas_1_5.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'investments'})

fiscal_in_gas_1_5 = fiscal_1_5.xs(("Gas",'royalties'), level=("product",0), axis=1)+fiscal_1_5.xs(("Gas",'export duties'), level=("product",0), axis=1)
fiscal_in_gas_1_5 = fiscal_in_gas_1_5.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'fiscal_in'})

fiscal_out_gas_1_5 = fiscal_1_5.xs(("Gas",'production subsidy'), level=("product",0), axis=1)+fiscal_1_5.xs(("Gas",'import subsidy'), level=("product",0), axis=1)
fiscal_out_gas_1_5 = fiscal_out_gas_1_5.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'fiscal_out'})

trade_bal_gas_1_5 = fiscal_1_5.xs(("Gas",'trade balance'), level=("product",0), axis=1)
trade_bal_gas_1_5 = trade_bal_gas_1_5.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'trade_bal'})

lineplot_comparison2(fiscal_out_gas_1_5["year"],fiscal_in_gas_1_5["fiscal_in"]/1000000,fiscal_out_gas_1_5["fiscal_out"]/1000000,investments_gas_1_5["investments"]/1000000,"Fiscal Transfers and Investments Gas Net Zero (MUSD)")

#oil
investments_oil_1_5 = fiscal_1_5.xs(("Oil",'ds_capex'), level=("product",0), axis=1)+fiscal_1_5.xs(("Oil",'us_capex'), level=("product",0), axis=1)+fiscal_1_5.xs(("Oil",'opex'), level=("product",0), axis=1)
investments_oil_1_5 = investments_oil_1_5.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'investments'})

fiscal_in_oil_1_5 = fiscal_1_5.xs(("Oil",'royalties'), level=("product",0), axis=1)+fiscal_1_5.xs(("Oil",'export duties'), level=("product",0), axis=1)
fiscal_in_oil_1_5 = fiscal_in_oil_1_5.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'fiscal_in'})

fiscal_out_oil_1_5 = fiscal_1_5.xs(("Oil",'production subsidy'), level=("product",0), axis=1)+fiscal_1_5.xs(("Oil",'import subsidy'), level=("product",0), axis=1)
fiscal_out_oil_1_5 = fiscal_out_oil_1_5.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'fiscal_out'})

trade_bal_oil_1_5 = fiscal_1_5.xs(("Oil",'trade balance'), level=("product",0), axis=1)
trade_bal_oil_1_5 = trade_bal_oil_1_5.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'trade_bal'})

lineplot_comparison2(fiscal_out_oil_1_5["year"],fiscal_in_oil_1_5["fiscal_in"]/1000,fiscal_out_oil_1_5["fiscal_out"]/1000,investments_oil_1_5["investments"]/1000,"Fiscal Transfers and Investments Oil Net Zero (MUSD)")

#lock
investments_gas_lock = fiscal_lock.xs(("Gas",'ds_capex'), level=("product",0), axis=1)+fiscal_lock.xs(("Gas",'us_capex'), level=("product",0), axis=1)+fiscal_lock.xs(("Gas",'opex'), level=("product",0), axis=1)
investments_gas_lock = investments_gas_lock.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'investments'})

fiscal_in_gas_lock = fiscal_lock.xs(("Gas",'royalties'), level=("product",0), axis=1)+fiscal_lock.xs(("Gas",'export duties'), level=("product",0), axis=1)
fiscal_in_gas_lock = fiscal_in_gas_lock.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'fiscal_in'})

fiscal_out_gas_lock = fiscal_lock.xs(("Gas",'production subsidy'), level=("product",0), axis=1)+fiscal_lock.xs(("Gas",'import subsidy'), level=("product",0), axis=1)
fiscal_out_gas_lock = fiscal_out_gas_lock.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'fiscal_out'})

trade_bal_gas_lock = fiscal_lock.xs(("Gas",'trade balance'), level=("product",0), axis=1)
trade_bal_gas_lock = trade_bal_gas_lock.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'trade_bal'})

lineplot_comparison2(fiscal_out_gas_lock["year"],fiscal_in_gas_lock["fiscal_in"]/1000000,fiscal_out_gas_lock["fiscal_out"]/1000000,investments_gas_lock["investments"]/1000000,"Fiscal Transfers and Investments Gas Lock In (MUSD)")

#oil
investments_oil_lock = fiscal_lock.xs(("Oil",'ds_capex'), level=("product",0), axis=1)+fiscal_lock.xs(("Oil",'us_capex'), level=("product",0), axis=1)+fiscal_lock.xs(("Oil",'opex'), level=("product",0), axis=1)
investments_oil_lock = investments_oil_lock.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'investments'})

fiscal_in_oil_lock = fiscal_lock.xs(("Oil",'royalties'), level=("product",0), axis=1)+fiscal_lock.xs(("Oil",'export duties'), level=("product",0), axis=1)
fiscal_in_oil_lock = fiscal_in_oil_lock.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'fiscal_in'})

fiscal_out_oil_lock = fiscal_lock.xs(("Oil",'production subsidy'), level=("product",0), axis=1)+fiscal_lock.xs(("Oil",'import subsidy'), level=("product",0), axis=1)
fiscal_out_oil_lock = fiscal_out_oil_lock.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'fiscal_out'})

trade_bal_oil_lock = fiscal_lock.xs(("Oil",'trade balance'), level=("product",0), axis=1)
trade_bal_oil_lock = trade_bal_oil_lock.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'trade_bal'})

lineplot_comparison2(fiscal_out_oil_lock["year"],fiscal_in_oil_lock["fiscal_in"]/1000,fiscal_out_oil_lock["fiscal_out"]/1000,investments_oil_lock["investments"]/1000,"Fiscal Transfers and Investments Oil Lock In (MUSD)")

#total fiscal impact
net_fiscal_pess = fiscal_in_oil_pess['fiscal_in'] - fiscal_out_oil_pess["fiscal_out"] + fiscal_in_gas_pess["fiscal_in"] - fiscal_out_gas_pess["fiscal_out"]
net_fiscal_lock = fiscal_in_oil_lock['fiscal_in'] - fiscal_out_oil_lock['fiscal_out'] + fiscal_in_gas_lock['fiscal_in'] - fiscal_out_gas_lock['fiscal_out']
net_fiscal_1_5 = fiscal_in_oil_1_5['fiscal_in'] - fiscal_out_oil_1_5['fiscal_out'] + fiscal_in_gas_1_5['fiscal_in'] - fiscal_out_gas_1_5['fiscal_out']

lineplot_comparison(fiscal_out_oil_pess["year"],net_fiscal_pess,net_fiscal_1_5,net_fiscal_lock,"Net Fiscal Impacts (USD)")

#gas fiscal impact 
net_fiscal_gas_pess =  fiscal_in_gas_pess["fiscal_in"] - fiscal_out_gas_pess["fiscal_out"]
net_fiscal_gas_lock =  fiscal_in_gas_lock['fiscal_in'] - fiscal_out_gas_lock['fiscal_out']
net_fiscal_gas_1_5 =   fiscal_in_gas_1_5['fiscal_in'] - fiscal_out_gas_1_5['fiscal_out']
lineplot_comparison(fiscal_out_oil_pess["year"],net_fiscal_gas_pess,net_fiscal_gas_1_5,net_fiscal_gas_lock,"Net Fiscal Gas Impacts (USD)")

#oil_fiscal impact
net_fiscal_oil_pess = fiscal_in_oil_pess['fiscal_in'] - fiscal_out_oil_pess["fiscal_out"] 
net_fiscal_oil_lock = fiscal_in_oil_lock['fiscal_in'] - fiscal_out_oil_lock['fiscal_out'] 
net_fiscal_oil_1_5 = fiscal_in_oil_1_5['fiscal_in'] - fiscal_out_oil_1_5['fiscal_out'] 
lineplot_comparison(fiscal_out_oil_pess["year"],net_fiscal_oil_pess,net_fiscal_oil_1_5,net_fiscal_oil_lock,"Net Fiscal Oil Impacts (USD)")

#trade balance gas
lineplot_comparison(fiscal_out_oil_pess["year"],trade_bal_gas_pess['trade_bal'],trade_bal_gas_1_5['trade_bal'],trade_bal_gas_lock['trade_bal'],"Trade Balance Gas (USD)")
lineplot_comparison(fiscal_out_oil_pess["year"],trade_bal_oil_pess['trade_bal'],trade_bal_oil_1_5['trade_bal'],trade_bal_oil_lock['trade_bal'],"Trade Balance Oil (USD)")


#Current Policy
#starts
starts_pess = fiscal_pess.xs('starts', level=(0), axis=1)
starts_pess = investments_gas_pess.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'starts'})
#Gas Starts
#currPol
starts_gas_pess = fiscal_pess.xs(("Gas",'starts'), level=("product",0), axis=1)
starts_gas_pess = investments_gas_pess.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'starts'})
#Oil Starts
starts_oil_pess = fiscal_pess.xs(("Oil",'starts'), level=("product",0), axis=1)
starts_oil_pess = investments_oil_pess.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'starts'})

#Lock In Policy
#starts
starts_lock = fiscal_lock.xs('starts', level=(0), axis=1)
starts_lock = investments_gas_lock.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'starts'})
#Gas Starts
#currPol
starts_gas_lock = fiscal_lock.xs(("Gas",'starts'), level=("product",0), axis=1)
starts_gas_lock = investments_gas_lock.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'starts'})
#Oil Starts
starts_oil_lock = fiscal_lock.xs(("Oil",'starts'), level=("product",0), axis=1)
starts_oil_lock = investments_oil_lock.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'starts'})

#Net Zero Policy
#starts
starts_1_5 = fiscal_1_5.xs('starts', level=(0), axis=1)
starts_1_5 = investments_gas_1_5.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'starts'})
#Gas Starts
#currPol
starts_gas_1_5 = fiscal_1_5.xs(("Gas",'starts'), level=("product",0), axis=1)
starts_gas_1_5 = investments_gas_1_5.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'starts'})
#Oil Starts
starts_oil_1_5 = fiscal_1_5.xs(("Oil",'starts'), level=("product",0), axis=1)
starts_oil_1_5 = investments_oil_1_5.reset_index().set_index('year').sum(axis=1).reset_index().rename(columns = {'year':'year',0:'starts'})

lineplot_comparison(starts_pess["year"],starts_pess["starts"],starts_1_5["starts"],starts_lock["starts"],"Total Starts")
lineplot_comparison(starts_gas_pess["year"],starts_gas_pess["starts"],starts_gas_1_5["starts"],starts_gas_lock["starts"],"Gas Starts")
lineplot_comparison(starts_oil_pess["year"],starts_oil_pess["starts"],starts_oil_1_5["starts"],starts_oil_lock["starts"],"Oil Starts")