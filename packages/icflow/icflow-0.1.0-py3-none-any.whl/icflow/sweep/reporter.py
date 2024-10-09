"""
This module allows reporting on past or current parameter sweeps.
"""

import logging
from typing import Callable

from ictasks.task import Task


logger = logging.getLogger()


def deserialize_args(cli_args: str, delimiter: str = "--") -> dict[str, str]:
    """
    Convert command line args in the form 'program --key0 value0 --key1 value1'
    to a dict of key value pairs.

    TODO: Should live in iccore.cli_utils
    """
    stripped_entries = [e.strip() for e in cli_args]
    args: dict = {}
    last_key = ""
    for entry in stripped_entries:
        if entry.startswith(delimiter):
            if last_key:
                # Flag
                args[last_key] = ""
            last_key = entry[len(delimiter) :]
        else:
            if last_key:
                args[last_key] = entry
                last_key = ""
    return args


def serialize_task(task: Task, attributes: list[str] | None) -> str:
    """
    Convert a task to a string. If attributes are given only serialize those
    instance attributes
    TODO: This should use Pydantic filtering instead
    """
    if attributes:
        return "".join(f"{key}: {getattr(task, key)}\n" for key in attributes)
    return str(task)


def serialize_tasks(tasks: list[Task], attributes: list[str] | None) -> str:
    """
    Convert a list of tasks to a string. If attributes are given only serialize
    those task attributes.
    it.
    """
    return "".join(serialize_task(t, attributes) + "\n" for t in tasks)


def task_params_in_range(task: Task, config: dict[str, dict]) -> bool:
    """
    Check that this task's parameters are in line with the upper and lower bounds
    and specific values given in the config.
    """

    for key, value in deserialize_args(task.launch_cmd).items():
        if key not in config:
            continue
        param = config[key]

        if "range" in param:
            value_range = param["range"]
            if "lower" in value_range:
                if value < param["lower"]:
                    return False
            if "upper" in value_range:
                if value > param["upper"]:
                    return False
        if "values" in param:
            values = param["values"]
            if "exclude" in values:
                if value in values["exclude"]:
                    return False
            if "include" in values:
                if value not in values["include"]:
                    return False
    return True


def filter_tasks_with_config(
    tasks: list[Task], config: dict, predicate: Callable
) -> list[Task]:
    return [t for t in tasks if predicate(t, config)]
