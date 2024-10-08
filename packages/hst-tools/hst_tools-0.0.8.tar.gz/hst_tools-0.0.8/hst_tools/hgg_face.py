"""
HS tools
"""
from functools import cache
from os.path import join, isdir
from pathlib import Path
from typing import Any

_CPU="cpu"
_CUDA="cuda"

@cache
class PipeLine:
    """
    HuggingFace model without reloading
    """

    def __init__(self, name:str, task:str, path:str, pipe:Any):
        self._name_model = name
        self._task_model = task
        self._path_model = path
        self._pipe_model = pipe
        self._pipe_line = None
        self._device = _CPU


    def _get_path(self):
        return str(join(self._path_model, self._name_model))


    def get_pipe(self):
        """
        Return pipeline instance
        Returns:
            any: pipeline
        """
        return self._pipe_line


    def set_cuda(self, cuda:bool = True):
        """
        Set device type _CUDA or _CPU
        """
        self._device = _CUDA if cuda else _CPU


    def load(self):
        """
        Load model to the memory
        """
        if isdir(self._get_path()):
            self._pipe_line = self._pipe_model(
                task=self._task_model,
                model=self._get_path(),
                device=self._device)
        else:
            Path(self._get_path()).mkdir(parents=True, exist_ok=True)
            self._pipe_line = self._pipe_model(
                task=self._task_model,
                model=self._name_model,
                device=self._device)
            self._pipe_line.save_pretrained(self._get_path())
