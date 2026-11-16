"""Self-check for Day 1: run `pytest days/day-01/python` from the repo root."""

import pytest

import practice


@pytest.mark.parametrize(
    "value, expected",
    [(5, "int"), ("hi", "str"), (None, "NoneType"), ([1], "list"), (2.5, "float"), (True, "bool"), ((1,), "tuple")],
)
def test_describe_type(value, expected):
    assert practice.describe_type(value) == expected


def test_format_receipt():
    assert practice.format_receipt("Pen", 3, 10.5) == "Pen x 3 @ 10.50 = 31.50"
    assert practice.format_receipt("Book", 1, 250) == "Book x 1 @ 250.00 = 250.00"


def test_compare_equal_but_different_objects():
    assert practice.compare([1], [1]) == (True, False)


def test_compare_same_object():
    x = [1]
    assert practice.compare(x, x) == (True, True)


def test_compare_different_values():
    assert practice.compare(1, 2) == (False, False)


def test_rename_in_place_mutates_the_same_list():
    names = ["a", "b", "a"]
    same = names
    result = practice.rename_in_place(names, "a", "z")
    assert result is None
    assert names == ["z", "b", "z"]
    assert same is names


def test_rename_in_place_no_match():
    names = ["x"]
    practice.rename_in_place(names, "a", "z")
    assert names == ["x"]


def test_uppercased_returns_new_list_and_keeps_original():
    names = ["asha", "ravi"]
    result = practice.uppercased(names)
    assert result == ["ASHA", "RAVI"]
    assert names == ["asha", "ravi"]
    assert result is not names


@pytest.mark.parametrize(
    "text, expected",
    [(" ₹1,234.50 ", 1234.5), ("$99", 99.0), ("7.25", 7.25), ("1,000,000", 1000000.0)],
)
def test_parse_price(text, expected):
    result = practice.parse_price(text)
    assert isinstance(result, float)
    assert result == pytest.approx(expected)


def test_fizzbuzz():
    assert practice.fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
    assert practice.fizzbuzz(15)[-1] == "FizzBuzz"
    assert practice.fizzbuzz(15)[2] == "Fizz"
    assert practice.fizzbuzz(15)[9] == "Buzz"
    assert practice.fizzbuzz(0) == []


def test_make_grid_shape():
    assert practice.make_grid(2, 3) == [[0, 0, 0], [0, 0, 0]]
    assert practice.make_grid(0, 3) == []


def test_make_grid_rows_are_independent():
    grid = practice.make_grid(3, 3)
    grid[0][0] = 99
    assert grid[1][0] == 0
    assert grid[2][0] == 0
    assert grid[0] is not grid[1]
