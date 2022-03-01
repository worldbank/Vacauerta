
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os 
from pandas.core.indexing import convert_missing_indexer, convert_to_index_sliceable
import os 
import warnings
from math import floor

indir = "C:\\Users\\wb558960\\OneDrive - WBG\\CCDRs LAC\\Argentina\\DeepDives\\Vaca Muerta\\Report"

# read in POLES
poles = pd.read_csv(indir+"\\POLES Data Combined\\POLES Scenarios Combined.csv")
print(poles.head())
#Read in NGFS
ngfs = pd.read_csv(indir+"\\NGFS Data\\NGFS combined series.csv")
print(ngfs.head())

#Read in My Scenario Results 


# CONVERT EVERYTHING TO KTOE and 2015 Dollars
# 1EJ = 	23.488	MTOE		1 2010$ is	1.088583383	in 2015 $
# 1 GJ	2.3488E-08	MTOE				
# 1 MTOE	1000	ktoe

#################################### 
# #		  Process NGFS             #
####################################

#MELT NGFS for Conversion
years = list(np.arange(1990,2105,5))
years =  [str(x) for x in years]
# print(ngfs.columns)
print(years)
ngfs = pd.melt(ngfs, id_vars=['Model','Scenario','Region','Variable','Unit'], value_vars=years, var_name='year')
ngfs.drop_duplicates(subset =['Model','Scenario','Region','Variable','Unit', 'year'],
                    inplace = True)
#subset ngfs scenarios
ngfs = ngfs[ngfs["Scenario"].isin(['Net Zero 2050','Nationally Determined Contributions (NDCs) ','Current Policies '])]

l = ["US$2010/kW", 'billion US$2010/yr', "US$2010/cap", "US$2010/t CO2"]
l2 = ["GJ/US$2010"]
l3 = ["EJ/yr"]
l4 = ["US$2010/GJ"]

ngfs_2010 = ngfs[ngfs["Unit"].isin(l)]
ngfs_2010['value'] = ngfs_2010['value']*1.088
print(ngfs_2010.head())
ngfs_2010['Unit'] = ngfs_2010['Unit'].str.replace('US\$2010', 'US$2015', regex=True)
print(ngfs_2010.head())
#add back to main
ngfs = ngfs.append(ngfs_2010)

#Convert GJ to MTOE
ngfs_GJ = ngfs[ngfs["Unit"].isin(l2)]
ngfs_GJ['value'] = ngfs_GJ['value']*2.3488E-08/1.088
print(ngfs_GJ.head())
ngfs_GJ['Unit'] = ngfs_GJ['Unit'].str.replace('GJ/US\$2010', 'MTOE/US$2015', regex=True)
print(ngfs_GJ.head())
#add back to main
ngfs = ngfs.append(ngfs_GJ)

#Convert GJ to MTOE
ngfs_GJ = ngfs[ngfs["Unit"].isin(l3)]
ngfs_GJ['value'] = ngfs_GJ['value']*23.488
print(ngfs_GJ.head())
ngfs_GJ['Unit'] = ngfs_GJ['Unit'].str.replace('EJ/yr', 'MTOE/yr', regex=True)
print(ngfs_GJ.head())
#add back to main
ngfs = ngfs.append(ngfs_GJ)

#Convert GJ to MTOE
ngfs_GJ = ngfs[ngfs["Unit"].isin(l4)]
ngfs_GJ['value'] = ngfs_GJ['value']*1.088/2.3488E-08
print(ngfs_GJ.head())
ngfs_GJ['Unit'] = ngfs_GJ['Unit'].str.replace('US\$2010/GJ', 'US$2015/MTOE', regex=True)
print(ngfs_GJ.head())
#add back to main
ngfs = ngfs.append(ngfs_GJ)

ngfs= ngfs.pivot(index=['Model','Scenario','Region','Variable','Unit'], columns='year', values='value')
# ngfs.to_csv(indir+"\\ngfs_test.csv")


#process POLES

#MELT NGFS for Conversion
print(poles.columns)
print(poles.head())
poles = poles.drop(['2005'], axis = 1)
print(poles.head())
years = list(np.arange(1990,2071,10))
years =  [str(x) for x in years]
# print(ngfs.columns)
print(years)
poles = pd.melt(poles, id_vars=['Indicator', 'Category', 'Subcategory', 'Sector', 'ID', 'Units','Scenario'], value_vars=years, var_name='year')
poles.drop_duplicates(subset =['Indicator', 'Category', 'Subcategory', 'Sector', 'ID', 'Units','Scenario', 'year'],
                    inplace = True)
#subset ngfs scenarios
poles = poles[poles["Scenario"].isin(['1. CurrPol','2. GECO2021 NDC-LTS','3. GECO2021 1.5-Unif'])]

l = ["USD15/boe"]
poles_boe = poles[poles["Units"].isin(l)]
print(len(poles_boe))
poles_boe['value'] = poles_boe['value']*1000000/.146
print(poles_boe.head())
poles_boe["Units"] = poles_boe["Units"].str.replace('USD15/boe', 'US$2015/MTOE', regex=True)
print(poles_boe.Units.unique())
print(poles_boe.head())
#add back to main
poles = poles.append(poles_boe)

