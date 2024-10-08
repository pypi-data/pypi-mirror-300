"""Module with some utility functions to handle user inputs.

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

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import numpy as np
import numpy.typing as npt

from emantis.exceptions import EmulationRangeError


def format_input_params_to_array(
    input_params: "dict[str, 'float | list[float] | npt.NDArray'] | npt.NDArray",
    required_params_names: "list[str] | None",
    required_params_range: "dict[str, dict[str, float]] | None" = None,
) -> npt.NDArray:
    """Format input parameters to an array.

    The input `input_params` can be an array or a dict.

    If the input is an array it is returned as is.
    If `required_params_range` is not None,  check the range of each parameter.
    If `required_params_names` is not None, it will assume that the parameters are ordered
    as in `required_params_names`.
    Otherwise, it will assume that the parameters are ordered as the keys of `required_params_range`.

    If the input is a dict, it will convert it into an array.
    First, it orders the input parameters according to `required_params_names`.
    At the same time, it checks that the provided dict entries have valid names, and
    that all the required parameters are present.
    If `required_params_names` is None, it raises an exception.
    If `required_params_range` is not None, it will check the range of each parameter.

    When checking the range of the parameters, it raises an exception if one sample is out of range.

    Parameters
    ----------
    input_params : dict or ndarray of shape (n_samples, n_params)
        A dictionary with the input parameters.
    required_params_names : list[str] of length `n_params`.
        The list of required parameters, where `n_params` is the number of parameters.
        The input parameters are ordered according to this list.
        Raises KeyError if one of the input parameters is not in this list, or if one parameter
        from this list is not in the input dict.
    required_params_range : dict or None, optional (default=None)
        The minimum and maximum accepted value for each parameter.
        If not None, raises EmulationRangeError if one of the input parameters is outside
        the accepted range.

    Returns
    -------
    params_array : ndarray of shape (n_params,) or (n_samples, n_params)
        Array containing the input parameters, where `n_params` is the number
        of parameters and `n_samples` the number of inputs per parameter.
    """
    if isinstance(input_params, np.ndarray):
        params_array = input_params

        # Reshape input parameters if necessary.
        if params_array.ndim == 1:
            params_array = params_array.reshape(1, -1)

        # Check each parameter range if necessary.
        if required_params_range is not None:
            if required_params_names is None:
                required_params_names = list(required_params_range)

            # Loop over all parameters.
            for i, param in enumerate(required_params_names):
                check_emulation_range(
                    params_array[:, i],
                    required_params_range[param]["min_value"],
                    required_params_range[param]["max_value"],
                    param,
                )

    elif isinstance(input_params, dict):
        if required_params_names is None:
            raise TypeError(
                """This instance only accepts the 'params' argument in the form of an array,
                    since the 'params_names' argument was not provided when instantiated."""
            )

        # First check names (and range) of input parameters.
        check_input_params_dict(
            input_params, required_params_names, required_params_range
        )

        # Init. counter for the number of samples per parameter.
        n_samples: int = 1
        # First loop over all parameters in the input dict. in order
        # to check how many values have been passed for each of them.
        for param in input_params:
            # Recover the set of values for a given parameter
            # in the form of a 1D array.
            param_array: npt.NDArray = format_input_to_1d_array(
                input_params[param], param
            )
            n: int = param_array.shape[0]
            if n > n_samples:
                if n_samples == 1:
                    n_samples = n
                else:
                    # TODO custom exception or better error message.
                    raise ValueError("Wrong format for input parameters.")

        # Init. final params array.
        params_array: npt.NDArray = np.zeros((n_samples, len(required_params_names)))
        # Second loop over all parameters in order
        # to gather them in an array.
        for i, param in enumerate(required_params_names):
            # Recover the set of values for a given parameter
            # in the form of a 1D array.
            # TODO optimize: avoid recomputing this.
            param_array = format_input_to_1d_array(input_params[param], param)
            n = param_array.shape[0]
            if n == 1:
                param_array = np.array([param_array[0] for k in range(n_samples)])
            params_array[:, i] = param_array
    else:
        raise TypeError("Argument 'params' must be a dict or a ndarray.")

    return params_array


def check_input_params_dict(
    input_params_dict: dict[str, "float | list[float] | npt.NDArray"],
    required_params_names: list[str],
    required_params_range: "dict[str, dict[str, float]] | None" = None,
) -> None:
    """Check input parameter dict.

    Check that the input parameters have valid names, and that all the required parameters
    have been provided.

    Can also check the range of the input parameters (see `required_params_range`).

    Parameters
    ----------
    input_params_dict : dict
        A dictionary with the input parameters.
    required_params_names : list[str] of length `n_params`.
        The list of required parameters, where `n_params` is the number of parameters.
        Raises KeyError if one of the input parameters is not in this list, or if one parameter
        from this list is not in the input dict.
    required_params_range : dict or None, optional (default=None)
        The minimum and maximum accepted value for each parameter.
        If not None, raises EmulationRangeError if one of the input parameters is outside
        the accepted range.
    """

    # Loop over input parameters.
    for param in input_params_dict:
        # Check that each input parameter names are valid.
        if param not in required_params_names:
            raise KeyError(
                f"Cosmological parameter {param} not supported by this emulator."
            )
        # If required_params_range is not None,
        # check that the input parameters are within the accepted range.
        if required_params_range is not None:
            check_emulation_range(
                input_params_dict[param],
                required_params_range[param]["min_value"],
                required_params_range[param]["max_value"],
                param,
            )
    # Finally, check that all the required parameters have been provided.
    for param in required_params_names:
        if param not in input_params_dict:
            raise KeyError(f"You need to provide at least one value for {param}.")


def check_emulation_range(
    values: npt.ArrayLike, range_min: float, range_max: float, name: str
) -> None:
    """Verifies that values for some arbitrary quantity are within the emulation range.

    Raises an EmulationRangeError exception if it's not the case.
    The exception will be raised if one or more values are outside the range.

    Parameters
    ----------
    values : array-like
        The values of the quantity of interest.
    range_min : float
        The minimum of the emulation range for the quantity of interest.
    range_max : float
        The maximum of the emulation range for the quantity of interest.
    name : str
        The name of the quantity of interest.
    """
    min_value: float = np.min(values)
    max_value: float = np.max(values)
    if min_value < range_min:
        raise EmulationRangeError(min_value, name, range_min, range_max)
    if max_value > range_max:
        raise EmulationRangeError(max_value, name, range_min, range_max)


def format_input_to_1d_array(
    x: "float | list | npt.NDArray", x_name: "str | None" = None
) -> npt.NDArray:
    """Transform input into a 1D numpy array.

    Raises TypeError if the input is not a float, list or a 1D array.

    Parameters
    ----------
    x : float or list or array of shape (N,)
        The input.
    x_name : str
        The name of the input variable, used to customize raised exception.

    Returns
    -------
    x_array : array of shape (N,)
        The input transformed into a numpy 1D array.
    """
    # Default x_name.
    if x_name is None:
        x_name = "x"
    # Check if x is an int or float (scalar).
    if not isinstance(x, bool) and isinstance(x, (int, float)):
        x_array = np.array([x])
    # Check if x is a list.
    elif isinstance(x, list):
        x_array = np.array(x)
    # Check if x is an array.
    elif isinstance(x, np.ndarray):
        # Check dimension.
        if x.ndim != 1:
            raise TypeError(f"{x_name} must be float, list or 1D array.")
        x_array = x
    else:
        raise TypeError(f"{x_name} must be float, list or 1D array.")

    return x_array
