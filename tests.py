import unittest
from utils.helpers import is_traj_in_volume

class TestIsTrajInVolume(unittest.TestCase):
    def test_inside_volume(self):
        traj = [1, 1, 1, 2, 2, 2]
        volume = [(0, 0, 0), (3, 3, 3)]
        self.assertTrue(is_traj_in_volume(traj, volume))

    def test_outside_volume(self):
        traj = [-1, -1, -1, -2, -2, -2]
        volume = [(0, 0, 0), (3, 3, 3)]
        self.assertFalse(is_traj_in_volume(traj, volume))

    def test_intersect_volume(self):
        traj = [-1, -1, -1, 2, 2, 2]
        volume = [(0, 0, 0), (3, 3, 3)]
        self.assertTrue(is_traj_in_volume(traj, volume))

    def test_on_edge_of_volume(self):
        traj = [0, 0, 0, 3, 3, 3]
        volume = [(0, 0, 0), (3, 3, 3)]
        self.assertTrue(is_traj_in_volume(traj, volume))

if __name__ == '__main__':
    unittest.main()

