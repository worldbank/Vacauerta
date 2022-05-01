'''
modified from EMA Workbench tutorial on ecxel models  developed by Jan Kwakkel. 
Last modified by Sara Turner on 8.18.2021

'''

#import warnings
# #print("warnings gone")
# warnings.simplefilter('ignore', ImportWarning)
# warnings.filterwarnings('ignore', message='netlogo connector not available')
print('hello')

from xml.dom import pulldom
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

#set wd
# Print the current working directory
#print("Current working directory: {0}".format(os.getcwd()))

# Change the current working directory
os.chdir('C:\\Users\\wb558960\\OneDrive - WBG\\CCDRs LAC\\Argentina\\DeepDives\\Vaca Muerta\\Python\\src')
#print("Current working directory: {0}".format(os.getcwd()))

outdir = "C:\\Users\\wb558960\\OneDrive - WBG\\CCDRs LAC\\Argentina\\DeepDives\\Vaca Muerta\\Python\\outputs\\"
indir ='C:\\Users\\wb558960\\OneDrive - WBG\\CCDRs LAC\\Argentina\\DeepDives\\Vaca Muerta\\Python\\inputs\\'
# outdir = 'C:\\Users\\wb558960\\OneDrive - WBG\\CCDRs LAC\\Argentina\\DeepDives\\Vaca Muerta\\Python\\outputs\\'

num_experiments = 100


