import sys
from pathlib import Path

_here = Path(__file__).parent

# minseok/apps → "sherlock_homes.*" 임포트 활성화
_apps_dir = str(_here.parent.parent)
# minseok/ → "core.*" 임포트 활성화
_minseok_dir = str(_here.parent.parent.parent)

for _p in (_apps_dir, _minseok_dir):
    if _p not in sys.path:
        sys.path.insert(0, _p)
