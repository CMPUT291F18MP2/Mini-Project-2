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

def test_parse_for_date_1():
    ip = InputParser()
    query = r"camera date>=2018/11/05 date<=2018/11/07 price > 20 price < 40"
    search_dict = dict()
    new_query = ip.parse_for_date(query, search_dict)
    assert search_dict == {"date": [(">=", "2018/11/05"), ("<=", "2018/11/07")]}
    assert new_query == r"camera   price > 20 price < 40"

def test_parse_for_date_2():
    ip = InputParser()
    query = r"date >= 2018/11/05"
    search_dict = dict()
    new_query = ip.parse_for_date(query, search_dict)
    assert search_dict == {"date": [(">=", "2018/11/05")]}
    assert new_query == r""

def test_parse_for_date_3():
    ip = InputParser()
    query = r"camera date=2025/01/01"
    search_dict = {"date": [(">=", "2018/11/05")]}
    new_query = ip.parse_for_date(query, search_dict)
    assert search_dict == {"date": [(">=", "2018/11/05"), ("=", "2025/01/01")]}
    assert new_query == r"camera "

def test_parse_for_price_1():
    ip = InputParser()
    query = r"price < 20"
    search_dict = dict()
    new_query = ip.parse_for_price(query, search_dict)
    assert search_dict == {"price": [("<", "20")]}
    assert new_query == r""

def test_parse_for_price_2():
    ip = InputParser()
    query = r"price < 20 price=40"
    search_dict = dict()
    new_query = ip.parse_for_price(query, search_dict)
    assert search_dict == {"price": [("<", "20"), ("=", "40")]}
    assert new_query == r" "

def test_parse_for_price_3():
    ip = InputParser()
    query = r"price >=420 have you ever heard the tragedy of dark plagueis the wise"
    search_dict = {"price": [("<", "20")]}
    new_query = ip.parse_for_price(query, search_dict)
    assert search_dict == {"price": [("<", "20"), (">=", "420")]}
    assert new_query == r" have you ever heard the tragedy of dark plagueis the wise"

def test_parse_for_location_1():
    ip = InputParser()
    query = r"location=edmonton date=2018/11/07"
    search_dict = dict()
    new_query = ip.parse_for_location(query, search_dict)
    assert search_dict == {"location": [("=", "edmonton")]}
    assert new_query == r" date=2018/11/07"

def test_parse_for_location_2():
    ip = InputParser()
    query = r"location=coruscant location=tatooine"
    search_dict = dict()
    new_query = ip.parse_for_location(query, search_dict)
    assert search_dict == {"location": [("=", "coruscant"), ("=", "tatooine")]}
    assert new_query == r" "

def test_parse_for_location_3():
    ip = InputParser()
    query = r"location=coruscant date=2019/11/11 location=tatooine"
    search_dict = {"location": [("=", "edmonton")]}
    new_query = ip.parse_for_location(query, search_dict)
    assert search_dict == {"location": [("=", "edmonton"), ("=", "coruscant"), ("=", "tatooine")]}
    assert new_query == r" date=2019/11/11 "

def test_parse_for_location_4():
    ip = InputParser()
    query = r"date=2019/11/11 location=tatooine"
    search_dict = {"price": [("=", "30")]}
    new_query = ip.parse_for_location(query, search_dict)
    assert search_dict == {
        "price": [("=", "30")],
        "location": [("=", "tatooine")]
        }
    assert new_query == r"date=2019/11/11 "

def test_parse_for_category_1():
    ip = InputParser()
    query = r"cat=art-collectibles camera"
    search_dict = dict()
    new_query = ip.parse_for_category(query, search_dict)
    assert search_dict == {"category": [("=", "art-collectibles")]}
    assert new_query == r" camera"

def test_parse_for_category_2():
    ip = InputParser()
    query = r"cat=not-stories-jedi-would-tell-you camera cat=art-collectibles"
    search_dict = dict()
    new_query = ip.parse_for_category(query, search_dict)
    assert search_dict == {"category": [("=", "not-stories-jedi-would-tell-you"), ("=", "art-collectibles")]}
    assert new_query == r" camera "

def test_parse_for_category_3():
    ip = InputParser()
    query = r"cat=kenobi location=dagobah"
    search_dict = {"price": [(">", "500")], "category": [("=", "general")]}
    new_query = ip.parse_for_category(query, search_dict)
    assert search_dict == {
        "price": [(">", "500")],
        "category": [("=", "general"), ("=", "kenobi")]}
    assert new_query == r" location=dagobah"

