from main import *
import argparse
def test_1():
  f1()
  f2()
  f5()
  f4()
  f6()
  f7()
  
def test_2():
  parser = argparse.ArgumentParser(description='Demo of argparse')
  parser.add_argument('--line', type=int, default=1)
  args = parser.parse_args()
  if args.line:
     print('argparse:',args.line)
  print(args)
  return args
