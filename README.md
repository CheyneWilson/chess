Chess
=====

The aim of this project is to create a framework where various algorithms can be created to play chess and experimented with. This is still very much a work-in-progress with the following main outstanding items:

 1. Set up session based authentication for multiplayer over http(s)
 2. Enable a basic chat client
 3. Create 'RandomAgent' - the 1st agent that does random moves.
 4. Support pgn format
 5. Support reading in a a list of moves to recreate a board state

Development Setup
====
Requires Python 2.7

Install pip
----
(http://www.pip-installer.org/en/latest/installing.html)

To install or upgrade pip, securely download [get-pip.py] (https://raw.github.com/pypa/pip/master/contrib/get-pip.py)

Then run the following (which may require administrator access):

`python get-pip.py`

Install Virtualenv
----
(http://www.virtualenv.org/en/latest/virtualenv.html#installation)

Run `pip install virtualenv`

Setup Environment
----
Run the following commands:

`virtualenv env`

`source env/bin/activate`

`pip install -r etc/requirements.txt`

Web Server configuration
----
A web server needs to be configured to serve the www directory.

It also needs to map /rest/ to the running controller.

Running the controller
----
The controller runs all of the backend services. It is started as follows
`python controller.py`

Running tests
----

The tests are currently partitioned into two separate sets, unittests and integration tests.
The unit tests test the model, and can be run as follows from the root directoy (same directory as this README):

    python -m chess.tests_2.test_board
    python -m chess.tests_2.test_square

The integration tests test the webservices. From the root directory (same directory as this README) all tests can be
run as follows:
    python manage.py test chess
