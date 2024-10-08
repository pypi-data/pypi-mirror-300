"""Module containing some useful types.

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

from pydantic import BaseModel

##### Some custom pydantic classes used for the different configuration files. #####

# Emulation config.


class ConfigPCA(BaseModel):
    do_pca: bool = True
    pca_components: "int | float | str | None" = None
    pca_scale_data_mean: bool = True
    pca_scale_data_std: bool = True
    niter: int = 1000


class ConfigGP(BaseModel):
    kernel_nu: float = -1
    normalize_y: bool = True
    n_restarts_optimizer: int = 10


class ConfigEmulatorStd(BaseModel):
    allow_return_std: bool = True
    use_gp_std_factor: bool = False
    niter: int = 1000


class ConfigData1D(BaseModel):
    data_type: str = "binned"
    bin_name: str = "bin"
    use_data_std: bool = False
    binned_x_interp_type: str = "lin"
    binned_y_interp_type: str = "lin"
    bspline_x_transform: str = "lin"
    bspline_y_transform: str = "lin"


class ConfigGPE1D(BaseModel):
    pca: ConfigPCA = ConfigPCA()
    gp: ConfigGP = ConfigGP()
    emulator_std: ConfigEmulatorStd = ConfigEmulatorStd()
    data: ConfigData1D = ConfigData1D()


class ConfigNode(BaseModel):
    x_interp_type: str = "lin"
    y_interp_type: str = "lin"
    node_name: str = "node_var"
    niter: int = 1000

class ConfigGPE1Dx1D(BaseModel):
    config_gpe_1D: ConfigGPE1D = ConfigGPE1D()
    config_node: ConfigNode = ConfigNode()
