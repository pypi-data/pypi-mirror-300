"""Module used to load emulation data.

Copyright (C) 2023 Iñigo Sáez-Casares - Université Paris Cité

inigo.saez-casares@obspm.fr

This file is part of e-mantis.

e-mantis is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import h5py
import numpy as np
import numpy.typing as npt

try:
    from importlib.resources import as_file, files
except ModuleNotFoundError:
    from importlib_resources import as_file, files

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

RESOURCES = files("emantis")


def read_config_emu(observable: str, model: str, sim_version: int) -> dict:

    # Emulation config file name.
    filename = (
        RESOURCES
        / f"data/{observable}/{observable}_{model}_emu_v{sim_version}_emulation_config.toml"
    )
    # Read emulation data config.
    with as_file(filename) as mytoml:
        with open(mytoml, "rb") as f:
            config_emu_dict: dict = tomllib.load(f)

    return config_emu_dict


def read_cosmo_params(model: str, sim_version: int) -> tuple[npt.NDArray, list, dict]:

    # Read names and values of the cosmological parameters.
    with as_file(
        RESOURCES / f"data/cosmo_params_{model}_emu_v{sim_version}.txt"
    ) as mytxt:
        # First read the names of the cosmological parameters.
        cosmo_params_names: list = list(np.genfromtxt(mytxt, dtype="U20", max_rows=1))
        # Now read the values of the cosmological parameters for all models.
        cosmo_params: npt.NDArray = np.genfromtxt(mytxt, skip_header=1)

    # Read emulation range in terms of cosmological parameters.
    with as_file(
        RESOURCES / f"data/cosmo_params_{model}_emu_v{sim_version}_config.toml"
    ) as mytoml:
        with open(mytoml, "rb") as f:
            config_dict: dict = tomllib.load(f)
            cosmo_params_range: dict = config_dict["range"]

    return cosmo_params, cosmo_params_names, cosmo_params_range


def read_bspline_data(
    observable: str,
    model: str,
    sim_version: int,
    prefix: "str | None" = None,
    read_data_std: bool = False,
    read_gp_std_factor: bool = False,
) -> tuple[
    list[float],
    dict[float, npt.NDArray],
    "dict[float, npt.NDArray] | None",
    dict[float, npt.NDArray],
    dict[float, int],
    "dict[float, npt.NDArray] | None",
]:

    if prefix is None:
        prefix = ""

    # Init. empty dicts. to store the data at different scale factors.
    data = {}
    bspline_knots = {}
    bspline_degree = {}

    if read_data_std:
        data_std = {}
    else:
        data_std = None

    if read_gp_std_factor:
        gp_std_factor = {}
    else:
        gp_std_factor = None

    # Data filename.
    filename = f"{observable}_{model}_emu_v{sim_version}_data.h5"

    # Read data.
    with as_file(RESOURCES / f"data/{observable}/{filename}") as myh5file:
        with h5py.File(myh5file) as f:
            aexp_nodes = list(f[f"{prefix}/aexp_list"][:])
            for aexp in aexp_nodes:
                data[aexp] = f[f"{prefix}/data_aexp_{aexp:.4f}"][:]
                bspline_knots[aexp] = f[f"{prefix}/bspline_knots_aexp_{aexp:.4f}"][:]
                bspline_degree[aexp] = f[f"{prefix}/bspline_degree_aexp_{aexp:.4f}"][()]
                if read_data_std:
                    data_std[aexp] = f[f"{prefix}/data_std_aexp_{aexp:.4f}"][:]
                if read_gp_std_factor:
                    gp_std_factor[aexp] = f[f"{prefix}/gp_std_factor_aexp_{aexp:.4f}"][:]

    return aexp_nodes, data, data_std, bspline_knots, bspline_degree, gp_std_factor
