These tests are in a different folder because they need to use unittest instead of
django's inbuilt test runner. This could be consolidated in the future.

They can be run via

    python -m chess.tests_2.test_board

and via

    python -m chess.tests_2.test_square
