# pybind11_coordtransform

## install

from pypi:

```bash
pip install pybind11_coordtransform
```

local:

```bash
make python_install
```

## usage

```bash
from pybind11_coordtransform import wgs84_to_gcj02_Nx2 as wgs84_to_gcj02
wgs84_to_gcj02(lon_lats)
```

## development

```bash
make build
```
