import typing

import py_gen_ml as pgml

from . import enum_demo_patch as patch
from . import enum_demo_base as base


ActivationSweepField = typing.Union[
    pgml.Choice[base.Activation],
    base.Activation,
]


class MLPSweep(pgml.Sweeper[patch.MLPPatch]):
    """MLP configuration"""

    activation: ActivationSweepField | None = None
    """Activation function"""

    num_layers: pgml.IntSweep | None = None
    """Number of layers"""



MLPSweepField = typing.Union[
    MLPSweep,
    pgml.NestedChoice[MLPSweep, patch.MLPPatch],  # type: ignore
]

