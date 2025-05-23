"""Mock FHI-aims functions for executing tutorials."""

import contextlib
import os
import shutil
import tempfile
from collections.abc import Generator
from pathlib import Path

from pytest import MonkeyPatch

from atomate2.utils.testing.aims import monkeypatch_aims

TEST_ROOT = Path(__file__).parent.parent / "tests"
TEST_DIR = TEST_ROOT / "test_data"


@contextlib.contextmanager
def mock_aims(ref_paths: dict) -> Generator:
    """Mock FHI-aims functions.

    Parameters
    ----------
    ref_paths (dict): A dictionary of reference paths to the test data.

    Yields
    ------
        function: A function that mocks calls to FHI-aims.
    """
    for mf in monkeypatch_aims(MonkeyPatch(), TEST_DIR / "aims"):
        fake_run_aims_kwargs = {k: {"check_inputs": ()} for k in ref_paths}
        old_cwd = os.getcwd()
        new_path = tempfile.mkdtemp()
        os.chdir(new_path)
        try:
            yield mf(ref_paths, fake_run_aims_kwargs)
        finally:
            os.chdir(old_cwd)
            shutil.rmtree(new_path)
