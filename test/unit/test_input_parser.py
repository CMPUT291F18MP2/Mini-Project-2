""" Unit tests for input_parser.py """

import mini_project_2
from mini_project_2.input_parser import InputParser

def test_validate_input_1():
    ip = InputParser()
    query = "camera"
    val = ip.validate_query(query)
    assert val == True

def test_validate_input_2():
    ip = InputParser()
    query = "camera%"
    val = ip.validate_query(query)
    assert val == True

def test_validate_input_3():
    ip = InputParser()
    query = "date <= 2018/11/05"
    val = ip.validate_query(query)
    assert val == True

def test_validate_input_4():
    ip = InputParser()
    query = "date > 2018/11/05"
    val = ip.validate_query(query)
    assert val == True

def test_validate_input_5():
    ip = InputParser()
    query = "price < 20"
    val = ip.validate_query(query)
    assert val == True

def test_validate_input_6():
    ip = InputParser()
    query = "price >= 20"
    val = ip.validate_query(query)
    assert val == True

def test_validate_input_7():
    ip = InputParser()
    query = "location=edmonton date=2018/11/07"
    val = ip.validate_query(query)
    assert val == True

def test_validate_input_8():
    ip = InputParser()
    query = "cat=art-collectibles camera"
    val = ip.validate_query(query)
    assert val == True

def test_validate_input_9():
    ip = InputParser()
    query = "camera date>=2018/11/05 date<=2018/11/07 price > 20 price < 40"
    val = ip.validate_query(query)
    assert val == True

def test_validate_input_10():
    ip = InputParser()
    query = " "
    val = ip.validate_query(query)
    assert val == False

def test_validate_input_11():
    ip = InputParser()
    query = r"hello []"
    val = ip.validate_query(query)
    assert val == False

def test_validate_input_12():
    ip = InputParser()
    query = r"      camera date>=2018    /11/05 "
    val = ip.validate_query(query)
    assert val == False

def test_validate_input_13():
    ip = InputParser()
    query = r"3413"
    val = ip.validate_query(query)
    assert val == True

def test_validate_input_14():
    ip = InputParser()
    query = r"date >=      2018/11/05    cat=yolo"
    val = ip.validate_query(query)
    assert val == True

def test_validate_input_15():
    ip = InputParser()
    query = r"date=hello"
    val = ip.validate_query(query)
    assert val == False

def test_validate_input_16():
    ip = InputParser()
    query = r" dafjeoj      date=30"
    val = ip.validate_query(query)
    assert val == False

def test_validate_input_17():
    ip = InputParser()
    query = r"weeueueeee hello"
    val = ip.validate_query(query)
    assert val == True

def test_validate_input_18():
    ip = InputParser()
    query = r"price <=> 50"
    val = ip.validate_query(query)
    assert val == False

def test_validate_input_19():
    ip = InputParser()
    query = r"50 < price <60"
    val = ip.validate_query(query)
    assert val == False

def test_parse_input_1():
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