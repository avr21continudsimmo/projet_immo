# py -m unittest unittest_Position.py

import unittest
from Position import Position as pos

class TestPosition(unittest.TestCase):
    def test_instance(self):
        help(pos)
        # without params
        p = pos()
        self.assertEqual(0,p.lat)
        self.assertEqual(0,p.lgt)

        # with gps coordinates
        p = pos(gps=[46.249847, 4.894293])
        self.assertEqual(46.249847,p.lat)
        self.assertEqual(4.894293,p.lgt)

        # with addressName
        p = pos(addressName='2, boulevard Blaise Pascal, 93160 Noisy le Grand')
        self.assertEqual(48.838173 ,p.lat)
        self.assertEqual(2.583538,p.lgt) 


if __name__ == '__main__':
    unittest.main()