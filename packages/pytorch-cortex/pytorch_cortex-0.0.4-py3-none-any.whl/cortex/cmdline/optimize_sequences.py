import json
import logging
import random
import time
import warnings

import hydra
import numpy as np
import pandas as pd
import torch
import wandb
import lightning as L

from cortex.constants import ALIGNMENT_GAP_TOKEN
from cortex.optim import select_initial_sequences
from cortex.io import load_hydra_config, load_model_checkpoint
from cortex.logging import wandb_setup
from cortex.metrics import edit_dist



@hydra.main(config_path="../config/hydra", config_name="optimize_proteins", version_base=None)
def main(cfg):
    """
    general setup
    """
    random.seed(
        None
    )  # make sure random seed resets between Hydra multirun jobs for random job-name generation

    wandb_setup(cfg)
    cfg.random_seed = random.randint(0, int(1e6)) if cfg.random_seed is None else cfg.random_seed
    L.seed_everything(cfg.random_seed)

    dtype = torch.double if cfg.dtype == "double" else torch.float
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"using device: {device}")

    try:
        with warnings.catch_warnings():
            warnings.simplefilter(cfg.warnings_filter)
            ret_val = execute(cfg, dtype, device)
    except Exception as err:
        ret_val = float("NaN")
        logging.exception(err)

    wandb.finish()  # necessary to log Hydra multirun output to different jobs
    return ret_val


def execute(cfg, dtype, device):
    print("==== loading model checkpoint ====")
    # load Hydra config from s3 or locally
    ckpt_cfg = load_hydra_config(cfg.ckpt_cfg)
    # load model checkpoint from s3 or locally
    surrogate_model, _ = load_model_checkpoint(ckpt_cfg, cfg.ckpt_file, device=device, dtype=dtype)
    print("==== model checkpoint loaded successfully ====")

    opt_domain = cfg.optim.domain_name

    print("==== constructing initial solution ====")
    init_df = select_initial_sequences(
        data=cfg.init_candidates,
        model=surrogate_model,
        graph_objectives=cfg.guidance_objective.static_kwargs.objectives,
        graph_constraints=cfg.guidance_objective.static_kwargs.constraints,
        graph_obj_transform=cfg.guidance_objective.static_kwargs.scaling,
    )

    # up or downsample seed dataframe
    if len(init_df) > cfg.num_designs:
        init_df = init_df.sample(n=cfg.num_designs)
    elif len(init_df) < cfg.num_designs:
        init_df = init_df.sample(n=cfg.num_designs, replace=True)
    init_df = init_df.reset_index(drop=True)
    print("==== initial solution complete ====")

    # construct guidance objective
    acq_fn_runtime_kwargs = hydra.utils.call(
        cfg.guidance_objective.runtime_kwargs, model=surrogate_model, seed_df=init_df
    )
    acq_fn = hydra.utils.instantiate(cfg.guidance_objective.static_kwargs, **acq_fn_runtime_kwargs)

    # evaluate seeds
    print("==== calculating initial objective values ====")
    surrogate_model.eval()
    surrogate_model.requires_grad_(False)

    tree_output = surrogate_model.call_from_str_array(
        init_df[opt_domain].values, corrupt_frac=0.0
    )
    init_preds = acq_fn.get_objective_vals(tree_output)
    init_preds = {k: v.cpu().numpy().mean(0) for k, v in init_preds.items()}
    init_preds["obj_val"] = acq_fn(tree_output).cpu().numpy()
    for col in init_preds:
        init_df.loc[:, col] = list(init_preds[col])

    print("==== generating designs ====")
    mark = time.time()
    design_df = run_optimizer(
        cfg=cfg,
        init_df=init_df.copy(),
        model=surrogate_model,
        objective_fn=acq_fn,
        constraint_fn=None,
    )
    opt_time = time.time() - mark
    print(f"Optimization completed in {opt_time:.2f} seconds")

    design_df.loc[:, "edit_dist"] = np.array(
        [edit_dist(x, y) for x, y in zip(design_df[opt_domain].values, init_df[opt_domain].values)]
    )

    print("==== predicting final objective values ====")
    with torch.inference_mode():
        surrogate_model.eval()
        tree_output = surrogate_model.call_from_str_array(design_df[opt_domain].values)

    design_preds = acq_fn.get_objective_vals(tree_output)
    design_preds = {k: v.cpu().numpy().mean(0) for k, v in design_preds.items()}
    design_preds["obj_val"] = acq_fn(tree_output).cpu().numpy()
    for col in design_preds:
        if design_preds[col].ndim == 1:
            design_df.loc[:, col] = design_preds[col]
        else:
            design_df.loc[:, col] = [json.dumps(v.tolist()) for v in design_preds[col]]
            design_df.loc[:, col + "_init"] = [json.dumps(v.tolist()) for v in init_preds[col]]

    obj_val_delta = (design_df.obj_val - design_df.obj_val_init).values.mean().item()
    frac_improved = (design_df.obj_val > design_df.obj_val_init).values.mean().item()
    metrics = {
        "obj_val_delta_mean": obj_val_delta,
        "frac_improved": frac_improved,
        "wallclock_time": opt_time,
        "num_steps": cfg.num_steps,
    }
    metrics.update(get_column_stats(design_df, "obj_val"))
    metrics.update(get_column_stats(design_df, "obj_val_init"))
    metrics.update(get_column_stats(design_df, "edit_dist"))
    wandb.log(metrics)

    log_result(cfg, design_df)

    return design_df.obj_val.median().item()


def run_optimizer(cfg, init_df, model, objective_fn, constraint_fn):
    if not cfg.allow_length_change:
        model.default_tokenizer.corruption_vocab_excluded.add(ALIGNMENT_GAP_TOKEN)
        model.default_tokenizer.sampling_vocab_excluded.add(ALIGNMENT_GAP_TOKEN)

    opt_domain = cfg.optim.domain_name
    with torch.inference_mode():
        tree_output = model.call_from_str_array(init_df[opt_domain].values)
        tok_idxs = tree_output.root_outputs[cfg.optim.domain_name].tgt_tok_idxs

    # get mutable token position mask
    mutable_masks = hydra.utils.call(
        cfg.is_mutable.mask_callback,
        base_tok_idxs=tok_idxs,
        tokenizer=model.default_tokenizer,
    )
    is_mutable = torch.sum(
        torch.stack([mutable_masks[k] for k in cfg.is_mutable.mask_keys]), dim=0
    ).bool()

    optimizer = hydra.utils.instantiate(
        cfg.optim,
        params=tok_idxs,
        is_mutable=is_mutable,
        model=model,
        objective=objective_fn,
        max_num_solutions=cfg.num_designs,
        constraint_fn=constraint_fn,
    )
    for _ in range(cfg.num_steps):
        step_metrics = optimizer.step()
        wandb.log(step_metrics)
    new_designs = optimizer.get_best_solutions()

    new_designs["method"] = "lambo"
    return new_designs


def get_column_stats(df, col):
    stats = df[col].describe().to_dict()
    del stats["count"]
    stats = {f"{col}_{k}": v for k, v in stats.items()}
    return stats


def log_result(cfg, data):
    design_table = wandb.Table(dataframe=data)
    wandb.log({"designs": design_table})

    design_table_artifact = wandb.Artifact("design_artifact", type="dataset")
    design_table_artifact.add(design_table, "design_table")
    wandb.log_artifact(design_table_artifact)


if __name__ == "__main__":
    main()
