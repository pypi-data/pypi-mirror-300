"""Module with some utility functions.

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

import numpy as np
import numpy.typing as npt


def lin_interp(
    x0: "float | npt.NDArray",
    x1: "float | npt.NDArray",
    x2: "float | npt.NDArray",
    y1: "float | npt.NDArray",
    y2: "float | npt.NDArray",
) -> "float | npt.NDArray":
    """Performs a linear interpolation.

    Linearly interpolates at location *x0* between two nodes *x1* and *x2*, with
    values *y1* and *y2* respectively.

    It assumes that *x1* < *x0* < *x2*.

    Parameters
    ----------
    x0 : float or array of shape (n,)
        The location at which the interpolation is returned.
    x1 : float or array of shape (n,)
        The lower interpolation node.
    x2 : float or array of shape (n,)
        The upper interpolation node.
    y1 : float or array of shape (n,)
        The value at *x1*.
    y2 : float or array of shape (n,)
        The value at *x2*.

    Returns
    -------
    y0 : float or array of shape (n,)
        The interpolated value at *x0*.
    """
    y0 = y1 + (x0 - x1) * (y2 - y1) / (x2 - x1)

    return y0


def simple_transform(
    x: "float | npt.NDArray", transform_type: str
) -> "float | npt.NDArray":
    """Apply a simple mathematical transformation to an input array.

    Parameters
    ----------
    x : float or ndarray
        The input array.
    transform_type : str
        The type of transformation, among:
            - lin: linear transformation, i.e. do nothing.
            - log10: base 10 logarithm

    Returns
    -------
    x_transformed : float or ndarray
        The transformed array.
    """
    if transform_type == "lin":
        pass
    elif transform_type == "log10":
        x = np.log10(x)
    else:
        raise ValueError("Unsupported transform_type, must be: lin or log10.")
    return x


def inverse_simple_transform(
    x: "float | npt.NDArray", transform_type: str
) -> "float | npt.NDArray":
    """Apply the inverse of simple mathematical transformation to an input array.

    Parameters
    ----------
    x : float or ndarray
        The input array.
    transform_type : str
        The type of transformation, among:
            - lin: linear transformation, i.e. do nothing.
            - log10: base 10 logarithm

    Returns
    -------
    x_transformed : float or ndarray
        The array obtained after the inverse transformation.
    """
    if transform_type == "lin":
        pass
    elif transform_type == "log10":
        x = 10 ** (x)
    else:
        raise ValueError("Unsupported transform_type, must be: lin or log10.")
    return x


def interp_data_1D(
    x_target: npt.NDArray,
    x_data: npt.NDArray,
    data: npt.NDArray,
    interpx: str = "lin",
    interpy: str = "lin",
) -> npt.NDArray:
    """Interpolate the predictions at some target locations.

    Parameters
    ----------
    x_target : ndarray of shape (N,)
        The locations at which to interpolate/extrapolate the predictions.
    x_data : ndarray of shape (M,)
        The locations at which the data is known.
    data : ndarray of shape (n_samples, M)
        The data to interpolate/extrapolate.

    Returns
    -------
    pred_interp : ndarray of shape (n_samples, N)
        The interpolated/extrapolated predictions at the requested locations.
    """
    # Initialize empty array for the interpolated predictions.
    pred_interp = np.zeros((data.shape[0], x_target.shape[0]))

    # Targets within interpolation range.
    index_interp = (x_target >= x_data[0]) & (x_target <= x_data[-1])

    # TODO support extrapolation in some way, need to be careful!
    # Interpolate/extrapolate the data for each model.
    for i in range(data.shape[0]):
        # Transform target and prediction locations according
        # to interpolation settings.
        x_targets = simple_transform(x_target[index_interp], interpx)
        x_preds = simple_transform(x_data, interpx)

        # Transform predictions according to interpolation
        # settings.
        y_interp = simple_transform(data[i], interpy)

        # Make the linear interpolation.
        pred_interp[i][index_interp] = np.interp(
            x_targets,
            x_preds,
            y_interp,
        )

        # Inverse transform interpolated predictions
        # according to interpolation settings.
        pred_interp[i][index_interp] = inverse_simple_transform(
            pred_interp[i][index_interp], interpy
        )

    return pred_interp