def VacaMuerta(yr0 = 2020, 
                final_yr = 2050, 
                model = "POLES",
                rcp = 'CURR', 
                switch = 'responsive',
                pes_oil = 1.2,
                pes_gas = 0.66,
                a_gas_res = .0, 
                a_oil_res = .0, 
                a_el_res = .0,
                a_gas_ind = .0,
                a_oil_ind = .0,
                a_el_ind = .0,
                a_gas_trans = .0,
                a_oil_trans = .0,
                a_el_trans = .0,
                l= 10.0, 
                t_rate_gas = 0.00, 
                t_rate_oil = 0.00, 
                t_rate_e  = .00,
                us_capex_gas = 7100000, 
                us_capex_oil = 7100000, 
                m = 9542, 
                oil_opex = (5/.000146),  
                gas_opex = (5/.000146), 
                prod_subsidy_p_ratio = 1.3, 
                share_covered = .17, 
                royalty_rate_gas = .12, 
                royalty_rate_oil = .12, 
                duty_rate_gas = .08, 
                duty_rate_oil = .08, 
                price_threshold_gas = 5.0*3965.261, 
                price_threshold_oil = 60.0*733, 
                price_floor_gas = 3.75*3965.261, 
                price_floor_oil = 45.0*733, 
                T_bond_rate = .0245, 
                arg_sov_risk = .0315, 
                opp_cost_own_finance = .1029, 
                share_own_capital =  .6803, 
                opp_cost_debt =  .0312, 
                GDP = 643629000000, 
                export_share_oil = .0,
                export_share_gas =.0, 
                #speed of decline for demand 
                gas_export_dem_start = 1.0, 
                oil_export_dem_start = 1.0, 
                gas_export_dem_end = 0.0,
                oil_export_dem_end = 0.0,
                gas_demand_decline_speed = 20,
                oil_demand_decline_speed = 20, 
                #speed of export capacity increase
                gas_ex_cap_start = 1905, 
                gas_ex_cap_end= 4631, 
                gas_ex_cap_increase = 10,
                oil_ex_cap_start= 33215, 
                oil_ex_cap_end= 33215, 
                oil_ex_cap_increase = 10,
                conv_start_gr_gas  = 0.0,
                conv_start_gr_oil  = 0.0, 
                conv_prod_decline_start =.06,
                conv_prod_decline_end_gas =  .06,
                conv_prod_decline_end_oil =.06,
                unconv_prod_decline_start =.0, 
                unconv_prod_decline_end_gas =.00,
                unconv_prod_decline_end_oil =.00,
                cons_wedge_start_gas = .25, 
                cons_wedge_end_gas = .5, 
                cons_wedge_start_oil = 10, 
                cons_wedge_end_oil = 2,
                intl_wedge_start_gas = 3,  
                intl_wedge_end_gas = 4, 
                intl_wedge_start_oil = 1, 
                intl_wedge_end_oil = 1, 
                well_life = 25,
                oil_responsiveness = 1.0,
                gas_responsiveness = 1.0, 
                public_ds_capex_share = 0.67,
                foreign_capex_share = .12,
                profit_tax_rate = .30,
                discount = .06):

    # #supply side
    #format us capex
    us_capex_cost ={'prod_type':['Gas','Oil'],'product':['Gas','Oil'],'capex':[us_capex_gas , us_capex_oil]}
    us_capex_cost = pd.DataFrame(us_capex_cost)

    #format op_ex
    opex_cost ={'product':['Gas','Oil'],'opex':[gas_opex , oil_opex]}
    opex_cost = pd.DataFrame(opex_cost)

    p_thr ={'prod_type':['Gas','Oil'],'threshold':[price_threshold_gas , price_threshold_oil]}
    p_thr = pd.DataFrame(p_thr)

    p_floor ={'prod_type':['Gas','Oil'],'threshold':[price_floor_gas , price_floor_oil]}
    p_floor = pd.DataFrame(p_floor)

    royalty_rate ={'prod_type':['Gas','Oil'],'rate':[royalty_rate_gas , royalty_rate_oil]}
    royalty_rate = pd.DataFrame(royalty_rate)

    duty_rate ={'prod_type':['Gas','Oil'],'rate':[duty_rate_gas , duty_rate_oil]}
    duty_rate = pd.DataFrame(duty_rate)

    conv_start_gr ={'prod_type':['Gas','Oil'],'rate':[conv_start_gr_gas,  conv_start_gr_oil]}
    conv_start_gr = pd.DataFrame(conv_start_gr)

    export_share = {'prod_type':['Gas','Oil'],'rate':[export_share_gas,  export_share_oil]}
    export_share = pd.DataFrame(export_share)

    responsiveness = {'prod_type':['Gas','Oil'],'rate':[gas_responsiveness,  oil_responsiveness]}
    responsiveness = pd.DataFrame(responsiveness)


    ################################
    ##          Well Starts       ##
    ################################
    #read in well and production data for unconventional gas and oil
    #get starts
    well_starts = pd.read_csv(indir + "first_appearance_combined_starts only.csv").groupby(['anio','tipo_de_recurso','oil_or_gas'])['idpozo'].agg('count').reset_index().rename(columns = {'idpozo':'starts','tipo_de_recurso':'well_type', 'oil_or_gas':'prod_type','anio':'year'})
    well_starts['well_type'] = well_starts['well_type'].replace({'CONVENCIONAL':'Conventional', 'NO CONVENCIONAL':'Unconventional'}) 
    well_starts['avgd_starts'] = well_starts.groupby(['well_type','prod_type'])['starts'].transform(lambda x: x.rolling(3,1).mean())
    # well_starts.to_csv(outdir+'well_starts.csv')
    # prices['Gas'] = prices.rolling(window=2)['Price Gas Bolivia']
    # print(well_starts.head(20))
    #we use three types of well - conventional, shale, and tight. All threee produce both oil and gas, but in different proportions. have generated an indicator for gas and oil wells based on threshold of 6000cf/bbl or 33.922 thousand m3 gas/ m3 oil.  
    #this makes work conssitent with newell and prest who separated analysis by conventional and unconventional oil and gas. 
    # can use tipo_de_recurso and oil_or_gas to achieve the same breakout

    ################################
    ##     Well Productivity      ##
    ################################

    oil_prod = pd.read_csv(indir+"fitted_oil_starts.csv").rename(columns = {'anio':'year'})
    oil_prod = oil_prod[oil_prod['year']>=2011]
    oil_prod = oil_prod[['year', 'idpozo', 'class', 'oil_or_gas', 'recurso','qi', 'popt_hyp0','popt_hyp1','popt_hyp2']].groupby(["recurso","oil_or_gas"]).agg("mean").reset_index()
    oil_prod['production_type'] = "Oil"

    gas_prod = pd.read_csv(indir+"fitted_gas_starts.csv").rename(columns = {'anio':'year'})
    gas_prod = gas_prod[gas_prod['year']>=2011]
    gas_prod = gas_prod[['year', 'idpozo', 'class', 'oil_or_gas', 'recurso','qi', 'popt_hyp0','popt_hyp1','popt_hyp2']].groupby(["recurso","oil_or_gas"]).agg("mean").reset_index()
    gas_prod['production_type'] = "Gas"

    production_profiles = gas_prod.append(oil_prod, ignore_index = True)
    production_profiles = production_profiles.rename(columns = {'recurso': 'well_type','production_type':'product', 'oil_or_gas':'prod_type','popt_hyp1':'b','popt_hyp2':'di'})
    production_profiles['well_type'] = production_profiles['well_type'].replace({'CONVENCIONAL':'Conventional', 'NO CONVENCIONAL':'Unconventional'}) 
    production_profiles.to_csv(outdir+"production profiles.csv")

    ################################
    ##          Prices            ##
    ################################
    #read in price scenarios - Brent crude for oil, henry hub for gas for now
    # #read in historical prices
    # prices_hist = pd.read_csv(indir + "Prices_hist.csv").set_index('year')
    # prices_hist = prices_hist.iloc[10: , :]

    #read in forecast price indices
    gas_init = 4.9 #($/mmbtu) 2020 weighted global average from WB
    oil_init = 41.3 #(70 in 2022)($/BBL) 2020 value from WB (Includes Ukraine price shock)
    e_init = 628000 #from GCAM ($/ktoe)
    prices = pd.read_csv(indir + "price_indices.csv").set_index('year')
    prices['Gas ktoe'] = prices['{}_{}_Gas'.format(model,rcp)]*41868*gas_init
    prices['Oil ktoe'] = prices['{}_{}_Oil'.format(model,rcp)]*7142*oil_init
    try:
        prices['Cons El Local ktoe'] = prices['{}_{}_El'.format(model,rcp)]*e_init
    except: 
        prices['Cons El Local ktoe'] = prices['GCAM_{}_El'.format(rcp)] *e_init

    # print(len(prices))

    # gas_gr = np.random.normal(gas_price_gr_mean, gas_price_gr_std)
    # print(gas_gr)
    # oil_gr = np.random.normal(oil_price_gr_mean, oil_price_gr_std)

    #CONVERT FROM GJ TO KTOE FOR CONSUMPTION
    # prices['Gas ktoe'] = prices['GCAM_CURR_S_Gas'] *4184
    # print(prices['Gas ktoe'].head())
    # print(prices['Gas ktoe'].apply(lambda x:  x+x*(np.random.normal(gas_price_gr_mean, gas_price_gr_std))))
    # prices['Gas ktoe'] = prices['Gas ktoe']+prices['Gas ktoe'].apply(lambda x:  x*gas_gr)

    #ngfs units aree in 2010$/GJ. Conversion 4184 ktoe per GJ
    # #POLES is in 2015$/boe. Conversion 7142 ktoe per boe
    # prices['Oil ktoe'] = prices['POLES_'+rcp+'_Oil_boe'] *7142
    # prices['Gas ktoe'] = prices['POLES_'+rcp+'_Gas_boe'] *7142
    # prices['Gas ktoe'] = prices['GCAM_'+rcp+'_S_Gas'] *41868
    # prices['Oil ktoe'] = prices['GCAM_'+rcp+'_S_Oil'] *41868
    # prices['Cons El Local ktoe'] = prices_hist['GCAM_'+rcp+'_S_Electricity'] *41868

    #create price wedge for international vs domestic prices
    intl_gas = np.linspace(intl_wedge_start_gas, intl_wedge_end_gas,len(prices))
    #intl_gas = intl_gas.cumsum()
    intl_oil = np.linspace(intl_wedge_start_oil, intl_wedge_end_oil, len(prices))
    #intl_oil = intl_oil.cumsum()

    prices['Gas Local ktoe'] =prices['Gas ktoe']/intl_gas
    prices['Oil Local ktoe'] =prices['Oil ktoe']/intl_oil

    #CONVERT FROM KTOE TO M3 for Production
    prices['Gas'] = prices['Gas ktoe'] /3965.2
    prices['Oil'] = prices['Oil ktoe'] /733.0

    #convert to local prices (ratio of bolivia to local argentina prices)
    prices['Gas Local'] =prices['Gas']/intl_gas
    prices['Oil Local'] =prices['Oil']/intl_oil

    #create price wedge for consumer behavior
    s_gas = np.linspace(cons_wedge_start_gas, cons_wedge_end_gas,len(prices))
    ##s_gas = s_gas.cumsum()
    s_oil = np.linspace(cons_wedge_start_oil, cons_wedge_end_oil,len(prices))
    #s_oil = s_gas.cumsum()

    prices['Cons Gas Local ktoe'] = (prices['Gas Local ktoe']/s_gas)
    # print(prices['Cons Gas Local ktoe'])
    prices['Cons Oil Local ktoe'] = (prices['Oil Local ktoe']/s_oil)

    prices['expected_price_Conventional_Oil'] = prices['Oil ktoe']
    prices['expected_price_Conventional_Gas'] = prices['Gas ktoe']
    prices['expected_price_Unconventional_Oil'] = prices['Oil ktoe']
    prices['expected_price_Unconventional_Gas'] = prices['Gas ktoe']

    prices['expected_local_price_Conventional_Oil'] = prices['Oil Local ktoe']
    prices['expected_local_price_Conventional_Gas'] = prices['Gas Local ktoe']
    prices['expected_local_price_Unconventional_Oil'] = prices['Oil Local ktoe']
    prices['expected_local_price_Unconventional_Gas'] = prices['Gas Local ktoe']
    # prices = prices.set_index('year')
    # print(len(prices))

    # # drop last rows
    # n = len(prices)-(final_yr-yr0)-2
    # prices = prices.iloc[:-n]
    # print(len(prices))

    #####################################
    ##   Export Capacity Limits        ##
    #####################################
    gas_export_cap = pd.concat([pd.Series(np.linspace(gas_ex_cap_start, gas_ex_cap_end,gas_ex_cap_increase)), pd.Series(np.linspace(gas_ex_cap_end, gas_ex_cap_end,((final_yr-yr0+1)-gas_ex_cap_increase)))], ignore_index = True)
    oil_export_cap = pd.concat([pd.Series(np.linspace(oil_ex_cap_start, oil_ex_cap_end,oil_ex_cap_increase)), pd.Series(np.linspace(oil_ex_cap_end, oil_ex_cap_end,((final_yr-yr0+1)-oil_ex_cap_increase)))], ignore_index = True)    
    
    #####################################
    ##   Export Demand Delines         ##
    #####################################
    gas_export_decline = pd.concat([pd.Series(np.linspace(gas_export_dem_start, gas_export_dem_end,gas_demand_decline_speed)), pd.Series(np.linspace(gas_export_dem_end, gas_export_dem_end,((final_yr-yr0+1)-gas_demand_decline_speed)))], ignore_index = True)
    oil_export_decline = pd.concat([pd.Series(np.linspace(oil_export_dem_start, oil_export_dem_end,oil_demand_decline_speed)), pd.Series(np.linspace(gas_export_dem_end, gas_export_dem_end,((final_yr-yr0+1)-oil_demand_decline_speed)))], ignore_index = True)    
    
    #####################################
    ##     Load Demand Data            ##
    #####################################
    #load energy balance
    demand_bal = pd.read_csv(indir+"balance_2020_V0_horizontal.csv")

    #load demand side elasticities
    ped = pd.read_csv(indir+"demand_elasticities.csv")
    #print(ped.head())

    #load income forecast
    income = pd.read_csv(indir+"income.csv")
    income = income[['year',"ln_GCAM5.3_NGFS -Net Zero_USD2015/cap"]]
    income = income.rename(columns={"ln_GCAM5.3_NGFS -Net Zero_USD2015/cap": "Ln_GDPPC"})
    #ln_GCAM5.3_NGFS_Net Zero_USD2015/cap	ln_POLES_USD2015/cap
    # print(income.head())

    demand_bal = demand_bal.rename( 
        columns = {'OFERTA_PRODUCCION': "prim_prod",'OFERTA_IMPORTACION': "prim_imports",'OFERTA_VARIACION DE STOCK':'prim_stockvar',
        'OFERTA_EXPORTACION Y BUNKER': "prim_exports", 'OFERTA_NO APROVECHADO': 'prim_unapproved','OFERTA_PERDIDAS':'prim_losses','OFERTA_AJUSTES':'prim_adjust',
        'OFERTA_OFERTA INTERNA':'prim_internal_supply', 'TRANSFORMACION_CENTRALES ELECTRICAS-SERVICIO PUBLICO':'trans_elect_utilities','TRANSFORMACION_CENTRALES ELECTRICAS-AUTOPRODUCCION':'trans_elect_ownprod',
        "TRANSFORMACION_PLANTAS DE TRATAMIENTO DE GAS":'trans_gas_treat',"TRANSFORMACION_REFINERIAS":"trans_refinery", 'TRANSFORMACION_ACEITERAS Y DESTILERiAS': 'trans_oil_distillate',
        'TRANSFORMACION_COQUERiAS':'trans_cokery', 'TRANSFORMACION_CARBONERAS':'trans_thermal','TRANSFORMACION_ALTOS HORNOS':'trans_blast_furnace',
        'CONSUMO_CONSUMO PROPIO':'cons_own','CONSUMO FINAL_TOTAL':'cons_final_tot','CONSUMO FINAL_NO ENERGETICO':'cons_non_energy',
        'CONSUMO FINAL_COMERCIAL Y PUBLICO':'cons_commercial_public','CONSUMO FINAL_RESIDENCIAL': "cons_residential",
        "CONSUMO FINAL_TRANSPORTE": "cons_transport",'CONSUMO FINAL_AGROPECUARIO':'cons_agriculture',"CONSUMO FINAL_INDUSTRIA":"cons_industry"})
    #Sum electricity production
    demand_bal["trans_electricity"]=demand_bal["trans_elect_utilities"]+demand_bal["trans_elect_ownprod"]
    demand_bal['trans_other'] = demand_bal['trans_oil_distillate']+demand_bal['trans_cokery'] +demand_bal['trans_thermal']+ demand_bal['trans_blast_furnace']
    demand_bal['cons_other'] =-1*(demand_bal['cons_agriculture']+ demand_bal['cons_commercial_public']+ demand_bal['cons_non_energy'])
    demand_bal['cons_residential'] = -1*demand_bal['cons_residential']
    demand_bal['cons_transport'] = -1*demand_bal['cons_transport']
    demand_bal['cons_industry'] = -1*demand_bal['cons_industry']

    demand_bal['type_cat'] = demand_bal['Type']+str("_") +demand_bal['Category']
    demand_bal = demand_bal[['type_cat', 'prim_prod', 'prim_imports', 'prim_stockvar',
        'prim_exports', 'prim_unapproved', 'prim_losses', 'prim_adjust',
            'trans_electricity','trans_gas_treat', 'trans_refinery', 'trans_other', 'cons_own',
            'cons_residential','cons_transport', 'cons_industry','cons_other' ]].T
    demand_bal.columns = demand_bal.iloc[0]
    demand_bal = demand_bal.iloc[1: , :]
    #print(demand_bal.columns)

    collist = ['Energia Hidraulica_Primaria', 'Energia Nuclear_Primaria',
        'Carbon Mineral_Primaria', 'Lena_Primaria', 'Bagazo_Primaria',
        'Aceites Vegetales_Primaria', 'Alcoholes Vegetales_Primaria',
        'Energia Eolico_Primaria', 'Energia Solar_Primaria',
        'Otros Primarios_Primaria']
    demand_bal['other_Primaria']=demand_bal[collist].sum(axis=1)
    demand_bal = demand_bal.drop(collist, axis = 1)

    demand_bal['petroleum_other_Secondaria'] = demand_bal[['Gas de Refineria_Secondaria','Gas Licuado_Secondaria','Gasolina Natural_Secondaria','Otras Naftas_Secondaria','Motonafta Total_Secondaria', 
                                                            'Kerosene y Aerokerosene_Secondaria','Diesel Oil + Gas Oil_Secondaria', 'Coque_Secondaria', 'Fuel Oil_Secondaria']].sum(axis=1)
    demand_bal['energy_other_Secondaria'] =  demand_bal[['Carbon Residual_Secondaria','Gas de Coqueria_Secondaria', 'Gas de Alto Horno_Secondaria',
                                                            'Carbon de Lena_Secondaria', 'Bioetanol_Secondaria','Biodiesel_Secondaria']].sum(axis=1)

    collist = ['Gas de Refineria_Secondaria', 'Gas Licuado_Secondaria','Gasolina Natural_Secondaria', 'Otras Naftas_Secondaria',
        'Motonafta Total_Secondaria', 'Kerosene y Aerokerosene_Secondaria',
        'Diesel Oil + Gas Oil_Secondaria', 'Fuel Oil_Secondaria',
        'Carbon Residual_Secondaria', 
        'Gas de Coqueria_Secondaria', 'Gas de Alto Horno_Secondaria',
        'Coque_Secondaria', 'Carbon de Lena_Secondaria', 'Bioetanol_Secondaria',
        'Biodiesel_Secondaria','TOTAL I_Primaria', 'TOTAL II_Secondaria']
    demand_bal = demand_bal.drop(collist, axis = 1)

    # print(demand_bal)
    demand_bal= demand_bal.reset_index().rename(columns={'index': 'step'})
    #demand_bal.to_csv(outdir+"simplified_balance.csv")

    primary_inflows = ['prim_prod','prim_imports','prim_adjust','prim_stockvar']
    secondary_inflows = ['prim_imports', 'prim_adjust','prim_stockvar']

    p_s_outflows = ['prim_exports','prim_unapproved','trans_gas_treat','prim_losses','trans_electricity','trans_refinery',
    'trans_other','cons_own', 'cons_residential', 'cons_transport','cons_industry','cons_other']


    #####################################
    #      SAVE percent                ##
    #####################################
    # def safe_pct(s1,s2,p1,p2):
    #     # print(x/y)
    #     print('terror!')
    #     if s1 and s2 and p1 and p2:  
    #         print( "values exist!")
    #     else:
    #         print('dont exist!')
    #     # return min(1.0,max(0,((s2/p2-s1/p1)/(s1/p1)))) if s1 and s2 and p1 and p2 else 1

    #####################################
    #      SAVE DIVISION               ##
    #####################################
    def safe_div(x,y):
        # print(x/y)
        # return min(1,max(0,x/y)) if y else 1
        return max(0,x/y) if y else 1

    #####################################
    ##              WACC               ##
    #####################################
    #why does Mariana's calculation include both adding and subtracting the t-bond rate? 
    # wacc = T_bond_rate +arg_sov_risk + (opp_cost_own_finance*share_own_capital) + (opp_cost_debt*(1-share_own_capital)) - T_bond_rate 
    wacc = discount

    #########################################
    ##  Hyperbolic Production Function     ##
    #########################################
    def hyperbolic(t,qi,b,di):
        return qi/((1.0+b*di*t)**(1.0/b))

    #########################################
    ##      Demand Balance Processing      ##
    #########################################
    type_cat = ['prim_prod', 'prim_imports', 'prim_stockvar',
        'prim_exports', 'prim_unapproved', 'prim_losses', 'prim_adjust',
            'trans_electricity','trans_gas_treat', 'trans_refinery', 'trans_other', 'cons_own',
            'cons_residential','cons_transport', 'cons_industry','cons_other' ]

    def balance_processing(type, products, primary_inflows,secondary_inflows, outflows):
        bal = demand_bal[type]
        #try if product list contains more than one item. if not use single item formula
        try:
                i_flows = (bal[bal['step'].isin(primary_inflows)][products[0]].squeeze()).sum()+(bal[bal['step'].isin(secondary_inflows)][products[1]].squeeze()).sum()
                o_flows = (bal[bal['step'].isin(outflows)][products[0]].squeeze()).sum()+(bal[bal['step'].isin(outflows)][products[1]].squeeze()).sum()
        except: 
                i_flows = (bal[bal['step'].isin(secondary_inflows)][products[0]].squeeze()).sum()
                o_flows = (bal[bal['step'].isin(outflows)][products[0]].squeeze()).sum()
        # print(i_flows+o_flows)
        flow_share = bal[products]/i_flows
        flow_share['type']=type_cat
        return bal,flow_share 

    oil_type = ['step','Petroleo_Primaria','petroleum_other_Secondaria']
    oil_products =['Petroleo_Primaria','petroleum_other_Secondaria']

    # print('oil check:')
    oil_bal, oil_share = balance_processing(oil_type,oil_products,primary_inflows,secondary_inflows, p_s_outflows)

    gas_type = ['step', 'Gas Natural de Pozo_Primaria','Gas Distribuido por Redes_Secondaria']
    gas_products =['Gas Natural de Pozo_Primaria','Gas Distribuido por Redes_Secondaria']
    # print('gas check:')
    gas_bal, gas_share = balance_processing(gas_type,gas_products,primary_inflows,secondary_inflows, p_s_outflows)

    e_type = ['step', 'Energia Electrica_Secondaria']
    e_products =['Energia Electrica_Secondaria']
    e_primary_inflows = []
    e_secondary_inflows = ['prim_imports','prim_adjust','prim_stockvar','trans_electricity']
    p_s_outflows = ['prim_exports','prim_unapproved','prim_losses', 'trans_gas_treat','trans_refinery',
    'trans_other','cons_own', 'cons_residential', 'cons_transport','cons_industry','cons_other']
    # print('electricity check:')
    e_bal, e_share = balance_processing(e_type,e_products,e_primary_inflows,e_secondary_inflows, p_s_outflows)

    #########################################
    ##            consumption              ##
    #########################################
    def consumption(product, sector,prev_cons,price_type, a):
        ped_sr = ped[(ped["Type"]=="SR own-price elasticity")&(ped["Product"]==product) &(ped["Sector"]==sector)]['Elasticity'].squeeze()
        ped_lr = ped[(ped["Type"]=="LR own-price elasticity")&(ped["Product"]==product) &(ped["Sector"]==sector)]['Elasticity'].squeeze()
        ped_inc = ped[(ped["Type"]=="Income elasticity")&(ped["Product"]==product) &(ped["Sector"]==sector)]['Elasticity'].squeeze()

        if t<=t+l:
            cons = (cons_df[cons_df['year']==t-1][prev_cons].squeeze())*(1+a)**-(1+ped_sr)*((income[income['year']==t]['Ln_GDPPC'].squeeze()/
            income[income['year']==t-1]['Ln_GDPPC'].squeeze())**ped_inc)*((prices[(prices['year']==t) & (prices['prod_type']==price_type)]['value'].squeeze()/
            prices[(prices['year']==t-1) & (prices['prod_type']==price_type)]['value'].squeeze())**ped_sr)*((prices[(prices['year']==t) & (prices['prod_type']==price_type)]['value'].squeeze()/
            prices[(prices['year']==yr0) & (prices['prod_type']==price_type)]['value'].squeeze())**((ped_lr*(1+ped_sr))/l))
            
        else: 
            cons = (cons_df[cons_df['year']==t-1][prev_cons].squeeze())*(1+a)**-(1+ped_sr)*((income[income['year']==t]['Ln_GDPPC'].squeeze()/
            income[income['year']==t-1]['Ln_GDPPC'].squeeze())**ped_inc)*((prices[(prices['year']==t) & (prices['prod_type']==price_type)]['value'].squeeze()/
            prices[(prices['year']==t-1) & (prices['prod_type']==price_type)]['value'].squeeze())**ped_sr)*((prices[(prices['year']==t) & (prices['prod_type']==price_type)]['value'].squeeze()/
            prices[(prices['year']==t-l) & (prices['prod_type']==price_type)]['value'].squeeze())**((ped_lr*(1+ped_sr))/l))
            
        return cons

    ################################################
    ##              state variables               ##
    ################################################
    ff = []
    cc = pd.DataFrame()
    fiscal = pd.DataFrame()
    # columns = ['year',"prod_type",'well_type','product','us_capex']
    #us capex rtreated separately since not on q, on # well starts
    def calculate_us_capex(df,t,p,w,k):
        df = df.reset_index()
        st = df[(df['year']==t)&(df['prod_type']==p)&(df['well_type']==w)&(df['product']==k)]['starts'].squeeze()

        us_cap = us_capex_cost[(us_capex_cost['prod_type']==p)]['capex'].squeeze() * df[(df['year']==t)&(df['prod_type']==p)&(df['well_type']==w)&(df['product']==k)]['starts'].squeeze()
        us_capex = [t,p,w,k,us_cap,st]
        return us_capex

    #variables: all financial var calculated on quantities 
    def calculate_state(t,w,k):
        pr = prices[(prices['prod_type']=='{} Local ktoe'.format(k))&(prices['year']==t)]['value'].squeeze()
        intl_pr = prices[(prices['prod_type']=='{} ktoe'.format(k))&(prices['year']==t)]['value'].squeeze()

        # # ds capex - on production
        #same as vm.py
        if k == 'Gas':
                ds_capex = m*(mp[mp['sim_year']==t]['{}_Gas'.format(w)].squeeze())
        else:  ds_capex = 0

        # #opex - on production
        opex =(mp[mp['sim_year']==t]['{}_{}'.format(w,k)].squeeze())*opex_cost[opex_cost['product']==p]['opex'].squeeze()
        # print(production)
        # print((mp[mp['sim_year']==t]['{}_{}'.format(w,k)].squeeze()))
        # print(opex_cost[opex_cost['product']==p]['opex'].squeeze())

        #domestic_revenue
        dom_rev = (((mp[mp['sim_year']==t]['{}_{}'.format(w,k)].squeeze())-
                    exports[exports['year']==t]['exports_{}_{}'.format(w,k)].squeeze()-
                    exports[exports['year']==t]['surplus_{}_{}'.format(w,k)].squeeze())*
                    prices[(prices['prod_type']=='{} Local ktoe'.format(k))&(prices['year']==t)]['value'].squeeze())

        # #export revenue
        exp_rev = exports[exports['year']==t]['exports_{}_{}'.format(w,k)].squeeze()*prices[(prices['prod_type']=='{} ktoe'.format(k))&(prices['year']==t)]['value'].squeeze()
        try: 
                if exp_rev <= 0: 
                        exp_rev =0
        except:
                print("end ot timeseries")
        
        trade_balance = exports[exports['year']==t]['im_ex_{}'.format(k)].squeeze()*prices[(prices['prod_type']=='{} ktoe'.format(k))&(prices['year']==t)]['value'].squeeze()

        # # #import subsidies
        if (prices[(prices['prod_type']=='{} ktoe'.format(k))&(prices['year']==t)]['value'].squeeze() > prices[(prices['prod_type']=='{} Local ktoe'.format(k))&(prices['year']==t)]['value'].squeeze()):
            import_sub = (exports[exports['year']==t]['imports_{}_{}'.format(w,k)].squeeze()*(prices[(prices['prod_type']=='{} ktoe'.format(k))&(prices['year']==t)]['value'].squeeze()-prices[(prices['prod_type']=='{} Local ktoe'.format(k))&(prices['year']==t)]['value'].squeeze()))
        else: 
            import_sub =0
        
        try:
                if import_sub >= 0: 
                        import_sub =0
        except: 
                print("end of series")
        
        # #production subsidies       
        # prod_sub = share_covered*(mp[mp['sim_year']==t]['{}_{}'.format(w,k)].squeeze())*np.maximum(0,(prices[(prices['prod_type']=='{} ktoe'.format(k))&(prices['year']==t)]['value'].squeeze()-prices[(prices['prod_type']=='{} Local ktoe'.format(k))&(prices['year']==t)]['value'].squeeze()))
        
        if k == 'Gas' :     
            prod_sub = share_covered*mp[mp['sim_year']==t]['{}_{}'.format(w,k)].squeeze()*((prod_subsidy_p_ratio-1)*
                    prices[(prices['prod_type']=='{} Local ktoe'.format(k))&(prices['year']==t)]['value'].squeeze())
        else: prod_sub = 0
        

        # #royalties
        royalties = royalty_rate[royalty_rate['prod_type']=='{}'.format(k)]['rate'].squeeze()*mp[mp['sim_year']==t]['{}_{}'.format(w,k)].squeeze()*prices[(prices['prod_type']=='{} Local ktoe'.format(k))&(prices['year']==t)]['value'].squeeze()

        # #export duties
        export_duties = duty_rate[duty_rate['prod_type']=='{}'.format(k)]['rate'].squeeze()*exports[exports['year']==t]['exports_{}_{}'.format(w,k)].squeeze()*prices[(prices['prod_type']=='{} ktoe'.format(k))&(prices['year']==t)]['value'].squeeze()
        try: 
            if (prices[(prices['prod_type']=='{} ktoe'.format(k))&(prices['year']==t)]['value'].squeeze() <= p_thr[p_thr['prod_type']=='{}'.format(k)]['threshold'].squeeze()) & (prices[(prices['prod_type']=='{} ktoe'.format(k))&(prices['year']==t)]['value'].squeeze() > p_floor[p_floor['prod_type']=='{}'.format(k)]['threshold'].squeeze()) :
                    #.24 is the slope of the function used to calculate export duties
                    export_duties = .24 * ((prices[(prices['prod_type']=='{} ktoe'.format(k))&(prices['year']==t)]['value'].squeeze() - p_floor[p_floor['prod_type']=='{}'.format(k)]['threshold'].squeeze())/p_floor[p_floor['prod_type']=='{}'.format(k)]['threshold'].squeeze())
            if exports[exports['year']==t]['exports_{}_{}'.format(w,k)].squeeze() <=0:
                    export_duties = 0
        except: 
            print("end of series")
        


        ff = [t,w,k, pr, intl_pr, ds_capex,opex, dom_rev,exp_rev,prod_sub,import_sub,royalties,export_duties, trade_balance]

        return(ff)

    #########################################
    ##                model                ##
    #########################################

    #Set up data framews for CONSUMPTION
    #consumption
    cons_df = pd.DataFrame(columns = ['year',"gas_cons_residential",'gas_cons_industry','gas_cons_transport','gas_cons_other','gas_own_cons','gas_loss_adj',
        "oil_cons_residential",'oil_cons_industry','oil_cons_transport','oil_cons_other', 'oil_own_cons','oil_loss_adj',
        "el_cons_residential",'el_cons_industry','el_cons_transport','el_cons_other','el_own_cons','el_loss_adj','gas_cons','oil_cons','electricity_cons','total_cons'])

    gas_rescons0 = -1*(gas_bal[gas_bal['step'].isin(['cons_residential'])]['Gas Distribuido por Redes_Secondaria'].squeeze())
    gas_indcons0 = -1*(gas_bal[gas_bal['step'].isin(['cons_industry'])]['Gas Distribuido por Redes_Secondaria'].squeeze())
    gas_transcons0 = -1*(gas_bal[gas_bal['step'].isin(['cons_transport'])]['Gas Distribuido por Redes_Secondaria'].squeeze())
    gas_othercons0 = -1*(gas_bal[gas_bal['step'].isin(['cons_other'])]['Gas Distribuido por Redes_Secondaria'].squeeze())
    #add primary own consumption
    gas_owncons0 = -1*(gas_bal[gas_bal['step'].isin(['cons_own'])]['Gas Distribuido por Redes_Secondaria'].squeeze()) +-1*(gas_bal[gas_bal['step'].isin(['cons_own'])]['Gas Natural de Pozo_Primaria'].squeeze())

    # 'prim_exports',
    loss_adj = ['prim_stockvar','prim_unapproved','prim_losses','prim_adjust','trans_electricity','trans_gas_treat','trans_refinery','trans_other']
    gas_loss_adj0=(gas_bal[gas_bal['step'].isin(loss_adj)]['Gas Distribuido por Redes_Secondaria'].sum())+(gas_bal[gas_bal['step'].isin(loss_adj)]['Gas Natural de Pozo_Primaria'].sum())

    oil_rescons0 = -1*(oil_bal[oil_bal['step'].isin(['cons_residential'])]['petroleum_other_Secondaria'].squeeze())
    oil_indcons0 = -1*(oil_bal[oil_bal['step'].isin(['cons_industry'])]['petroleum_other_Secondaria'].squeeze())
    oil_transcons0 = -1*(oil_bal[oil_bal['step'].isin(['cons_transport'])]['petroleum_other_Secondaria'].squeeze())
    oil_othercons0 = -1*(oil_bal[oil_bal['step'].isin(['cons_other'])]['petroleum_other_Secondaria'].squeeze())
    #add primary own consumption
    oil_owncons0 = -1*(oil_bal[oil_bal['step'].isin(['cons_own'])]['petroleum_other_Secondaria'].squeeze()) + -1*(oil_bal[oil_bal['step'].isin(['cons_own'])]['Petroleo_Primaria'].squeeze())
    oil_loss_adj0= (oil_bal[oil_bal['step'].isin(loss_adj)]['petroleum_other_Secondaria'].sum())+(oil_bal[oil_bal['step'].isin(loss_adj)]['Petroleo_Primaria'].sum())

    el_rescons0 = -1*(e_bal[e_bal['step'].isin(['cons_residential'])]['Energia Electrica_Secondaria'].squeeze())
    el_indcons0 = -1*(e_bal[e_bal['step'].isin(['cons_industry'])]['Energia Electrica_Secondaria'].squeeze())
    el_transcons0 = -1*(e_bal[e_bal['step'].isin(['cons_transport'])]['Energia Electrica_Secondaria'].squeeze())
    el_othercons0 = -1*(e_bal[e_bal['step'].isin(['cons_other'])]['Energia Electrica_Secondaria'].squeeze())
    el_owncons0 = -1*(e_bal[e_bal['step'].isin(['cons_own'])]['Energia Electrica_Secondaria'].squeeze())
    el_loss_adj0= (e_bal[e_bal['step'].isin(loss_adj)]['Energia Electrica_Secondaria'].sum())

    non_energy0 = demand_bal[demand_bal['step'].isin(['cons_residential','cons_industry','cons_transport','cons_other','cons_own'])]['No Energetico_Secondaria'].sum()
    other_primary_energy0 = demand_bal[demand_bal['step'].isin(['cons_residential','cons_industry','cons_transport','cons_other','cons_own'])]['other_Primaria'].sum()
    other_secondary_energy0 = demand_bal[demand_bal['step'].isin(['cons_residential','cons_industry','cons_transport','cons_other','cons_own'])]['energy_other_Secondaria'].sum()

    gas_cons0 = gas_rescons0+gas_indcons0+gas_transcons0+gas_owncons0 + gas_othercons0 
    oil_cons0 = oil_rescons0+oil_indcons0+oil_transcons0+oil_owncons0 + oil_othercons0
    electricity_cons0 = el_rescons0+el_indcons0+el_transcons0+el_owncons0 + el_othercons0
    total_cons0 = gas_cons0+oil_cons0+electricity_cons0

    # print(df.head())
    cons_df.loc[0] = [2020, gas_rescons0,gas_indcons0,gas_transcons0,gas_othercons0,gas_owncons0,gas_loss_adj0,oil_rescons0,oil_indcons0,oil_transcons0,oil_othercons0,oil_owncons0,oil_loss_adj0,
        el_rescons0,el_indcons0,el_transcons0,el_othercons0,el_owncons0,el_loss_adj0,gas_cons0,oil_cons0,electricity_cons0,total_cons0]

    #a is exogenous increase in energy efficiency
    prices = prices.reset_index()
    # print(prices.head())

    gas_own_cons_share =  gas_owncons0/(gas_rescons0+gas_transcons0+gas_indcons0+gas_othercons0)
    oil_own_cons_share = oil_owncons0/(oil_rescons0+oil_transcons0+oil_indcons0+oil_othercons0)
    el_own_cons_share = el_owncons0/(el_rescons0+el_transcons0+el_indcons0+el_othercons0)
    # other_energy_share = other_energy0/(gas_rescons0+gas_indcons0+gas_othercons0+gas_owncons0+oil_rescons0+oil_indcons0+oil_othercons0+oil_owncons0+el_rescons0+el_indcons0+el_othercons0+el_owncons0)

    gas_loss_adj_share = gas_loss_adj0/(gas_rescons0+gas_transcons0+gas_indcons0+gas_othercons0)
    oil_loss_adj_share = oil_loss_adj0/(oil_rescons0+oil_transcons0+oil_indcons0+oil_othercons0)
    el_loss_adj_share = el_loss_adj0/(el_rescons0+el_transcons0+el_indcons0+el_othercons0)

    #set up Data frames for PRODUCTION
    df=pd.DataFrame(columns = ['year', 'well_type', 'prod_type','starts']).set_index(['prod_type','well_type'])
    well_starts = well_starts.set_index(['prod_type','well_type'])

    #function for elasticities
    well_type = ["Conventional","Unconventional"]
    production_type = ["Oil","Gas"]
    product = ["Oil","Gas"]

    d = {'prod_type': ["Oil", "Gas"], 'p_elast_supply': [pes_oil, pes_gas]}
    pes = pd.DataFrame(d).set_index('prod_type')

    pp = pd.DataFrame()
    prices=prices.melt(id_vars = 'year').rename(columns ={'variable':'prod_type'}).set_index(['prod_type','year'])
    s = pd.DataFrame(columns = ['prod_type','year', 'starts'])

    # prod_df = pd.DataFrame( columns = ['year', 'well_type', 'prod_type','production'])
    
    production_profiles = production_profiles.set_index(['prod_type','well_type']).drop(columns = ['idpozo','year'])
    pp = pd.DataFrame()

    #set up data frames for Consumption

    for t in range(yr0,final_yr+1):
        ##Consumption##
        #Production##
        if t == yr0:
        #CONSUMPTION
            prices = prices.reset_index()
            #currently set above in consumption definitions
            ratio =1
            cumratio=0
        
            ##PRODUCTION
            #starts
            prices = prices.set_index(['prod_type','year'])
            # print(prices.head())
            # well_starts
            wells0=well_starts[(well_starts["year"]==t)].reset_index().set_index('well_type')

            df=df.append(wells0).reset_index().rename(columns={"index":'well_type'}).set_index(['prod_type','well_type','year'])
            df = df.join(production_profiles, on =['prod_type','well_type'])

            df['starts'] = df['avgd_starts'].astype(float, errors = 'raise')
            df['product'] = df['product'].astype(str, errors = 'raise')
            df= df.reset_index().set_index(['prod_type','well_type','year','product'])
            # print(df.head())
            print('t0 done')

            initial_prod_2020_m3 = [2020,26230 ,18910,21321 , 6965]

        else:
            #CONSUMPTION
            try:
                    prices = prices.reset_index().drop(columns='index')
            except:
                    prices = prices.reset_index()

            gas_res_cons = (1+t_rate_gas)*consumption('natural gas','residential','gas_cons_residential','Cons Gas Local ktoe',a_gas_res)
            gas_ind_cons = (1+t_rate_gas)*consumption('natural gas','industry','gas_cons_industry','Cons Gas Local ktoe', a_gas_ind)
            gas_trans_cons = (1+t_rate_gas)*consumption('natural gas','general','gas_cons_transport','Cons Gas Local ktoe', a_gas_trans)
            gas_other_cons = (1+t_rate_gas)*consumption('natural gas','general','gas_cons_other','Cons Gas Local ktoe',0)
            gas_own_cons = (gas_res_cons+gas_ind_cons+gas_trans_cons+gas_other_cons)*(gas_own_cons_share)
            gas_loss_adj = (gas_res_cons+gas_ind_cons+gas_trans_cons+gas_other_cons)*(gas_loss_adj_share)

            #oil products or gasoline here. or need to split? COuld do if I could identify which products go into gasoline
            oil_res_cons = (1+t_rate_oil)*consumption('oil products','residential','oil_cons_residential','Cons Oil Local ktoe',a_oil_res)
            oil_ind_cons = (1+t_rate_oil)*consumption('oil products','industry','oil_cons_industry','Cons Oil Local ktoe',a_oil_ind)
            oil_trans_cons = (1+t_rate_oil)*consumption('oil products','general','oil_cons_transport','Cons Oil Local ktoe',a_oil_trans)
            oil_other_cons = (1+t_rate_oil)*consumption('oil products','general','oil_cons_other','Cons Oil Local ktoe',0)
            oil_own_cons = (oil_res_cons+oil_ind_cons+oil_trans_cons+oil_other_cons)*(oil_own_cons_share)
            oil_loss_adj = (oil_res_cons+oil_ind_cons+oil_trans_cons+oil_other_cons)*(oil_loss_adj_share)

            #need electricity price forecasts
            el_res_cons = (1+t_rate_e)*consumption('electricity','residential','el_cons_residential','Cons El Local ktoe',a_el_res)
            el_ind_cons = (1+t_rate_e)*consumption('electricity','industry','el_cons_industry','Cons El Local ktoe',a_el_ind)
            el_trans_cons = (1+t_rate_e)*consumption('electricity','general','el_cons_transport','Cons El Local ktoe',a_el_trans)
            el_other_cons = (1+t_rate_e)*consumption('electricity','general','el_cons_other','Cons El Local ktoe',0)
            el_own_cons = (el_res_cons+el_ind_cons+el_trans_cons+el_other_cons)*(el_own_cons_share)
            el_loss_adj = (el_res_cons+el_ind_cons+el_trans_cons+el_other_cons)*(el_loss_adj_share)

            gas_cons = gas_res_cons+gas_ind_cons+gas_trans_cons+gas_own_cons+gas_other_cons

            oil_cons = oil_res_cons+oil_ind_cons+oil_trans_cons+oil_own_cons+oil_other_cons

            electricity_cons = el_res_cons+el_ind_cons+el_trans_cons+el_own_cons+el_other_cons

            total_cons = gas_cons+oil_cons+electricity_cons    

            h=[t,gas_res_cons,gas_ind_cons,gas_trans_cons,gas_other_cons,gas_own_cons,gas_loss_adj,
            oil_res_cons,oil_ind_cons,oil_trans_cons,oil_other_cons,oil_own_cons,oil_loss_adj,
            el_res_cons,el_ind_cons,el_trans_cons,el_other_cons,el_own_cons,el_loss_adj,gas_cons,oil_cons,electricity_cons,total_cons]

            cons_df.loc[t]= h
            prices = prices.set_index(['prod_type','year'])

            #PRODUCTION
            for w in well_type:
                for p in production_type:
                    for k in product: 
                            #current loop  
                        # print(str(t) +" "+ p + " " + w +" "+ k)
                        prices=prices.reset_index()

                        ex_share = export_share[export_share['prod_type']=='{}'.format(p)]['rate'].squeeze()

                        #note this should be responsive to both exports and domestic prices - need to come and reactivate that
                            #estimate current year well starts
                            # s=round(df.loc[(p,w,t-1,k),'starts'] + df.loc[(p,w,t-1,k),'starts']*((prices.loc[(p,t),"value"] - prices.loc[(p,t-1),"value"])/prices.loc[(p,t-1),"value"])*pes.loc[p,"p_elast_supply"],0)

                        if w == "Unconventional":
                                avg_s=round(np.maximum(df.loc[(p,w,t-1,k),'avgd_starts']+ 
                                    ex_share*df.loc[(p,w,t-1,k),'avgd_starts']*
                                    ((prices[(prices['prod_type']=='expected_price_Unconventional_{}'.format(k))&(prices['year']==t)]['value'].squeeze() - 
                                    prices[(prices['prod_type']=='expected_price_Unconventional_{}'.format(k))&(prices['year']==t-1)]['value'].squeeze())
                                    / prices[(prices['prod_type']=='expected_price_Unconventional_{}'.format(k))&(prices['year']==t-1)]['value'].squeeze())*pes.loc[p,"p_elast_supply"]+

                                    (1-ex_share)*df.loc[(p,w,t-1,k),'avgd_starts']*
                                    ((prices[(prices['prod_type']=='expected_local_price_Unconventional_{}'.format(k))&(prices['year']==t)]['value'].squeeze() - 
                                    prices[(prices['prod_type']=='expected_local_price_Unconventional_{}'.format(k))&(prices['year']==t-1)]['value'].squeeze())
                                    / prices[(prices['prod_type']=='expected_local_price_Unconventional_{}'.format(k))&(prices['year']==t-1)]['value'].squeeze())*pes.loc[p,"p_elast_supply"],0.0),0)

                                s=round(np.maximum(df.loc[(p,w,t-1,k),'starts']+  
                                    ex_share*df.loc[(p,w,t-1,k),'starts']*
                                    ((prices[(prices['prod_type']=='expected_price_Unconventional_{}'.format(k))&(prices['year']==t)]['value'].squeeze() - 
                                    prices[(prices['prod_type']=='expected_price_Unconventional_{}'.format(k))&(prices['year']==t-1)]['value'].squeeze())
                                    / prices[(prices['prod_type']=='expected_price_Unconventional_{}'.format(k))&(prices['year']==t-1)]['value'].squeeze())*pes.loc[p,"p_elast_supply"]+

                                    (1-ex_share)*df.loc[(p,w,t-1,k),'starts']*
                                    ((prices[(prices['prod_type']=='expected_local_price_Unconventional_{}'.format(k))&(prices['year']==t)]['value'].squeeze() - 
                                    prices[(prices['prod_type']=='expected_local_price_Unconventional_{}'.format(k))&(prices['year']==t-1)]['value'].squeeze())
                                    / prices[(prices['prod_type']=='expected_local_price_Unconventional_{}'.format(k))&(prices['year']==t-1)]['value'].squeeze())*pes.loc[p,"p_elast_supply"],0.0),0)

                        elif w == "Conventional":
                                avg_s = round(np.maximum(0.0, conv_start_gr[conv_start_gr['prod_type']=='{}'.format(k)]['rate'].squeeze()*df.loc[(p,w,t-1,k),'avgd_starts']),0)
                                s =   round(np.maximum(0.0, conv_start_gr[conv_start_gr['prod_type']=='{}'.format(k)]['rate'].squeeze()*df.loc[(p,w,t-1,k),'starts']),0)

                        
                        if df.loc[(p,w,t-1,k),'starts'].squeeze() <= 1.0 or df.loc[(p,w,t-1,k),'avgd_starts'].squeeze() <= 1.0  :
                            avg_s = 0.0
                            s = 0.0

                        prices = prices.set_index(['prod_type','year'])
                        qi1=df.loc[(p,w,t-1,k),'qi']
                        popt_hyp01 = df.loc[(p,w,t-1,k),'popt_hyp0']
                        b1 = df.loc[(p,w,t-1,k),'b']
                        di1 = df.loc[(p,w,t-1,k),'di']
                        wt = [p,w,t,k,s,avg_s,qi1,popt_hyp01,b1,di1]
                        
                        df = df.reset_index()
                        df.loc[len(df)] = wt
                        df = df.set_index(['prod_type','well_type','year','product'])

                        #calculate production from well productivity over time
                        qi = df.loc[(p,w,t-1,k),"qi"]                            
                        b = df.loc[(p,w,t-1,k),"b"]
                        di = df.loc[(p,w,t-1,k),"di"]
                        a_starts = df.loc[(p,w,t-1,k),"avgd_starts"]
                        prod_df = pd.DataFrame(columns = ['prod_type','well_type','product','year','sim_year',"starts","production"])
                        for sy in range(t,t+well_life):
                            pr=hyperbolic(sy-t,qi,b,di)*a_starts
                            h=[p,w,k,t,sy,a_starts,pr]
                            prod_df.loc[sy-t]= h

                        # print(str(t)+p+w+k+str(sy))
                        # print(cumratio)
                        # print(prod_df.loc[(prod_df["year"]==t)&(prod_df["prod_type"]==p)&(prod_df["well_type"]==w)&(prod_df["product"]==k),"production"])
                        # prod_df.loc[(prod_df["year"]==t)&(prod_df["prod_type"]==p)&(prod_df["well_type"]=="Unconventional")&(prod_df["product"]==k),"production"] = (prod_df.loc[(prod_df["year"]==t)&(prod_df["prod_type"]==p)&(prod_df["well_type"]==w)&(prod_df["product"]==k),'production'].transform(lambda x: x*(1-cumratio)))
                        # print(prod_df.loc[(prod_df["year"]==t)&(prod_df["prod_type"]==p)&(prod_df["well_type"]==w)&(prod_df["product"]==k),"production"]) 

                        pp = pp.append(prod_df)
                    
                    #UPSTREAM CAPEX
                    us_capex_df = pd.DataFrame(columns = ['year','prod_type','well_type','product',"us_capex",'starts'])
                    us_capex_df.loc[t]= calculate_us_capex(df,t,p,w,k)
                    cc = cc.append(us_capex_df)
            #gas produced from shale oil wells is flared off - so only a certain percentage is captured
            pp.loc[(pp['prod_type']=='oil')&(pp['product']=='gas')] = 0 

            #sum production by
            mp = pp.groupby(["sim_year",'well_type','product']).agg('sum').reset_index().drop('starts',axis = 1)

            mp['cat_type'] = mp['product']+ "_" + mp['well_type']

            mp = mp.pivot(index="sim_year", columns=["cat_type"],values="production")
            mp = mp.reset_index()

            #convert to mm3 for gas and 1000m3 for oil
            mp['Gas_Conventional']= mp['Gas_Conventional']/1000
            mp['Gas_Unconventional']=mp['Gas_Unconventional']/1000
            mp['Oil_Conventional']=mp['Oil_Conventional']/1000
            mp['Oil_Unconventional']=mp['Oil_Unconventional']/1000

            #add initial production
            mp.loc[-1] = initial_prod_2020_m3
            mp.index = mp.index + 1  # shifting index
            mp.sort_index(inplace=True) 
            mp = mp[yr0-yr0:final_yr-yr0+1]
            # print(mp)

            conventional_gas_decline = np.linspace(conv_prod_decline_start, conv_prod_decline_end_oil,len(mp)).cumsum()
            conventional_oil_decline = np.linspace(conv_prod_decline_start, conv_prod_decline_end_gas,len(mp)).cumsum()
            unconventional_oil_decline = np.linspace(unconv_prod_decline_start, unconv_prod_decline_end_oil,len(mp)).cumsum()
            unconventional_gas_decline = np.linspace(unconv_prod_decline_start, unconv_prod_decline_end_gas,len(mp)).cumsum()

            mp['Conventional_Gas']=(mp['Gas_Conventional'].cumsum())*1000000/1110000 #ktoe
            try:
                mp['Conventional_Gas']= mp['Conventional_Gas'] - mp['Conventional_Gas'].transform(lambda x: max(x,0))*conventional_gas_decline
                mp.loc[mp['Conventional_Gas'] <= 0, 'Conventional_Gas'] =0
            except: 
                mp['Conventional_Gas']=0

            #mp.loc[mp['Conventional_Gas']<=0] = 0.00001
            mp['Unconventional_Gas']=mp['Gas_Unconventional'].cumsum()*1000000/1110000 #ktoe
            try:
                mp['Unconventional_Gas']= mp['Unconventional_Gas'] - mp['Unconventional_Gas'].transform(lambda x: max(x,0))*unconventional_gas_decline
                mp.loc[mp['Unconventional_Gas'] <= 0, 'Unconventional_Gas'] =0
            except: 
                mp['Unconventional_Gas']=0

        
            mp['Conventional_Oil']=mp['Oil_Conventional'].cumsum()*.86 #ktoe (1000/1000 cancels out)
            try:
                mp['Conventional_Oil']= mp['Conventional_Oil'] - mp['Conventional_Oil'].transform(lambda x: max(x,0.00001))*conventional_oil_decline
                mp.loc[mp['Conventional_Oil'] <= 0, 'Conventional_Oil'] =0
            except: 
                mp['Conventional_Oil']=0

            #mp.loc[mp['Conventional_Oil']<=0] = 0.00001
            mp['Unconventional_Oil']=mp['Oil_Unconventional'].cumsum()*.86 #ktoe
            #try:
            
            mp['Unconventional_Oil']= mp['Unconventional_Oil'] - mp['Unconventional_Oil'].transform(lambda x: max(x,0.00001))*unconventional_oil_decline
            
            mp.loc[mp['Unconventional_Oil'] <= 0, 'Unconventional_Oil'] =0
            #except: 
                #mp['Unonventional_Oil']=0
            # print(mp['Unconventional_Oil'])
            # except: 
            # mp['Unonventional_Oil']=0

            mp['Gas_prod'] = mp['Conventional_Gas'] + mp['Unconventional_Gas']
            mp['Oil_prod'] = mp['Conventional_Oil'] + mp['Unconventional_Oil']

            prod = mp[['sim_year','Gas_prod','Oil_prod','Conventional_Gas','Unconventional_Gas','Conventional_Oil','Unconventional_Oil']].rename(columns={'sim_year':'year'})
            cons = cons_df[['year','total_cons','gas_cons','oil_cons','electricity_cons', 'gas_loss_adj','oil_loss_adj','el_loss_adj']]
            #calculate net exports
            exports = pd.merge(prod, cons, on = 'year')

            exports['net_imports_Gas'] = (exports['Gas_prod'] - exports['gas_cons'] + exports['gas_loss_adj']) 
            exports.loc[exports['net_imports_Gas'] > 0, 'net_imports_Gas'] = 0

            exports['net_imports_Oil'] = (exports['Oil_prod'] - exports['oil_cons'] + exports['oil_loss_adj']) 
            exports.loc[exports['net_imports_Oil'] > 0, 'net_imports_Oil'] = 0

            exports['net_export_dem_Gas'] = (gas_export_decline)*(exports['Gas_prod'] - exports['gas_cons'] + exports['gas_loss_adj'])
            exports.loc[exports['net_export_dem_Gas'] < 0, 'net_export_dem_Gas'] = 0 
            exports = exports.assign(gas_ex_cap = gas_export_cap)

            exports.loc[exports['net_export_dem_Gas'] <= exports['gas_ex_cap'],'net_exports_Gas'] = exports['net_export_dem_Gas']          
            exports.loc[exports['net_export_dem_Gas'] > exports['gas_ex_cap'],'net_exports_Gas'] = exports['gas_ex_cap']
            exports['unexportable_gas_prod'] =np.maximum(0.0, exports['net_export_dem_Gas']-exports['gas_ex_cap'])

            exports['net_export_dem_Oil'] = (oil_export_decline)*(exports['Oil_prod'] - exports['oil_cons'] + exports['oil_loss_adj'])
            exports.loc[exports['net_export_dem_Oil'] < 0, 'net_export_dem_Oil'] = 0
            exports = exports.assign(oil_ex_cap = oil_export_cap)

            exports.loc[exports['net_export_dem_Oil'] <= exports['oil_ex_cap'],'net_exports_Oil'] = exports['net_export_dem_Oil'] 
            exports.loc[exports['net_export_dem_Oil'] > exports['oil_ex_cap'],'net_exports_Oil'] = exports['oil_ex_cap']
            exports['unexportable_oil_prod'] = np.maximum(0.0,exports['net_export_dem_Oil']-exports['oil_ex_cap'])

            exports['net_exports_El'] =  -exports['electricity_cons'] + exports['el_loss_adj']

            exports['surplus_Gas'] = exports['Gas_prod']+exports['gas_loss_adj']- exports['net_exports_Gas']-exports['gas_cons'] + exports['unexportable_gas_prod']
            exports.loc[exports['surplus_Gas'] < 0, 'surplus_Gas'] = 0
            exports['surplus_Oil'] = exports['Oil_prod']+exports['oil_loss_adj']- exports['net_exports_Oil']-exports['oil_cons']+ exports['unexportable_oil_prod']
            exports.loc[exports['surplus_Oil'] < 0, 'surplus_Oil'] = 0

            exports['im_ex_Gas'] = exports['net_exports_Gas']+exports['net_imports_Gas']
            exports['im_ex_Oil'] = exports['net_exports_Oil']+exports['net_imports_Oil']

            exports['exports_Unconventional_Gas'] = exports['net_exports_Gas'] *(mp['Unconventional_Gas']/exports['Gas_prod'] )
            exports['exports_Unconventional_Oil'] = exports['net_exports_Oil'] *(mp['Unconventional_Oil']/exports['Oil_prod'] )
            exports['exports_Conventional_Gas'] = exports['net_exports_Gas']-exports['exports_Unconventional_Gas']
            exports['exports_Conventional_Oil'] = exports['net_exports_Oil']-exports['exports_Unconventional_Oil']
            exports['surplus_Unconventional_Gas'] = exports['surplus_Gas'] *(mp['Unconventional_Gas']/exports['Gas_prod'] )
            exports['surplus_Unconventional_Oil'] = exports['surplus_Oil'] *(mp['Unconventional_Oil']/exports['Oil_prod'] )
            exports['surplus_Conventional_Gas'] = exports['surplus_Gas']-exports['surplus_Unconventional_Gas']
            exports['surplus_Conventional_Oil'] = exports['surplus_Oil']-exports['surplus_Unconventional_Oil']
            exports['imports_Unconventional_Gas'] = exports['net_imports_Gas'] *(mp['Unconventional_Gas']/exports['Gas_prod'] )
            exports['imports_Unconventional_Oil'] = exports['net_imports_Oil'] *(mp['Unconventional_Oil']/exports['Oil_prod'] )
            exports['imports_Conventional_Gas'] = exports['net_imports_Gas']-exports['imports_Unconventional_Gas']
            exports['imports_Conventional_Oil'] = exports['net_imports_Oil']-exports['imports_Unconventional_Oil']
            exports['Unconventional_Gas_loss_adj'] = exports['gas_loss_adj'] * (mp['Unconventional_Gas']/exports['Gas_prod'])
            exports['Conventional_Gas_loss_adj'] =  exports['gas_loss_adj'] * (mp['Conventional_Gas']/exports['Gas_prod'])
            exports['Unconventional_Oil_loss_adj'] = exports['oil_loss_adj'] * (mp['Unconventional_Oil']/exports['Oil_prod'])
            exports['Conventional_Oil_loss_adj'] = exports['oil_loss_adj'] * (mp['Conventional_Oil']/exports['Oil_prod'])

            # print(mp.head())
            prices = prices.reset_index()

            #used to append data and prep next year values
            for w in well_type: 
                    for k in product:
                        # print(str(t) +" " + w +" "+ k)
                        #calculate fiscal states
                        fiscal_df = pd.DataFrame(columns = ['year','well_type','product',"price", "intl_pr","ds_capex","opex","domestic revenue","export revenue","production subsidy","import subsidy","royalties","export duties","trade balance"])
                        fiscal_df.loc[t] = calculate_state(t,w,k)
                        fiscal = fiscal.append(fiscal_df)
                        # print(cc[['year','prod_type','well_type','product']])
                        # print(cc.columns)
                        #make responsive to changes in the surplus exports v imports
                        
                        # ratio = safe_div(exports.loc[(exports['year']==t),'surplus_{}_{}'.format(w,k)].squeeze(),exports.loc[(exports['surplus_{}_{}'.format(w,k)]>1).idxmax,'surplus_{}_{}'.format(w,k)].squeeze())
                        ratio = safe_div(exports.loc[(exports['year']==t),'surplus_{}'.format(k)].squeeze(),exports.loc[(exports['year']==t),'{}_prod'.format(k)].squeeze())

                        cumratio +=ratio

                        if exports.loc[(exports['year']==t),'surplus_{}'.format(k)].squeeze() > 1.0:
                            prices.loc[(prices['year']==t+1)&(prices['prod_type']=='expected_price_Unconventional_{}'.format(k)),'value'] = (prices.loc[(prices['year']==t)&(prices['prod_type']=='expected_price_Unconventional_{}'.format(k)),'value'].squeeze() -
                                                                                                                                (1-1/(1+ratio))*responsiveness[responsiveness['prod_type']=='{}'.format(k)]['rate'].squeeze()*prices.loc[(prices['year']==t)&(prices['prod_type']=='expected_price_Unconventional_{}'.format(k)),'value'].squeeze())
                        
                        # (pow(ratio,well_response[well_response['prod_type']=='{}'.format(k)]['rate'].squeeze()))                                                                                                                    
                            prices.loc[(prices['year']==t+1)&(prices['prod_type']=='expected_local_price_Unconventional_{}'.format(k)),'value'] = (prices.loc[(prices['year']==t)&(prices['prod_type']=='expected_local_price_Unconventional_{}'.format(k)),'value'].squeeze() -
                                                                                                                                (1-1/(1+ratio))*responsiveness[responsiveness['prod_type']=='{}'.format(k)]['rate'].squeeze()*prices.loc[(prices['year']==t)&(prices['prod_type']=='expected_local_price_Unconventional_{}'.format(k)),'value'].squeeze())
                        
                        #print(prices.loc[(prices['year']==t+1)&(prices['prod_type']=='expected_local_price_{}_{}'.format(w,k)),'value'].squeeze())
                        else:
                            # prices.loc[(prices['year']==t+1)&(prices['prod_type']=='expected_price_Conventional_{}'.format(k)),'value'] = 1/2*(prices.loc[(prices['year']==t+1)&(prices['prod_type']=='{} ktoe'.format(k)),'value'].squeeze() + prices.loc[(prices['year']==t)&(prices['prod_type']=='expected_price_Unconventional_{}'.format(k)),'value'].squeeze())             
                            # prices.loc[(prices['year']==t+1)&(prices['prod_type']=='expected_local_price_Conventional_{}'.format(k)),'value'] = 1/2*(prices.loc[(prices['year']==t+1)&(prices['prod_type']=='{} Local ktoe'.format(k)),'value'].squeeze()+ prices.loc[(prices['year']==t)&(prices['prod_type']=='expected_local_price_Unconventional_{}'.format(k)),'value'].squeeze())
                            prices.loc[(prices['year']==t+1)&(prices['prod_type']=='expected_price_Unconventional_{}'.format(k)),'value'] =  1/2*(prices.loc[(prices['year']==t+1)&(prices['prod_type']=='{} ktoe'.format(k)),'value'].squeeze()+(prices.loc[(prices['year']==t)&(prices['prod_type']=='expected_price_Unconventional_{}'.format(k)),'value'].squeeze() -
                                                                                                                                (1-1/(1+ratio))*responsiveness[responsiveness['prod_type']=='{}'.format(k)]['rate'].squeeze()*prices.loc[(prices['year']==t)&(prices['prod_type']=='expected_price_Unconventional_{}'.format(k)),'value'].squeeze()))
                            prices.loc[(prices['year']==t+1)&(prices['prod_type']=='expected_local_price_Unconventional_{}'.format(k)),'value'] =  1/2*(prices.loc[(prices['year']==t+1)&(prices['prod_type']=='{} Local ktoe'.format(k)),'value'].squeeze()+(prices.loc[(prices['year']==t)&(prices['prod_type']=='expected_local_price_Unconventional_{}'.format(k)),'value'].squeeze() -
                                                                                                                                (1-1/(1+ratio))*responsiveness[responsiveness['prod_type']=='{}'.format(k)]['rate'].squeeze()*prices.loc[(prices['year']==t)&(prices['prod_type']=='expected_local_price_Unconventional_{}'.format(k)),'value'].squeeze()))

            for w in well_type: 
                for p in production_type: 
                        #calculate new export shares
                        export_share.loc[(export_share['prod_type']=='{}'.format(p)),'rate'] = safe_div(exports[(exports['year']==t)]['net_exports_{}'.format(p)].squeeze(),exports[(exports['year']==t)]['{}_prod'.format(p)].squeeze())
                        # print('export share')
                        # print(exports[(exports['year']==t)]['net_exports_{}'.format(p)].squeeze())
                        # print(exports[(exports['year']==t)]['{}_prod'.format(p)].squeeze())                        
                      
    # prices.to_csv(outdir+'prices.csv')    
    #merge US capex with downstresam Fiscal befor calculating 
    cc = cc.drop(columns = 'product').rename(columns = {'prod_type':'product'}).set_index(['year','well_type','product'])
    fiscal = fiscal.set_index(['year','well_type','product']).join(cc, on = ['year','well_type','product'], how= 'outer')

    # discount factor calculation
    fiscal=fiscal.reset_index()
    fiscal['discount_factor'] = 1/(1*(1 + wacc)**(fiscal['year']-yr0-1))

    ############################
    #   data for macro model   #
    ############################
    # fiscal['col_name'] = fiscal['product']+ "_" + fiscal['well_type']
    fiscal['total_capex'] = fiscal['us_capex'] + fiscal['ds_capex'] 
    fiscal2 = fiscal.reset_index().groupby(['year', 'product']).agg({
        'price':'first',    # Sum duration per group
        'intl_pr':'first',    # Sum duration per group
        'total_capex':sum,    # Sum duration per group
        'ds_capex':sum,    # Sum duration per group
        'opex':sum,    # Sum duration per group
        'domestic revenue':sum,    # Sum duration per group
        'export revenue':sum,    # Sum duration per group
        'production subsidy':sum,    # Sum duration per group
        'import subsidy':sum,    # Sum duration per group
        'royalties':sum,    # Sum duration per group
        'export duties':sum,    # Sum duration per group
        'trade balance':sum,    # Sum duration per group
        'us_capex':sum,    # Sum duration per group
        'starts':sum,    # Sum duration per grou
        'discount_factor': 'first'    # Sum duration per grou
        }).reset_index()
    # print(fiscal2.head())
    macro_inputs = fiscal2.pivot(index="year", columns=["product"],values=["price","intl_pr","ds_capex",'opex','domestic revenue','export revenue','production subsidy','import subsidy','royalties','export duties','trade balance','us_capex','starts','discount_factor', 'total_capex'])  
   
    # fiscal_collist = [' '.join(col).strip() for col in macro_inputs.columns.values]
    macro_inputs.columns = [' '.join(col).strip() for col in macro_inputs.columns.values]
    macro_inputs.reset_index(inplace=True)
    macro_inputs.columns = macro_inputs.columns.to_flat_index()
    exports2 = exports[['year','Gas_prod','Oil_prod','gas_cons', 'oil_cons','im_ex_Gas','im_ex_Oil']]
    macro_inputs = macro_inputs.merge(exports2, left_on='year', right_on='year')
    # column_names=['year','price_Gas','price_Oil', 'intl_pr_Gas','intl_pr_Oil','ds_capex_Gas','ds_capex_Oil','opex_Gas','opex_Oil','domestic revenue_Gas','domestic revenue_Oil','export revenue_Gas','export revenue_Oil','production subsidy_Gas','production subsidy_Oil','import subsidy_Gas','import subsidy_Oil','royalties_Gas','royalties_Oil','export duties_Gas','export duties_Oil','trade balance_Gas','trade balance_Oil','us_capex_Gas','us_capex_Oil','total_capex_Gas','total_capex_Oil', 'Gas_prod',	'Oil_prod',	'gas_cons',	'oil_cons','electricity_cons','im_ex_Gas','im_ex_Oil']

    # opex Gas	opex Oil	domestic revenue Gas	domestic revenue Oil	export revenue Gas	export revenue Oil	production subsidy Gas	production subsidy Oil	import subsidy Gas	import subsidy Oil	royalties Gas	royalties Oil	export duties Gas	export duties Oil	trade balance Gas	trade balance Oil	total_capex Gas	total_capex Oil

    #calculate profit tax adapted from IDB study : https://publications.iadb.org/publications/english/document/High-and-Dry-Stranded-Natural-Gas-Reserves-and-Fiscal-Revenues-in-Latin-America-and-the-Caribbean.pdf
    # taxe
    macro_inputs['profit tax Oil'] = (((macro_inputs['domestic revenue Oil']+macro_inputs['export revenue Oil'])*(1-royalty_rate_oil))-(macro_inputs["opex Oil"]+macro_inputs['ds_capex Oil']*(1-public_ds_capex_share)+macro_inputs['us_capex Oil'])-macro_inputs["production subsidy Oil"])*profit_tax_rate
    macro_inputs['profit tax Gas'] = (((macro_inputs["domestic revenue Gas"]+macro_inputs['export revenue Gas'])*(1-royalty_rate_gas))-(macro_inputs["opex Gas"]+macro_inputs['ds_capex Gas']*(1-public_ds_capex_share)+macro_inputs['us_capex Gas'])-macro_inputs["production subsidy Gas"])*profit_tax_rate
    macro_inputs.loc[macro_inputs['profit tax Gas'] <= 0, 'profit tax Gas'] =0
    macro_inputs.loc[macro_inputs['profit tax Oil'] <= 0, 'profit tax Oil'] =0

    # This is a hack because the model is looping through the trade balance caluclation twice (for unconventional and conventional, but im_ex_ is already aggregated from conventional/unconventional
    macro_inputs['trade balance Oil'] = macro_inputs['trade balance Oil']/2
    macro_inputs['trade balance Gas'] = macro_inputs['trade balance Gas']/2

    #for francis 
    macro_inputs['production subsidy Gas'] = macro_inputs['production subsidy Gas']*-1
    macro_inputs['production subsidy Oil'] = macro_inputs['production subsidy Oil']*-1
 
    #convert to $/ bbl and $/mmbtu
    macro_inputs['price_Gas_mmbtu'] = macro_inputs['price Gas']/39652
    macro_inputs['intl_pr_Gas_mmbtu']= macro_inputs['intl_pr Gas']/39652
    macro_inputs['price_Oil_bbl'] = macro_inputs['price Oil']/7330
    macro_inputs['intl_pr_Oil_bbl'] = macro_inputs['intl_pr Oil']/7330  
    macro_inputs['Gas_prod_mmbtu'] = macro_inputs['Gas_prod']*39652
    macro_inputs['gas_cons_mmbtu'] = macro_inputs['gas_cons']*39652
    macro_inputs['im_ex_Gas_mmbtu'] = macro_inputs['im_ex_Gas']*39652
    macro_inputs['Oil_prod_bbl'] = macro_inputs['Oil_prod']*7330
    macro_inputs['oil_cons_bbl'] = macro_inputs['oil_cons']*7330
    macro_inputs['im_ex_Oil_bbl'] = macro_inputs['im_ex_Oil']*7330
    macro_inputs['foreign_capex Oil'] = macro_inputs['total_capex Oil']*foreign_capex_share
    macro_inputs['foreign_capex Gas'] = macro_inputs['total_capex Gas']*foreign_capex_share

    macro_inputs = macro_inputs[['year','price_Gas_mmbtu','intl_pr_Gas_mmbtu','price_Oil_bbl','intl_pr_Oil_bbl',
                                'opex Gas','opex Oil','domestic revenue Gas','domestic revenue Oil','export revenue Gas','export revenue Oil',
                                'profit tax Oil', 'profit tax Gas',
                                'production subsidy Gas','production subsidy Oil','import subsidy Gas','import subsidy Oil',
                                'royalties Gas','royalties Oil','export duties Gas','export duties Oil',
                                'trade balance Gas','trade balance Oil','total_capex Gas','total_capex Oil','foreign_capex Gas','foreign_capex Oil',
                                'Gas_prod_mmbtu','gas_cons_mmbtu','im_ex_Gas_mmbtu',
                                'Oil_prod_bbl','oil_cons_bbl','im_ex_Oil_bbl']]

    #######################
    #   outputs for RDM   #
    #######################
    fiscal = fiscal.set_index(['year','well_type','product'])

    #process fiscal for Charl
    # macro_inputs = fiscal.pivot_table(index="year", 
    #                 columns=['well_type','product'], 
    #                 values=['price','total_capex','opex','domestic revenue','export revenue','production subsidy','import subsidy','royalties','export duties','starts','trade balance'])
    # # macro_inputs = pd.concat([macro_inputs,exports], axis = 1)

    finance = pd.DataFrame(index = fiscal.index)

    #split public and private share of downstream capex
    finance['public_ds_capex'] = public_ds_capex_share*fiscal['ds_capex']
    finance['private_ds_capex'] =(1-public_ds_capex_share)*fiscal['ds_capex']

    #profit tax
    finance['profit tax'] = (((fiscal["domestic revenue"]+fiscal["export revenue"])*(1-royalty_rate_gas))-fiscal["opex"]-finance["private_ds_capex"]-fiscal["us_capex"]+fiscal["production subsidy"])*profit_tax_rate
    finance.loc[finance['profit tax'] <= 0, 'profit tax'] =0

    # FT as % GDP
    finance['subsidies'] = fiscal['production subsidy']+fiscal['import subsidy']
    finance['govt_income'] = fiscal['export duties'] + fiscal['royalties'] + finance['profit tax']
    finance['total gov transfers'] = finance['govt_income'] - finance['subsidies'] - finance['public_ds_capex'] 
    # finance['total gov transfers no imports'] = fiscal['export duties'] + fiscal['royalties']-fiscal['production subsidy']
    total_ft_gdp = ((fiscal['discount_factor']*finance['total gov transfers']).sum())/GDP*100

    #Subsidized NPV as % 
    finance['disc_revenue'] = fiscal['discount_factor'] *(fiscal['domestic revenue'] + fiscal['export revenue']+finance['subsidies']-finance['govt_income'])
    finance['disc_exp']= fiscal['discount_factor'] *(fiscal['us_capex'] + finance['private_ds_capex']+ fiscal['opex'])
    finance['disc_net_rev'] = finance['disc_revenue'] - finance['disc_exp']
    npv_gdp = (finance['disc_net_rev'].sum())/GDP*100

    #Unsubsidized npv NPV as % GDP
    finance['disc_private_unsub_revenue'] = fiscal['discount_factor']*(fiscal['domestic revenue'] + fiscal['export revenue'])
    finance['disc_exp']= fiscal['discount_factor'] *(fiscal['us_capex'] + finance['private_ds_capex']+ fiscal['opex'])
    finance['disc_net_unsub_rev'] = finance['disc_private_unsub_revenue'] - finance['disc_exp']
    npv_unsub_gdp = (finance['disc_net_unsub_rev'].sum())/GDP*100
    
    #NPV and FT a by production type
    subcomponents_ft_gdp = finance.reset_index().groupby(['well_type','product'])['total gov transfers'].agg('sum')/GDP*100
    subcomponents_npv_gdp = finance.reset_index().groupby(['well_type','product'])['disc_net_rev'].agg('sum')/GDP*100

    gdp_npv_conv_gas = subcomponents_npv_gdp[0]
    gdp_npv_conv_oil = subcomponents_npv_gdp[1]
    gdp_npv_unconv_gas = subcomponents_npv_gdp[2]
    gdp_npv_unconv_oil = subcomponents_npv_gdp[3]

    ft_npv_conv_gas = subcomponents_ft_gdp[0]
    ft_npv_conv_oil = subcomponents_ft_gdp[1]
    ft_npv_unconv_gas = subcomponents_ft_gdp[2]
    ft_npv_unconv_oil = subcomponents_ft_gdp[3]

    #total wells
    wells_output = df['avgd_starts'].groupby(['prod_type','well_type']).sum()
    wells_total = df['avgd_starts'].sum()

    try: 
        finance.to_csv(outdir+'finance_{}_{}.csv'.format(rcp, switch))
        fiscal.to_csv(outdir+"fiscal_{}_{}.csv".format(rcp, switch))
        cc.to_csv(outdir+"us_capex_{}_{}.csv".format(rcp, switch))
        cons.to_csv(outdir+"consumption_{}_{}.csv".format(rcp, switch))
        exports.to_csv(outdir+"exports_{}_{}.csv".format(rcp, switch))
        macro_inputs.to_csv(outdir+"macro_inputs_{}_{}.csv".format(rcp, switch))
        #note this value is about 10k ktoe below minem for 2020 because it excludes own consumption. Could add to match + keep same going forward
        cons_df.to_csv(outdir+'consumption forecast_{}_{}.csv'.format(rcp, switch))
        pp.to_csv(outdir+'production_per_well_year_{}_{}.csv'.format(rcp, switch))
        prices.to_csv(outdir+"prices_{}_{}.csv".format(rcp, switch))
        mp.to_csv(outdir+"production_{}_{}.csv".format(rcp, switch))
    except: 
        print('open csv could not save results')

    return npv_gdp, npv_unsub_gdp, total_ft_gdp, wells_total, gdp_npv_conv_gas,gdp_npv_conv_oil,gdp_npv_unconv_gas,gdp_npv_unconv_oil, ft_npv_conv_gas, ft_npv_conv_oil, ft_npv_unconv_gas, ft_npv_unconv_oil