def test_parse_for_keyword_1():
    ip = InputParser()
    query = r"camera location=my-house"
    search_dict = dict()
    new_query = ip.parse_for_keyword(query, search_dict)
    assert search_dict == {"keyword": [("=", "camera")]}
    assert new_query == r" location=my-house"

def test_parse_for_keyword_2():
    ip = InputParser()
    query = r"camera%"
    search_dict = dict()
    new_query = ip.parse_for_keyword(query, search_dict)
    assert search_dict == {"keyword": [("%", "camera")]}
    assert new_query == r""

def test_parse_for_keyword_3():
    ip = InputParser()
    query = r"midichlorians cat=starwars darth%"
    search_dict = dict()
    new_query = ip.parse_for_keyword(query, search_dict)
    assert search_dict == {"keyword": [("=", "midichlorians"), ("%", "darth")]}
    assert new_query == r" cat=starwars "

def test_parse_for_keyword_4():
    ip = InputParser()
    query = r"location=deathstar ihatesand%"
    search_dict = {
        "keyword": [("=", "prequelsarethebest")],
        "date": [(">=", "2018/05/03")]
    }
    new_query = ip.parse_for_keyword(query, search_dict)
    assert search_dict == {
        "keyword": [("=", "prequelsarethebest"), ("%", "ihatesand")],
        "date": [(">=", "2018/05/03")]
    }
    assert new_query == r"location=deathstar "

def test_parse_input_1():
    ip = InputParser()
    query = "camera"
    searches_actual = ip.parse_input(query)
    searches_expected = {
        "keyword": [("=", "camera")]
    }
    assert searches_actual == searches_expected

def test_parse_input_2():
    ip = InputParser()
    query = "camera%"
    searches_actual = ip.parse_input(query)
    searches_expected = {
        "keyword": [("%", "camera")]
    }
    assert searches_actual == searches_expected

def test_parse_input_3():
    ip = InputParser()
    query = "date <= 2018/11/05"
    searches_actual = ip.parse_input(query)
    searches_expected = {
        "date": [("<=", "2018/11/05")]
    }
    assert searches_actual == searches_expected

def test_parse_input_4():
    ip = InputParser()
    query = "date > 2018/11/05 camera%"
    searches_actual = ip.parse_input(query)
    searches_expected = {
        "date": [(">", "2018/11/05")],
        "keyword": [("%", "camera")]
    }
    assert searches_actual == searches_expected

def test_parse_input_5():
    ip = InputParser()
    query = "price < 20"
    searches_actual = ip.parse_input(query)
    searches_expected = {
        "price": [("<", "20")]
    }
    assert searches_actual == searches_expected

def test_parse_input_6():
    ip = InputParser()
    query = "price >= 20 date > 2018/11/05"
    searches_actual = ip.parse_input(query)
    searches_expected = {
        "price": [(">=", "20")],
        "date": [(">", "2018/11/05")]
    }
    assert searches_actual == searches_expected

def test_parse_input_7():
    ip = InputParser()
    query = "location=edmonton date=2018/11/07"
    searches_actual = ip.parse_input(query)
    searches_expected = {
        "location": [("=", "edmonton")],
        "date": [("=", "2018/11/07")]
    }
    assert searches_actual == searches_expected

def test_parse_input_8():
    ip = InputParser()
    query = "cat=art-collectibles camera"
    searches_actual = ip.parse_input(query)
    searches_expected = {
        "keyword": [("=", "camera")],
        "category": [("=", "art-collectibles")]
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

def test_parse_input_10():
    ip = InputParser()
    query = "camera date>=2018/11/05 date<=2018/11/07 price > 20 price < 40 location=white-house obama"
    searches_actual = ip.parse_input(query)
    searches_expected = {
        "keyword": [("=", "camera"), ("=", "obama")],
        "date": [(">=", "2018/11/05"), ("<=", "2018/11/07")],
        "price": [(">", "20"), ("<", "40")],
        "location": [("=", "white-house")]
    }
    assert searches_actual == searches_expected

def test_parse_input_11():
    ip = InputParser()
    query = "     "
    searches_actual = ip.parse_input(query)
    searches_expected = {
    }
    assert searches_actual == searches_expected