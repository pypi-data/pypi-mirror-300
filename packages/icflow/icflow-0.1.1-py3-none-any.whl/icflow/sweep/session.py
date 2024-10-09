"""
This module allows a parameter sweep to be performed.
"""

import logging
import uuid
import shutil
import os
from pathlib import Path
import queue
from functools import partial

import iccore
from iccore.cli_utils import serialize_args

import ictasks
from ictasks.task import Task

from .config import ParameterSweepConfig

logger = logging.getLogger()


def run(
    config: ParameterSweepConfig,
    work_dir: Path = Path(os.getcwd()),
    config_path: Path | None = None,
):
    """
    Run a parameter sweep defined by the config.

    :param config: The config to control the sweep
    :param work_dir: Directory to run the sweep in
    :param config_path: If provided will copy the config into the work dir
    """

    timestamp = iccore.time_utils.get_timestamp_for_paths()
    sweep_dir = work_dir / f"sweep_{config.title}_{timestamp}"
    os.makedirs(sweep_dir)

    if config_path:
        shutil.copyfile(config_path, sweep_dir / config_path.name)

    tasks = [
        Task(
            id=str(uuid.uuid4()), launch_cmd=f"{config.program} {serialize_args(args)}"
        )
        for args in config.get_expanded_params()
    ]
    task_queue: queue.Queue[Task] = queue.Queue()
    for task in tasks:
        task_queue.put(task)

    write_task_func = partial(ictasks.task.write, sweep_dir)
    ictasks.session.run(
        task_queue,
        sweep_dir,
        config.tasks,
        on_task_launched=write_task_func,
        on_task_completed=write_task_func,
    )