# ##run macro scenarios - domestic price remains subsidized, incentives for unconventional oil and gas  

#base - continued demand   

mp2050_075 = VacaMuerta(yr0 = 2020, final_yr = 2050, model = 'WB', rcp = 'CURR', switch = 'pessimistic_075',pes_oil = 1.2,pes_gas = .9,
    a_gas_res = .005, a_oil_res = .005, a_el_res = .005 ,a_gas_ind = .005, a_oil_ind = .005,a_el_ind = .005,a_gas_trans = .005,a_oil_trans = .005,a_el_trans = .005,
    l= 10.0, t_rate_gas = 0.02, t_rate_oil = 0.0, t_rate_e  = .01,
    us_capex_gas = 7100000, us_capex_oil = 7100000, 
    m = 9542, oil_opex = (6.7/.000146),  gas_opex = (17.29/.000146), prod_subsidy_p_ratio=1.3, 
    share_covered = .17, royalty_rate_gas = .12, royalty_rate_oil = .12, duty_rate_gas = .08, duty_rate_oil = .08, 
    price_threshold_gas = 5.0*39652.61, price_threshold_oil = 60.0*7330, price_floor_gas = 3.75*39652.61, price_floor_oil = 45.0*7330, public_ds_capex_share = 0.67,
    T_bond_rate = .0245, arg_sov_risk = .0315, opp_cost_own_finance = .1029, share_own_capital =  .6803, opp_cost_debt =  .0312, GDP = 383100000000, 
    export_share_oil = .18, export_share_gas =.0,  
    gas_export_dem_start = 1.0, oil_export_dem_start = 1.0, gas_export_dem_end = 1.0, oil_export_dem_end = 1.0, gas_demand_decline_speed = 20, oil_demand_decline_speed = 20, 
    gas_ex_cap_start = 1905, gas_ex_cap_end= 42795, gas_ex_cap_increase = 30,oil_ex_cap_start= 33215, oil_ex_cap_end= 76650, oil_ex_cap_increase = 3,
    conv_start_gr_gas  = 0.0, conv_start_gr_oil  = 0.0, conv_prod_decline_start =.06, conv_prod_decline_end_gas =.06, conv_prod_decline_end_oil =.06, 
    unconv_prod_decline_start =.00, unconv_prod_decline_end_gas =.00, unconv_prod_decline_end_oil =.00,
    cons_wedge_start_gas = 1.5, cons_wedge_end_gas = 1.5, cons_wedge_start_oil = 1.5, cons_wedge_end_oil = 1.5,
    intl_wedge_start_gas = 1.5,  intl_wedge_end_gas = 1.5, intl_wedge_start_oil = 1.5, intl_wedge_end_oil = 1.5, discount = .075 )  

