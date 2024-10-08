import random
import logging
import warnings

import hydra
import torch
import wandb


@hydra.main(config_path="../config/hydra", config_name="train_cortex_optimizer", version_base=None)
def main(cfg):
    """
    general setup
    """
    random.seed(None)  # make sure random seed resets between Hydra multirun jobs for random job-name generation

    try:
        with warnings.catch_warnings():
            warnings.simplefilter(cfg.warnings_filter)
            ret_val = execute(cfg)
    except Exception as err:
        ret_val = float("NaN")
        logging.exception(err)

    wandb.finish()  # necessary to log Hydra multirun output to different jobs
    return ret_val


def execute(cfg):
    test_fn = hydra.utils.instantiate(cfg.test_function)

    # generate initial data
    unif_x = test_fn.random_solution(cfg.num_unif_samples)
    unif_y = test_fn(unif_x)

    feas_x = test_fn.initial_solution(cfg.num_feas_samples)
    feas_y = test_fn(feas_x)

    dataset = torch.utils.data.TensorDataset(
        torch.cat([unif_x, feas_x], dim=0),
        torch.cat([unif_y, feas_y], dim=0),
    )

    # instantiate the model

    # for each iteration

    # train the model

    # select the next batch of data

    # annotate the data

    # add to dataset


if __name__ == "__main__":
    main()
