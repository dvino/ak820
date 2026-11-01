#!/usr/bin/env python3
"""Check the filtered compiler environment for Linux pointer/pass30 builds."""
from pathlib import Path
import os
import sys

def validate_pointer_environment(environment, root, build, toolchain, qmk_bin):
    root, build, toolchain, qmk_bin = (Path(p).resolve() for p in (root, build, toolchain, qmk_bin))
    if not build.is_relative_to(root) or build == root:
        raise ValueError('Pointer build directory must be beneath the source root')
    if sys.platform != 'linux':
        raise ValueError('Pointer compiler policy supports Linux only')
    if any(c.isspace() for c in str(build.relative_to(root))):
        raise ValueError('Pointer build directory cannot contain whitespace')
    if (not isinstance(environment, dict) or set(environment) != {'PATH', 'AK820_CAPTURE_BUILD_ROOT', 'AK820_CAPTURE_OBJECT_ROOT'} or
            not isinstance(environment['PATH'], str) or
            environment['AK820_CAPTURE_BUILD_ROOT'] != str(build) or
            environment['AK820_CAPTURE_OBJECT_ROOT'] != str(build / 'obj_ajazz_ak820_vial')):
        raise ValueError('Recorded pointer compiler environment differs from policy')
    parts = environment['PATH'].split(os.pathsep)
    if (len(parts) < 2 or any(not part or not Path(part).is_absolute() for part in parts) or
            Path(parts[0]).resolve() != (toolchain / 'bin').resolve() or
            Path(parts[1]).resolve() != qmk_bin.parent):
        raise ValueError('Pointer compiler PATH differs from policy')
