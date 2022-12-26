import unittest
import main
import numpy as np
class TestDemo(unittest.TestCase):
     def setUp(self):
          print('setUp')
     def tearDown(self):
          print('tearDown')
     def test_demo_1(self):
          person=main.f2()
          self.assertEqual(person.id,1)
      
     def test_demo_2(self):
          self.assertEqual(main.f5(),np.array([1,2,3]))
  
     def test_demo_3(self):
          self.assertTrue(main.f6()!=3.14)

if __name__ == '__main__':
     unittest.main()
