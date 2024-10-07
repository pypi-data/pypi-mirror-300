.. highlight:: shell

============
Installation
============

Requirements
------------

.. This package has the following dependencies:
.. * `JAX`_: An `Autograd` and `XLA` framework for high-performance numerical computing

`JAX`_ is the core of this package and its installation is necessary to use it.
The CPU version of JAX is included, as dependency, in the default installation of Pantea.

For machines with an NVIDIA **GPU**, it is recommended to install JAX 
using the following command (only Linux users):

.. code-block:: bash

    $ pip install 'jax[cuda12]'

Please refer to the `JAX Install Guide`_ for full installation instructions.


.. .. note::
..     Installation with `conda` sometime takes too much time, 
..     an alternative option is of course to use `mamba`_ instead.
..     If you don't have `mamba` installed, you can do it using `conda` itself by running.

..     .. code-block:: bash
        
..         conda install -c conda-forge mamba

..     You can use now `mamba` to install, update, and manage packages just like `conda`.


.. _JAX: https://github.com/google/jax
.. _`JAX Install Guide`: https://github.com/google/jax#installation
.. _mamba: https://github.com/mamba-org/mamba

For atom visualization in Jupyter Notebooks, it is also recommended to
install `nglview`_ using conda as follows:

.. code-block:: python

    $ conda install -c conda-forge nglview

.. _nglview: https://github.com/nglviewer/nglview


Stable release
--------------

To install Pantea, run this command in your terminal:

.. code-block:: console

    $ pip install pantea

This is the preferred method to install Pantea, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for Pantea can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/hghcomphys/pantea

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/hghcomphys/pantea/tarball/main

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/hghcomphys/pantea
.. _tarball: https://github.com/hghcomphys/pantea/tarball/main
