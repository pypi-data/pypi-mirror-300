import os as _os
import sys as _sys
_axeSearchPath = _os.path.dirname(_os.path.abspath(__file__))
while not _os.path.exists(_os.path.join(_axeSearchPath,
    'axengine_1728046836_928193352.py')):
    _newAxeSearchPath = _os.path.normpath(_os.path.join(_axeSearchPath, '..'))
    if _newAxeSearchPath == _axeSearchPath or len(_axeSearchPath) == 0:
        break
    _axeSearchPath = _newAxeSearchPath
try:
    _sys.path.append(_axeSearchPath)
    import axengine_1728046836_928193352 as _axengine
except Exception as e:
    raise Exception('Failed to load AxEngine!') from e
finally:
    _sys.path.pop()
from axengine_1728046836_928193352 import WupiError, WupiLicenseError, WupiErrorCode
_axengine._axe_run(190, globals())
