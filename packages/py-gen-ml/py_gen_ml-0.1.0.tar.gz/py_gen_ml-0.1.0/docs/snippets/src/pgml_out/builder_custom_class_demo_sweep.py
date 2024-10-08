import typing

import py_gen_ml as pgml

from . import builder_custom_class_demo_patch as patch
from . import builder_custom_class_demo_base as base


class LinearBlockSweep(pgml.Sweeper[patch.LinearBlockPatch]):
    """Linear block configuration"""

    in_features: pgml.IntSweep | None = None
    """Number of input features"""

    out_features: pgml.IntSweep | None = None
    """Number of output features"""

    bias: pgml.BoolSweep | None = None
    """Bias"""

    dropout: pgml.FloatSweep | None = None
    """Dropout probability"""

    activation: pgml.StrSweep | None = None
    """Activation function"""



LinearBlockSweepField = typing.Union[
    LinearBlockSweep,
    pgml.NestedChoice[LinearBlockSweep, patch.LinearBlockPatch],  # type: ignore
]


class MLPSweep(pgml.Sweeper[patch.MLPPatch]):
    """MLP configuration"""

    layers: LinearBlockSweepField | None = None
    """Linear blocks"""



MLPSweepField = typing.Union[
    MLPSweep,
    pgml.NestedChoice[MLPSweep, patch.MLPPatch],  # type: ignore
]

