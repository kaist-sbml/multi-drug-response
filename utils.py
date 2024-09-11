import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def read_as_list(x):
    if "'" in x:
        x = x.replace("'", "")
    net = x.rstrip("]").lstrip("[")
    if len(net)==0:
        return None
    return net.split(", ")

def categorize_age(age):
    if age < 20:
        return 2
    elif 20 <= age <= 29:
        return 3
    elif 30 <= age <= 39:
        return 4
    elif 40 <= age <= 49:
        return 5
    elif 50 <= age <= 59:
        return 6
    elif 60 <= age <= 69:
        return 7
    elif 70 <= age <= 79:
        return 8
    else:
        return 9

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def parse_input_text(input_text):
    age = None
    sex = None
    rac = "other/unknown"
    pres_list = []
        
    lines = [each_line.lower() for each_line in input_text.strip().split('\n')]
    for line in lines:
        # Extract age
        if line.startswith('age:'):
            age = int(line.split(':')[1].strip())
        
        # Extract sex
        elif line.startswith('sex:'):
            sex = line.split(':')[1].strip()
            if sex not in ['male', 'female']:
                raise ValueError('Sex should be Male or Female. Current value is %s'%(sex))
        
        # Extract race
        elif line.startswith('race:'):
            race = line.split(':')[1].strip()
            if race in ['white', 'black', 'asian', 'hispanic/latino']:
                rac = race
            elif race in ['hispanic', 'latino']:
                rac = 'hispanic/latino'
            else:
                rac = "other"
        
        # Extract prescriptions
        elif line.startswith('prescriptions:'):
            pres_index = lines.index(line) + 1
            pres_list = [lines[i].strip() for i in range(pres_index, len(lines)) if lines[i].strip()]

    return age, sex, rac, pres_list

def generate_feature(input_text_path, feature_type):
    input_text = read_input_file(input_text_path)
    age, sex, rac, pres_list = parse_input_text(input_text)
    ingredients_df = pd.read_csv('./data/ingredients.csv', converters={'Fingerprint':read_as_list, 'DTI':read_as_list})
    rxcui_dict = dict(zip(ingredients_df['Name'].str.lower(), ingredients_df['RxCUI']))
    ingredients_df = ingredients_df.set_index('RxCUI', drop=True)
    syn_mimic = pd.read_csv('./data/synthetic_mimic.csv', index_col=0)
    
    feature_dict = {}
    for each_column in syn_mimic.columns:
        feature_dict[each_column] = 0
    feature_dict['Sex_%s'%(sex.upper())] = 1
    feature_dict['Race_%s'%(rac.upper())] = 1
    feature_dict['Age'] = age

    for each_drug in pres_list:
        if each_drug in rxcui_dict:
            rxcui = str(rxcui_dict[each_drug])
            feature_dict[rxcui] = 1

    feature_df = pd.DataFrame.from_dict(feature_dict, orient='index').T
    feature_df['AgeGroup'] =  feature_df['Age'].map(categorize_age)

    if feature_type == 'DTI':
        ti_sum = np.zeros(len(ingredients_df['DTI'][1223]))
        for each_drug in pres_list:
            rxcui = rxcui_dict[each_drug]
            each_ti = np.array(ingredients_df['DTI'][rxcui], dtype=np.float64)
            ti_sum += each_ti
        ti_df = pd.DataFrame(ti_sum).T
        ti_df = pd.concat([ti_df, feature_df.loc[:, 'Sex_FEMALE':]], axis=1)
        return ti_df
    
    elif feature_type == 'MF':
        fp_sum = np.zeros(len(ingredients_df['Fingerprint'][1223]))
        for each_drug in pres_list:
            rxcui = rxcui_dict[each_drug]
            each_fp = np.array(ingredients_df['Fingerprint'][rxcui], dtype=np.float64)
            fp_sum += each_fp
        fp_df = pd.DataFrame(fp_sum).T
        fp_df = pd.concat([fp_df, feature_df.loc[:, 'Sex_FEMALE':]], axis=1)
        return fp_df

    else:
        return feature_df