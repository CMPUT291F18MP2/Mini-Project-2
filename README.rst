##############
mini-project-2
##############

.. image:: https://travis-ci.com/CMPUT291F18MP2/Mini-Project-2.svg?branch=master
    :target: https://travis-ci.com/CMPUT291F18MP2/Mini-Project-2
    :alt: Build Status

.. image:: https://readthedocs.org/projects/mini-project-2/badge/?version=latest
    :target: https://mini-project-2.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
    
.. image:: https://codecov.io/gh/CMPUT291F18MP2/Mini-Project-2/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/CMPUT291F18MP2/Mini-Project-2
  :alt: CodeCov


Requirements
============

* Python 3.5+
* libdb4.8-dev
* libdb4.8++-dev
* db-util


Overview
========

mini-project-2 is a python command-line application that interfaces with the Berkeley 
DB Python 3 package (bsddb3). Using the program users can specify queries written in the 
query language grammar seen here: https://github.com/CMPUT291F18MP2/Mini-Project-2/blob/master/mini_project_2/input_parser.py. These queries are processed by the program and the associated 
data is retrieved and presented to the user.


Installation
============

To install the Berkeley DB dependencies for mini-project-2 on Ubuntu run the
following commands:

.. code-block:: bash

    sudo add-apt-repository ppa:bitcoin/bitcoin
    sudo apt-get update
    sudo apt-get install libdb4.8-dev libdb4.8++-dev
    sudo apt-get install db-util -y

mini-project-2 can then be installed from source by running:

.. code-block:: bash

    pip install .

Within the same directory as mini-project-2's ``setup.py`` file.


Usage
=====

After installing mini-project-2's shell can be started by the following console
command:

.. code-block:: bash

    mini-project-2 --phase [1-3]

To get additional usage help on starting mini-project-2 run the following
console command:

.. code-block:: bash

    mini-project-2 --help
