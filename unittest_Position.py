# py -m unittest unittest_Position.py

import unittest
from Position import Position as pos

class TestPosition(unittest.TestCase):
    def test_instance(self):
        # help(pos)
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

    def test_distance(self):
        # exemple
        # d=pos.distance([46.249847, 4.894293],[45.249847, 4.894293])
        # print(d)
        # calcul distance Paris-Lyon 
        # Paris : [48.862725,2.287592]  - Lyon : [45.7578137,4.8320114]
        d=pos.distance([48.862725,2.287592],[45.7578137,4.8320114])
        self.assertEqual(d,394.9092900222981)



if __name__ == '__main__':
    unittest.main()