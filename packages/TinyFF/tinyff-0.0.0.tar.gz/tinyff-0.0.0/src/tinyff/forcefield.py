# TinyFF is a minimalistic Force Field evaluator.
# Copyright (C) 2024 Toon Verstraelen
#
# This file is part of TinyFF.
#
# TinyFF is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# TinyFF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
# --
"""Basic Force Field models."""

from collections.abc import Callable

import attrs
import numpy as np
from numpy.typing import ArrayLike, NDArray

from .neighborlist import NLIST_DTYPE, build_nlist_simple, recompute_nlist

__all__ = ("PairwiseForceField",)


@attrs.define
class PairPotential:
    def __call__(self, dist: ArrayLike) -> tuple[NDArray, NDArray]:
        """Compute pair potential energy and its derivative towards distance."""
        raise NotImplementedError  # pragma: nocover


@attrs.define
class LennardJones(PairPotential):
    epsilon: float = attrs.field(converter=float)
    sigma: float = attrs.field(converter=float)

    def __call__(self, dist: ArrayLike) -> tuple[NDArray, NDArray]:
        """Compute pair potential energy and its derivative towards distance."""
        dist = np.asarray(dist, dtype=float)
        x = self.sigma / dist
        energy = (4 * self.epsilon) * (x**12 - x**6)
        gdist = (-4 * self.epsilon * self.sigma) * (12 * x**11 - 6 * x**5) / dist**2
        return energy, gdist


@attrs.define
class CutOffWrapper(PairPotential):
    original: PairPotential = attrs.field()
    rcut: float = attrs.field(converter=float)
    ecut: float = attrs.field(init=False, default=0.0, converter=float)
    gcut: float = attrs.field(init=False, default=0.0, converter=float)

    def __attrs_post_init__(self):
        """Post initialization changes."""
        self.ecut, self.gcut = self.original(self.rcut)

    def __call__(self, dist: ArrayLike) -> tuple[NDArray, NDArray]:
        """Compute pair potential energy and its derivative towards distance."""
        dist = np.asarray(dist, dtype=float)
        mask = dist < self.rcut
        if mask.ndim == 0:
            # Deal with non-array case
            if mask:
                energy, gdist = self.original(dist)
                energy -= self.ecut + self.gcut * (dist - self.rcut)
                gdist -= self.gcut
            else:
                energy = 0.0
                gdist = 0.0
        else:
            energy, gdist = self.original(dist)
            energy[mask] -= self.ecut + self.gcut * (dist[mask] - self.rcut)
            energy[~mask] = 0.0
            gdist[mask] -= self.gcut
            gdist[~mask] = 0.0
        return energy, gdist


@attrs.define
class PairwiseForceField:
    pair_potential: PairPotential = attrs.field(
        validator=attrs.validators.instance_of(PairPotential)
    )
    """A definition of the pair potential."""

    rcut: float = attrs.field(converter=float)
    """The cutoff radius used to build the neighbor list."""

    @rcut.validator
    def _validate_rcut(self, attribute, value):
        if value > self.rmax:
            raise ValueError("rmax cannot be less than rcut.")

    build_nlist: Callable = attrs.field(default=build_nlist_simple, kw_only=True)
    """Function used to build the neigbor list from scratch."""

    rmax: float = attrs.field(converter=float, kw_only=True)
    """The maximum radius up to which pairs are kept in the neigborlist."""

    @rmax.default
    def _default_rmax(self):
        return self.rcut

    @rmax.validator
    def _validate_rmax(self, attribute, value):
        if value < self.rcut:
            raise ValueError("rmax cannot be less than rcut.")

    nlist_reuse: int = attrs.field(converter=int, default=0, kw_only=True)
    """Number of times the neighbor list is reused (recomputed without rebuilding)."""

    _nlist_use_count: int = attrs.field(converter=int, default=0, init=False)
    """Internal counter to decide when to rebuild neigborlist."""

    @property
    def nlist_use_count(self):
        """The number of times the current neighborlist will be reused in future calculations."""
        return self._nlist_use_count

    nlist: NDArray[NLIST_DTYPE] | None = attrs.field(init=False, default=None)

    def __call__(self, atpos: NDArray, cell_length: float):
        """Compute microscopic properties related to the potential energy.

        Parameters
        ----------
        atpos
            Atomic positions, one atom per row.
            Array shape = (natom, 3).
        cell_length
            The length of the edge of the cubic simulation cell.

        Returns
        -------
        energy
            The potential energy.
        forces
            The forces acting on the atoms, same shape as atpos.
        mech_pressure
            The force-contribution to the pressure.
        """
        # Sanity check
        if cell_length < 2 * self.rcut:
            raise ValueError("Cell length is too short.")
        # Build or reuse the neighborlist
        if self._nlist_use_count <= 1:
            self.nlist = None
        else:
            self._nlist_use_count -= 1
        cell_lengths = np.full(3, cell_length)
        if self.nlist is None:
            nlist = self.build_nlist(atpos, cell_lengths, self.rcut)
            self._nlist_use_count = self.nlist_reuse
        else:
            nlist = self.nlist
            recompute_nlist(atpos, cell_lengths, nlist)
        # Compute all pairwise quantities
        nlist["energy"], nlist["gdist"] = self.pair_potential(nlist["dist"])
        nlist["gdelta"] = (nlist["gdist"] / nlist["dist"]).reshape(-1, 1) * nlist["delta"]
        # Compute the totals
        energy = nlist["energy"].sum()
        forces = np.zeros(atpos.shape, dtype=float)
        np.add.at(forces, nlist["iatom0"], nlist["gdelta"])
        np.add.at(forces, nlist["iatom1"], -nlist["gdelta"])
        mech_pressure = -np.dot(nlist["gdist"], nlist["dist"]) / (3 * cell_length**3)
        # Keep the neigborlist for the following function call
        self.nlist = nlist
        return energy, forces, mech_pressure
