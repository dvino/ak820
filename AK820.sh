#!/bin/sh
set -eu
AK820_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ -x "$AK820_ROOT/.venv-ak820-installer/bin/python" ]; then
    AK820_PYTHON="$AK820_ROOT/.venv-ak820-installer/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    AK820_PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    AK820_PYTHON=python
else
    echo 'Python 3.10+ is required. Install python3 and python3-venv, then retry.' >&2
    exit 1
fi
exec "$AK820_PYTHON" -B "$AK820_ROOT/tools/installer/ak820.py" "$@"
