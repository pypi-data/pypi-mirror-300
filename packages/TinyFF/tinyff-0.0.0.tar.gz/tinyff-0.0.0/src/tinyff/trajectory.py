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
"""Utilities for writing trajectories to disk.

This module supports two output formats:

- Human readiable PDB trajectories (for nglview and mdtraj).
- Directory of NPY files (for custom post-processing)
"""

import os
from functools import partial
from glob import glob

import attrs
import numpy as np
from npy_append_array import NpyAppendArray
from numpy.typing import ArrayLike, NDArray

from .utils import parse_atpos, parse_cell_lengths

__all__ = ("PDBWriter", "NPYWriter")

SYMBOLS = """
H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn
Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La
Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po
At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg
Cn Nh Fl Mc Lv Ts Og""".split()


@attrs.define
class PDBWriter:
    """PDB Trajectory writer.

    Notes
    -----
    Upon creation of an instance, a previously existing PDB is removed, if any.
    """

    path_pdb: str = attrs.field(converter=str)
    """Path of the PDB file to be written."""

    to_angstrom: float = attrs.field(converter=float, kw_only=True)
    """Conversion factor to be multiplied with positions to get value in Angstrom, 1e-10 neter."""

    atnums: NDArray[float] = attrs.field(converter=partial(np.asarray, dtype=int), kw_only=True)

    def __attrs_post_init__(self):
        if os.path.isfile(self.path_pdb):
            os.unlink(self.path_pdb)

    def dump(self, atpos: ArrayLike, cell_lengths: ArrayLike):
        atpos = parse_atpos(atpos, len(self.atnums))
        cell_lengths = parse_cell_lengths(cell_lengths)
        with open(self.path_pdb, "a") as fh:
            a, b, c = cell_lengths * self.to_angstrom
            print(f"CRYST1{a:9.3f}{b:9.3f}{c:9.3f}  90.00  90.00  90.00 P 1           1", file=fh)
            for i, (x, y, z) in enumerate(atpos * self.to_angstrom):
                symbol = SYMBOLS[self.atnums[i] - 1]
                print(
                    f"HETATM{i+1:5d} {symbol:2s}   ATM     1    {x:8.3f}{y:8.3f}{z:8.3f}"
                    f"  1.00  1.00          {symbol:2s}",
                    file=fh,
                )
            print("END", file=fh)


@attrs.define
class NPYWriter:
    """Write trajectory to bunch of NPY files in directory.

    Notes
    -----
    - If the directory does not exist, it is created.
    - If the directory exists and it contains no other files than NPY files, it is removed first.
    - In all other cases, an error is raised.
    """

    dir_out: str = attrs.field(converter=str)
    """Path of the output directory."""

    fields: dict[str] = attrs.field(init=False, factory=dict)
    """Fields to be written at every dump call."""

    def __attrs_post_init__(self):
        if os.path.isdir(self.dir_out):
            for path in glob(os.path.join(self.dir_out, "*.npy")):
                os.unlink(path)
            os.rmdir(self.dir_out)
        if os.path.exists(self.dir_out):
            raise RuntimeError(f"{self.dir_out} cannot be cleaned up: unexpected old contents.")
        os.makedirs(self.dir_out)

    def dump(self, **kwargs):
        for key, value in kwargs.items():
            # Check array properties
            shape, dtype = self.fields.get(key, (None, None))
            arvalue = np.asarray(value)
            if shape is None:
                shape = arvalue.shape
                dtype = arvalue.dtype
                self.fields[key] = (shape, dtype)
            else:
                if shape != arvalue.shape:
                    raise TypeError(
                        f"The shape of {key}, {arvalue.shape}, differs from the first one, {shape}"
                    )
                if dtype != arvalue.dtype:
                    raise TypeError(
                        f"The dtype of {key}, {arvalue.dtype}, differs from the first one, {dtype}"
                    )
            # Append to NPY file
            path = os.path.join(self.dir_out, f"{key}.npy")
            with NpyAppendArray(path, delete_if_exists=False) as npaa:
                npaa.append(arvalue.reshape(1, *arvalue.shape))
