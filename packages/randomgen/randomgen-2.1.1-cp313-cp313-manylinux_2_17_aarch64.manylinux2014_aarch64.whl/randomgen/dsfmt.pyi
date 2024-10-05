from collections.abc import Sequence

import numpy as np
from typing_extensions import TypeAlias

from randomgen.common import BitGenerator
from randomgen.typing import IntegerSequenceSeed, SeedMode

DSFMTState: TypeAlias = dict[str, str | int | np.ndarray | dict[str, int | np.ndarray]]

class DSFMT(BitGenerator):
    def __init__(
        self, seed: IntegerSequenceSeed | None = ..., *, mode: SeedMode | None = ...
    ) -> None: ...
    def seed(self, seed: int | Sequence[int] = ...) -> None: ...
    def jump(self, iter: int = ...) -> DSFMT: ...
    def jumped(self, iter: int = ...) -> DSFMT: ...
    @property
    def state(self) -> DSFMTState: ...
    @state.setter
    def state(self, value: DSFMTState) -> None: ...