mp2050_15_075 = VacaMuerta(yr0 = 2020, final_yr = 2050, model = 'WB', rcp = '1.5', switch = 'optimistic_075',pes_oil = 1.2,pes_gas = .9,
    a_gas_res = .02, a_oil_res = .02, a_el_res = .02, a_gas_ind = .02,a_oil_ind = .02,a_el_ind = .02,a_gas_trans = .02,a_oil_trans = .02,a_el_trans = .02,
    l= 10.0, t_rate_gas = -0.01, t_rate_oil = -0.01, t_rate_e  = .03,
    us_capex_gas = 7100000, us_capex_oil = 7100000, 
    m = 9542*2, oil_opex = (6.7/.000146),  gas_opex = (17.29/.000146),  prod_subsidy_p_ratio=1.3,
    share_covered = .17, royalty_rate_gas = .12, royalty_rate_oil = .12, duty_rate_gas = .08, duty_rate_oil = .08, 
    price_threshold_gas = 5.0*39652.61, price_threshold_oil = 60.0*7330, price_floor_gas = 3.75*39652.61, price_floor_oil = 45.0*7330, 
    T_bond_rate = .0245, arg_sov_risk = .0315, opp_cost_own_finance = .1029, share_own_capital =  .6803, opp_cost_debt =  .0312, GDP = 383100000000,public_ds_capex_share = 0.67, 
    export_share_oil = 0.18, export_share_gas =.0,  
    gas_export_dem_start = 1.0, oil_export_dem_start = 1.0, gas_export_dem_end = 0.0, oil_export_dem_end = 0.0, gas_demand_decline_speed = 10, oil_demand_decline_speed = 10, 
    gas_ex_cap_start = 1905, gas_ex_cap_end= 4631, gas_ex_cap_increase = 3,oil_ex_cap_start= 33215, oil_ex_cap_end= 33215, oil_ex_cap_increase = 3,
    conv_start_gr_gas  = 0.0, conv_start_gr_oil  = 0.0, conv_prod_decline_start =.06, conv_prod_decline_end_gas =.06, conv_prod_decline_end_oil =.06, 
    unconv_prod_decline_start =.00, unconv_prod_decline_end_gas =.06, unconv_prod_decline_end_oil =.05,
    cons_wedge_start_gas = 1.5, cons_wedge_end_gas = 1, cons_wedge_start_oil = 1.5, cons_wedge_end_oil = 1,
    intl_wedge_start_gas = 1.5,  intl_wedge_end_gas =1, intl_wedge_start_oil = 1.5, intl_wedge_end_oil = 1, discount =.075)

