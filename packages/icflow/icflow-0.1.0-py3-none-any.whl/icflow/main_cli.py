#!/usr/bin/env python3

import argparse
import logging
import os
from pathlib import Path

import ictasks
import icflow
from icflow.sweep import reporter


logger = logging.getLogger(__name__)


def sweep(args):
    config_path = args.config.resolve()
    config = icflow.sweep.config.read(config_path)
    icflow.sweep.run(config, args.work_dir.resolve(), config_path)


def report_sweep_progress(args):
    result_dir = args.result_dir.resolve()
    tasks = ictasks.task.read_all(result_dir)
    unfinished_tasks = [t for t in tasks if not t.is_finished]

    task_str = reporter.serialize_tasks(unfinished_tasks, ["id", "launch_cmd", "pid"])
    print("Unfinished tasks\n", task_str)


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry_run",
        type=int,
        default=0,
        help="Dry run script - 0 can modify, 1 can read, 2 no modify - no read",
    )
    subparsers = parser.add_subparsers(required=True)

    sweep_parser = subparsers.add_parser("sweep")
    sweep_parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to the config file to use for sweep",
    )
    sweep_parser.add_argument(
        "--work_dir",
        type=Path,
        default=Path(os.getcwd()),
        help="Path to the working directory for output",
    )
    sweep_parser.set_defaults(func=sweep)

    sweep_progress_parser = subparsers.add_parser("sweep_progress")
    sweep_progress_parser.add_argument(
        "--result_dir",
        type=Path,
        required=True,
        help="Path to the working directory for output",
    )
    sweep_progress_parser.set_defaults(func=report_sweep_progress)
    args = parser.parse_args()

    fmt = "%(asctime)s%(msecs)03d | %(filename)s:%(lineno)s:%(funcName)s | %(message)s"
    logging.basicConfig(
        format=fmt,
        datefmt="%Y%m%dT%H:%M:%S:",
        level=logging.INFO,
    )

    args.func(args)


if __name__ == "__main__":
    main_cli()
