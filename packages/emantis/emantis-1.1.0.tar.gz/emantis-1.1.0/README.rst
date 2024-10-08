|PyPI|_ |DOI|_

.. |PyPI| image:: https://img.shields.io/pypi/v/emantis
.. _PyPI: https://pypi.org/project/emantis/

.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.7738362.svg
.. _DOI: https://doi.org/10.5281/zenodo.7738362

e-MANTIS: Emulator for Multiple observable ANalysis in extended cosmological TheorIeS
=====================================================================================

.. contents:: Table of Contents
   :local:

Description
-----------

e-MANTIS is an emulator for the study of the non-linear large-scale structure formation in the context
of alternative dark energy and gravity theories.
It uses Gaussian Processes to perform a fast and accurate interpolation between the outputs of
high resolution cosmological N-body simulations.
Currently, e-MANTIS is able to provide theoretical predictions for the following quantities:

* Matter power spectrum boost in f(R) gravity, described in `The e-MANTIS emulator: fast predictions of the non-linear matter power spectrum in f(R)CDM cosmology <https://arxiv.org/abs/2303.08899>`_.

* Halo mass function in f(R)CDM and wCDM cosmologies, described in COMING SOON.

Please cite the corresponding papers if you use e-MANTIS in your work.

More observables and cosmological models will be added in the future. Stay tuned!

Installation
------------

You can install the emulator from `PyPI <https://pypi.org/project/emantis/>`_ via pip::

  pip install emantis

Or you can directly clone the emulator from our public `repository <https://gitlab.obspm.fr/e-mantis/e-mantis>`_ and install it from source::

  git clone https://gitlab.obspm.fr/e-mantis/e-mantis.git
  cd e-mantis
  pip install [-e] .

The emulator only works with python >= 3.9. The main dependencies are:

* h5py (tested with version >= 3.8)
* scikit-learn (tested with version >= 1.0)
* numpy (tested with version >= 1.26)
* pydantic (tested with version >= 2.6)
* joblib (tested with version >= 1.3.2)
* tomli (tested with version >= 2.0, required only for python < 3.11)

All the dependencies should be installed automatically by pip.

Documentation and usage
-----------------------

The up-to-date documentation for this project (with code examples and a detailed API) is available `here <https://e-mantis.pages.obspm.fr/e-mantis/index.html>`_.

Licence
-------

Copyright (C) 2023 Iñigo Sáez-Casares - Université Paris Cité

inigo.saez-casares@obspm.fr

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/.