mp2050_lock_075 = VacaMuerta(yr0 = 2020, final_yr = 2050, model = 'WB', rcp = '1.5', switch = 'lock_in_075',pes_oil = 1.2,pes_gas = .9,
    a_gas_res = .02, a_oil_res = .02, a_el_res = .02, a_gas_ind = .02,a_oil_ind = .02,a_el_ind = .02,a_gas_trans = .02,a_oil_trans = .02,a_el_trans = .02,
    l= 10.0, t_rate_gas = -0.01, t_rate_oil = -0.01, t_rate_e  = .03,
    us_capex_gas = 7100000, us_capex_oil = 7100000, 
    m = 9542*2, oil_opex = (6.7/.000146),  gas_opex = (17.29/.000146), prod_subsidy_p_ratio=1.3, 
    share_covered = .17, royalty_rate_gas = .12, royalty_rate_oil = .12, duty_rate_gas = .08, duty_rate_oil = .08, 
    price_threshold_gas = 5.0*39652.61, price_threshold_oil = 60.0*7330, price_floor_gas = 3.75*39652.61, price_floor_oil = 45.0*7330, public_ds_capex_share = 0.67,
    T_bond_rate = .0245, arg_sov_risk = .0315, opp_cost_own_finance = .1029, share_own_capital =  .6803, opp_cost_debt =  .0312, GDP = 383100000000, 
    export_share_oil = .18, export_share_gas =.0,  
    gas_export_dem_start = 1.0, oil_export_dem_start = 1.0, gas_export_dem_end = 0.0, oil_export_dem_end = 0.0, gas_demand_decline_speed = 10, oil_demand_decline_speed = 10, 
    gas_ex_cap_start = 1905, gas_ex_cap_end= 42795, gas_ex_cap_increase = 30,oil_ex_cap_start= 33215, oil_ex_cap_end= 76650, oil_ex_cap_increase = 3,
    conv_start_gr_gas  = 0.0, conv_start_gr_oil  = 0.0, conv_prod_decline_start =.06, conv_prod_decline_end_gas =.06, conv_prod_decline_end_oil =.06, 
    unconv_prod_decline_start =.00, unconv_prod_decline_end_gas =.00, unconv_prod_decline_end_oil =.00,
    cons_wedge_start_gas = 1.5, cons_wedge_end_gas = 5, cons_wedge_start_oil = 1.5, cons_wedge_end_oil = 5,
    intl_wedge_start_gas = 1.5,  intl_wedge_end_gas = 5, intl_wedge_start_oil = 1.5, intl_wedge_end_oil = 4, discount = .075)  

