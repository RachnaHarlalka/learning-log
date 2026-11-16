"""Day 1 practice: setup and basics.

Fill in each function. Check your work with:
    pytest days/day-01/python

Exercises go from easy to interview-level. Do them in order.
"""


# ---------------------------------------------------------------- 1. Easy
def describe_type(value):
    """Return the NAME of the value's type as a string.

    describe_type(5)      -> "int"
    describe_type("hi")   -> "str"
    describe_type(None)   -> "NoneType"
    describe_type([1])    -> "list"

    Hint: type(...) gives the type; types have a __name__ attribute.
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------- 2. Easy
def format_receipt(item, quantity, unit_price):
    """Return a one-line receipt using an f-string.

    format_receipt("Pen", 3, 10.5)   -> "Pen x 3 @ 10.50 = 31.50"
    format_receipt("Book", 1, 250)   -> "Book x 1 @ 250.00 = 250.00"

    Both money values must have exactly 2 decimal places.
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------- 3. Easy
def compare(a, b):
    """Return a tuple (equal, same_object) for the two arguments.

    equal        -> do a and b have equal VALUES?
    same_object  -> are a and b the very same OBJECT?

    compare([1], [1])   -> (True, False)
    x = [1]; compare(x, x)   -> (True, True)
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------- 4. Medium
def rename_in_place(names, old, new):
    """Replace every occurrence of `old` with `new` INSIDE the given list.

    Mutate the list you were given and return None. Do not build a new list.

    names = ["a", "b", "a"]
    rename_in_place(names, "a", "z")
    names -> ["z", "b", "z"]
    """
    # TODO
    raise NotImplementedError


def uppercased(names):
    """Return a NEW list with every name upper-cased.

    The list passed in must stay unchanged.

    names = ["asha", "ravi"]
    uppercased(names) -> ["ASHA", "RAVI"]
    names             -> ["asha", "ravi"]   (untouched)
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------- 5. Medium
def parse_price(text):
    """Turn a price string into a float.

    Ignore surrounding whitespace, a leading currency sign "₹" or "$",
    and thousands commas.

    parse_price(" ₹1,234.50 ")  -> 1234.5
    parse_price("$99")          -> 99.0
    parse_price("7.25")         -> 7.25
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------- 6. Interview
def fizzbuzz(n):
    """Classic: return a list of strings for 1..n.

    Multiples of 3 -> "Fizz", of 5 -> "Buzz", of both -> "FizzBuzz",
    otherwise the number as a string.

    fizzbuzz(5) -> ["1", "2", "Fizz", "4", "Buzz"]
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------- 7. Interview
def make_grid(rows, cols):
    """Return a rows x cols grid of zeros as a list of lists.

    The rows must be INDEPENDENT lists: changing grid[0][0] must not change
    any other row.

    make_grid(2, 3) -> [[0, 0, 0], [0, 0, 0]]

    Interview trap: [[0] * cols] * rows is wrong. Why? Write the reason in
    a comment here once you know it:
    """
    # TODO
    raise NotImplementedError
