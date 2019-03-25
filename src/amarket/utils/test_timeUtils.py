# coding=utf-8

import pytest
from .timeUtils import *

def test_get_workday_backward():
    assert get_workday('20190325', False) == '20190325'
    assert get_workday('20190324', False) == '20190322'
    assert get_workday('20190323', False) == '20190322'
    assert get_workday('20190322', False) == '20190322'

def test_get_workday_forward():
    assert get_workday('20190325', True) == '20190325'
    assert get_workday('20190324', True) == '20190325'
    assert get_workday('20190323', True) == '20190325'
    assert get_workday('20190322', True) == '20190322'

def test_get_workday_offset():
    assert get_workday('20190325', 0) == '20190325'
    assert get_workday('20190325', 1) == '20190326'
    assert get_workday('20190325', -1) == '20190322'
    assert get_workday('20190325', 5) == '20190401'    
    assert get_workday('20190324', 0) == '20190322'
    assert get_workday('20190324', 1) == '20190325'
    assert get_workday('20190324', -1) == '20190321'
    assert get_workday('20190324', 5) == '20190329'    