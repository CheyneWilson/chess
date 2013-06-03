chess
=====

A python implementation of chess

This is still very much a work-in-progress with the following main outstanding items:
 1. Implement logic to check if a piece is pinned (limited movement)
 2. Implment logic for stalemate
 3. Implement logic for 50 move stalemate
 4. Implement logic for check
 5. Implment logic for checkmate
 6. Refactor unit tests to be more 'unit-y', add more 'negative' tests
 7. Refactor some of the methods / attribues to clearly delinate intended access levels
 8. Review all of the docstrings and tidy them up
 9. Create 'Game' class which wraps up board and allows a player to play
10. Create 'RandomAgent' - an agent that does random moves

Development Setup 
----
0. Requirements
    Pythom 2.7 (for PyLint)
1. Install hamcrest using distribute
    a. Install Distribute (https://pypi.python.org/pypi/distribute)
       If your shell has the `curl` program you can do:
        $ curl -O http://python-distribute.org/distribute_setup.py
        $ python distribute_setup.py
    b. Install hamcrest
       With Distribute installed hamcrest can be installed by running: 
        $ easy_install PyHamcrest