mp2050_06 = VacaMuerta(yr0 = 2020, final_yr = 2050, model = 'WB', rcp = 'CURR', switch = 'pessimistic_06',pes_oil = 1.2,pes_gas = .9,
    a_gas_res = .005, a_oil_res = .005, a_el_res = .005 ,a_gas_ind = .005, a_oil_ind = .005,a_el_ind = .005,a_gas_trans = .005,a_oil_trans = .005,a_el_trans = .005,
    l= 10.0, t_rate_gas = 0.02, t_rate_oil = 0.0, t_rate_e  = .01,
    us_capex_gas = 7100000, us_capex_oil = 7100000, 
    m = 9542, oil_opex = (6.7/.000146),  gas_opex = (17.29/.000146), prod_subsidy_p_ratio=1.3, 
    share_covered = .17, royalty_rate_gas = .12, royalty_rate_oil = .12, duty_rate_gas = .08, duty_rate_oil = .08, 
    price_threshold_gas = 5.0*39652.61, price_threshold_oil = 60.0*7330, price_floor_gas = 3.75*39652.61, price_floor_oil = 45.0*7330, public_ds_capex_share = 0.67,
    T_bond_rate = .0245, arg_sov_risk = .0315, opp_cost_own_finance = .1029, share_own_capital =  .6803, opp_cost_debt =  .0312, GDP = 383100000000, 
    export_share_oil = .18, export_share_gas =.0,  
    gas_export_dem_start = 1.0, oil_export_dem_start = 1.0, gas_export_dem_end = 1.0, oil_export_dem_end = 1.0, gas_demand_decline_speed = 20, oil_demand_decline_speed = 20, 
    gas_ex_cap_start = 1905, gas_ex_cap_end= 42795, gas_ex_cap_increase = 30,oil_ex_cap_start= 33215, oil_ex_cap_end= 76650, oil_ex_cap_increase = 3,
    conv_start_gr_gas  = 0.0, conv_start_gr_oil  = 0.0, conv_prod_decline_start =.06, conv_prod_decline_end_gas =.06, conv_prod_decline_end_oil =.06, 
    unconv_prod_decline_start =.00, unconv_prod_decline_end_gas =.00, unconv_prod_decline_end_oil =.00,
    cons_wedge_start_gas = 1.5, cons_wedge_end_gas = 1.5, cons_wedge_start_oil = 1.5, cons_wedge_end_oil = 1.5,
    intl_wedge_start_gas = 1.5,  intl_wedge_end_gas = 1.5, intl_wedge_start_oil = 1.5, intl_wedge_end_oil = 1.5, discount = .06)  

