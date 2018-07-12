#!/usr/bin/env python

import itree
import pprint
import unittest


class TestITree(unittest.TestCase):
    def test_str(self):
        intervals = [
            (1, 4), (6, 8), (15, 19)
        ]
        n = itree.ITNode(2.78, intervals)
        print str(n)

        n = itree.ITNode(3.14, None)
        print str(n)

        n = itree.ITNode(3.14, [])
        print str(n)

    def test_ptree(self):
        intervals = [
            (8, 11), (10, 12), (9, 13)
        ]
        mytree = itree.ITree()
        mytree.construct(intervals)
        mytree.dump()

    def test_big(self):
        intervals = [
            (1, 4),
            (6, 8),
            (15, 19),
            (2, 6),
            (10, 12),
            (17, 22),
            (5, 6),
            (8, 11),
            (14, 18),
            (22, 25),
            (1, 3),
            (9, 13),
            (17, 20),
            (21, 24),
            (1, 12)
        ]
        mytree = itree.ITree()
        mytree.construct(intervals)
        mytree.dump()
        for x in mytree.find_intervals_for_point(16):
            print x

        for x in mytree.find_intervals_for_interval((7, 11)):
            print x

    def test_small(self):
        intervals = [
            (0, 8),
            (1, 3),
            (5, 7),
        ]
        mytree = itree.ITree()
        mytree.construct(intervals)
        mytree.dump()


if __name__ == '__main__':
    unittest.main()
