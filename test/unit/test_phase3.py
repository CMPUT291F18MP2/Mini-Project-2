# from mini_project_2.phase3 import AdsDatabase


def check_multiple_equals(criteria):
    one = None
    for op, value_str in criteria:
        if one and op == "=" and one != value_str:
            return True
        if op == "=":
            one = value_str
    return False


def test_check_multiple_equals():
    assert not check_multiple_equals([('=', '20'), ('=', '20')])
    assert check_multiple_equals([('=', '20'), ('=', '30')])


# def test_execute1():
#     with AdsDatabase() as ads_database:
#         pass
#     pass
#
#
# def test_execute2():
#     with AdsDatabase() as ads_database:
#         pass
#     pass
#
#
# def test_execute3():
#     with AdsDatabase() as ads_database:
#         pass
#     pass
#
#
# def test_execute4():
#     with AdsDatabase() as ads_database:
#         pass
#     pass
#
#
# def test_execute5():
#     with AdsDatabase() as ads_database:
#         pass
#     pass
#
#
# def test_execute6():
#     with AdsDatabase() as ads_database:
#         pass
#     pass
#
#
# def test_execute7():
#     with AdsDatabase() as ads_database:
#         pass
#     pass
#
#
# def test_phase3():
#     pass
#
#
# def test_parse_date():
#     pass
#
#
# def test_parse_price_range():
#     pass
#
#
# def test_parse_date_range():
#     pass
#
#
# def test_change_mode():
#     with AdsDatabase() as ads_database:
#         pass
#     pass
#
#
# def test_get_matching_terms():
#     with AdsDatabase() as ads_database:
#         pass
#     pass
#
#
# def test_get_matching_prices():
#     with AdsDatabase() as ads_database:
#         pass
#     pass
#
#
# def test_get_matching_dates():
#     with AdsDatabase() as ads_database:
#         pass
#     pass
#
#
# def test_print_matching_ads():
#     with AdsDatabase() as ads_database:
#         pass
#     pass
#
#
# def test_merge_results():
#     with AdsDatabase() as ads_database:
#         pass
#     pass
#
#
# def test_print_results():
#     with AdsDatabase() as ads_database:
#         pass
#     pass
#
#
# def test_print_one_result():
#     with AdsDatabase() as ads_database:
#         pass
#     pass
