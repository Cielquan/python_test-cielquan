.. only:: not builder_confluence

    .. highlight:: console

Installation
============

This part of the documentation covers how to install the package.
It is recommended to install the package in a virtual environment.


Create virtual environment
--------------------------
There are several packages/modules for creating python virtual environments.
You are free to use which you want. Here I use ``venv`` because it is build in::

    $ python -m venv venv

After creation activate the `venv` to work with it (Linux)::

    $ source venv/bin/activate

.. only:: not builder_confluence

    .. highlight:: default

On windows machines call instead::

    > venv\Scripts\activate

.. only:: not builder_confluence

    .. highlight:: console

Installation from source
------------------------
You can install SpotInkCalc directly from a Git repository clone. This can be done
either by cloning the repo and installing from the local clone::

    $ git clone https://github.com/Cielquan/python_test.git
    $ cd python_test
    $ pip install .


Or installing directly via git::

    $ pip install git+https://github.com/Cielquan/python_test.git


You can also download the current version as `tar.gz` or `zip` file, extract it and
install it with pip like above.

.. highlight:: default
