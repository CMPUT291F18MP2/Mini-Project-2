""" Unit tests for input_parser.py """

import mini_project_2
from mini_project_2.input_parser import InputParser

def test_validate_input_1():
    ip = InputParser()
    query = "camera"
    val = ip.validate_input(query)
    assert val == True

def test_validate_input_9():
    ip = InputParser()
    query = "camera date>=2018/11/05 date<=2018/11/07 price > 20 price < 40"
    val = ip.validate_input(query)
    assert val == True

def test_parse_input_9():
    ip = InputParser()
    query = "camera"
    searches_actual = ip.parse_input(query)
    searches_expected = {
        "keyword": [("=", "camera")]
    }
    assert searches_actual == searches_expected

def test_parse_input_9():
    ip = InputParser()
    query = "camera date>=2018/11/05 date<=2018/11/07 price > 20 price < 40"
    searches_actual = ip.parse_input(query)
    searches_expected = {
        "keyword": [("=", "camera")],
        "date": [(">=", "2018/11/05"), ("<=", "2018/11/07")],
        "price": [(">", "20"), ("<", "40")]
    }
    assert searches_actual == searches_expected