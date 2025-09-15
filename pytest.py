# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 10:41:27 2022

@author: gowrishankar.p
"""

# from unittest import TestCase

# class TryTesting(TestCase):
#     def test_always_passes(self):
#         self.assertTrue(True)

#     def test_always_fails(self):
#         self.assertTrue(False)
#         # print(self.assertTrue)

# a = TryTesting()
# a.test_always_passes()
# a.test_always_fails()

import pytest

print('start')
def test_file1_method1():
	x=5
	y=6
	assert x+1 == y,"test failed"
	assert x == y,"test failed"
    
    
def test_file1_method2():
	x=5
	y=6
	assert x+1 == y,"test failed" 