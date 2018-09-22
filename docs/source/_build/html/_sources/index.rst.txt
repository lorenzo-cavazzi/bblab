.. bblab documentation master file, created by
   sphinx-quickstart on Sat Sep 22 15:16:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to bblab's documentation!
=================================

Introduction
------------

bblab is a Python package containing utilities to process and analyze images.
In this first release the focus is on a few image processing algorithms, according
to the tasks in the "2018 assignement"

Library structure
`````````````````
The library is meant to be used both as an imported module and as a command line tool.
Therefore, the author decided to use stateless functions. Another possibility was
to use an object oriented approach by defining a class and implementing methods on
that.

Function parameters
```````````````````
The library should be flexible, and this means every function has a number of parameters.
The most relevant are defined as named argument, while all other are handled by the
**kwargs argument.  
Please check single function descriptions to know the full list of available parameters.

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   install
   test
   modules
   examples

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
