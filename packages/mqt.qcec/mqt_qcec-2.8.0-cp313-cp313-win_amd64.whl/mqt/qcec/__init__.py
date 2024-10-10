"""MQT QCEC library.

This file is part of the MQT QCEC library released under the MIT license.
See README.md or go to https://github.com/cda-tum/qcec for more information.
"""

from __future__ import annotations


# start delvewheel patch
def _delvewheel_patch_1_8_2():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'mqt_qcec.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_8_2()
del _delvewheel_patch_1_8_2
# end delvewheel patch

from ._version import version as __version__
from .compilation_flow_profiles import AncillaMode, generate_profile
from .pyqcec import (
    ApplicationScheme,
    Configuration,
    EquivalenceCheckingManager,
    EquivalenceCriterion,
    StateType,
)
from .verify import verify
from .verify_compilation_flow import verify_compilation

__all__ = [
    "AncillaMode",
    "ApplicationScheme",
    "Configuration",
    "EquivalenceCheckingManager",
    "EquivalenceCriterion",
    "StateType",
    "__version__",
    "generate_profile",
    "verify",
    "verify_compilation",
]
