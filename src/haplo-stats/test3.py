#!/usr/bin/env python
import sys
from pathlib import Path

import numpy as np

DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(Path(DIR) / ".."))

from PyPop.Haplo import _compute_LD  # noqa: E402

# FIXME: these arrays have to be in same order
# this is fragile and probably needs changing in main code
haplos = np.array([["A1", "B1"], ["A2", "B1"], ["A1", "B2"], ["A2", "B2"]], dtype="O")
freqs = np.array([0.3, 0.1, 0.1, 0.5])

_compute_LD(haplos, freqs, compute_ALD=True, debug=True)
