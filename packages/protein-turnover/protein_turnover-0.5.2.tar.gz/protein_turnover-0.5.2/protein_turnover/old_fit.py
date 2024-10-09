from __future__ import annotations

from typing import Any
from typing import Callable

import numpy as np
from scipy.fft import fft
from scipy.fft import ifft

from .utils import ATOMICPROPERTIES
from .utils import ensure_pos
from .utils import getEnrichments
from .utils import labelledAtomicAbundances
from .utils import labelledAtomicAbundancesAtMaxEnrich
from .utils import NAMES
from .utils import peptideFormula
from .utils import PeptideSettings
from .utils import resize

# **UNUSED now**
assert False


def heavy_dist(
    peptide: str,
    _settings: PeptideSettings,
    isotopeEnvelopes: np.ndarray,
) -> np.ndarray:
    ndist = isotopicDistribution(peptide)
    # remove neagive massDiff
    env = isotopeEnvelopes[1:]

    monoPeakArea = env[0]

    naturalIsotopeEnvelope = monoPeakArea * ndist / ndist[0]
    naturalIsotopeEnvelope = resize(naturalIsotopeEnvelope, len(env))

    heavyDistribution = ensure_pos(
        env - naturalIsotopeEnvelope,
    ).astype(np.float32)
    return heavyDistribution


def natural_dist(
    peptide: str,
    _settings: PeptideSettings,
    isotopeEnvelopes: np.ndarray,
) -> np.ndarray:
    isod = isotopicDistribution(peptide)
    denom = isod[0]
    denom = denom if denom > 0.0 else 1.0
    return isotopeEnvelopes[1] * isod / denom


# see https://pubs.acs.org/doi/pdf/10.1021/ac500108n
def makeEnvelopeArray(
    peptide: str,
    maxIso: int,
    settings: PeptideSettings,
) -> tuple[np.ndarray, np.ndarray]:
    enrichments = getEnrichments(peptide, settings)
    ncols = len(enrichments)
    # elementCount = ncols - 1
    isotopeEnvelopeBasis = np.zeros(shape=(maxIso + 1, ncols))
    for i, elementEnrichmentLevel in enumerate(enrichments):
        abundances = {
            settings.labelledElement: labelledAtomicAbundances(
                settings.labelledIsotopeNumber,
                settings.labelledElement,
                elementEnrichmentLevel,
            ),
        }

        d = isotopicDistribution(peptide, abundances)
        maxEl = min(len(d), maxIso + 1)
        isotopeEnvelopeBasis[:maxEl, i] = d[:maxEl]
    return enrichments, isotopeEnvelopeBasis


def isotopicDistribution(
    peptideSequence: str,
    abundances: dict[str, np.ndarray] | None = None,
    abundanceCutoff: float = 1e-10,
    maxMass: int = 100,
) -> np.ndarray[Any, np.dtype[np.float64]]:
    """return abundance of "heavy" peptides"""
    if abundances is None:
        abundances = {}

    formula = peptideFormula(peptideSequence)

    maxElements = np.sum(formula > 0, dtype=int)

    A = np.zeros((maxElements, maxMass))

    elements = []
    for i, e in enumerate(NAMES):
        n = formula[i]
        if n > 0:
            elements.append(n)
            if e in abundances:
                a = abundances[e]
            else:
                # use natural abundance
                a = ATOMICPROPERTIES[e]["abundance"]
            A[len(elements) - 1, 0 : len(a)] = a
    tA = fft(A)
    ptA = np.ones((maxMass,), dtype=np.complex128)

    for i in range(maxElements):
        ptA *= tA[i] ** elements[i]

    riptA = np.real(ifft(ptA))
    mx = np.max(np.where(riptA > abundanceCutoff))
    riptA = riptA[0 : int(mx) + 1]
    return np.fmax(riptA, 0.0)
    # return np.where(riptA > 0.0, riptA, 0.0)


def mk_maxIso(settings: PeptideSettings) -> Callable[[str], int]:
    from .config import ABUNDANCE_CUTOFF

    abundances = {
        settings.labelledElement: labelledAtomicAbundancesAtMaxEnrich(settings),
    }

    # maxIso length of ndist[E] to 0.01
    def maxIso(peptide: str) -> int:
        return len(isotopicDistribution(peptide, abundances, ABUNDANCE_CUTOFF)) - 1

    return maxIso
