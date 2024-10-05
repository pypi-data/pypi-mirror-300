from __future__ import annotations

import pybind11_coordtransform as m


def test_version():
    assert m.__version__ == "0.1.2"