mp2050_15_06 = VacaMuerta(yr0 = 2020, final_yr = 2050, model = 'WB', rcp = '1.5', switch = 'optimistic_06',pes_oil = 1.2,pes_gas = .9,
    a_gas_res = .02, a_oil_res = .02, a_el_res = .02, a_gas_ind = .02,a_oil_ind = .02,a_el_ind = .02,a_gas_trans = .02,a_oil_trans = .02,a_el_trans = .02,
    l= 10.0, t_rate_gas = -0.01, t_rate_oil = -0.01, t_rate_e  = .03,
    us_capex_gas = 7100000, us_capex_oil = 7100000, 
    m = 9542*2, oil_opex = (6.7/.000146),  gas_opex = (17.29/.000146),  prod_subsidy_p_ratio=1.3,
    share_covered = .17, royalty_rate_gas = .12, royalty_rate_oil = .12, duty_rate_gas = .08, duty_rate_oil = .08, 
    price_threshold_gas = 5.0*39652.61, price_threshold_oil = 60.0*7330, price_floor_gas = 3.75*39652.61, price_floor_oil = 45.0*7330, 
    T_bond_rate = .0245, arg_sov_risk = .0315, opp_cost_own_finance = .1029, share_own_capital =  .6803, opp_cost_debt =  .0312, GDP = 383100000000,public_ds_capex_share = 0.67, 
    export_share_oil = 0.18, export_share_gas =.0,  
    gas_export_dem_start = 1.0, oil_export_dem_start = 1.0, gas_export_dem_end = 0.0, oil_export_dem_end = 0.0, gas_demand_decline_speed = 10, oil_demand_decline_speed = 10, 
    gas_ex_cap_start = 1905, gas_ex_cap_end= 4631, gas_ex_cap_increase = 3,oil_ex_cap_start= 33215, oil_ex_cap_end= 33215, oil_ex_cap_increase = 3,
    conv_start_gr_gas  = 0.0, conv_start_gr_oil  = 0.0, conv_prod_decline_start =.06, conv_prod_decline_end_gas =.06, conv_prod_decline_end_oil =.06, 
    unconv_prod_decline_start =.00, unconv_prod_decline_end_gas =.06, unconv_prod_decline_end_oil =.05,
    cons_wedge_start_gas = 1.5, cons_wedge_end_gas = 1, cons_wedge_start_oil = 1.5, cons_wedge_end_oil = 1,
    intl_wedge_start_gas = 1.5,  intl_wedge_end_gas =1, intl_wedge_start_oil = 1.5, intl_wedge_end_oil = 1, discount =.06)