#rename variables to append

poles= poles.pivot(index=['Indicator', 'Category', 'Subcategory', 'Sector', 'ID', 'Units','Scenario'], columns='year', values='value')
poles["Model"] = "POLES"
poles["Region"] ="Argentina"
poles = poles.reset_index().drop(['Indicator','Category','Subcategory','Sector'], axis = 1)
poles = poles.rename(columns={"Units": "Unit", "ID": "Variable"})


poles.to_csv(indir+"\\poles_test.csv")

poles = poles.set_index(['Model','Region','Variable','Unit'])
ngfs = ngfs.reset_index().set_index(['Model','Region','Variable','Unit'])
ngfs = ngfs.append(poles).reset_index()
ngfs = ngfs.reset_index().drop(['1990','1995','2000','2005','2015','2025','2035','2045','2055','2060','2065','2070','2075', '2080','2085', '2090','2095','2100'], axis = 1)
print(ngfs.columns)
# ngfs = ngfs.set_index(['Model','Region','Variable','Unit'])
print(ngfs.head())
try: 
    ngfs.to_csv(indir+"\\combined_test.csv")
except: print('open csv')

#graphs

ngfs = pd.melt(ngfs, id_vars=['Model','Scenario','Region','Variable','Unit'], value_vars=['2010',
       '2020', '2030', '2040', '2050'], var_name='year')

#Regional Subsets
all_World = ngfs[ngfs["Region"]=="World"]
all_arg = ngfs[(ngfs["Region"]=="Argentina")|(ngfs["Region"]=="Argentina (downscaled)")]
#scenarios to use
#NG: Net Zero 2050, Nationally Determined Contributions, Current Policies
#POLES: CurrPol, NDC-LTS, 1.5-Unif

#Geography
# POLES - Argentina
# NGFS - Argentina, Argentina (downscaled), World

#Gas prices
# Price|Primary Energy|Gas
# Gas|Prices|Gas
fig = plt.figure(figsize=(15,10))
prices_arg = all_arg[((all_arg["Variable"]=="Gas|Prices|Gas")|(all_arg["Variable"]=="Price|Primary Energy|Gas"))&(all_arg["Unit"]=="US$2015/MTOE")]
prices_arg=prices_arg.drop(['Region','Unit','Variable'],axis = 1)
prices_arg = prices_arg.pivot(index = 'year',columns =['Model','Scenario' ], values ='value' )

prices_arg.plot()
plt.title('Gas Prices')
plt.ylabel('US$2015/MTOE')
plt.savefig(indir+'\\gas prices.png', bbox_inches="tight")

#Oil prices
# Price|Primary Energy|Oil
# Oil|Prices|Oil
prices_arg = all_arg[((all_arg["Variable"]=="Oil|Prices|Oil")|(all_arg["Variable"]=="Price|Primary Energy|Oil"))&(all_arg["Unit"]=="US$2015/MTOE")]
prices_arg=prices_arg.drop(['Region','Unit','Variable'],axis = 1)
prices_arg = prices_arg.pivot(index = 'year',columns =['Model','Scenario' ], values ='value' )
prices_arg.plot()
plt.title('Gas Prices')
plt.ylabel('US$2015/MTOE')
plt.legend(bbox_to_anchor=(1.05, 1))
plt.savefig(indir+'\\Gas prices.png', bbox_inches="tight")


#primary Energy - Gas
# Primary Energy|Gas
# Natural gas|Primary Production|gas
prim_arg = all_arg[((all_arg["Variable"]=="Primary Energy|Gas")|(all_arg["Variable"]=="Natural gas|Primary Production|gas"))&((all_arg["Unit"]=="Mtoe")|(all_arg["Unit"]=="MTOE/yr"))]
prim_arg=prim_arg.drop(['Region','Unit','Variable'],axis = 1)
prim_arg = prim_arg.pivot(index = 'year',columns =['Model','Scenario' ], values ='value' )
prim_arg.plot()
plt.title('Primary Production - Gas')
plt.ylabel('MTOE')
plt.legend(bbox_to_anchor=(1.05, 1))
plt.savefig(indir+'\\Primary prod Gas.png', bbox_inches="tight")

#primary energy oil
# Primary Energy|Oil
# Oil|Primary Production|Oil
prim_arg = all_arg[((all_arg["Variable"]=="Primary Energy|Oil")|(all_arg["Variable"]=="Oil|Primary Production|Oil"))&((all_arg["Unit"]=="Mtoe")|(all_arg["Unit"]=="MTOE/yr"))]
prim_arg=prim_arg.drop(['Region','Unit','Variable'],axis = 1)
prim_arg = prim_arg.pivot(index = 'year',columns =['Model','Scenario' ], values ='value' )
prim_arg.plot()
plt.title('Primary Production - Oil')
plt.ylabel('MTOE')
plt.legend(bbox_to_anchor=(1.05, 1))
plt.savefig(indir+'\\Primary prod Oil.png', bbox_inches="tight")


