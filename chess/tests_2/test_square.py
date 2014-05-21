# -*- coding: UTF-8 -*-
import unittest
from hamcrest import is_, assert_that, equal_to, all_of, contains_inanyorder, instance_of
from chess.square import Square, InvalidSquareException


class TestSquareFunctions(unittest.TestCase):
    def setUp(self):
        pass

    def testCreateSquare(self):
        u"""Super simple, should just run with no assertions"""
        Square('A7')

    # TODO: Square bounds checks

    def testGetSquarePiece(self):
        s = Square('A1')
        assert_that(s.piece, is_(None))

    def testSetSquarePiece(self):
        s = Square('H4')
        d = u'dummy_piece'
        s.piece = d
        assert_that(s.piece, is_(d))

    def testFromCoords(self):
        s = Square(x=1, y=8)
        assert_that(s.name, is_('A8'))

    def testFromCoords2(self):
        s = Square(x=8, y=1)
        assert_that(s.name, is_('H1'))


if __name__ == '__main__':
        unittest.main()
