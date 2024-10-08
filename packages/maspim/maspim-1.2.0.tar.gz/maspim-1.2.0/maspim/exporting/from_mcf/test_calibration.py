"""
trying to implement internal lock-masss calibration from
https://pubs.acs.org/doi/epdf/10.1021/ac400972y?ref=article_openPDF
using binomial averages (section 'Internal Calibration')
"""
from collections.abc import Callable

import numpy as np
from scipy.special import binom

# mz = np.array([])  # true mz values
# A = np.array([])  # true abundance

# mass error function (to be determined)
# def epsilon(mz: np.ndarray, A: np.ndarray) -> np.ndarray:
#     pass

# mz_obs = np.array([])  # observed mz values (we take those from closest values in the spectra)
# observed intensities assumed to be the same as true abundances

# we obtain (relative) mass errors
# (eq. 9)
# epsilon_j = (mz_obs - mz) / mz

# accuracy increases for more calibrants but limited by SNR

# iterative approach
#   i) assign elemental composition with current mass accuracy
#   ii) estimate mass error function using calibrants
#   iii) recalibrate using estimated calibration function
# --> maximizes accuracy
# (sounds like we need something more light-weight for MALDI)

# obtaining error function from mz, mz_obs, A
# we want to find epsilon_est such that abs(epsilon_est - epsilon) is minimized

# we are assuming epsilon varies from observed epsilon_j by random errors delta_j
# delta_j may vary with m/z, we define
# epsilon_j_exp = epsilon(mz[j]) + delta_j

# it is a good assumption that epsilon can be estimated from some local average
# epsilon(mz) = sum_{j=0}^n w_j(mz) * epsilon_j_exp
# where we have to determine w_j
# in the paper they advocate the binomial average


def B(k: int, l: int, rs: np.ndarray) -> float:
    """
    calculate binomial central averaged values

    :param rs: points
    :param l: index of point to be averaged
    :param k: order of binomial central moving average (0 <= k <= n)
    """
    s = 0
    for j in range(k):
        s += 1 / 2 ** k * binom(k, j) * rs[l + j]
    return s

# now we choose k to be as big as possible for each l in [0, n_k]
# for r0 this is n
# for r1 this is n-1


def B_max_k(l: int, rs: np.ndarray) -> float:
    # k is limited by number of entries in rs
    # since n = len(rs) and the loop accesses elements l+r,
    # k has to be at most n-l
    k: int = len(rs) - l
    return B(k, l, rs)


# epsilon_est is now this coefficient and values in-between are linearly interpolated
# mz_averaged = [B_max_k(l, mz_obs) for l in range(len(mz_obs))]
# epsilon_averaged = [B_max_k(l, epsilon_j) for l in range(len(epsilon_j))]


# def epsilon(mz: float | np.ndarray) -> float | np.ndarray:
#     """binomial average"""
#     return np.interp(mz, mz_averaged, epsilon_averaged)


# or putting everything into one function
def find_epsilon(mz_obs: np.ndarray, mz_theo: np.ndarray) -> Callable:
    epsilon_j: np.ndarray = (mz_obs - mz_theo) / mz_theo

    mz_averaged: list[float] = [B_max_k(l, mz_obs) for l in range(len(mz_obs))]
    epsilon_averaged: list[float] = [B_max_k(l, epsilon_j) for l in range(len(epsilon_j))]

    def epsilon(mz: float | np.ndarray) -> float | np.ndarray:
        """binomial average"""
        return np.interp(mz, mz_averaged, epsilon_averaged)

    return epsilon


# %% test
import matplotlib.pyplot as plt

mz_theo = np.arange(100, 120)

mz_obs = mz_theo.copy() + np.random.normal(size=mz_theo.shape)

eps = find_epsilon(mz_obs, mz_theo)

plt.plot(mz_obs, eps(mz_obs))
plt.show()


# TODO: check if this is corrected (i am not too confident)
# iteration using assigned formulas
