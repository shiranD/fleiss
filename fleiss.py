import pandas as pd
import numpy as np
from read_gsheet import read_sheet

def fleiss_interp(number):
    if number < 0:
        print("Fleiss kappa is", number, "resulting in poor agreement (1/6)")
    if number < 0.2:
        print("Fleiss kappa is", number, "resulting in slight agreement (2/6)")
    if number < 0.4:
        print("Fleiss kappa is", number, "resulting in fair agreement (3/6)")
    if number < 0.6:
        print("Fleiss kappa is", number, "resulting in moderate agreement (4/6)")
    if number < 0.8:
        print("Fleiss kappa is", number, "resulting in substaintial agreement (5/6)")
    if number < 0.1:
        print("Fleiss kappa is", number, "resulting in almost perfect agreement (6/6)")

def compute_fleiss_kappa(sheet, categories):
    num_raters = 4 # hard coded TBD
    table = pd.DataFrame(sheet, columns = ['l', 'c', 'm', 'n']).astype('int32')
    total_sum = table.sum().sum()
    # count agreement per category for every prompt
    for i in categories:
        table[i] = table.apply(lambda row: sum(row[0:num_raters]==int(i)) ,axis=1)
    # raise to power
    for i in categories:
        name = i+'^2'
        table[name] = np.power((table[i]),2)
    # compute p_i
    x = table.shape[1]
    table['p_i'] = table.apply(lambda row: (sum(row[x-len(categories):x])-num_raters)/(num_raters*(num_raters-1)) ,axis=1)
    # compute p_j 
    table.loc['p_j'] = pd.Series([table[categories[0]].sum()/total_sum,table[categories[1]].sum()/total_sum,table[categories[2]].sum()/total_sum, table[categories[3]].sum()/total_sum], index = categories)
    p_bar = pd.Series(table['p_i'].sum()/(table.shape[0]-1))
    p_e = table.loc['p_j'].sum()
    fleiss = (p_bar-p_e)/(1-p_e) 
    fleiss_interp(float(fleiss))

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE='keys.json'
RANGE = 'All!d2:g261'
sheet = read_sheet(SCOPES, SERVICE_ACCOUNT_FILE, RANGE)

categories =  ['0', '1', '2', '3'] # the numerical categories
compute_fleiss_kappa(sheet, categories)
