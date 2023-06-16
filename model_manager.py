import os
import json
import numpy as np
from constants import ACCUM_CLIENT_NUM

GLOBAL_MODEL_DIR = '/home/tsuts/fl_server/global_model'
CUR_UPLOADED_DIR = '/home/tsuts/fl_server/cur_uploaded_params'

def save_as_file(params: dict) -> None:

    # count up the number of files in cur_upload_dir
    num_of_files = len(os.listdir(CUR_UPLOADED_DIR))
    cur_params_idx = num_of_files + 1

    json_file = f"params_{cur_params_idx}.json"

    json_fileptr = open(os.path.join(CUR_UPLOADED_DIR, json_file), "w")
    json.dump(params, json_fileptr)
    json_fileptr.close()

def try_to_update_model() -> bool:
    # if the number of uploaded params-set is less than 5, abort updating
    if len(os.listdir(CUR_UPLOADED_DIR)) < ACCUM_CLIENT_NUM:
        return False
    
    aggregate_and_update_model()


def aggregate_and_update_model() -> None:

    params_json_list = os.listdir(CUR_UPLOADED_DIR)

    params_dict_list = [json.load(open(os.path.join(CUR_UPLOADED_DIR, params_json), "r")) for params_json in params_json_list]
    weights = [params_dict["weights"] for params_dict in params_dict_list]
    biases = [params_dict["biases"] for params_dict in params_dict_list]

    mean_weights = np.mean(weights, axis=0)
    mean_biases = np.mean(biases, axis=0)

    # update model



    




