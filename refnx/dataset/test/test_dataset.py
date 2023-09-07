from pathlib import Path
import glob
import os

import pytest

from refnx.dataset import ReflectDataset, Data1D, load_data, OrsoDataset
from refnx.dataset.reflectdataset import load_orso
import numpy as np
from numpy.testing import assert_equal


class TestReflectDataset:
    @pytest.fixture(autouse=True)
    def setup_method(self, tmp_path):
        self.pth = Path(__file__).absolute().parent
        self.cwd = Path(".").resolve()
        self.tmp_path = tmp_path
        os.chdir(self.tmp_path)

    def teardown_method(self):
        os.chdir(self.cwd)

    def test_ort_load(self):
        f = self.pth / "ORSO_data.ort"
        assert f.exists()
        try:
            load_orso(str(f))
            load_orso(f)
        except ImportError:
            # load_orso had problems on Python 3.10, so bypass the test
            return

        d = load_data(f)
        assert len(d) == 2
        assert isinstance(d, OrsoDataset)
        d.refresh()

    def test_load_data(self):
        # test the load_data function by trying to load all the files in the
        # test directory
        fs = glob.glob("*.*")
        fs = [f for f in fs if not f.endswith(".py")]
        fs = [f for f in fs if not f.startswith("coef_")]

        for f in fs:
            load_data(f)
            load_data(Path(f))
