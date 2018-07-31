#!/user/bin/env python
import logging
import subprocess
import json, os
import glob
import random

def write_fake_data_to_local(region, et_model, year, geo_fl, data_fl, data_cols):
    data = {
        'type': 'FeatureCollection',
        'features': []
    }
    with open(geo_fl) as f:
        j_data = json.load(f)
    feats = j_data['features']
    for f_idx, feat in enumerate(feats):
        data_dict = {
            'properties': {'idx': f_idx}
        }
        # Add metadata
        props = feat['properties']
        for prop_key in props.keys():
            data_dict['properties'][prop_key] = props[prop_key]
        # Add fake ET DATA
        for prop_key in data_cols:
            data_dict['properties'][prop_key] = random.randint(1,101)
        data['features'].append(data_dict)
    with open(data_fl, 'w') as f:
        json.dump(data, f)

def upload_file_to_bucket(upload_path, bucket_fl_path):
    if os.name == 'posix':
        shell_flag = False
    else:
        shell_flag = True

    args = ['gsutil', 'cp', upload_path, bucket_fl_path]
    try:
        subprocess.check_output(args, shell=shell_flag)
        os.remove(upload_path)
        logging.info('Successfully uploaded to bucket: ' + bucket_fl_path)
    except Exception as e:
        logging.exception(
        '    Exception: {}\n'.format(e))

def make_file_public(bucket_fl_name):
    if os.name == 'posix':
        shell_flag = False
    else:
        shell_flag = True
    args = ['gsutil', 'acl', 'ch', '-u', 'AllUsers:R', bucket_fl_path]
    try:
        subprocess.check_output(args, shell=shell_flag)
    except Exception as e:
        logging.exception(
        '    Exception: {}\n'.format(e))

if __name__ == '__main__':
    data_cols = ["etr_annual", "et_annual", "etrf_annual", "pr_annual", "net_annual",
            "etr_seasonal", "et_seasonal", "etrf_seasonal", "pr_seasonal", "net_seasonal",
            "pr_m01", "pr_m02", "pr_m03", "pr_m04", "pr_m05",
            "pr_m06", "pr_m07", "pr_m08", "pr_m09", "pr_m10", "pr_m11", "pr_m12",
            "etr_m01", "etr_m02", "etr_m03", "etr_m04", "etr_m05",
            "etr_m06", "etr_m07", "etr_m08", "etr_m09", "etr_m10", "etr_m11", "etr_m12",
            "et_m01", "et_m02" , "et_m03" , "et_m04", "et_m05",
            "et_m06", "et_m07", "et_m08", "et_m09", "et_m10", "et_m11", "et_m12",
            "etrf_m01", "etrf_m02", "etrf_m03", "etrf_m04", "etrf_m05",
            "etrf_m06", "etrf_m07", "etrf_m08", "etrf_m09", "etrf_m10", "etrf_m11", "etrf_m12"
    ]
    geo_dir = '/Users/bdaudert/EE/nasa-roses-data/geojson/'
    bucket_name = 'gs://roses-data'
    # regions = ['Mason', 'US_states_west_500k', 'US_counties_west_500k']
    regions = ['US_states_west_500k']
    # regions = ['US_HUC2', 'US_HUC4', 'US_HUC6', 'US_HUC8', 'US_HUC10']
    # regions = ['CentralValley_15']
    et_models = ['SSEBop']
    years = range(2003, 2012)
    for region in regions:
        for et_model in et_models:
            bucket_path = bucket_name + '/' + et_model + '/'
            data_dir = '/Users/bdaudert/EE/nasa-roses-data/' + et_model + '/'
            for year in years:
                if region == 'Mason':
                    # geojsons for MASON vary by years
                    geo_fl = geo_dir + region + '_' + str(year) + '_GEOM.geojson'
                else:
                    geo_fl = geo_dir + region + '_GEOM.geojson'
                print('PROCESSING region/model/year: ' + region + '/' + et_model + '/' + str(year))
                data_fl = region + '_' + str(year) + '_DATA' + '.json'
                data_fl_path = data_dir = data_fl
                #write_fake_data_to_local(region, et_model, year, geo_fl, data_fl, data_cols)
                bucket_fl_path = bucket_path + data_fl
                #upload_file_to_bucket(data_fl, bucket_fl_path)
                make_file_public(bucket_fl_path)

