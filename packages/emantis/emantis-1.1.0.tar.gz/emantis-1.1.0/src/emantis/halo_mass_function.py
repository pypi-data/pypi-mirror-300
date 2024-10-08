"""Module implementing an emulator for the halo mass function.

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

import numpy.typing as npt

from emantis._gp_emulation import GaussianProcessEmulator1Dx1D
from emantis._read_data import read_bspline_data, read_config_emu, read_cosmo_params

_MODELS = ["wCDM", "fR"]

_FOF_B_VALUES = [0.2]
_SO_DELTAC_VALUES = [200, 500, 1000]


class HMFEmulator(GaussianProcessEmulator1Dx1D):
    """Emulator for the halo mass function (HMF).

    Multiple types of cosmological models and dark matter halo definitions are supported.

    Parameters
    ----------

    model : str
        Type of cosmological model. Possible choices are:

            - "wCDM": dark energy with constant equation of state parameter,
            - "fR": Hu & Sawicki :math:`f(R)` gravity (limited to :math:`n=1`).
    mass_def : str
        Mass definition. Possible choices are:

            - For Friend-of-Friends (FoF) haloes, parameterized by the linking length: 'b0.2'
            - For Spherical Overdensity (SO) haloes, parameterized by the critical overdensity threshold: '200c', '500c', '1000c'.
    use_resolution_correction : bool, optional (default=True)
        Whether to use or not a resolution correction for the low mass end of the HMF.
    random_seed : int or None, optional (default=None)
        A random seed used for different random generators.
    n_jobs : int, optional (default=1)
        Maximum number of independent processes used to train the emulator.
        A value of -1 uses all available cores.
        Predictions always use ``n_jobs=1``, since they are already fast and the parallelism overhead is not worth it.
        Additional parallelism might be used (via Numpy, SciPy, OpenMP), even when ``n_jobs=1``.
        See the scikit-learn `documentation <https://scikit-learn.org/stable/computing/parallelism.html#parallelism>`_ for more details.
    verbose : bool, optional (default=True)
        Whether to activate or not verbose output.
    """

    def __init__(
        self,
        model: str,
        mass_def: str,
        use_resolution_correction: bool = True,
        random_seed: "int | None" = None,
        n_jobs: int = 1,
        verbose: bool = True,
    ) -> None:

        # Check model.
        if model not in _MODELS:
            raise ValueError(f"`model` must be one of: {_MODELS}.")

        # Observable name and simulation suite version.
        observable = "halo_mass_function"
        sim_version = 2

        # Read emulation configuration.
        config_emu_dict = read_config_emu(observable, model, sim_version)

        # Read cosmological parameters.
        cosmo_params, cosmo_params_names, cosmo_params_range = read_cosmo_params(
            model, sim_version
        )

        # Process mass_def.
        mass_def_string = self._process_mass_def(mass_def)

        # Read training data.
        data_prefix = f"{mass_def_string}/res_corr_{use_resolution_correction}"
        (
            aexp_nodes,
            data,
            data_std,
            bspline_knots,
            bspline_degree,
            gp_std_factor,
        ) = read_bspline_data(
            observable,
            model,
            sim_version,
            prefix=data_prefix,
            read_data_std=config_emu_dict["config_gpe_1D"]["data"]["use_data_std"],
            read_gp_std_factor=config_emu_dict["config_gpe_1D"]["emulator_std"][
                "use_gp_std_factor"
            ],
        )

        super().__init__(
            params=cosmo_params,
            data=data,
            data_bins=bspline_knots,
            data_nodes=aexp_nodes,
            data_std=data_std,
            bspline_degree=bspline_degree,
            gp_std_factor=gp_std_factor,
            params_names=cosmo_params_names,
            params_range=cosmo_params_range,
            config_emu=config_emu_dict,
            random_seed=random_seed,
            n_jobs=n_jobs,
            verbose=verbose,
            ignore_training_warnings=True,
            logger_name=f"e-MANTIS:hmf:{mass_def}",
        )

    def _process_mass_def(self, mass_def: str) -> str:
        """Process the user provided mass definition.

        Return the required mass definition string to read the emulation data.
        """

        # FoF haloes.
        if "b" in mass_def:
            # Read linking length.
            try:
                b_fof = float(mass_def.replace("b", ""))
            except ValueError:
                raise ValueError("Incorrect `mass_def` value.")
            # Check linking length.
            if b_fof not in _FOF_B_VALUES:
                raise ValueError(
                    f"Unsupported linking length for FoF haloes. Allowed values are: {_FOF_B_VALUES}."
                )
            mass_def_string = f"b_fof_{b_fof:g}"

        # SO haloes with overdensity threshold in critical density units.
        elif "c" in mass_def:
            # Read overdensity threshold.
            try:
                delta_c = float(mass_def.replace("c", ""))
            except ValueError:
                raise ValueError("Incorrect `mass_def` value.")
            # Check overdensity threshold.
            if delta_c not in _SO_DELTAC_VALUES:
                raise ValueError(
                    f"Unsupported critical overdensity threshold for SO haloes. Allowed values are: {_SO_DELTAC_VALUES}."
                )
            mass_def_string = f"deltac_{delta_c:g}"

        else:
            raise ValueError(f"Incorrect mass definition (`mass_def`).")

        return mass_def_string

    def predict_hmf(
        self,
        mass_halo: "float | list[float] | npt.NDArray",
        cosmo_params: dict[str, "float | list[float] | npt.NDArray"],
        aexp: "float | list[float] | npt.NDArray",
        return_std: bool = False,
        squeeze: bool = True,
    ) -> npt.NDArray:
        """Predict the halo mass function.

        Multiple sets of cosmological parameters can be passed at once by giving them in the form of arrays or lists (see tutorial).
        This function will return a prediction for the halo mass function for each entry.
        Calling the function to give predictions for N models at once is significantly faster than calling it N times for a single model.

        Additionally, multiple scale factors per model can be requested at once.
        If `aexp` has ``n_aexp`` entries, then ``n_aexp`` outputs will be given for each model.

        The emulator training will be performed as necessary each time a new scale factor
        node is requested (or needed for scale factor interpolation) for the first time.
        Alternatively, :func:`~emantis.gp_emulation.GaussianProcessEmulator1Dx1D.train` can be called once in order to
        train all nodes before requesting any predictions.
        The training is fast and should not take more than a few seconds per node on a standard laptop processor.

        Parameters
        ----------
        mass_halo : float or list or array of shape (n_mass,)
            The halo mass values at which to output the halo mass function in units of Mpc/h.
            The same halo mass values are used for all cosmological models and scale factors.
        cosmo_params : dict
            A dictionary passing the cosmological parameters.
        aexp : float or list or array of shape (n_aexp,)
            Scale factor values.
        return_std : bool, optional (default=False)
            If True, also return the standard deviation of the predictions.
            Might slow down the computation.
        squeeze : bool, optional (default=True)
            If True, remove axes of length one from `pred`.

        Returns
        -------
        pred : ndarray
            Predicted halo mass function at the input halo masses, cosmological models, and scale factor values.
            The output is an array of shape (n_aexp, n_cosmo, n_mass),
            where ``n_aexp`` is the number of aexp values per cosmological model,
            ``n_cosmo`` is the number of cosmological models, and ``n_mass`` the number of halo mass values.
            By default the output array is squeezed to remove axes of length one.
            This behaviour can be changed with the `squeeze` parameter.
        """
        return super()._predict_observable(
            bins=mass_halo,
            params=cosmo_params,
            node_var=aexp,
            return_std=return_std,
            squeeze=squeeze,
        )
