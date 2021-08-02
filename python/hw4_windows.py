import binascii
import random
from typing import Generator, List

state = random.getstate()  # save the internal state to restore in tests


def my_collecion_generator() -> Generator[
    str, None, None
]:  # <- this reads as "Generator that produces (yields) only strings"
    # ! Important: wrapping this function call in a list will hang your interpreter
    """This is a function that returns a generator.
    for the difference between iterator and generator see that SO question: https://stackoverflow.com/questions/2776829/difference-between-pythons-generators-and-iterators

    this one is endless, it will never end
    """
    import string

    # str.join takes a list and "joins" all elements into one string; separator between elements is the string providing this method, see https://docs.python.org/3/library/stdtypes.html#str.join
    # string.ascii_lowercase is just a constant
    while True:
        random_str = "".join([random.choice(string.ascii_lowercase) for _ in range(8)])
        yield random_str


def take_n(g: Generator[str, None, None], n: int) -> List[str]:
    """Takes n elements from generator g

    Args:
        n (int): number of elements to take
        g (Generator[str, None, None]): generator to take elements from

    Returns:
        List[str]: List of taken elements
    """
    return [next(g) for _ in range(n)]


class InfiniteGeneratorWrapper:
    """This class should wrap a generator we defined above (tests will pass it to the __init__)
    and do the following:
       • implement an iterator method that will do the following for each element BEFORE returning:
            • reverse a string
            • and encode the whole string as hex using `binascii.hexlify`. see: https://docs.python.org/3/library/binascii.html#binascii.hexlify
            Hint: you want to look at `take_n` code for inspiration
            Note: binascii will asks for bytes, but you have a str, to convert str to bytes, you'll need to use str.encode https://docs.python.org/3/library/stdtypes.html#str.encode
       • return AT MOST max_elements! (Don't forget that generator is infinite!)
    """

    def __init__(self, g: Generator[str, None, None], max_elements=1000) -> None:
        self.g = g
        self.max_elements = max_elements
        #return [next(g) for _ in range(max_elements)]
        #self = [binascii.hexlify(next(g)[::-1].encode()) for _ in range(max_elements)]
        # insert code here
        pass

    def __iter__(self):
        self.iteration = 0
        return self

    def __next__(self):
        if self.iteration >= self.max_elements:
            raise StopIteration
        self.iteration += 1
        return binascii.hexlify(next(self.g)[::-1].encode()).decode()

    

        
    


class BaseRule:  # this is our base class
    deny_reason = "decided to keep {item} because i'm a base class"
    allow_reason = "allow {item}, because i'm a base class"

    def __init__(self) -> None:
        self.x = 42

    def allow(self, item):  # instance method
        print(self.allow_reason.format(item=item))
        return True

    def deny(self, item):
        print(self.deny_reason.format(item=item))
        return False

    def check(self, item) -> bool:
        return self.allow(item)


# For next two classes (KeepEverythingStartsFrom and DenyEverythingStartsFrom) your task is to fill the code according to
# the following specification:
#  both classes should inherit from BaseRule
#  for both classes, initializer (__init__) should accept argument named `starts_from` of type str.
#  for KeepEverythingStartsFrom:
#    • check method should allow items that startswith `starts_from`. Deny everything else.
#
#  for DenyEverythingStartsFrom the inverse is true:
#    • check method should deny items that startswith `starts_from`. Allow everything else.
#
# The `test_ruleset` function is used by tests to verify the actual logic.


class KeepEverythingStartsFrom(BaseRule):
    def __init__(self, starts_from: str) -> None:
        BaseRule.__init__(self)
        self.starts_from = starts_from
    pass

    def check(self, item):
        length = len(self.starts_from)
        if item[0:length] == self.starts_from[0:length]:
            return self.allow(item)
        else:
            return self.deny(item)


class DenyEverythingStartsFrom(BaseRule):
    def __init__(self, starts_from: str) -> None:
        BaseRule.__init__(self)
        self.starts_from = starts_from
    pass

    def check(self, item):
        length = len(self.starts_from)
        if item[0:length] == self.starts_from[0:length]:
            return self.deny(item)
        else:
            return self.allow(item)


def test_ruleset(items):
    rules = [
        DenyEverythingStartsFrom(starts_from="ab"),
        KeepEverythingStartsFrom(starts_from="a"),
    ]
    passed = []
    for item in items:
        evaluation_result = False  # deny everything until proven wrong
        for rule in rules:
            evaluation_result |= rule.check(item)
            if not evaluation_result:
                # break on deny
                break
        if evaluation_result:
            passed.append(item)
    return passed


#### TEST CODE HERE ####
# Beware of dragons: please don't try too much to understand tests code
# for now it's specifically written in "obfuscated" way, so i won't spoil all answers!


import unittest
import itertools


class TestHomework4(unittest.TestCase):

    @staticmethod
    def do_a_barrel_roll(el):
        import binascii
        el = el[::-1]
        return binascii.hexlify(el.encode()).decode()

    def test_barrel_roll(self):
        self.assertEqual(self.do_a_barrel_roll("52"), "3235")

    def test_generator_wrapper(self):
        source_of_truth = take_n(my_collecion_generator(), 5)
        random.setstate(
            state
        )  # restore state so generator above and generator beyond will have the same outputs
        wrapper = InfiniteGeneratorWrapper(my_collecion_generator(), max_elements=5)
        for (truth, candidate) in itertools.zip_longest(source_of_truth, wrapper):
            truth = self.do_a_barrel_roll(truth)
            self.assertEqual(truth, candidate)

    def test_ruleset_passed(self):
        items = ["aa", "ab", "abc", "acd"]
        should_stay = ["aa", "acd"]
        self.assertEqual(test_ruleset(items), should_stay)

    def test_ruleset_preserves_vars(self):
        base = BaseRule()
        keep = KeepEverythingStartsFrom(starts_from="x")
        self.assertEqual(keep.x, base.x)


if __name__ == "__main__":
    unittest.main()
