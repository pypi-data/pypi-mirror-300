#####################################
cpplint - static code checker for C++
#####################################

.. image:: https://img.shields.io/pypi/v/cpplint.svg
    :target: https://pypi.python.org/pypi/cpplint

.. image:: https://img.shields.io/pypi/pyversions/cpplint.svg
    :target: https://pypi.python.org/pypi/cpplint

.. image:: https://img.shields.io/pypi/status/cpplint.svg
    :target: https://pypi.python.org/pypi/cpplint

.. image:: https://img.shields.io/pypi/l/cpplint.svg
    :target: https://pypi.python.org/pypi/cpplint

.. image:: https://img.shields.io/pypi/dd/cpplint.svg
    :target: https://pypi.python.org/pypi/cpplint

.. image:: https://img.shields.io/pypi/dw/cpplint.svg
    :target: https://pypi.python.org/pypi/cpplint

.. image:: https://img.shields.io/pypi/dm/cpplint.svg
    :target: https://pypi.python.org/pypi/cpplint

Cpplint is a command-line tool to check C/C++ files for style issues according to `Google's C++ style guide <http://google.github.io/styleguide/cppguide.html>`_.

Cpplint used to be developed and maintained by Google Inc. at `google/styleguide <https://github.com/google/styleguide>`_. Nowadays, `Google is no longer maintaining the public version of cpplint <https://github.com/google/styleguide/pull/528#issuecomment-592315430>`_, and pretty much everything in their repo's PRs and issues about cpplint have gone unimplemented.

This fork aims to update cpplint to modern specifications, and be (somewhat) more open to adding fixes and features to make cpplint usable in wider contexts.


Installation
============

To install cpplint from PyPI, run:

.. code-block:: bash

    $ pip install cpplint

Externally managed environments
-------------------------------
If you get the "This environment is externally managed" error, try to search and install cpplint with your system's package manager (e.g. apt, rpm, pacman...). If it doesn't exist, you can either package cpplint for your distribution or repeat the steps above with the :code:`--break-system-packages` flag.

Usage
-----
.. code-block:: bash

    $ cpplint [OPTIONS] files

For full usage instructions, run:

.. code-block:: bash

    $ cpplint --help

Changes
=======

* python 3 compatibility
* more default file extensions
* customizable file extensions with the --extensions argument
* continuous integration on github
* support for recursive file discovery via the --recursive argument
* support for excluding files via --exclude
* JUnit XML output format
* Overriding repository root auto-detection via --repository
* Support ``#pragma once`` as an alternative to header include guards
* ... and `quite a bit <https://github.com/cpplint/cpplint/blob/master/CHANGELOG.rst>`_ more

Acknowledgements
================

Thanks to Google Inc. for open-sourcing their in-house tool.

Thanks to `our contributors <https://github.com/cpplint/cpplint/graphs/contributors>`_.

Maintainers
-----------

* `@aaronliu0130 <https://github.com/aaronliu0130>`_
* `@jayvdb <https://github.com/jayvdb>`_

Former
^^^^^^

* `@tkruse <https://github.com/tkruse>`_
* `@mattyclarkson <https://github.com/mattyclarkson>`_
* `@theandrewdavis <https://github.com/theandrewdavis>`_
