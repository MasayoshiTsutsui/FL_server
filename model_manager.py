import os
import json
import numpy as np
import coremltools
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

    
def test_save_as_file() -> None:

    params = {
        "weights": [1, 2, 3, 4, 5],
        "biases": [5, 4, 3, 2, 1]
    }

    save_as_file(params)


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

    mean_weights = np.mean(weights, axis=0, dtype=np.float32)
    mean_biases = np.mean(biases, axis=0, dtype=np.float32)

    # update model
    # load "HandsTuri.mlmodel" as model
    model = coremltools.models.MLModel(os.path.join(GLOBAL_MODEL_DIR, "HandsTuri.mlmodel"))

    # update weights and biases of the last fully connected layer
    model._spec.neuralNetwork.layers[-2].innerProduct.weights.floatValue = mean_weights
    model._spec.neuralNetwork.layers[-2].innerProduct.bias.floatValue = mean_biases

    # save the model as new HandsTuri.mlmodel file
    model.save(os.path.join(GLOBAL_MODEL_DIR, "HandsTuri_v2.mlmodel"))


if __name__ == "__main__":
    test_save_as_file()