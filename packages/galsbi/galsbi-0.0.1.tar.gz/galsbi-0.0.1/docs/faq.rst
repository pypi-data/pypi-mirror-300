===================================
FAQs
===================================

.. _faq:

Here are some frequently asked questions (FAQs) regarding the project. Click on the links below to jump to the corresponding answer.

.. contents:: Table of Contents
   :local:
   :depth: 1

.. _citation:

Which papers should I cite when using `galsbi`?
-----------------------------------------------

You can find out which papers to cite by using the following command in Python:

.. code-block:: python

    from galsbi import GalSBI
    model = GalSBI("model_name")
    model.cite()

This will print the bibtex entries of the papers that should be cited when using your
configuration.

.. _pycosmo-error:

I get an error when I run the code for the first time during the compilation of `PyCosmo`. What should I do?
------------------------------------------------------------------------------------------------------------

If you get an error when you run the code for the first time during the compilation of `PyCosmo`,
(e.g. `ModuleNotFoundError: No module named '_wrapper_1db8b055_fc3ec'`), something went
wrong during the compilation of the code. This can normally be resolved by deleting the
cache and recompiling the code. To do this, run the following commands:

.. code-block:: bash

    cd /path/to/cache
    rm -rf PyCosmo
    rm -rf gsl
    rm -rf libf2c
    rm -rf sympy2c

The cache is located under `~/Library/Cache` on macOS and `~/_cache` on Linux.
After deleting the cache, recompile the code by running the following python code:

.. code-block:: python

    import PyCosmo
    PyCosmo.build()

This should resolve the issue. If you still encounter problems, please contact the developers.
