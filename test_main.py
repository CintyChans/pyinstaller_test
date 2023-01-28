import pytest
import main
import numpy as np
class TestDemo():

     def test_demo_1(self):
          print('----测试用例执行-----------')
          person=main.f2()
          assert person.id==1
      
     def test_demo_2(self):
          print('----测试用例执行-----------')
          x=main.f5()
          assert 1 in x
  
     def test_demo_3(self):
          print('----测试用例执行-----------')
          assert main.f6()!=3.14


