import runpy
from unittest.mock import ANY, patch

from fastapi import FastAPI


@patch('core.run')
def test_main_run(run, api):
    runpy.run_module('core.main', run_name='__main__')
    run.assert_called_once_with(ANY)
    assert isinstance(run.call_args[0][0], FastAPI)


@patch('core.run')
def test_main_dont_run(run, api):
    runpy.run_module('core.main')
    run.assert_not_called()
