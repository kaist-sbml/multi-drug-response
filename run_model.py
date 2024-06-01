import pandas as pd
import numpy as np
import argparse
import joblib
import os
from sklearn.preprocessing import MinMaxScaler
from utils import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input_file', required=True, help="Input file path")
    parser.add_argument('-o', '--output_dir', help="Output directory")
    parser.add_argument('-f', '--feature_type', help="Feature type: AI, MF, DTI (Active ingredients, Molecular fingerprints, Drug-target interactions)")
    parser.add_argument('-m', '--measurement_item', help="Measurement item: 5-digit integer from Item ID column of item_list.tsv or 'all', default: urea nitrogen")

    options = parser.parse_args()
    input_file = options.input_file
    output_dir = options.output_dir
    feature_type = options.feature_type
    measurement_item = options.measurement_item

    item_list = pd.read_csv('./data/item_list.tsv', index_col=0, sep='\t')
    all_items = [str(each) for each in item_list.index.tolist()]
    dir_to_verb = {'Low': 'decreased', 'High': 'increased'}

    if feature_type == None:
        feature_type = 'AI'

    feature_type = feature_type.upper()
    if feature_type not in ['AI', 'MF', 'DTI']:
        raise ValueError("feature_type should be in ['AI', 'MF', 'DTI'], current feature_type is %s"%(feature_type))

    print('Generate input')
    
    feature = generate_feature(input_file, feature_type)
 
    if measurement_item == None:
        measurement_item = 'all'
    
    if measurement_item == 'all':
        measurement_items = all_items
        
    elif measurement_item not in all_items:
        raise ValueError("measurement_item should be in Item ID in item_list.tsv or 'all', current measurement_item is %s"%(measurement_item))
        
    else:
        measurement_items = [measurement_item]
        
    if output_dir == None:
        output_dir = './results/'
    
    if not output_dir.endswith('/'):
        output_dir = output_dir+'/'
        
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    print('Loading model')
    written = False
    threshold = 0.5
    risk_list = []
    
    with open(output_dir+'prediction.txt', 'w') as fp:
        for each_item in measurement_items:
            with open('./model/scaler_%s_%s.joblib'%(each_item, feature_type), 'rb') as f:
                scaler = joblib.load(f)
                
            with open('./model/model_%s_%s.joblib'%(each_item, feature_type), 'rb') as f:
                clf = joblib.load(f)
    
            X = scaler.transform(feature.values)
            pred_prob = clf.predict_proba(X)
            
            if pred_prob[0, 1]>threshold:
                risk_list.append(int(each_item))
                
        if len(risk_list)==0:
            fp.write('No risks were predicted for this patient.')
            
        else:
            fp.write('This patient is predicted to be at risk of:\n')
            for each_risk in risk_list:   
                fp.write('\t%s %s level in blood\n'# (score: %.4f)'
                        %(dir_to_verb[item_list['Direction of signal'][each_risk]], item_list['Test name'][each_risk].lower()))#, pred_prob)
            
    print('Prediction completed for %d items'%(len(measurement_items)))