import os
import json
import numpy as np
import coremltools
from constants import ACCUM_CLIENT_NUM, GLOBAL_MODEL_DIR, UPLOADED_DIR


def save_as_file(params: dict, gModel_idx: int) -> None:

    # count up the number of files in cur_upload_dir
    model_version_to_make = f"v{gModel_idx + 1}"
    
    dir_to_save = os.path.join(UPLOADED_DIR, model_version_to_make)
    num_of_files = len(os.listdir(dir_to_save))
    cur_params_idx = num_of_files + 1

    json_file = f"params_{cur_params_idx}.json"

    json_fileptr = open(os.path.join(dir_to_save, json_file), "w")
    json.dump(params, json_fileptr)
    json_fileptr.close()

    
def test_save_as_file() -> None:

    params = {
        "weights": [1] * 1000 * 6,
        "biases": [0] * 6
    }

    save_as_file(params, len(os.listdir(GLOBAL_MODEL_DIR)))
    try_to_update_model(len(os.listdir(GLOBAL_MODEL_DIR)))


def try_to_update_model(gModel_idx: int) -> bool:
    # count up the number of files in cur_upload_dir
    model_version_to_make = f"v{gModel_idx + 1}"
    dir_to_save = os.path.join(UPLOADED_DIR, model_version_to_make)

    # if the number of uploaded params-set is less than 5, abort updating
    if len(os.listdir(dir_to_save)) < ACCUM_CLIENT_NUM:
        return False
    
    aggregate_and_update_model(model_version_to_make)


def aggregate_and_update_model(model_version_to_make: int) -> None:
    cur_round_dir = os.path.join(UPLOADED_DIR, model_version_to_make)

    params_json_list = os.listdir(cur_round_dir)

    params_dict_list = [json.load(open(os.path.join(cur_round_dir, params_json), "r")) for params_json in params_json_list]
    weights = [params_dict["weights"] for params_dict in params_dict_list]
    biases = [params_dict["biases"] for params_dict in params_dict_list]

    mean_weights = np.mean(weights, axis=0, dtype=np.float32)
    mean_biases = np.mean(biases, axis=0, dtype=np.float32)

    # update model
    # load "Hands2num.mlmodel" as model
    gModel_idx = len(os.listdir(GLOBAL_MODEL_DIR))
    model = coremltools.models.MLModel(os.path.join(GLOBAL_MODEL_DIR, f"Hands2num_v{gModel_idx}.mlmodel"))

    # update weights and biases of the last fully connected layer
    last_fc_layer = model._spec.neuralNetworkClassifier.layers[-2]

    if len(last_fc_layer.innerProduct.weights.floatValue) != len(mean_weights):
        raise ValueError("The length of mean_weights is not equal to the length of the weights of the last fully connected layer")

    last_fc_layer.innerProduct.weights.ClearField("floatValue")
    last_fc_layer.innerProduct.weights.floatValue.extend(mean_weights)
    
    if len(last_fc_layer.innerProduct.bias.floatValue) != len(mean_biases):
        raise ValueError("The length of mean_bias is not equal to the length of the bias of the last fully connected layer")

    last_fc_layer.innerProduct.bias.ClearField("floatValue")
    last_fc_layer.innerProduct.bias.floatValue.extend(mean_biases)

    # save the model as new Hands2num.mlmodel file
    model.save(os.path.join(GLOBAL_MODEL_DIR, f"Hands2num_v{gModel_idx + 1}.mlmodel"))

    # new directory to keep clients params for the next round
    os.mkdir(os.path.join(UPLOADED_DIR, f"v{gModel_idx + 2}")) 



if __name__ == "__main__":
    test_save_as_file()