#final energy total
# Final Energy
# Final consumption|Primary Energy Demand, by sector (Mtoe)|consumption
final_arg = all_arg[((all_arg["Variable"]=="Final Energy")|(all_arg["Variable"]=="Total Final Consumption3 (Mtoe)|Total Final Consumption3 (Mtoe)|Mtoe|Total Final Consumption3 (Mtoe)"))&((all_arg["Unit"]=="Mtoe")|(all_arg["Unit"]=="MTOE/yr"))]
final_arg=final_arg.drop(['Region','Unit','Variable'],axis = 1)
final_arg = final_arg.pivot(index = 'year',columns =['Model','Scenario' ], values ='value' )
final_arg.plot()
plt.title('Final Consumption')
plt.ylabel('MTOE')
plt.legend(bbox_to_anchor=(1.05, 1))
plt.savefig(indir+'\\Final Consumption.png', bbox_inches="tight")

#final energy Electricity
# Final Energy|Electricity
# Electricity|Total Final Consumption3 (Mtoe)|Electricity|Total Final Consumption3 (Mtoe)

final_arg = all_arg[((all_arg["Variable"]=="Final Energy|Electricity")|(all_arg["Variable"]=="Electricity|Total Final Consumption3 (Mtoe)|Electricity|Total Final Consumption3 (Mtoe)"))&((all_arg["Unit"]=="MTOE")|(all_arg["Unit"]=="MTOE/yr"))]
final_arg=final_arg.drop(['Region','Unit','Variable'],axis = 1)
final_arg = final_arg.pivot(index = 'year',columns =['Model','Scenario' ], values ='value' )
final_arg.plot()
plt.title('Final Consumption Electricity')
plt.ylabel('MTOE')
plt.legend(bbox_to_anchor=(1.05, 1))
plt.savefig(indir+'\\Final Consumption Electricity.png', bbox_inches="tight")

#population
# Population
# Population (Million)|Main Economic Indicators|Million

final_arg = all_arg[((all_arg["Variable"]=="Final Energy|Electricity")|(all_arg["Variable"]=="Electricity|Total Final Consumption3 (Mtoe)|Electricity|Total Final Consumption3 (Mtoe)"))&((all_arg["Unit"]=="MTOE")|(all_arg["Unit"]=="MTOE/yr"))]
final_arg=final_arg.drop(['Region','Unit','Variable'],axis = 1)
final_arg = final_arg.pivot(index = 'year',columns =['Model','Scenario' ], values ='value' )
final_arg.plot()
plt.title('Final Consumption Electricity')
plt.ylabel('MTOE')
plt.legend(bbox_to_anchor=(1.05, 1))
plt.savefig(indir+'\\Final Consumption Electricity.png', bbox_inches="tight")

#GDPPC
# GDPpc|PPP
# GDP per capita (ppp, k$'15)|Main Economic Indicators|

#emissions
# CO2|GHG emissions (Mt CO2 eq.)|CO
# Emissions|CO2

#imports Gas
# Natural gas|Net Imports|gas

#imports oil
# Oil|Net Imports|Oil





#Save specific series: 
#emissions 
    #NGFS - Emissions|CO2
    #POLES - Total GHG (all, excluding LULUCF), Total GHG (all, including LULUCF)
#prices
    #NGFS: Price|Primary Energy|Gas, Price|Primary Energy|Oil
    #POLES: Gas Prices Gas, Oil Prices Oil
#Investment Needs
    #NGFS: Investment|Energy Supply, Investment|Energy Supply|CO2 Transport and Storage
    #POLES:
#Energy Mix
    #NGFS: Primary Energy|Gas,Primary Energy|Oil,Primary Energy|Coal,Primary Energy|Non-Biomass Renewables,Primary Energy|Biomass,Primary Energy|Other,Primary Energy|Nuclear
    #POLES:Biomass,Coal, Natural gas,Non-biomass renewables,Nuclear,Oil | Primary Production

#opex
    #NGFS: NA
    #POLES:NA
#capex
    #NGFS:Capital Cost|Electricity|Biomass|w/ CCS,Capital Cost|Electricity|Biomass|w/o CCS,Capital Cost|Electricity|Coal|w/ CCS,Capital Cost|Electricity|Coal|w/o CCS,Capital Cost|Electricity|Gas|w/ CCS
    # Capital Cost|Electricity|Gas|w/o CCS,Capital Cost|Electricity|Solar|CSP,Capital Cost|Electricity|Solar|PV,Capital Cost|Electricity|Wind|Offshore,Capital Cost|Electricity|Wind|Onshore
    #Capital Cost|Liquids|Gas|w/ CCS,Capital Cost|Liquids|Gas|w/o CCS,Capital Cost|Liquids|Oil
    #POLES:NA

#LCOE
    #NGFS:
    #POLES:

#Primary Production
    #NGFS: Primary Energy
    #POLES: Primary Production	|	Primary Production	|	Production

#Final Consumption
    #NGFS: Final Energy
    #POLES: Final Consumption | Primary Energy Demand, by sector (Mtoe) | consumption

#percent renewables
    #NGFS:
    #POLES:


#calculate percent changes/ratios for 2030/2040/2050

# Line graphs 



#line graph for specific series
