import json
from datetime import datetime
import pandas as pd
import csv
import torch
from typing import Optional
from ..models.utils import FocalLoss


def load_params(params_path):
    with open(params_path, "r") as f:
        params = json.load(f)
    params_flatten = pd.json_normalize(params, sep=".").to_dict(orient="records")[0]
    return params, params_flatten


def time2weekday(time):
    """
    0 -> 6
    Mon -> Sun
    """
    return int(datetime.fromisoformat(time).weekday())


def time2daytime(time):
    dt = datetime.fromisoformat(time)
    h = int(dt.hour)
    m = int(dt.minute)
    return 2 * h if m < 30 else 2 * h + 1


def lookup_table_to_dict(table_path, idx_col, val_col, file_format="json"):
    if file_format == "json":
        with open(table_path, "r") as file:
            lookup = json.load(file)
            lookup_dict = {
                lookup[idx_col][i]: lookup[val_col][i]
                for i in lookup[idx_col].keys()
            }
    elif file_format == "csv":
        with open(table_path, "r") as file:
            lookup_reader = csv.DictReader(file)
            lookup_dict = {}
            for row in lookup_reader:
                # idx_value = int(row[idx_col]) if row[idx_col].isdecimal() else row[idx_col]
                val_value = int(row[val_col]) if row[val_col].isdecimal() else row[val_col]
                idx_value = row[idx_col]
                # val_value = row[val_col]
                lookup_dict.update({idx_value: val_value})
    else:
        raise NotImplementedError()
    return lookup_dict


def focal_loss(
    input: torch.Tensor,
    target: torch.Tensor,
    alpha: float,
    gamma: Optional[float] = 2.0,
    reduction: Optional[str] = 'none') -> torch.Tensor:
    r"""Function that computes Focal loss.

    See :class:`~torchgeometry.losses.FocalLoss` for details.
    """
    return FocalLoss(alpha, gamma, reduction)(input, target)


# def model_logging_setup(new_log_path, run_name, model_name, params_flatten):
#     # WandB
#     global wandb_run
#     logger = logging.getLogger()
#     logger.setLevel(logging.DEBUG)
#     logging.basicConfig(
#         filename=new_log_path,
#         level=logging.INFO
#     )

#     # MLflow
#     experiment_paths = [e.name for e in mlflow.list_experiments()]
#     experiment_path = f"/MLflow/{model_name}"
#     if experiment_path in experiment_paths:
#         experiment_id = mlflow.get_experiment_by_name(name=experiment_path).experiment_id
#     else:
#         experiment_id = mlflow.create_experiment(name=experiment_path)
#     return logger, experiment_id