mp2050_lock_06 = VacaMuerta(yr0 = 2020, final_yr = 2050, model = 'WB', rcp = '1.5', switch = 'lock_in_06',pes_oil = 1.2,pes_gas = .9,
    a_gas_res = .02, a_oil_res = .02, a_el_res = .02, a_gas_ind = .02,a_oil_ind = .02,a_el_ind = .02,a_gas_trans = .02,a_oil_trans = .02,a_el_trans = .02,
    l= 10.0, t_rate_gas = -0.01, t_rate_oil = -0.01, t_rate_e  = .03,
    us_capex_gas = 7100000, us_capex_oil = 7100000, 
    m = 9542*2, oil_opex = (6.7/.000146),  gas_opex = (17.29/.000146), prod_subsidy_p_ratio=1.3, 
    share_covered = .17, royalty_rate_gas = .12, royalty_rate_oil = .12, duty_rate_gas = .08, duty_rate_oil = .08, 
    price_threshold_gas = 5.0*39652.61, price_threshold_oil = 60.0*7330, price_floor_gas = 3.75*39652.61, price_floor_oil = 45.0*7330, public_ds_capex_share = 0.67,
    T_bond_rate = .0245, arg_sov_risk = .0315, opp_cost_own_finance = .1029, share_own_capital =  .6803, opp_cost_debt =  .0312, GDP = 383100000000, 
    export_share_oil = .18, export_share_gas =.0,  
    gas_export_dem_start = 1.0, oil_export_dem_start = 1.0, gas_export_dem_end = 0.0, oil_export_dem_end = 0.0, gas_demand_decline_speed = 10, oil_demand_decline_speed = 10, 
    gas_ex_cap_start = 1905, gas_ex_cap_end= 42795, gas_ex_cap_increase = 30,oil_ex_cap_start= 33215, oil_ex_cap_end= 76650, oil_ex_cap_increase = 3,
    conv_start_gr_gas  = 0.0, conv_start_gr_oil  = 0.0, conv_prod_decline_start =.06, conv_prod_decline_end_gas =.06, conv_prod_decline_end_oil =.06, 
    unconv_prod_decline_start =.00, unconv_prod_decline_end_gas =.00, unconv_prod_decline_end_oil =.00,
    cons_wedge_start_gas = 1.5, cons_wedge_end_gas = 5, cons_wedge_start_oil = 1.5, cons_wedge_end_oil = 5,
    intl_wedge_start_gas = 1.5,  intl_wedge_end_gas = 5, intl_wedge_start_oil = 1.5, intl_wedge_end_oil = 4, discount = .06) 

mp2050_045 = VacaMuerta(yr0 = 2020, final_yr = 2050, model = 'WB', rcp = 'CURR', switch = 'pessimistic_045',pes_oil = 1.2,pes_gas = .9,
    a_gas_res = .005, a_oil_res = .005, a_el_res = .005 ,a_gas_ind = .005, a_oil_ind = .005,a_el_ind = .005,a_gas_trans = .005,a_oil_trans = .005,a_el_trans = .005,
    l= 10.0, t_rate_gas = 0.02, t_rate_oil = 0.0, t_rate_e  = .01,
    us_capex_gas = 7100000, us_capex_oil = 7100000, 
    m = 9542, oil_opex = (6.7/.000146),  gas_opex = (17.29/.000146), prod_subsidy_p_ratio=1.3, 
    share_covered = .17, royalty_rate_gas = .12, royalty_rate_oil = .12, duty_rate_gas = .08, duty_rate_oil = .08, 
    price_threshold_gas = 5.0*39652.61, price_threshold_oil = 60.0*7330, price_floor_gas = 3.75*39652.61, price_floor_oil = 45.0*7330, public_ds_capex_share = 0.67,
    T_bond_rate = .0245, arg_sov_risk = .0315, opp_cost_own_finance = .1029, share_own_capital =  .6803, opp_cost_debt =  .0312, GDP = 383100000000, 
    export_share_oil = .18, export_share_gas =.0,  
    gas_export_dem_start = 1.0, oil_export_dem_start = 1.0, gas_export_dem_end = 1.0, oil_export_dem_end = 1.0, gas_demand_decline_speed = 20, oil_demand_decline_speed = 20, 
    gas_ex_cap_start = 1905, gas_ex_cap_end= 42795, gas_ex_cap_increase = 30,oil_ex_cap_start= 33215, oil_ex_cap_end= 76650, oil_ex_cap_increase = 3,
    conv_start_gr_gas  = 0.0, conv_start_gr_oil  = 0.0, conv_prod_decline_start =.06, conv_prod_decline_end_gas =.06, conv_prod_decline_end_oil =.06, 
    unconv_prod_decline_start =.00, unconv_prod_decline_end_gas =.00, unconv_prod_decline_end_oil =.00,
    cons_wedge_start_gas = 1.5, cons_wedge_end_gas = 1.5, cons_wedge_start_oil = 1.5, cons_wedge_end_oil = 1.5,
    intl_wedge_start_gas = 1.5,  intl_wedge_end_gas = 1.5, intl_wedge_start_oil = 1.5, intl_wedge_end_oil = 1.5, discount = .045 )  

mp2050_15_045 = VacaMuerta(yr0 = 2020, final_yr = 2050, model = 'WB', rcp = '1.5', switch = 'optimistic_045',pes_oil = 1.2,pes_gas = .9,
    a_gas_res = .02, a_oil_res = .02, a_el_res = .02, a_gas_ind = .02,a_oil_ind = .02,a_el_ind = .02,a_gas_trans = .02,a_oil_trans = .02,a_el_trans = .02,
    l= 10.0, t_rate_gas = -0.01, t_rate_oil = -0.01, t_rate_e  = .03,
    us_capex_gas = 7100000, us_capex_oil = 7100000, 
    m = 9542*2, oil_opex = (6.7/.000146),  gas_opex = (17.29/.000146),  prod_subsidy_p_ratio=1.3,
    share_covered = .17, royalty_rate_gas = .12, royalty_rate_oil = .12, duty_rate_gas = .08, duty_rate_oil = .08, 
    price_threshold_gas = 5.0*39652.61, price_threshold_oil = 60.0*7330, price_floor_gas = 3.75*39652.61, price_floor_oil = 45.0*7330, 
    T_bond_rate = .0245, arg_sov_risk = .0315, opp_cost_own_finance = .1029, share_own_capital =  .6803, opp_cost_debt =  .0312, GDP = 383100000000,public_ds_capex_share = 0.67, 
    export_share_oil = 0.18, export_share_gas =.0,  
    gas_export_dem_start = 1.0, oil_export_dem_start = 1.0, gas_export_dem_end = 0.0, oil_export_dem_end = 0.0, gas_demand_decline_speed = 10, oil_demand_decline_speed = 10, 
    gas_ex_cap_start = 1905, gas_ex_cap_end= 4631, gas_ex_cap_increase = 3,oil_ex_cap_start= 33215, oil_ex_cap_end= 33215, oil_ex_cap_increase = 3,
    conv_start_gr_gas  = 0.0, conv_start_gr_oil  = 0.0, conv_prod_decline_start =.06, conv_prod_decline_end_gas =.06, conv_prod_decline_end_oil =.06, 
    unconv_prod_decline_start =.00, unconv_prod_decline_end_gas =.06, unconv_prod_decline_end_oil =.05,
    cons_wedge_start_gas = 1.5, cons_wedge_end_gas = 1, cons_wedge_start_oil = 1.5, cons_wedge_end_oil = 1,
    intl_wedge_start_gas = 1.5,  intl_wedge_end_gas =1, intl_wedge_start_oil = 1.5, intl_wedge_end_oil = 1, discount =.045)

mp2050_lock_045 = VacaMuerta(yr0 = 2020, final_yr = 2050, model = 'WB', rcp = '1.5', switch = 'lock_in_045',pes_oil = 1.2,pes_gas = .9,
    a_gas_res = .02, a_oil_res = .02, a_el_res = .02, a_gas_ind = .02,a_oil_ind = .02,a_el_ind = .02,a_gas_trans = .02,a_oil_trans = .02,a_el_trans = .02,
    l= 10.0, t_rate_gas = -0.01, t_rate_oil = -0.01, t_rate_e  = .03,
    us_capex_gas = 7100000, us_capex_oil = 7100000, 
    m = 9542*2, oil_opex = (6.7/.000146),  gas_opex = (17.29/.000146), prod_subsidy_p_ratio=1.3, 
    share_covered = .17, royalty_rate_gas = .12, royalty_rate_oil = .12, duty_rate_gas = .08, duty_rate_oil = .08, 
    price_threshold_gas = 5.0*39652.61, price_threshold_oil = 60.0*7330, price_floor_gas = 3.75*39652.61, price_floor_oil = 45.0*7330, public_ds_capex_share = 0.67,
    T_bond_rate = .0245, arg_sov_risk = .0315, opp_cost_own_finance = .1029, share_own_capital =  .6803, opp_cost_debt =  .0312, GDP = 383100000000, 
    export_share_oil = .18, export_share_gas =.0,  
    gas_export_dem_start = 1.0, oil_export_dem_start = 1.0, gas_export_dem_end = 0.0, oil_export_dem_end = 0.0, gas_demand_decline_speed = 10, oil_demand_decline_speed = 10, 
    gas_ex_cap_start = 1905, gas_ex_cap_end= 42795, gas_ex_cap_increase = 30,oil_ex_cap_start= 33215, oil_ex_cap_end= 76650, oil_ex_cap_increase = 3,
    conv_start_gr_gas  = 0.0, conv_start_gr_oil  = 0.0, conv_prod_decline_start =.06, conv_prod_decline_end_gas =.06, conv_prod_decline_end_oil =.06, 
    unconv_prod_decline_start =.00, unconv_prod_decline_end_gas =.00, unconv_prod_decline_end_oil =.00,
    cons_wedge_start_gas = 1.5, cons_wedge_end_gas = 5, cons_wedge_start_oil = 1.5, cons_wedge_end_oil = 5,
    intl_wedge_start_gas = 1.5,  intl_wedge_end_gas = 5, intl_wedge_start_oil = 1.5, intl_wedge_end_oil = 4, discount = .045) 


# # #save high level summary results for all 4 scenarios
# print(mp2050)

out = pd.DataFrame([mp2050_075, mp2050_15_075, mp2050_lock_075,mp2050_06, mp2050_15_06, mp2050_lock_06,mp2050_045, mp2050_15_045, mp2050_lock_045])
out.columns = ['Total NPV GDP', 'Total NPV GDP No transfers','Total FT GDP', 'Total Wells', 'NPV GDP Conv. Gas', 'NPV GDP Conv. Oil', 'NPV GDP Unconv. Gas', 'NPV GDP Unconv. Oil','FT GDP Conv. Gas', 'FT GDP Conv. Oil', 'FT GDP Unconv. Gas', 'FT GDP Unconv. Oil']
# out['Scenario'] = ['Current Policies', "1_5 degrees",'Lock In', "Lock-In Electrification"]
out['Scenario'] = ['Current Policies 7.5', "1_5 Degrees 7.5","Lock-in 7.5",'Current Policies 6', "1_5 Degrees 6","Lock-in 6", 'Current Policies 4.5', "1_5 Degrees 4.5","Lock-in 4.5"]
print(out)
out.to_csv(outdir+'summary results.csv')

# #three only for testing
# out = pd.DataFrame([mp2050_06, mp2050_15_06, mp2050_lock_06])
# out.columns = ['Total NPV GDP', 'Total NPV GDP No transfers','Total FT GDP', 'Total Wells', 'NPV GDP Conv. Gas', 'NPV GDP Conv. Oil', 'NPV GDP Unconv. Gas', 'NPV GDP Unconv. Oil','FT GDP Conv. Gas', 'FT GDP Conv. Oil', 'FT GDP Unconv. Gas', 'FT GDP Unconv. Oil']
# # out['Scenario'] = ['Current Policies', "1_5 degrees",'Lock In', "Lock-In Electrification"]
# out['Scenario'] = ['Current Policies 6', "1_5 Degrees 6","Lock-in 6"]
# print(out)
# out.to_csv(outdir+'summary results.csv')

