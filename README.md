chess
=====

A python implementation of chess

This is still very much a work-in-progress with the following main outstanding items:
 1. Refactor unit tests to be more 'unit-y', add more negative tests (invalid operations).
 2. Refactor some of the methods / attribues to clearly delinate intended access levels.
 3. Review all of the docstrings and tidy them up.
 4. Create 'Game' class which wraps up the board and allows a player to play.
 5. Add a console UI
 6. Add a web based UI
 7. Create 'RandomAgent' - an agent that does random moves.

Development Setup 
----
0. Requirements:
    a. python 2.7 (for PyLint)
1. Install hamcrest using distribute
    a. Install Distribute (https://pypi.python.org/pypi/distribute)
       If your shell has the `curl` program you can do:
        $ curl -O http://python-distribute.org/distribute_setup.py
        $ python distribute_setup.py
    b. Install hamcrest
       With Distribute installed hamcrest can be installed by running: 
        $ easy_install PyHamcrest
