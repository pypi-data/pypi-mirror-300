from functools import cache
from os.path import join, isdir
from pathlib import Path
from typing import Any


@cache
class PipeLine(object):
    """
    HuggingFace model without reloading
    """

    def __init__(self, name, task, path, pipe:Any, device:str = "cpu"):
        self._name_model = name
        self._task_model = task
        self._path_model = path
        self._pipe_model = pipe
        self._device = device
        self.pipe_line = None
        self._load_model()

    def _get_path(self):
        return str(join(self._path_model, self._name_model))

    def _load_model(self):
        if isdir(self._get_path()):
            self.pipeline = self._pipe_model(
                task=self._task_model,
                model=self._get_path(),
                device=self._device)
        else:
            Path(self._get_path()).mkdir(parents=True, exist_ok=True)
            self.pipeline = self._pipe_model(
                task=self._task_model,
                model=self._name_model,
                device=self._device)
            self.pipeline.save_pretrained(self._get_path())
